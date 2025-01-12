import pygame
import random

# Game window
pygame.init()
screen = pygame.display.set_mode((570, 630))
pygame.display.set_caption("Pac-Man")
fps = 60
timer = pygame.time.Clock()

# Game components
pacman = pygame.image.load("paceye.png")
pacman = pygame.transform.scale(pacman, (25, 25))
speed = 1.5

# Initialize score
score = 0

# Create font for score display
font = pygame.font.SysFont("Arial", 24)

# Power-Up class 
class PowerUp: 
    def __init__(self, image, x, y, effect):
        self.image = pygame.transform.scale(image, (25, 25))
        self.x = x 
        self.y = y
        self.effect = effect


# Ghost class
    class Ghost:
      def __init__(self, image, start_x, start_y):
        self.image = pygame.transform.scale(image, (25, 25))
        self.x = start_x
        self.y = start_y
        self.speed = 1.5
        self.direction = random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])

    def move(self, walls):
        if self.direction == 'UP' and not check_wall_collision(self.x, self.y - self.speed, walls):
            self.y -= self.speed
        elif self.direction == 'DOWN' and not check_wall_collision(self.x, self.y + self.speed, walls):
            self.y += self.speed
        elif self.direction == 'LEFT' and not check_wall_collision(self.x - self.speed, self.y, walls):
            self.x -= self.speed
        elif self.direction == 'RIGHT' and not check_wall_collision(self.x + self.speed, self.y, walls):
            self.x += self.speed
        else:
            self.direction = random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])

        # Randomly change direction
        if random.random() < 0.02:
            self.direction = random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])

        # Teleport to the other side of the screen
        if self.x < 0:
            self.x = 570
        elif self.x > 570:
            self.x = 0
        if self.y < 0:
            self.y = 630
        elif self.y > 630:
            self.y = 0

    def draw(self, screen):
        screen.blit(self.image, (self.x - tile_size // 2, self.y - tile_size // 2))


# Initialization of walls
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
    ['1',' ',' ',' ',' ','1',' ','1','s','z','o','1',' ','1',' ',' ',' ',' ','1'],
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
ghosts = []
pacman_x = pacman_y = 0

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

        elif item == 'r':  # Red ghost spawn
            ghosts.append(Ghost(pygame.image.load("ghostr.png"), x, y))

        elif item == 'z':  # Blue ghost spawn
            ghosts.append(Ghost(pygame.image.load("ghostb.png"), x, y))

        elif item == '-':  # Yellow ghost spawn
            ghosts.append(Ghost(pygame.image.load("ghosty.png"), x, y))

        elif item == ' ':  # Dot
            dots.append((x, y))


# Function to check collision with walls
def check_wall_collision(x, y, walls):
    rect = pygame.Rect(x - tile_size // 2, y - tile_size // 2, tile_size, tile_size)
    for wall in walls:
        if rect.colliderect(wall):
            return True
    return False

# Function to check collision with ghosts
def check_ghost_collision(pacman_rect, ghosts):
    for ghost in ghosts:
        ghost_rect = pygame.Rect(ghost.x - tile_size // 2, ghost.y - tile_size // 2, tile_size, tile_size)
        if pacman_rect.colliderect(ghost_rect):
            return True
    return False

# Function to handle Pac-Man movement
def handle_pacman_movement(pacman_x, pacman_y, speed, walls):
    keys = pygame.key.get_pressed()
    rotation_angle = 0

    if keys[pygame.K_UP]:
        if not check_wall_collision(pacman_x, pacman_y - speed, walls):
            pacman_y -= speed
            rotation_angle = 90
    if keys[pygame.K_DOWN]:
        if not check_wall_collision(pacman_x, pacman_y + speed, walls):
            pacman_y += speed
            rotation_angle = -90
    if keys[pygame.K_LEFT]:
        if not check_wall_collision(pacman_x - speed, pacman_y, walls):
            pacman_x -= speed
            rotation_angle = 180
    if keys[pygame.K_RIGHT]:
        if not check_wall_collision(pacman_x + speed, pacman_y, walls):
            pacman_x += speed
            rotation_angle = 0

    return pacman_x, pacman_y, rotation_angle


# Recursive function to draw walls
def draw_walls_recursive(screen, walls, index=0):
    if index >= len(walls):  # Base case: No more walls to draw
        return

    pygame.draw.rect(screen, (128, 128, 128), walls[index])  # Draw current wall
    draw_walls_recursive(screen, walls, index + 1)  # Recurse for the next wall

# Recursive function to draw dots
def draw_dots_recursive(screen, dots, index=0):
    if index >= len(dots):  # Base case: No more dots to draw
        return

    dot_x, dot_y = dots[index]
    pygame.draw.circle(screen, (255, 255, 0), (dot_x, dot_y), 5)  # Draw the dot
    draw_dots_recursive(screen, dots, index + 1)  # Recurse to the next dot


# Function to handle dots
def handle_dots(screen, pacman_x, pacman_y, dots, score):
    for dot in dots[:]:
        dot_x, dot_y = dot
        if ((pacman_x - dot_x) ** 2 + (pacman_y - dot_y) ** 2) ** 0.5 < 15:
            dots.remove(dot)
            score += 10

    # Use the recursive function to draw the remaining dots
    draw_dots_recursive(screen, dots)


    return dots, score

# Function to check win condition
def check_win_condition(dots):
    return len(dots) == 0

# Function to draw text (score, game over, etc.)
def draw_text(screen, text, font, color, position):
    rendered_text = font.render(text, True, color)
    screen.blit(rendered_text, position)

# Function to respawn ghosts
def respawn_ghosts():
    global ghost_respawn_timers 
    current_time = pygame.time.get_ticks()
    for ghost_timer in ghost_respawn_timers[:]:
        if current_time - ghost_timer[1] > 5000: # 5 seconds
            ghost_respawn_timers.remove(ghost_timer)
            # Respawn at the nest
            ghost = Ghost(pygame.image.load("ghostr.png")('ghostb.png')('ghosty.png'), ghost_respawn_positions[0], ghost_respawn_positions[1])
            ghosts.append(ghost)

# ghosts respawn position
ghost_respawn_positions = [ 
    (570 // 2 - 30 * 2, 630 // 2), 
    (570 // 2 + 30 * 2, 630 // 2) 
    ]

# ghosts initialisation
ghosts = [pygame.Rect(pos[0], pos[1], 30, 30) for pos in ghost_respawn_positions]
ghost_respawn_timers = []

 # Game loop
running = True
game_over = False
you_win = False  # Added win condition
power_up_active = False # Power-up state
power_up_timer = 0 # Power-up timer

# Initialize power-up
power_up_image = pygame.image.load("powerup.png") 
power_up = PowerUp(power_up_image, 285, 315, "effect")

while running:
    timer.tick(fps)

    if game_over:
        draw_text(screen, "Game Over", font, (255, 0, 0), (200, 300))
        pygame.display.flip()
        pygame.time.wait(3000)  # Wait for 3 seconds
        running = False
        continue

    if you_win:
        draw_text(screen, "You Win!", font, (0, 255, 0), (200, 300))
        pygame.display.flip()
        pygame.time.wait(3000)  # Wait for 3 seconds
        running = False
        continue

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle Pac-Man movement
    pacman_x, pacman_y, rotation_angle = handle_pacman_movement(pacman_x, pacman_y, speed, walls)

    # Rotate Pac-Man based on direction
    rotated_pacman = pygame.transform.rotate(pacman, rotation_angle)
    pacman_rect = rotated_pacman.get_rect(center=(pacman_x, pacman_y))

    # Check for collision with ghosts
    for ghosts in ghost[:]:
        if pacman_rect.colliderect(ghost):
            if power_up_active: # Eat the ghost
                ghosts.remove(ghost)
                ghost_respawn_timers.append((ghost, pygame.time.get_ticks())) # Schedule respawn
                score+= 50
            else: # Pac-Man is caught 
                if check_ghost_collision(pacman_rect, ghosts):
                    game_over = True

    # Move ghosts
    for ghost in ghosts:
        ghost.move(walls)

    # Draw everything
    screen.fill((0, 0, 0))
    draw_walls_recursive(screen, walls)
    screen.blit(rotated_pacman, pacman_rect)

    for ghost in ghosts:
        ghost.draw(screen)

    # Handle dots
    dots, score = handle_dots(screen, pacman_x, pacman_y, dots, score)

    # Check if player wins
    if check_win_condition(dots):
        you_win = True

    draw_text(screen, f"SCORE: {score}", font, (255, 165, 0), (10, 2))
    
    # Respawn ghosts
    respawn_ghosts()

    # Check for collision with power-up
    if pacman_rect.colliderect(power_up):
         power_up_active = True
         power_up_timer = pygame.time.get_ticks() # Activate the timer
         power_up.x, power_up.y = -100, -100 # Remove the power-up from the screen

    # Check power-up ending
    if power_up_active and pygame.time.get_ticks() - power_up_timer > 5000: # Duration of 5 seconds
        power_up_active = False

    # Draw power-up
    if not power_up_active: 
        power_up.draw(screen)
    
    pygame.display.flip()

pygame.quit()
