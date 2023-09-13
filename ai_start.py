import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width, screen_height = 800, 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Dino Jump")

# Colors
white = (255, 255, 255)
black = (0, 0, 0)

# Dino attributes
dino_width, dino_height = 50, 50
dino_x, dino_y = 100, screen_height - dino_height
dino_y_velocity = 0

# Obstacle attributes
obstacle_width, obstacle_height = 20, 40
obstacle_x = screen_width
obstacle_y = screen_height - obstacle_height
obstacle_speed = 5

# Gravity
gravity = 0.5

# Game variables
score = 0
game_over = False

# Fonts
font = pygame.font.Font(None, 36)
game_over_font = pygame.font.Font(None, 72)

def draw_dino(x, y):
    pygame.draw.rect(screen, black, [x, y, dino_width, dino_height])

def draw_obstacle(x, y):
    pygame.draw.rect(screen, black, [x, y, obstacle_width, obstacle_height])

def display_score(score):
    score_text = font.render("Score: " + str(score), True, black)
    screen.blit(score_text, (10, 10))

def display_game_over():
    game_over_text = game_over_font.render("Game Over", True, black)
    screen.blit(game_over_text, (screen_width // 2 - 150, screen_height // 2 - 36))

# Function to generate a random obstacle position
def random_obstacle_y():
    return random.randint(screen_height - obstacle_height - 20, screen_height - obstacle_height)

# Game loop
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_SPACE] and dino_y == screen_height - dino_height:
        dino_y_velocity = -10

    dino_y += dino_y_velocity

    # Apply gravity
    dino_y_velocity += gravity

    # Collision with ground
    if dino_y >= screen_height - dino_height:
        dino_y = screen_height - dino_height
        dino_y_velocity = 0

    # Move the obstacle and reset if it goes off-screen
    obstacle_x -= obstacle_speed
    
    if obstacle_x < 0:
        obstacle_x = screen_width
        obstacle_y = random_obstacle_y()
        score += 1

    # Check for collision
    if dino_x + dino_width > obstacle_x and dino_x < obstacle_x + obstacle_width:
        if dino_y + dino_height > obstacle_y:
            game_over = True

    # Clear the screen
    screen.fill(white)

    draw_dino(dino_x, dino_y)
    draw_obstacle(obstacle_x, obstacle_y)
    display_score(score)

    if game_over:
        display_game_over()

    pygame.display.update()

# Quit Pygame
pygame.quit()
sys.exit()
