import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))

# Title and Icon
pygame.display.set_caption("Shoot 'Em Up")
icon = pygame.image.load('spaceship.png')  # Replace with your spaceship icon file
pygame.display.set_icon(icon)

# Player
player_img = pygame.image.load('spaceship.png')  # Replace with your spaceship image file
player_x = 370
player_y = 480
player_x_change = 0

# Enemy
enemy_img = pygame.image.load('enemy.png')  # Replace with your enemy image file
enemy_x = random.randint(0, 735)
enemy_y = random.randint(50, 150)
enemy_x_change = 4 # Adjusted for slower speed
enemy_y_change = 40  # Adjusted for slower descent

# Bullet
bullet_img = pygame.image.load('bullet.png')  # Replace with your bullet image file
bullet_x = 0
bullet_y = 480
bullet_y_change = 18  # Adjusted for slower bullet speed
bullet_state = "ready"  # "ready" - you can't see the bullet, "fire" - the bullet is moving

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

text_x = 10
text_y = 10

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Function to show the score
def show_score(x, y):
    score = font.render(f"Score: {score_value}", True, (255, 255, 255))
    screen.blit(score, (x, y))

# Function to draw the player
def player(x, y):
    screen.blit(player_img, (x, y))

# Function to draw the enemy
def enemy(x, y):
    screen.blit(enemy_img, (x, y))

# Function to fire the bullet
"""(I used AI here)"""
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x + 16, y + 10))

# Function to check for collisions
def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt(math.pow(enemy_x - bullet_x, 2) + math.pow(enemy_y - bullet_y, 2))
    return distance < 27

# Game Loop
running = True
while running:
    # RGB - Red, Green, Blue
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # If keystroke is pressed, check if it's left or right
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -5
            if event.key == pygame.K_RIGHT:
                player_x_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_x = player_x
                    fire_bullet(bullet_x, bullet_y)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0

    # Player Movement
    player_x += player_x_change

    # Boundary checking for player
    if player_x <= 0:
        player_x = 0
    elif player_x >= 736:
        player_x = 736

    # Enemy Movement
    enemy_x += enemy_x_change
    if enemy_x <= 0:
        enemy_x_change = 2  # Adjusted speed
        enemy_y += enemy_y_change
    elif enemy_x >= 736:
        enemy_x_change = -2  # Adjusted speed
        enemy_y += enemy_y_change

    # Bullet Movement
    if bullet_state == "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_y_change

    # Bullet Reset
    if bullet_y <= 0:
        bullet_y = 480
        bullet_state = "ready"

    # Collision Detection
    """(I used AI here)"""
    collision = is_collision(enemy_x, enemy_y, bullet_x, bullet_y)
    if collision:
        bullet_y = 480
        bullet_state = "ready"
        score_value += 1
        enemy_x = random.randint(0, 735)
        enemy_y = random.randint(50, 150)

    # Draw Everything
    player(player_x, player_y)
    enemy(enemy_x, enemy_y)
    show_score(text_x, text_y)

    # Update the display
    pygame.display.update()

    # Control the frame rate
    clock.tick(60)  # Adjust FPS as needed (e.g., 30 for slower gameplay)
