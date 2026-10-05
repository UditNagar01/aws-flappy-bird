import random
import sys
import pygame

# -----------------------------
# Settings
# -----------------------------
WIDTH = 800
HEIGHT = 600
FPS = 60

SKY = (135, 206, 235)
GREEN = (76, 175, 80)
DARK_GREEN = (46, 125, 50)
YELLOW = (255, 221, 70)
BLACK = (25, 25, 25)
WHITE = (255, 255, 255)
GROUND = (222, 184, 135)

BIRD_X = 180
BIRD_SIZE = 28
GRAVITY = 0.32
FLAP_VELOCITY = -7.5

PIPE_WIDTH = 75
PIPE_GAP = 200
PIPE_SPEED = 3.5
PIPE_INTERVAL = 1500  # milliseconds

GROUND_HEIGHT = 70


class Bird:
    def __init__(self):
        self.reset()

    def reset(self):
        self.x = BIRD_X
        self.y = HEIGHT // 2
        self.velocity = 0

    def flap(self):
        self.velocity = FLAP_VELOCITY

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity

    def rect(self):
        return pygame.Rect(
            int(self.x),
            int(self.y),
            BIRD_SIZE,
            BIRD_SIZE
        )

    def draw(self, screen):
        pygame.draw.circle(
            screen,
            YELLOW,
            (int(self.x + BIRD_SIZE / 2), int(self.y + BIRD_SIZE / 2)),
            BIRD_SIZE // 2
        )


class Pipe:
    def __init__(self, x):
        self.x = x

        # Keep the gap away from the top and ground.
        min_gap_y = 90
        max_gap_y = HEIGHT - GROUND_HEIGHT - PIPE_GAP - 60
        self.gap_y = random.randint(min_gap_y, max_gap_y)

        self.passed = False

    def update(self):
        self.x -= PIPE_SPEED

    def off_screen(self):
        return self.x + PIPE_WIDTH < 0

    def rects(self):
        top_rect = pygame.Rect(
            int(self.x),
            0,
            PIPE_WIDTH,
            self.gap_y
        )

        bottom_y = self.gap_y + PIPE_GAP
        bottom_rect = pygame.Rect(
            int(self.x),
            bottom_y,
            PIPE_WIDTH,
            HEIGHT - GROUND_HEIGHT - bottom_y
        )

        return top_rect, bottom_rect

    def draw(self, screen):
        top_rect, bottom_rect = self.rects()

        pygame.draw.rect(screen, GREEN, top_rect)
        pygame.draw.rect(screen, GREEN, bottom_rect)

        # Small darker edges make the pipes easier to see.
        pygame.draw.rect(screen, DARK_GREEN, top_rect, 4)
        pygame.draw.rect(screen, DARK_GREEN, bottom_rect, 4)


class FlappyBirdGame:
    START = "start"
    PLAYING = "playing"
    GAME_OVER = "game_over"

    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Flappy Bird - AWS Student Builder Group")

        self.clock = pygame.time.Clock()

        self.title_font = pygame.font.Font(None, 64)
        self.large_font = pygame.font.Font(None, 52)
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 28)

        self.bird = Bird()
        self.pipes = []
        self.score = 0
        self.state = self.START
        self.last_pipe_time = 0

    def reset_game(self):
        self.bird.reset()
        self.pipes.clear()
        self.score = 0
        self.last_pipe_time = pygame.time.get_ticks()

    def start_game(self):
        self.reset_game()
        self.state = self.PLAYING
        self.bird.flap()

    def game_over(self):
        self.state = self.GAME_OVER

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                if self.state == self.START:
                    if event.key in (pygame.K_SPACE, pygame.K_UP):
                        self.start_game()

                elif self.state == self.PLAYING:
                    if event.key in (pygame.K_SPACE, pygame.K_UP):
                        self.bird.flap()

                elif self.state == self.GAME_OVER:
                    if event.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_r):
                        self.start_game()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.state == self.START:
                    self.start_game()
                elif self.state == self.PLAYING:
                    self.bird.flap()
                elif self.state == self.GAME_OVER:
                    self.start_game()

    def spawn_pipes(self):
        now = pygame.time.get_ticks()

        if now - self.last_pipe_time >= PIPE_INTERVAL:
            self.pipes.append(Pipe(WIDTH + 20))
            self.last_pipe_time = now

    def update(self):
        if self.state != self.PLAYING:
            return

        self.bird.update()
        self.spawn_pipes()

        for pipe in self.pipes:
            pipe.update()

            if not pipe.passed and pipe.x + PIPE_WIDTH < self.bird.x:
                pipe.passed = True
                self.score += 1

        self.pipes = [pipe for pipe in self.pipes if not pipe.off_screen()]

        self.check_collisions()

    def check_collisions(self):
        bird_rect = self.bird.rect()

        # Top ceiling and ground boundaries.
        if bird_rect.top <= 0:
            self.game_over()
            return

        if bird_rect.bottom >= HEIGHT - GROUND_HEIGHT:
            self.game_over()
            return

        # Pipe collision.
        for pipe in self.pipes:
            top_rect, bottom_rect = pipe.rects()

            if bird_rect.colliderect(top_rect) or bird_rect.colliderect(bottom_rect):
                self.game_over()
                return

    def draw_background(self):
        self.screen.fill(SKY)

        # Simple clouds.
        for x, y in [(120, 90), (520, 130), (700, 70)]:
            pygame.draw.circle(self.screen, WHITE, (x, y), 22)
            pygame.draw.circle(self.screen, WHITE, (x + 25, y + 5), 18)
            pygame.draw.circle(self.screen, WHITE, (x - 22, y + 8), 16)

        # Ground.
        pygame.draw.rect(
            self.screen,
            GROUND,
            (0, HEIGHT - GROUND_HEIGHT, WIDTH, GROUND_HEIGHT)
        )

    def draw_centered(self, text, font, y, color=WHITE):
        surface = font.render(text, True, color)
        rect = surface.get_rect(center=(WIDTH // 2, y))
        self.screen.blit(surface, rect)

    def draw(self):
        self.draw_background()

        for pipe in self.pipes:
            pipe.draw(self.screen)

        self.bird.draw(self.screen)

        if self.state == self.START:
            self.draw_centered("FLAPPY BIRD", self.title_font, 190)
            self.draw_centered("Press SPACE or click to start", self.font, 270)
            self.draw_centered("Avoid the pipes and survive!", self.small_font, 315)

        elif self.state == self.PLAYING:
            score_surface = self.large_font.render(str(self.score), True, WHITE)
            score_rect = score_surface.get_rect(center=(WIDTH // 2, 55))
            self.screen.blit(score_surface, score_rect)

        elif self.state == self.GAME_OVER:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 100))
            self.screen.blit(overlay, (0, 0))

            self.draw_centered("GAME OVER", self.title_font, 200)
            self.draw_centered(f"Score: {self.score}", self.font, 270)
            self.draw_centered("Press SPACE, R, or click to restart", self.small_font, 320)

        pygame.display.flip()

    def run(self):
        while True:
            self.clock.tick(FPS)
            self.handle_input()
            self.update()
            self.draw()


if __name__ == "__main__":
    game = FlappyBirdGame()
    game.run()
