import pygame
import random

# Game window
pygame.init()
screen = pygame.display.set_mode((570, 630))
pygame.display.set_caption("Pac-Man")
fps = 60
timer = pygame.time.Clock()

# Game components
pacman = pygame.image.load("pacman/paceye.png")
pacman = pygame.transform.scale(pacman, (25, 25))
pacman_x, pacman_y = 300, 300
speed = 1.5
rotation_angle = 0

# Initialize score
score = 0

# Create font for score display
font = pygame.font.SysFont("Arial", 24)

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

        elif item == 'z':  # Red ghost spawn
            ghosts.append(Ghost(pygame.image.load("pacman/ghostr.png"), x, y))

        elif item == 's':  # Blue ghost spawn
            ghosts.append(Ghost(pygame.image.load("pacman/ghostb.png"), x, y))

        elif item == 'o':  # Yellow ghost spawn
            ghosts.append(Ghost(pygame.image.load("pacman/ghosty.png"), x, y))

        elif item == ' ':  # Dot
            dots.append((x, y))


# Function to check collision with walls
def check_wall_collision(x, y, walls):
    rect = pygame.Rect(x - tile_size // 2, y - tile_size // 2, tile_size, tile_size)
    for wall in walls:
        if rect.colliderect(wall):
            return True
    return False

# Game loop
running = True
while running:
    timer.tick(fps)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Keybinds for movements with collision check
    keys = pygame.key.get_pressed()
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

    # Rotate Pac-Man based on direction
    rotated_pacman = pygame.transform.rotate(pacman, rotation_angle)

    # Get the new rectangle after rotation and keep Pac-Man centered
    pacman_rect = rotated_pacman.get_rect(center=(pacman_x, pacman_y))

    # Move ghosts
    for ghost in ghosts:
        ghost.move(walls)

    # Draw everything
    screen.fill((0, 0, 0))
    for wall in walls:
        pygame.draw.rect(screen, (255, 255, 255), wall)

    screen.blit(rotated_pacman, pacman_rect)

    for ghost in ghosts:
        ghost.draw(screen)

    for dot in dots[:]:
        dot_x, dot_y = dot
        if ((pacman_x - dot_x) ** 2 + (pacman_y - dot_y) ** 2) ** 0.5 < 15:
            dots.remove(dot)
            score += 10

    for dot in dots:
        pygame.draw.circle(screen, (255, 255, 0), dot, 5)

    score_text = font.render(f"Score: {score}", True, (255, 0, 0))
    screen.blit(score_text, (10, 2))

    pygame.display.flip()

pygame.quit()
