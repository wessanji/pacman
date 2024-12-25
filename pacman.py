import pygame
import random

#game window
pygame.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Pac-Man")

#game components
pacman = pygame.image.load("pacman/paceye.png")
pacman = pygame.transform.scale(pacman, (25,25))
pacman_x, pacman_y = 300, 300
speed = 0.05
rotation_angle = 0



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
        rotation_angle = 90
    if keys[pygame.K_DOWN]: 
        pacman_y += speed
        rotation_angle = -90
    if keys[pygame.K_LEFT]:  
        pacman_x -= speed
        rotation_angle = 180
    if keys[pygame.K_RIGHT]:  
        pacman_x += speed
        rotation_angle = 0

    # Rotate Pac-Man based on direction
    rotated_pacman = pygame.transform.rotate(pacman, rotation_angle)

    # Get the new rectangle after rotation and keep Pac-Man centered
    pacman_rect = rotated_pacman.get_rect(center=(pacman_x, pacman_y))


    #fill screen with black colour
    screen.fill((0, 0, 0))

    #draw rotated pacman at the current position
    screen.blit(rotated_pacman, pacman_rect)
    
    #update screen display
    pygame.display.flip()
pygame.quit()