import pygame
import random
import sklearn
import os

pygame.mixer.init()

pygame.init()

# Colors
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
# https://source.unsplash.com/300x500/?snake,cobra
screen_width = 900
screen_height = 600

# Creating Window
gameWindow = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("SnakesWithHarshit")
pygame.display.update()

# Background Image
background_image = pygame.image.load("image/backimage2.jpg")
background_image = pygame.transform.scale(background_image, (screen_width, screen_height)).convert_alpha()
# Game Over Background
game_over_image = pygame.image.load("image/wasted.png")
game_over_image = pygame.transform.scale(game_over_image, (screen_width, screen_height)).convert_alpha()

# Welcome Image
welcome_image = pygame.image.load("image/Untitled.png")
welcome_image = pygame.transform.scale(welcome_image, (screen_width, screen_height)).convert_alpha()

# Creating Clock
clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 50)
font2 = pygame.font.SysFont(None, 40)


def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x, y])


def game_over_screen(text, color, x, y):
    screen_text2 = font2.render(text, True, color)
    gameWindow.blit(screen_text2, [int(x), int(y)])


def plot_snake(gamewindow, color, snk_list, snake_size):
    for x, y in snk_list:
        pygame.draw.rect(gamewindow, color, [x, y, snake_size, snake_size])


def welcome():
    exit_game = False
    while not exit_game:
        gameWindow.fill((230, 210, 229))
        gameWindow.blit(welcome_image, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.load('sound/background_music.mp3')
                    pygame.mixer.music.play()
                    game_loop()

        pygame.display.update()
        clock.tick(60)


def game_loop():
    # Game specific Variables
    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 55
    snake_width = 15
    fps = 30
    velocity_x = 0
    velocity_y = 0
    food_x = random.randint(20, screen_width)
    food_y = random.randint(60, screen_height)
    score = 0
    init_velocity = 5
    snk_list = []
    snk_length = 1

    if not os.path.exists('hiscore.txt'):
        with open('hiscore.txt', 'w') as f:
            f.write('0')

    with open("hiscore.txt", "r") as f:
        hiscore = f.read()

    # Creating a game loop
    while not exit_game:
        if game_over:

            gameWindow.fill((230, 210, 229))
            gameWindow.blit(game_over_image, (0, 0))
            game_over_screen(str(score), red, (screen_width / 2)+30, screen_height / 2 + 130)
            game_over_screen('Press Enter To Play Again', red, (screen_width / 2)-150, screen_height / 2 + 180)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0
                    elif event.key == pygame.K_LEFT:
                        velocity_x = -init_velocity
                        velocity_y = 0
                    elif event.key == pygame.K_UP:
                        velocity_y = -init_velocity
                        velocity_x = 0
                    elif event.key == pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0

            snake_x = snake_x + velocity_x
            snake_y = snake_y + velocity_y

            if abs(snake_x - food_x) < 10 and abs(snake_y - food_y) < 10:
                score = (score + 10)
                food_x = random.randint(20, screen_width / 2)
                food_y = random.randint(20, screen_height / 2)
                snk_length += 5
            if score > int(hiscore):
                hiscore = score

                with open('hiscore.txt', 'w') as f:
                    f.write(str(hiscore))

            gameWindow.fill((230, 210, 229))
            gameWindow.blit(background_image, (0, 0))
            text_screen('Score: ' + str(score) + "    Hi Score: " + str(hiscore), white, 270, 5)
            head = [snake_x, snake_y]
            snk_list.append(head)

            if len(snk_list) > snk_length:
                del snk_list[0]

            if head in snk_list[:-1]:
                game_over = True
                pygame.mixer.music.load('sound/Explosion.mp3')
                pygame.mixer.music.play()

            if snake_x < 0 or snake_x > screen_width or snake_y < 0 or snake_y > screen_height:
                game_over = True
                pygame.mixer.music.load('sound/Explosion.mp3')
                pygame.mixer.music.play()

            pygame.draw.circle(gameWindow, red, [food_x, food_y], 7)
            plot_snake(gameWindow, white, snk_list, snake_width)
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()


welcome()
