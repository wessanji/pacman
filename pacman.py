import pygame
import random

#game window
pygame.init()
screen = pygame.display.set_mode((570, 630))
pygame.display.set_caption("Pac-Man")

#game components
pacman = pygame.image.load("pacman/paceye.png")
pacman = pygame.transform.scale(pacman, (25,25))
pacman_x, pacman_y = 300, 300
speed = 0.4
rotation_angle = 0

#Initialisation of walls
maze = [
    ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
    ['1',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','1'],
    ['1','B','1','1',' ','1','1','1',' ','1',' ','1','1','1',' ','1','1','B','1'],
    ['1',' ',' ',' ',' ','1',' ',' ',' ','1',' ',' ',' ','1',' ',' ',' ',' ','1'],
    ['1','1',' ','1',' ','1',' ','1',' ','1',' ','1',' ','1',' ','1',' ','1','1'],
    ['1',' ',' ','1',' ',' ',' ','1',' ',' ',' ','1',' ',' ',' ','1',' ',' ','1'],
    ['1',' ','1','1','1','1',' ','1','1','1','1','1',' ','1','1','1','1',' ','1'],
    ['1',' ',' ',' ',' ',' ',' ',' ',' ','r',' ',' ',' ',' ',' ',' ',' ',' ','1'],
    ['1','1',' ','1','1','1',' ','1','1','-','1','1',' ','1','1','1',' ','1','1'],
    [' ',' ',' ',' ',' ','1',' ','1','s','p','o','1',' ','1',' ',' ',' ',' ',' '],
    ['1','1',' ','1',' ','1',' ','1','1','1','1','1',' ','1',' ','1',' ','1','1'],
    ['1',' ',' ','1',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','1',' ',' ','1'],
    ['1',' ','1','1','1','1',' ','1','1','1','1','1',' ','1','1','1','1',' ','1'],
    ['1',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','1'],
    ['1','1','1',' ','1','1','1',' ','1','1','1',' ','1','1','1',' ','1','1','1'],
    ['1',' ',' ',' ','1',' ',' ',' ',' ','P',' ',' ',' ',' ','1',' ',' ',' ','1'],
    ['1','B','1',' ','1',' ','1',' ','1','1','1',' ','1',' ','1',' ','1','B','1'],
    ['1',' ','1',' ',' ',' ','1',' ',' ',' ',' ',' ','1',' ',' ',' ','1',' ','1'],
    ['1',' ','1','1','1',' ','1','1','1',' ','1','1','1',' ','1','1','1',' ','1'],
    ['1',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','1'],
    ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1']
]
    

walls = []
tile_size = 30
for row_index, row in enumerate(maze):
    for col_index, item in enumerate(row):
        if item == '1':
            walls.append(pygame.Rect(col_index * tile_size, row_index * tile_size, tile_size, tile_size))


for row_index, row in enumerate(maze):
    for col_index, item in enumerate(row):
        if item == 'P':
            pacman_x = col_index * tile_size + tile_size // 2  # Center within the tile
            pacman_y = row_index * tile_size + tile_size // 2
            break

# Function to check collision with walls
def check_wall_collision(x, y):
    pacman_rect = pygame.Rect(x - tile_size // 2, y - tile_size // 2, tile_size, tile_size)
    for wall in walls:
        if pacman_rect.colliderect(wall):
            return True  # Collision detected
    return False

#game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #keybinds for movements
    keys = pygame.key.get_pressed()
       # Keybinds for movements with collision check
    if keys[pygame.K_UP]:
        if not check_wall_collision(pacman_x, pacman_y - speed):
            pacman_y -= speed
            rotation_angle = 90
    if keys[pygame.K_DOWN]:
        if not check_wall_collision(pacman_x, pacman_y + speed):
            pacman_y += speed
            rotation_angle = -90
    if keys[pygame.K_LEFT]:
        if not check_wall_collision(pacman_x - speed, pacman_y):
            pacman_x -= speed
            rotation_angle = 180
    if keys[pygame.K_RIGHT]:
        if not check_wall_collision(pacman_x + speed, pacman_y):
            pacman_x += speed
            rotation_angle = 0




    # Rotate Pac-Man based on direction
    rotated_pacman = pygame.transform.rotate(pacman, rotation_angle)

    # Get the new rectangle after rotation and keep Pac-Man centered
    pacman_rect = rotated_pacman.get_rect(center=(pacman_x, pacman_y))


    #fill screen with black colour
    screen.fill((0, 0, 0))

    #draw walls 
    for wall in walls:
        pygame.draw.rect(screen, (255, 255, 255), wall)

    #draw rotated pacman at the current position
    screen.blit(rotated_pacman, pacman_rect)
    
    #update screen display
    pygame.display.flip()
pygame.quit()