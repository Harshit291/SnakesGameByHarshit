import os
import random
import pygame
author = 'Harshit Gupta'

# Importing The Modules

# Initialization
pygame.mixer.init()
pygame.init()


# Colors
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)

# Game Backgrounds
gameBackground = pygame.image.load("image/backimage2.jpg")
welcomeScreen = pygame.image.load("image/welcome.png")
gameOverBackground = pygame.image.load("image/wasted.png")

# Creating The window
screen_width = 900
screen_height = 600
gameWindow = pygame.display.set_mode((screen_width, screen_height))

# Game Title
pygame.display.set_caption("Snakes Game By Harshit")
pygame.display.update()

# Sound


# Variables For The Game
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 40)


def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x, y])


def plot_snake(gameWindow, color, snk_list, snake_size):
    for x, y in snk_list:
        pygame.draw.circle(gameWindow, color, [x, y], snake_size)


# Welcome Screen

def welcome():
    pygame.mixer.music.load('sound/welcomeScreenMusic.mp3')
    pygame.mixer.music.play()
    pygame.mixer.music.set_volume(.6)
    exit_game = False
    while not exit_game:
        gameWindow.blit(welcomeScreen, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.load('sound/gameBackgroundMusic.mp3')
                    pygame.mixer.music.play(5)
                    gameloop()
        pygame.display.update()
        clock.tick(60)

# Game Loop


def gameloop():

    # Game specific variables
    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 55
    velocity_x = 0
    velocity_y = 0
    snk_list = []
    snk_length = 1

# Highscore Build
    if(not os.path.exists("highscore.txt")):
        with open("highscore.txt", "w") as f:
            f.write("0")
    with open("highscore.txt", "r") as f:
        highscore = f.read()

# Food
    food_x = random.randint(20, screen_width / 2)
    food_y = random.randint(20, screen_height / 2)

# Game Variables
    score = 0
    init_velocity = 5
    snake_size = 15
    fps = 40
    while not exit_game:
        if game_over:
            with open("highScore/highscore.txt", "w") as f:
                f.write(str(highscore))

            # GameOverScreen
            gameWindow.blit(gameOverBackground, (0, 0))
            text_screen("Score: " + str(score), white, 385, 350)
            text_screen("Press SpaceBar", white, 365, 400)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        welcome()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_LEFT:
                        velocity_x = - init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_UP:
                        velocity_y = - init_velocity
                        velocity_x = 0
                    if event.key == pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0
                    # Cheat Code    
                    if event.key == pygame.K_TAB:
                        score += 10
            snake_x = snake_x + velocity_x
            snake_y = snake_y + velocity_y

            # Snake Eating Food Logic
            if abs(snake_x - food_x) < 10 and abs(snake_y - food_y) < 10:
                score += 10
                food_x = random.randint(20, screen_width / 2)
                food_y = random.randint(20, screen_height / 2)
                snk_length += 5
                if score > int(highscore):
                    highscore = score
            gameWindow.blit(gameBackground, (0, 0))
            text_screen('Score: ' + str(score) + "    High Score: " +
                        str(highscore), white, 270, 5)
            pygame.draw.circle(gameWindow, red, [food_x, food_y], 15)
            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            # Snake Length Conrolling Logic
            if len(snk_list) > snk_length:
                del snk_list[0]

            # Commenting this game over logic as it makes game a little hard and Uninteresting
            # if head in snk_list[:-1]:
            #     game_over = True
            #     pygame.mixer.music.load('sound/Explosion.mp3')
            #     pygame.mixer.music.play()
            #     pygame.mixer.music.set_volume(.6)

            # Game Over Logic    
            if snake_x < 0 or snake_x > screen_width or snake_y < 0 or snake_y > screen_height:
                game_over = True
                pygame.mixer.music.load('sound/Explosion.mp3')
                pygame.mixer.music.play()
                pygame.mixer.music.set_volume(.6)
            plot_snake(gameWindow, white, snk_list, snake_size)
        pygame.display.update()
        clock.tick(fps)
    pygame.quit()
    quit()


welcome()
