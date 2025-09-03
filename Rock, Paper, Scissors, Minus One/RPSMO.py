# pyright: reportMissingImports=false
# type: ignore
import pygame
import sys

# Screen
pygame.init()

# Set window dimensions (windowed mode)
width = 1200
height = 800

# Create windowed display
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Rock Paper Scissors Minus One")
clock = pygame.time.Clock()
running = True

# Class RPS
class RPS(pygame.sprite.Sprite): 
    def __init__(self):
        super().__init__()
        self.rock_surf = pygame.image.load("Images/Rock.jpg").convert_alpha()
        self.paper_surf = pygame.image.load("Images/Paper.jpg").convert_alpha()
        self.scissors_surf = pygame.image.load("Images/Scissors.jpg").convert_alpha()
        
        # Start with rock as default
        self.image = self.rock_surf
        self.rect = self.image.get_rect()
    
    def show_rock(self):
        self.image = self.rock_surf
    
    def show_paper(self):
        self.image = self.paper_surf
    
    def show_scissors(self):
        self.image = self.scissors_surf

# Background Screen
game_background_original = pygame.image.load("Images/Wallpaper.png").convert_alpha()
game_background = pygame.transform.scale(game_background_original, (width, height))
intro = False
game_over = False
pause = False

# Text File
test_font = pygame.font.Font('Images/Pixeltype.ttf', 50)

# Create sprite and sprite group
rps_sprite = RPS()
all_sprites = pygame.sprite.Group()
all_sprites.add(rps_sprite)
    
# Game running
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if not intro and not pause and not game_over and event.key == pygame.K_SPACE:
                intro = True
            elif intro and not pause and event.key == pygame.K_q:
                game_over = True
            elif intro and event.key == pygame.K_p:
                pause = True
            elif pause and event.key == pygame.K_SPACE:
                pause = False
            elif game_over and not pause and event.key == pygame.K_SPACE:
                # Reset game
                intro = False
                game_over = False

    if intro and not pause and not game_over:     
        # Show game background and sprites
        screen.blit(game_background, (0, 0))
        
    elif game_over:
        # Show game over screen
        screen.fill((0, 0, 0))
        text_game_over = test_font.render('GAME OVER',False,"Red")
        text_restart = test_font.render('Press space to restart',False,"White")
        text_game_over_rect = text_game_over.get_rect(center = (int(width/2), int(height/2) - 50))
        text_restart_rect = text_restart.get_rect(center = (int(width/2), int(height/2) + 50))
        screen.blit(text_game_over, text_game_over_rect)
        screen.blit(text_restart, text_restart_rect)
        
    elif pause: 
        screen.fill((0, 0, 0))
        text_pause = test_font.render('Paused',False,"Green")
        text_continue = test_font.render('Press space to continue',False,"White")
        text_pause_rect = text_pause.get_rect(center = (int(width/2), int(height/2) - 50))
        text_continue_rect = text_continue.get_rect(center = (int(width/2), int(height/2) + 50))
        screen.blit(text_pause, text_pause_rect)
        screen.blit(text_continue, text_continue_rect)
    else:
        # Show intro screen (black screen for now)
        screen.fill((0, 0, 0))
        text_space = test_font.render('Press space to start',False,"White")
        text_rect = text_space.get_rect(center = (int(width/2), int(height/2)))
        screen.blit(text_space, text_rect)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()