# pyright: reportMissingImports=false
# type: ignore
import pygame
import sys
import random

# Screen
pygame.init()

# Set window dimensions (windowed mode)
width = 1200
height = 800

# Create windowed display
# Text File
test_font = pygame.font.Font('Images/Pixeltype.ttf', 50)
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
        self.rect = self.image.get_rect(center = ((600, 600)))
    
    def show_rock(self):
        self.image = self.rock_surf
    
    def show_paper(self):
        self.image = self.paper_surf
    
    def show_scissors(self):
        self.image = self.scissors_surf
        
def computer_choice(n): 
    computer_choices = []
    for _ in range(n):
        x = random.randint(1,3)
        computer_choices.append(int(x))
    conversion = {1: 'r', 2: 'p', 3: 's'}
    computer_letters = []
    for choice in computer_choices:
        computer_letters.append(conversion[choice])
    print(f"Computer choices: {computer_letters}")
    return computer_letters


    

# Background Screen
game_background_original = pygame.image.load("Images/Wallpaper.png").convert_alpha()
game_background = pygame.transform.scale(game_background_original, (width, height))
game_text = test_font.render('Choose R, P, S',False,"White")
game_text_rect = game_text.get_rect(center = (int(width/2), 50))
current_choice = ""  # Track the current choice
choice_1 = ""  # First locked choice
choice_2 = ""  # Second locked choice
choosing_stage = 1  # 1 = first choice, 2 = second choice, 3 = both locked, 4 = player selection, 5 = battle result
computer_letters = []  # Store computer choices
player_final = ""  # Player's final choice
computer_final = ""  # Computer's final choice
battle_result = ""  # Win/lose/tie result
intro = False
game_over = False
pause = False

# Create sprite and sprite group
rps_sprite = RPS()
all_sprites = pygame.sprite.Group()
all_sprites.add(rps_sprite)
computer_phase = 0
    
# Helper function to convert letters to names
def letter_to_name(letter):
    if letter == 'R':
        return 'Rock'
    elif letter == 'P':
        return 'Paper'
    elif letter == 'S':
        return 'Scissors'
    return letter

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
            elif intro and event.key == pygame.K_1:
                pause = True
            elif intro and not pause and choosing_stage <= 2 and event.key == pygame.K_p:
                rps_sprite.show_paper()  # Show paper image when P is pressed
                current_choice = "P"
            elif intro and not pause and choosing_stage <= 2 and event.key == pygame.K_r:
                rps_sprite.show_rock()   # Show rock image when R is pressed
                current_choice = "R"
            elif intro and not pause and choosing_stage <= 2 and event.key == pygame.K_s:
                rps_sprite.show_scissors()  # Show scissors image when S is pressed
                current_choice = "S"
            elif intro and not pause and choosing_stage <= 2 and event.key == pygame.K_RETURN and current_choice:
                # Lock in the current choice when Enter is pressed
                if choosing_stage == 1:
                    choice_1 = current_choice
                    choosing_stage = 2
                    current_choice = ""  # Reset for next choice
                    rps_sprite.show_rock()  # Reset to default display
                elif choosing_stage == 2:
                    choice_2 = current_choice
                    choosing_stage = 3  # Both choices locked
                    computer_letters = computer_choice(2)  # Generate computer choices once
                    rps_sprite.show_rock()  # Reset to default display
            elif intro and not pause and choosing_stage == 3 and event.key == pygame.K_RETURN:
                # Move to player selection phase
                choosing_stage = 4
            elif intro and not pause and choosing_stage == 4 and event.key in [pygame.K_3, pygame.K_4]:
                # Player selects final choice
                if event.key == pygame.K_3:
                    player_final = choice_1
                else:
                    player_final = choice_2
                
                # Computer randomly selects from its choices
                import random
                computer_final = random.choice(computer_letters).upper()  # Convert to uppercase
                
                # Determine battle result
                if player_final == computer_final:
                    battle_result = "TIE!"
                elif ((player_final == 'R' and computer_final == 'S') or 
                      (player_final == 'P' and computer_final == 'R') or 
                      (player_final == 'S' and computer_final == 'P')):
                    battle_result = "YOU WIN!"
                else:
                    battle_result = "YOU LOSE!"
                
                choosing_stage = 5  # Battle complete
            elif intro and not pause and choosing_stage == 5 and event.key == pygame.K_SPACE:
                # Restart the game after battle result
                choice_1 = ""
                choice_2 = ""
                choosing_stage = 1
                current_choice = ""
                computer_letters = []
            elif pause and event.key == pygame.K_SPACE:
                pause = False
            elif game_over and not pause and event.key == pygame.K_SPACE:
                # Reset game
                intro = False
                game_over = False
                choice_1 = ""
                choice_2 = ""
                choosing_stage = 1
                current_choice = ""
                computer_letters = []

    if intro and not pause and not game_over:     
        screen.blit(game_background, (0, 0))
        
        # Display text based on choosing stage
        if choosing_stage == 1:
            if current_choice:
                choice_text = test_font.render(f'Choice 1: {letter_to_name(current_choice)} - Press Enter to lock',False,"White")
                choice_text_rect = choice_text.get_rect(center = (int(width/2), 50))
                screen.blit(choice_text, choice_text_rect)
            else:
                instruction_text = test_font.render('Choice 1: Choose R, P, S',False,"White")
                instruction_text_rect = instruction_text.get_rect(center = (int(width/2), 50))
                screen.blit(instruction_text, instruction_text_rect)
        elif choosing_stage == 2:
            # Show locked choice 1 and current choice 2
            locked_text = test_font.render(f'Choice 1: {letter_to_name(choice_1)} (LOCKED)',False,"Green")
            locked_text_rect = locked_text.get_rect(center = (int(width/2), 30))
            screen.blit(locked_text, locked_text_rect)
            
            if current_choice:
                choice_text = test_font.render(f'Choice 2: {letter_to_name(current_choice)} - Press Enter to lock',False,"White")
                choice_text_rect = choice_text.get_rect(center = (int(width/2), 70))
                screen.blit(choice_text, choice_text_rect)
            else:
                instruction_text = test_font.render('Choice 2: Choose R, P, S',False,"White")
                instruction_text_rect = instruction_text.get_rect(center = (int(width/2), 70))
                screen.blit(instruction_text, instruction_text_rect)
        elif choosing_stage == 3:
            # Show both locked choices
            choice1_text = test_font.render(f'Choice 1: {letter_to_name(choice_1)} (LOCKED)',False,"Green")
            choice1_text_rect = choice1_text.get_rect(center = (int(width/2), 30))
            screen.blit(choice1_text, choice1_text_rect)
            
            choice2_text = test_font.render(f'Choice 2: {letter_to_name(choice_2)} (LOCKED)',False,"Green")
            choice2_text_rect = choice2_text.get_rect(center = (int(width/2), 70))
            screen.blit(choice2_text, choice2_text_rect)
            
            # Display computer choices (only once, since they're stored)
            complete_text = test_font.render(f'Computer chose {computer_letters}',False,"Yellow")
            complete_text_rect = complete_text.get_rect(center = (int(width/2), 110))
            screen.blit(complete_text, complete_text_rect)
            
            # Instructions to proceed
            proceed_text = test_font.render('Press Enter to select your final choice',False,"White")
            proceed_text_rect = proceed_text.get_rect(center = (int(width/2), 150))
            screen.blit(proceed_text, proceed_text_rect)
            
        elif choosing_stage == 4:
            # Player selection phase
            choice1_text = test_font.render(f'3: {letter_to_name(choice_1)}',False,"White")
            choice1_text_rect = choice1_text.get_rect(center = (int(width/2), 50))
            screen.blit(choice1_text, choice1_text_rect)
            
            choice2_text = test_font.render(f'4: {letter_to_name(choice_2)}',False,"White")
            choice2_text_rect = choice2_text.get_rect(center = (int(width/2), 90))
            screen.blit(choice2_text, choice2_text_rect)
            
            select_text = test_font.render('Select your final choice (Press 3 or 4)',False,"Yellow")
            select_text_rect = select_text.get_rect(center = (int(width/2), 130))
            screen.blit(select_text, select_text_rect)
            
        elif choosing_stage == 5:
            # Battle result phase
            player_text = test_font.render(f'You chose: {letter_to_name(player_final)}',False,"Green")
            player_text_rect = player_text.get_rect(center = (int(width/2), 50))
            screen.blit(player_text, player_text_rect)
            
            computer_text = test_font.render(f'Computer chose: {letter_to_name(computer_final)}',False,"Red")
            computer_text_rect = computer_text.get_rect(center = (int(width/2), 90))
            screen.blit(computer_text, computer_text_rect)
            
            result_text = test_font.render(battle_result,False,"Yellow")
            result_text_rect = result_text.get_rect(center = (int(width/2), 130))
            screen.blit(result_text, result_text_rect)
            
            restart_text = test_font.render('Press Space to play again',False,"White")
            restart_text_rect = restart_text.get_rect(center = (int(width/2), 170))
            screen.blit(restart_text, restart_text_rect)
            
        all_sprites.draw(screen)
        
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