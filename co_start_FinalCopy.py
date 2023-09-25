# initialize pygame
import pygame
# intilize random
import random

#For Model Training and Prediction
import tensorflow.keras

import neat


class Model:    
        DistanceFromCactus = 0
        CactusHeight = 0
        CactusVelocity = 0
        DistanceFromGround = 0
        Timer = 0


class ChromeDinoGame:
    def __init__(self):
        pygame.init()

        # set up the game window
        self.WINDOW_WIDTH = 1200
        self.WINDOW_HEIGHT = 300
        self.game_window = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption("Chrome Dino Game")

        # load the background image
        self.background_image = pygame.image.load("background.jpeg").convert_alpha()
        self.background_image = pygame.transform.scale(self.background_image, (self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        
        # load the background image
        self.background_image = pygame.image.load("background.jpeg").convert_alpha()
        self.background_image = pygame.transform.scale(self.background_image, (self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        # load grass image
        self.grass_image = pygame.image.load("grass.png").convert_alpha()
        self.grass_image = pygame.transform.scale(self.grass_image, (self.WINDOW_WIDTH, self.WINDOW_HEIGHT- 260))
       
       
        # set up the game clock
        self.clock = pygame.time.Clock()

        # set up the game variables
        self.GRAVITY = .9
        self.dino = Dino(80, 0, 60, 70)
        self.cactus = Cactus(self.WINDOW_WIDTH, 220)
        Model.CactusHeight = self.WINDOW_HEIGHT - 220
        self.score = 0
        self.font = pygame.font.Font(None, 30)

        # load the music
        self.background_sound = pygame.mixer.music.load("background.mp3")
        pygame.mixer.music.play(-1)
        self.jump_sound = pygame.mixer.Sound("jump.mp3")
        self.gameover_sound = pygame.mixer.Sound("gameover.mp3")
        

        pygame.draw.rect(self.game_window, (100, 200, 50), pygame.Rect((0,250), (self.WINDOW_WIDTH, self.WINDOW_HEIGHT - 250)), 0)
        pygame.display.flip() 
        
    def display_score(self):
        score_text = self.font.render("Score: " + str(self.score), True, (255, 255, 255))
        self.game_window.blit(score_text, (10, 10))

    def display_fps(self):
        fps_text = self.font.render("FPS: " + str(int(self.clock.get_fps())), True, (255, 255, 255))
        self.game_window.blit(fps_text, (10, self.WINDOW_HEIGHT - 20))

    def display_game_over(self):
        game_over_text = self.font.render("Game Over", True, (60, 60, 100))
        self.game_window.blit(game_over_text, (self.WINDOW_WIDTH/2 - 50, self.WINDOW_HEIGHT/2 - 15))
        restart_text = self.font.render("Press any key to restart", True, (60, 60, 100))
        self.game_window.blit(restart_text, (self.WINDOW_WIDTH/2 - 100, self.WINDOW_HEIGHT/2 + 15))
        
    def generate_cactus(self):
        self.cactus.x = self.WINDOW_WIDTH
        self.cactus.y = 200 + random.randint(-50, 0)
        Model.CactusHeight = self.WINDOW_HEIGHT - self.cactus.y
        print(self.cactus.y)

    def is_collision(self):
        if (self.cactus.x >= self.dino.x - 25 and self.cactus.x <= self.dino.x - 25 + self.dino.width) or \
           (self.dino.x - 50 >= self.cactus.x and self.dino.x <= self.cactus.x + self.cactus.width):
            if (self.dino.y - 25 + self.dino.height >= self.cactus.y):
                pygame.mixer.music.stop()
                self.gameover_sound.play()
                return True
        return False

    def run(self):
        # game loop
        game_running = True
        game_over = False
        Timer = 0
        while game_running:
            Timer += 1
            # handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_running = False
                if event.type == pygame.KEYDOWN:
                    if game_over:
                        game_over = False
                        self.score = 0
                        self.dino.y = 200
                        self.cactus.x = self.WINDOW_WIDTH
                        self.cactus.y = 200
                        self.dino.y_velocity = 0
                        pygame.mixer.music.play(-1)
                        Timer = 0

                    elif event.key == pygame.K_SPACE and self.dino.y == 200:
                        self.dino.y_velocity = -15
                        self.jump_sound.play()
                        Model.Timer = Timer
                        Timer = 0

            if not game_over:
                                # update game state
                self.dino.update(self.GRAVITY)
                self.dino.update_image(self.score)
                self.cactus.update(self.score)
                if self.cactus.x < -self.cactus.width:
                    self.cactus.x = self.WINDOW_WIDTH
                    self.generate_cactus()
                    self.score += 1
                if self.is_collision():

                    game_over = True

                # draw game objects
                self.game_window.blit(self.background_image, (0, 0))
                self.game_window.blit(self.dino.image, (self.dino.x, self.dino.y))
                self.game_window.blit(self.cactus.image, (self.cactus.x, self.cactus.y))
                self.game_window.blit(self.grass_image, (0, 250))
                # draw a brown rectangle for the ground (y = 250) 
                pygame.draw.rect(self.game_window, (150, 75, 0), pygame.Rect((0,290), (self.WINDOW_WIDTH, self.WINDOW_HEIGHT - 290)), 0)
                # draw a line in red color from dino right bottom to cactus top left
                pygame.draw.line(self.game_window, (255, 0, 0), (self.dino.x + self.dino.width, self.dino.y + self.dino.height), (self.cactus.x, self.cactus.y), 2)

                self.display_score()
                self.display_fps()

                # Model Calculations
                Model.DistanceFromGround = 200 - round(self.dino.y)
            else:
                self.display_game_over()

            print( Model.DistanceFromCactus, Model.CactusHeight, Model.CactusVelocity, Model.DistanceFromGround, Model.Timer)           
            # update the display
            pygame.display.update()

            # limit the frame rate
            self.clock.tick(60)

class Dino:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.y_velocity = 0
        self.images = [pygame.image.load("mario2.png").convert_alpha(),
                       pygame.image.load("mario3.png").convert_alpha()]
        self.current_image = 0
        self.image = pygame.transform.scale(self.images[self.current_image], (self.width, self.height))
        self.image_timer = 0
        self.image_interval = 100  # set the image interval to 0.1 seconds (100 milliseconds)
        
    def update_image(self, score):
        self.image_timer += 10 + round(score/5) # increment the timer by the time elapsed since the last frame
        if self.image_timer >= self.image_interval:  # if the image interval has elapsed
            self.current_image = (self.current_image + 1) % len(self.images)  # cycle through the images
            self.image = pygame.transform.scale(self.images[self.current_image], (self.width, self.height))
            self.image_timer = 0  # reset the timer

    def update(self, gravity):
        self.y_velocity += gravity
        self.y += self.y_velocity
        if self.y > 200:
            self.y = 200
            self.y_velocity = 0

class Cactus:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 170
        self.image = pygame.image.load("cactus.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.flip_timer = 0  # add a timer to keep track of when to flip the image
        self.flip_interval = 700  # set the flip interval to 0.5 seconds (500 milliseconds)

    def update(self, score):
        self.x -= 6 + round(score/4)
        Model.DistanceFromCactus = self.x
        Model.CactusVelocity = 6 + round(score/4)

        self.flip_timer += 50  # increment the timer by the time elapsed since the last frame
        if self.flip_timer >= self.flip_interval:  # if the flip interval has elapsed
            self.image = pygame.transform.flip(self.image, True, False)  # flip the image along its x-axis
            self.flip_timer = 0  # reset the timer

class AI_Player:
    def __init__(self):
        self.Game = ChromeDinoGame()
        

    

if __name__ == "__main__":
    game = ChromeDinoGame()
    game.run()


