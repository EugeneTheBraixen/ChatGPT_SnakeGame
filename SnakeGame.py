import pygame
import sys
import random

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
FPS = 10

# Цвета
WHITE = (255, 255, 255)
DARK_GREEN = (0, 100, 0)
LIGHT_GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Инициализация экрана
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake')

# Флаг "Игра окончена"
game_over = False

# Флаг для паузы
paused = False

# Шрифт для текста
font = pygame.font.Font(None, 36)

# Функция для вывода текста на экран
def draw_text(text, x, y, color=RED, size=36):
    text_surface = pygame.font.Font(None, size).render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

# Текущее состояние игры (0 - игра, 1 - Game Over)
current_state = 0

# Переменные для игры
snake = [(5, 5)]
snake_direction = (1, 0)
food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
score = 0

# Флаги для кнопок
continue_clicked = False
exit_clicked = False

# Кнопки для меню Game Over
continue_button = pygame.Rect(WIDTH // 2 - 70, HEIGHT // 2 + 70, 140, 50)
exit_button = pygame.Rect(WIDTH // 2 - 70, HEIGHT // 2 + 140, 140, 50)

# Игровой цикл
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:  # Пауза по клавише P
                if current_state == 0:  # Если игра идет, переходите в режим паузы
                    paused = not paused
                    current_state = 2  # Переключение в состояние "Пауза"
                elif current_state == 2:  # Если уже в режиме паузы, возобновите игру
                    paused = not paused
                    current_state = 0  # Вернуться в игру

        if current_state == 0 and not paused:  # Если игра запущена и не находится в состоянии паузы
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and snake_direction != (0, 1):
                    snake_direction = (0, -1)
                elif event.key == pygame.K_s and snake_direction != (0, -1):
                    snake_direction = (0, 1)
                elif event.key == pygame.K_a and snake_direction != (1, 0):
                    snake_direction = (-1, 0)
                elif event.key == pygame.K_d and snake_direction != (-1, 0):
                    snake_direction = (1, 0)

    if current_state == 0:  # Если игра запущена
        if not game_over and not paused:
            # Движение змейки
            new_head = (snake[0][0] + snake_direction[0], snake[0][1] + snake_direction[1])
            snake.insert(0, new_head)

            # Проверка на столкновение с границами
            if not (0 <= new_head[0] < GRID_WIDTH) or not (0 <= new_head[1] < GRID_HEIGHT):
                game_over = True

            # Проверка на столкновение с самой собой
            if new_head in snake[1:]:
                game_over = True

            # Проверка на поедание еды
            if new_head == food:
                food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
                score += 1  # Увеличиваем счет
            else:
                snake.pop()

            # Очистка экрана
            for y in range(0, HEIGHT, GRID_SIZE):
                for x in range(0, WIDTH, GRID_SIZE):
                    if (x // GRID_SIZE + y // GRID_SIZE) % 2 == 0:
                        pygame.draw.rect(screen, DARK_GREEN, (x, y, GRID_SIZE, GRID_SIZE))
                    else:
                        pygame.draw.rect(screen, LIGHT_GREEN, (x, y, GRID_SIZE, GRID_SIZE))

            # Отрисовка еды
            pygame.draw.rect(screen, RED, (food[0] * GRID_SIZE, food[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

            # Отрисовка змейки
            for segment in snake:
                pygame.draw.rect(screen, BLACK, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

            # Отображение счета
            draw_text(f"Score: {score}", WIDTH - 100, 20, color=RED)

        elif game_over:
            current_state = 1  # Переход в состояние "Game Over"

    if current_state == 1:  # Если состояние "Game Over"
        for y in range(0, HEIGHT, GRID_SIZE):
            for x in range(0, WIDTH, GRID_SIZE):
                if (x // GRID_SIZE + y // GRID_SIZE) % 2 == 0:
                    pygame.draw.rect(screen, DARK_GREEN, (x, y, GRID_SIZE, GRID_SIZE))
                else:
                    pygame.draw.rect(screen, LIGHT_GREEN, (x, y, GRID_SIZE, GRID_SIZE))

        # Вывод "Game Over" и кнопок
        draw_text("Game Over", WIDTH // 2, HEIGHT // 2 - 50, color=RED)

        pygame.draw.rect(screen, LIGHT_GREEN, continue_button)
        pygame.draw.rect(screen, LIGHT_GREEN, exit_button)

        draw_text("Continue", continue_button.centerx, continue_button.centery, color=BLACK)
        draw_text("Exit", exit_button.centerx, exit_button.centery, color=BLACK)

        # Обработка нажатий кнопок в меню Game Over
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if continue_button.collidepoint(mouse_pos) and not continue_clicked:
                    continue_clicked = True
                    # Сброс игры и счета
                    snake = [(5, 5)]
                    snake_direction = (1, 0)
                    food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
                    game_over = False
                    score = 0
                    current_state = 0  # Переход в игру
                    paused = False
                elif exit_button.collidepoint(mouse_pos) and not exit_clicked:
                    exit_clicked = True
                    pygame.quit()
                    sys.exit()

    # Обновление экрана
    pygame.display.flip()

    # Ограничение кадров в секунду
    clock.tick(FPS)
