import pygame
from pygame import mixer
import random
import math

# Initialize the pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))

# Background image
background = pygame.image.load('background.jpg')

# Background sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Player
player_image = pygame.image.load('spaceship.png')
player_position_x = 370
player_position_y = 480
player_x_change = 0

# Enemy
enemy_image = []
enemy_position_x = []
enemy_position_y = []
enemy_x_change = []
enemy_y_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemy_image.append(pygame.image.load('monster.png'))
    enemy_position_x.append(random.randint(0, 735))
    enemy_position_y.append(random.randint(50, 150))
    enemy_x_change.append(1)
    enemy_y_change.append(40)

# Bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 5
# Ready - You can't see the bullet on screen
# Fire - Bullet is currently moving
bullet_state = 'ready'

# Score
score_value = 0
font = pygame.font.Font('Alien Mine Italic.ttf', 18)
textX = 10
textY = 10

# Game Over
over_font = pygame.font.Font('Alien Mine Italic.ttf', 64)

# Game loop
running = True


def _show_score(x, y):
    score = font.render('Score: ' + str(score_value), True, (255, 0, 0))
    screen.blit(score, (x, y))


def _player(x, y):
    screen.blit(player_image, (x, y))


def _enemy(x, y, num):
    screen.blit(enemy_image[num], (x, y))


def _fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg, (x + 16, y + 10))


def _is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt((math.pow(enemy_x - bullet_x, 2)) +
                         (math.pow(enemy_y - bullet_y, 2)))
    return distance < 27


def _game_over():
    over_text = over_font.render('GAME OVER', True, (255, 0, 0))
    rect = over_text.get_rect()
    rect.center = screen.get_rect().center
    screen.blit(over_text, rect)


def _define_player_boundary():
    global player_position_x
    if player_position_x <= 0:
        player_position_x = 0
    elif player_position_x >= 764:
        player_position_x = 736


# -------- Main Program Loop -----------
while running:
    # RGB
    screen.fill((2, 20, 20))
    screen.blit(background, (0, 0))
    # --- Event Processing
    for event in pygame.event.get():  # Get all events
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                running = True

            if event.key == pygame.K_LEFT:
                player_x_change = -5
            if event.key == pygame.K_RIGHT:
                player_x_change = 5
            if event.key == pygame.K_SPACE and bullet_state is 'ready':
                bullet_sound = mixer.Sound('laser.wav')
                bullet_sound.play()
                # Get the x coordinate of spaceship
                bulletX = player_position_x
                _fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP and \
                (event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT):
            player_x_change = 0

    player_position_x += player_x_change

    # Checking for boundaries
    _define_player_boundary()

    # Enemy movement
    for i in range(num_of_enemies):
        # Game Over
        if enemy_position_y[i] > 440:
            for j in range(num_of_enemies):
                enemy_position_y[j] = 2000
            _game_over()
            break
        enemy_position_x[i] += enemy_x_change[i]
        if enemy_position_x[i] <= 0:
            enemy_x_change[i] = 2
            enemy_position_y[i] += enemy_y_change[i]
        elif enemy_position_x[i] >= 764:
            enemy_x_change[i] = -2
            enemy_position_y[i] += enemy_y_change[i]

        # Collision
        collision = _is_collision(enemy_position_x[i], enemy_position_y[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = 'ready'
            score_value += 1
            enemy_position_x[i] = random.randint(0, 735)
            enemy_position_y[i] = random.randint(50, 150)

        _enemy(enemy_position_x[i], enemy_position_y[i], i)

    # Bullet Movement
    if bulletY <= 0:
        bullet_state = 'ready'
        bulletY = 480
    if bullet_state is 'fire':
        _fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    if bulletX == enemy_position_x:
        print('gotchaaa!')

    _player(player_position_x, player_position_y)
    _show_score(textY, textY)
    pygame.display.update()
