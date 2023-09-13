import pygame
import sys
import random
import time



GAME_RUNNING = True

pygame.init()
screen = pygame.display.set_mode((1024,768))
pygame.display.set_caption('Snake Game')
screen.fill((255,255,255))
pygame.draw.rect(screen, (0,0,0), (0,0,1024,768), 10)
#while GAME_RUNNING:
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        

         #rewrite above if using keypress.get_pressed()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            print('Spacebar pressed')
        if keys[pygame.K_UP]:
            print('Up arrow pressed')
        if keys[pygame.K_DOWN]:
            print('Down arrow pressed')
        if keys[pygame.K_LEFT]:
            print('Left arrow pressed')
        if keys[pygame.K_RIGHT]:
            print('Right arrow pressed')
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()        



if __name__ == '__main__':
    main()

