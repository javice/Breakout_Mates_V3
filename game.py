import pygame
import random
import time

# Inicializar pygame
pygame.init()

# Constantes de configuración
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
FPS = 60
PADDLE_WIDTH, PADDLE_HEIGHT = 100, 20
BALL_RADIUS = 10
BRICK_WIDTH, BRICK_HEIGHT = 75, 30
INITIAL_LIVES = 5
INITIAL_SCORE = 0
INITIAL_LEVEL = 1
INITIAL_TIME_TO_ANSWER = 15

# Configuración de la pantalla
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Breakout Matemático")
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()

class Paddle:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH // 2 - PADDLE_WIDTH // 2, HEIGHT - 50, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.speed = [3,3]

    def move(self):
        self.rect.x += self.speed
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

    def draw(self):
        pygame.draw.rect(screen, WHITE, self.rect)

class Ball:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH // 2 - BALL_RADIUS, HEIGHT // 2 - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)
        self.speed = [3, -3]

    def move(self):
        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1]

    def bounce(self, axis):
        self.speed[axis] = -self.speed[axis]

    def draw(self):
        pygame.draw.ellipse(screen, RED, self.rect)

class Brick:
    def __init__(self, x, y, operation):
        self.rect = pygame.Rect(x, y, BRICK_WIDTH, BRICK_HEIGHT)
        self.operation = operation

    def draw(self):
        pygame.draw.rect(screen, GREEN, self.rect)

class PowerUp:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.speed = 3

    def move(self):
        self.rect.y += self.speed

    def draw(self):
        pygame.draw.rect(screen, BLUE, self.rect)

class Game:
    def __init__(self):
        self.paddle = Paddle()
        self.ball = Ball()
        self.bricks = []
        self.power_ups = []
        self.lives = INITIAL_LIVES
        self.score = INITIAL_SCORE
        self.level = INITIAL_LEVEL
        self.time_to_answer = INITIAL_TIME_TO_ANSWER
        self.running = True
        self.create_bricks()

    def create_bricks(self):
        self.bricks.clear()
        for i in range(5):
            for j in range(10):
                x = j * (BRICK_WIDTH + 10) + 50
                y = i * (BRICK_HEIGHT + 10) + 50
                operation = self.generate_operation()
                self.bricks.append(Brick(x, y, operation))

    def create_power_up(self, x, y):
        self.power_ups.append(PowerUp(x, y))

    def check_power_up_collision(self):
        for power_up in self.power_ups[:]:
            if self.paddle.rect.colliderect(power_up.rect):
                self.paddle.rect.width += 50
                self.power_ups.remove(power_up)

    def generate_operation(self):
        a = random.randint(1, 10)
        b = random.randint(1, 10)
        operation = random.choice(['+', '-', '*'])
        if operation == '+':
            result = a + b
        elif operation == '-':
            result = a - b
        else:
            result = a * b
        return f"{a} {operation} {b} = ?", result

    def draw_text(self, text, x, y, color):
        text_surface = font.render(text, True, color)
        screen.blit(text_surface, (x, y))

    def show_question(self, operation):
        start_time = time.time()
        answer = ""
        while True:
            screen.fill(BLACK)
            self.draw_text(f"Resuelve: {operation[0]}", WIDTH // 2 - 100, HEIGHT // 2 - 50, RED)
            self.draw_text(f"Tiempo restante: {int(self.time_to_answer - (time.time() - start_time))}", WIDTH // 2 - 100, HEIGHT // 2, WHITE)
            self.draw_text(f"Respuesta: {answer}", WIDTH // 2 - 100, HEIGHT // 2 + 50, RED)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        try:
                            if int(answer) == operation[1]:
                                self.score += 100
                            else:
                                self.lives -= 1
                            return
                        except ValueError:
                            pass
                    elif event.key == pygame.K_BACKSPACE:
                        answer = answer[:-1]
                    else:
                        answer += event.unicode

            if time.time() - start_time > self.time_to_answer:
                self.lives -= 1
                return

    def game_over(self):
        screen.fill(BLACK)
        self.draw_text("¡Game Over!", WIDTH // 2 - 100, HEIGHT // 2 - 50, RED)
        self.draw_text(f"Puntuación final: {self.score}", WIDTH // 2 - 100, HEIGHT // 2, WHITE)
        pygame.display.flip()
        pygame.time.wait(3000)
        pygame.quit()

    def next_level(self):
        self.level += 1
        self.time_to_answer -= 5
        self.create_bricks()

    def run(self):
        while self.running:
            self.check_power_up_collision()
            for power_up in self.power_ups:
                power_up.move()
                power_up.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.paddle.speed = -5
                    if event.key == pygame.K_RIGHT:
                        self.paddle.speed = 5
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        self.paddle.speed = 0

            self.paddle.move()
            self.ball.move()

            if self.ball.rect.left < 0 or self.ball.rect.right > WIDTH:
                self.ball.bounce(0)
            if self.ball.rect.top < 0:
                self.ball.bounce(1)
            if self.ball.rect.bottom > HEIGHT:
                self.lives -= 1
                if self.lives == 0:
                    self.game_over()
                    self.running = False
                else:
                    self.ball.rect.x, self.ball.rect.y = WIDTH // 2 - BALL_RADIUS, HEIGHT // 2 - BALL_RADIUS

            if self.ball.rect.colliderect(self.paddle.rect):
                self.ball.bounce(1)

            for brick in self.bricks[:]:
                if self.ball.rect.colliderect(brick.rect):
                    self.ball.bounce(1)
                    self.show_question(brick.operation)
                    self.bricks.remove(brick)
                    if not self.bricks:
                        self.next_level()

            screen.fill(BLACK)
            self.paddle.draw()
            self.ball.draw()
            for brick in self.bricks:
                brick.draw()
            self.draw_text(f"Vidas: {self.lives}", 10, 10, WHITE)
            self.draw_text(f"Puntuación: {self.score}", WIDTH - 200, 10, WHITE)
            self.draw_text(f"Nivel: {self.level}", WIDTH // 2 - 50, 10, WHITE)

            pygame.display.flip()
            clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.run()