import pygame
import random

#game window
pygame.init()
screen = pygame.display.set_mode((570, 630))
pygame.display.set_caption("Pac-Man")
fps = 60
timer = pygame.time.Clock()

#game components
pacman = pygame.image.load("pacman/paceye.png")
pacman = pygame.transform.scale(pacman, (25,25))
pacman_x, pacman_y = 300, 300
speed = 1.5
rotation_angle = 0

# Initialize score
score = 0

# Create font for score display
font = pygame.font.SysFont("Arial", 24)

#ghosts
red_ghost = pygame.image.load("pacman/ghostr.png")
blue_ghost = pygame.image.load("pacman/ghostb.png")
yellow_ghost = pygame.image.load("pacman/ghosty.png")

red_ghost = pygame.transform.scale(red_ghost, (25, 25))
blue_ghost = pygame.transform.scale(blue_ghost, (25, 25))
yellow_ghost = pygame.transform.scale(yellow_ghost, (25, 25))



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
    [' ',' ',' ',' ',' ','1',' ','1','s','z','o','1',' ','1',' ',' ',' ',' ',' '],
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


# Game setup
walls = []
dots = []
pacman_x = pacman_y = red_ghost_x = red_ghost_y = blue_ghost_x = blue_ghost_y = yellow_ghost_x = yellow_ghost_y = 0

tile_size = 30

# Iterate through maze
for row_index, row in enumerate(maze):
    for col_index, item in enumerate(row):
        x = col_index * tile_size + tile_size // 2
        y = row_index * tile_size + tile_size // 2

        if item == '1':  # Wall
            walls.append(pygame.Rect(col_index * tile_size, row_index * tile_size, tile_size, tile_size))

        elif item == 'P':  # Pac-Man spawn
            pacman_x, pacman_y = x, y

        elif item == 'z':  # Red ghost spawn
            red_ghost_x, red_ghost_y = x, y

        elif item == 's':  # Blue ghost spawn
            blue_ghost_x, blue_ghost_y = x, y

        elif item == 'o':  # Yellow ghost spawn
            yellow_ghost_x, yellow_ghost_y = x, y

        elif item == ' ':  # Dot
            dots.append((x, y))


def check_dot_collision(pacman_x, pacman_y, dot_x, dot_y, tolerance=15):
    distance = ((pacman_x - dot_x) ** 2 + (pacman_y - dot_y) ** 2) ** 0.5
    return distance < tolerance    
      
# Function to check collision with walls
def check_wall_collision(x, y):
    pacman_rect = pygame.Rect(x - tile_size // 2, y - tile_size // 2, tile_size, tile_size)
    for wall in walls:
        if pacman_rect.colliderect(wall):
            return True 
    return False




#game loop
running = True
while running:
    timer.tick(fps)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Keybinds for movements with collision check
    keys = pygame.key.get_pressed()
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

    #draw dots
    for dot in dots[:]:
        dot_x, dot_y = dot
        if check_dot_collision(pacman_x, pacman_y, dot_x, dot_y):
            dots.remove(dot)
            score += 10  

    #fill screen with black colour
    screen.fill((0, 0, 0))

    #draw walls 
    for wall in walls:
        pygame.draw.rect(screen, (255, 255, 255), wall)

    #draw rotated pacman at the current position
    screen.blit(rotated_pacman, pacman_rect)

    # Draw ghosts on the screen
    screen.blit(red_ghost, (red_ghost_x - tile_size // 2, red_ghost_y - tile_size // 2))
    screen.blit(blue_ghost, (blue_ghost_x - tile_size // 2, blue_ghost_y - tile_size // 2))
    screen.blit(yellow_ghost, (yellow_ghost_x - tile_size // 2, yellow_ghost_y - tile_size // 2))

     # Draw the remaining dots
    for dot in dots:
        pygame.draw.circle(screen, (255, 255, 0), dot, 5)
    
    score_text = font.render(f"Score: {score}", True, (255, 0, 0))
    screen.blit(score_text, (10, 2))

    #update screen display
    pygame.display.flip()
pygame.quit()