"""
Icon & Enemy made by Smashicons from www.flaticon.com
Player made by Freepik from www.flaticon.com
Background image from NASA
"""
# pylint: disable-msg=C0103
import math
import random
import pygame
from pygame import mixer

# Initialize pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

#background
background = pygame.image.load("background.jpg")

# background sound
mixer.music.load("background.wav")
mixer.music.set_volume(0.25)
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("space-ship.png")
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

# Enemy movement

for i in range(num_of_enemies):

    enemyImg.append(pygame.image.load('alien.png'))
    enemyX.append(random.randint(0, 743))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(2)
    enemyY_change.append(40)

# Ammo
# ready: you can't see the bullet on the screen
# fire: the bullet is currently moving

ammoImg = pygame.image.load('ammo.png')
ammoX = 0
ammoY = 480
ammoX_change = 0
ammoY_change = 5
ammo_state = "ready"

# score

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# game over text
over_font = pygame.font.Font('freesansbold.ttf', 64)

def show_score(x, y):
    """
    score function
    """
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def player(x, y):
    """
    player function
    """
    screen.blit(playerImg, (x, y))

def game_over_text():
    """
    game over function
    """
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

def enemy(x, y, i):
    """
    enemy function
    """
    screen.blit(enemyImg[i], (x, y))

def fire_ammo(x, y):
    """
    ammo function
    """
    global ammo_state
    ammo_state = "fire"
    screen.blit(ammoImg, (x, y -10))

def isCollision(enemy_X, enemy_Y, ammo_X, ammo_Y):
    """
    collision detection
    """
    distance = math.sqrt((math.pow(enemy_X - ammo_X, 2)) + (math.pow(enemy_Y - ammo_Y, 2)))
    if distance < 40:
        return True
    else:
        return False

# game loop
running = True
while running:
    #RGB
    screen.fill((0, 0, 0))
    # bg image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -3
            if event.key == pygame.K_RIGHT:
                playerX_change = 3
            if event.key == pygame.K_SPACE:
                if ammo_state is "ready":
                    ammo_sound = mixer.Sound('laser.wav')
                    ammo_sound.play()
                    ammoX = playerX
                    fire_ammo(ammoX, ammoY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change
    # prevents ship from going out of bounds
    if playerX <= 0:
        playerX = 0
    elif playerX >= 744:
        playerX = 744

    # enemy movement
    for i in range(num_of_enemies):
        #game over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 0:
            enemyX_change[i] = 2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 744:
            enemyX_change[i] = -2
            enemyY[i] += enemyY_change[i]

         # collision
        collision = isCollision(enemyX[i], enemyY[i], ammoX, ammoY)
        if collision:
            explosion_Sound = mixer.Sound("explosion.wav")
            explosion_Sound.play()
            ammoY = 480
            ammo_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 743)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # ammo movement
    if ammoY <= 0:
        ammoY = 480
        ammo_state = "ready"

    if ammo_state is "fire":
        fire_ammo(ammoX, ammoY)
        ammoY -= ammoY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
