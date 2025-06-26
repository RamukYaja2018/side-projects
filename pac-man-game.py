import pygame
import sys

pygame.init()

# Constants
WIDTH, HEIGHT = 600, 700
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
PINK = (255, 192, 203)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
DARK_BLUE = (0, 0, 139)
GRAY = (128, 128, 128)

# Game setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Retro Pac-Man")
clock = pygame.time.Clock()

# Maze layout (1 = wall, 0 = dot, 2 = empty)
maze = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,0,1,1,1,0,1,1,0,1,1,1,0,1,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,0,1,0,1,1,1,1,1,1,0,1,0,1,1,0,1],
    [1,0,0,0,0,1,0,0,0,1,1,0,0,0,1,0,0,0,0,1],
    [1,1,1,1,0,1,1,1,2,1,1,2,1,1,1,0,1,1,1,1],
    [1,1,1,1,0,1,2,2,2,2,2,2,2,2,1,0,1,1,1,1],
    [1,1,1,1,0,1,2,1,1,2,2,1,1,2,1,0,1,1,1,1],
    [2,2,2,2,0,2,2,1,2,2,2,2,1,2,2,0,2,2,2,2],
    [1,1,1,1,0,1,2,1,1,1,1,1,1,2,1,0,1,1,1,1],
    [1,1,1,1,0,1,2,2,2,2,2,2,2,2,1,0,1,1,1,1],
    [1,1,1,1,0,1,1,1,2,1,1,2,1,1,1,0,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,0,1,1,1,0,1,1,0,1,1,1,0,1,1,0,1],
    [1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1],
    [1,1,0,1,0,1,0,1,1,1,1,1,1,0,1,0,1,0,1,1],
    [1,0,0,0,0,1,0,0,0,1,1,0,0,0,1,0,0,0,0,1],
    [1,0,1,1,1,1,1,1,0,1,1,0,1,1,1,1,1,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]

class PacMan:
    def __init__(self):
        self.x = 9
        self.y = 15
        self.direction = 0  # 0=right, 1=down, 2=left, 3=up
        self.mouth_open = True
        
    def move(self):
        dx, dy = [(1,0), (0,1), (-1,0), (0,-1)][self.direction]
        new_x, new_y = self.x + dx, self.y + dy
        
        # Wrap around screen
        if new_x < 0: new_x = 19
        elif new_x > 19: new_x = 0
        
        # Check wall collision
        if 0 <= new_y < 21 and maze[new_y][new_x] != 1:
            self.x, self.y = new_x, new_y
            self.mouth_open = not self.mouth_open
            
    def draw(self):
        import math
        center = (self.x * 30 + 15, self.y * 30 + 15)
        
        if self.mouth_open:
            # Draw Pac-Man with mouth
            start_angle = [0, 90, 180, 270][self.direction]
            end_angle = start_angle + 300
            
            # Draw the arc (Pac-Man shape)
            points = [center]
            for angle in range(int(start_angle + 30), int(end_angle), 5):
                x = center[0] + 12 * math.cos(math.radians(angle))
                y = center[1] + 12 * math.sin(math.radians(angle))
                points.append((x, y))
            pygame.draw.polygon(screen, YELLOW, points)
        else:
            pygame.draw.circle(screen, YELLOW, center, 12)
        
        # Draw eye
        eye_x = center[0] + [-3, 0, 3, 0][self.direction]
        eye_y = center[1] + [0, -3, 0, 3][self.direction] - 3
        pygame.draw.circle(screen, BLACK, (int(eye_x), int(eye_y)), 2)

class Ghost:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.direction = 0
        
    def move(self):
        import random
        if random.randint(0, 10) == 0:
            self.direction = random.randint(0, 3)
            
        dx, dy = [(1,0), (0,1), (-1,0), (0,-1)][self.direction]
        new_x, new_y = self.x + dx, self.y + dy
        
        if new_x < 0: new_x = 19
        elif new_x > 19: new_x = 0
        
        if 0 <= new_y < 21 and maze[new_y][new_x] != 1:
            self.x, self.y = new_x, new_y
        else:
            self.direction = random.randint(0, 3)
            
    def draw(self):
        center = (self.x * 30 + 15, self.y * 30 + 15)
        
        # Draw ghost body (rounded rectangle)
        body_rect = pygame.Rect(center[0] - 12, center[1] - 12, 24, 20)
        pygame.draw.rect(screen, self.color, body_rect)
        pygame.draw.circle(screen, self.color, (center[0], center[1] - 2), 12)
        
        # Draw ghost bottom (wavy)
        points = [
            (center[0] - 12, center[1] + 8),
            (center[0] - 8, center[1] + 12),
            (center[0] - 4, center[1] + 8),
            (center[0], center[1] + 12),
            (center[0] + 4, center[1] + 8),
            (center[0] + 8, center[1] + 12),
            (center[0] + 12, center[1] + 8),
            (center[0] + 12, center[1] - 12)
        ]
        pygame.draw.polygon(screen, self.color, points)
        
        # Draw eyes
        pygame.draw.circle(screen, WHITE, (center[0] - 4, center[1] - 4), 3)
        pygame.draw.circle(screen, WHITE, (center[0] + 4, center[1] - 4), 3)
        pygame.draw.circle(screen, BLACK, (center[0] - 3, center[1] - 4), 1)
        pygame.draw.circle(screen, BLACK, (center[0] + 5, center[1] - 4), 1)

# Game objects
pacman = PacMan()
ghosts = [Ghost(9, 9, RED), Ghost(10, 9, PINK), Ghost(9, 10, CYAN), Ghost(10, 10, ORANGE)]
score = 0
font = pygame.font.Font(None, 36)
paused = False
game_over = False

def draw_maze():
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            rect = pygame.Rect(x * 30, y * 30, 30, 30)
            if cell == 1:  # Wall
                pygame.draw.rect(screen, DARK_BLUE, rect)
                pygame.draw.rect(screen, BLUE, rect, 2)
            elif cell == 0:  # Dot
                pygame.draw.circle(screen, YELLOW, rect.center, 4)
                pygame.draw.circle(screen, WHITE, rect.center, 2)

def collect_dot():
    global score
    if maze[pacman.y][pacman.x] == 0:
        maze[pacman.y][pacman.x] = 2
        score += 10

def check_win():
    return not any(0 in row for row in maze)

def draw_pause_menu():
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(128)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))
    
    pause_text = font.render("PAUSED", True, WHITE)
    resume_text = font.render("Press ESC to Resume", True, WHITE)
    quit_text = font.render("Press Q to Quit", True, WHITE)
    
    screen.blit(pause_text, (WIDTH//2 - 60, HEIGHT//2 - 60))
    screen.blit(resume_text, (WIDTH//2 - 120, HEIGHT//2 - 20))
    screen.blit(quit_text, (WIDTH//2 - 80, HEIGHT//2 + 20))

def check_collision():
    global game_over
    for ghost in ghosts:
        if pacman.x == ghost.x and pacman.y == ghost.y:
            game_over = True

def draw_game_over():
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(128)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))
    
    game_over_text = font.render("GAME OVER", True, WHITE)
    restart_text = font.render("Press R to Restart", True, WHITE)
    quit_text = font.render("Press Q to Quit", True, WHITE)
    
    screen.blit(game_over_text, (WIDTH//2 - 80, HEIGHT//2 - 60))
    screen.blit(restart_text, (WIDTH//2 - 110, HEIGHT//2 - 20))
    screen.blit(quit_text, (WIDTH//2 - 80, HEIGHT//2 + 20))

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                paused = not paused
            elif event.key == pygame.K_q and (paused or game_over):
                running = False
            elif event.key == pygame.K_r and game_over:
                pacman = PacMan()
                ghosts = [Ghost(9, 9, RED), Ghost(10, 9, PINK), Ghost(9, 10, CYAN), Ghost(10, 10, ORANGE)]
                score = 0
                game_over = False
            elif not paused and not game_over:
                if event.key == pygame.K_RIGHT:
                    pacman.direction = 0
                elif event.key == pygame.K_DOWN:
                    pacman.direction = 1
                elif event.key == pygame.K_LEFT:
                    pacman.direction = 2
                elif event.key == pygame.K_UP:
                    pacman.direction = 3
    
    if not paused and not game_over:
        pacman.move()
        for ghost in ghosts:
            ghost.move()
        collect_dot()
        check_collision()
    
    screen.fill(BLACK)
    draw_maze()
    pacman.draw()
    for ghost in ghosts:
        ghost.draw()
    
    # Display score with background
    score_bg = pygame.Rect(5, HEIGHT - 45, 150, 35)
    pygame.draw.rect(screen, DARK_BLUE, score_bg)
    pygame.draw.rect(screen, BLUE, score_bg, 2)
    score_text = font.render(f"Score: {score}", True, YELLOW)
    screen.blit(score_text, (10, HEIGHT - 40))
    
    # Check win condition
    if check_win() and not game_over:
        win_text = font.render("YOU WIN!", True, WHITE)
        screen.blit(win_text, (WIDTH//2 - 70, HEIGHT//2))
    
    # Draw menus
    if paused:
        draw_pause_menu()
    elif game_over:
        draw_game_over()
    
    pygame.display.flip()
    clock.tick(6)

pygame.quit()
sys.exit()
