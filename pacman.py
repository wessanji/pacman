import pygame
import random

#game window
pygame.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Pac-Man")

#game components
pacman = pygame.image.load("pacman/pac.png")
pacman = pygame.transform.scale(pacman, (25,25))
pacman_x, pacman_y = 300, 300
speed = 0.05



#game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #keybounds for movements
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        pacman_y -= speed
    if keys[pygame.K_DOWN]: 
            pacman_y += speed
    if keys[pygame.K_LEFT]:  
        pacman_x -= speed
    if keys[pygame.K_RIGHT]:  
        pacman_x += speed







    #fill screen with black colour
    screen.fill((0, 0, 0))

    #draw pacman at the current position
    screen.blit(pacman, (pacman_x, pacman_y))
    
    #update screen display
    pygame.display.flip()
pygame.quit()