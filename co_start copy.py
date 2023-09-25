# initialize pygame
import pygame
import random
import pyautogui



pygame.init()

# set up the game window
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 300
game_window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Chrome Dino Game")

# load the background image
background_image = pygame.image.load("background.jpeg").convert_alpha()
background_image = pygame.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))

# set up the game clock
clock = pygame.time.Clock()

# set up the game variables
GRAVITY = .9
dino_x = 70
dino_y = 0
dino_y_velocity = 0
dino_width = 50
dino_height = 50
cactus_x = WINDOW_WIDTH
cactus_y = 0
cactus_width = 30
cactus_height = 70
score = 0
font = pygame.font.Font(None, 30)

# load the images
dino_image = pygame.image.load("dino.png").convert_alpha()
dino_image = pygame.transform.scale(dino_image, (dino_width, dino_height))
cactus_image = pygame.image.load("cactus.png").convert_alpha()
cactus_image = pygame.transform.scale(cactus_image, (cactus_width, cactus_height))

# load the music
background_sound = pygame.mixer.music.load("background.mp3")
pygame.mixer.music.play(-1)
jump_sound = pygame.mixer.Sound("jump.mp3")
gameover_sound = pygame.mixer.Sound("gameover.mp3")

# define the functions
def display_score():
    score_text = font.render("Score: " + str(score), True, (255, 255, 255))
    game_window.blit(score_text, (10, 10))

# define the function which shows clock.tick value in left bottom corner of game window
def display_fps():
    fps_text = font.render("FPS: " + str(int(clock.get_fps())), True, (255, 255, 255))
    game_window.blit(fps_text, (10, WINDOW_HEIGHT - 20))


def display_game_over():
    game_over_text = font.render("Game Over", True, (255, 255, 255))
    game_window.blit(game_over_text, (WINDOW_WIDTH/2 - 50, WINDOW_HEIGHT/2 - 15))
    restart_text = font.render("Press any key to restart", True, (255, 255, 255))
    game_window.blit(restart_text, (WINDOW_WIDTH/2 - 200, WINDOW_HEIGHT/2 + 15))
    #pygame.mixer.music.play(-1)
    

def generate_cactus():
    global cactus_x, cactus_y
    cactus_x = WINDOW_WIDTH
    cactus_y = 220 + random.randint(-40, 0)

def is_collision():
    if (cactus_x >= dino_x and cactus_x <= dino_x + dino_width) or \
       (dino_x >= cactus_x and dino_x <= cactus_x + cactus_width):
        if (dino_y + dino_height >= cactus_y):
            pygame.mixer.music.stop()
            gameover_sound.play()
            return True
    return False

# game loop
game_running = True
game_over = False
while game_running:
    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False
        if event.type == pygame.KEYDOWN:
            if game_over:
                game_over = False
                score = 0
                dino_y = 200
                cactus_x = WINDOW_WIDTH
                cactus_y = 200
                dino_y_velocity = 0
            elif event.key == pygame.K_SPACE and dino_y == 200:
                dino_y_velocity = -15
                jump_sound.play()

    # update the game
    if not game_over:
        # move the dino
        dino_y_velocity += GRAVITY
        dino_y += dino_y_velocity
        if dino_y >= 200:
            dino_y = 200
            dino_y_velocity = 0

        # move the cactus
        cactus_x -= 5
        if cactus_x < -cactus_width:
            generate_cactus()
            score += 1

        # check for collision
        if is_collision():
            game_over = True

    # if jump is successful, then print "Jump Successful" in console
    if cactus_x == dino_x + 100:
        print("Press Space")
        #pyautogui.press('space')

    
    # draw the game
    game_window.fill((0, 0, 0))
    game_window.blit(dino_image, (dino_x, dino_y))
    game_window.blit(cactus_image, (cactus_x, cactus_y))
    # draw a green line on the platform
    #pygame.draw.rect(game_window, (0, 255, 0), (0, 250), (WINDOW_WIDTH, 250), 4)
  
    pygame.draw.rect(game_window, (100, 200, 50), pygame.Rect((0,250), (WINDOW_WIDTH, WINDOW_HEIGHT - 250)), 0)
    display_fps()
    display_score()
    if game_over:
        display_game_over()
    pygame.display.update()
   
    clock.tick(score*5 + 60)

# quit pygame
pygame.quit()