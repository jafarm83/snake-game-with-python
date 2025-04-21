import pygame
import random
import traceback

# Initialize pygame
pygame.init()

# Game settings
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CHOICES = ["rock", "paper", "scissors"]

# Create game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rock Paper Scissors Ultimate 2D")

# Function to display error messages on screen
def display_error(message):
    screen.fill(WHITE)
    font = pygame.font.Font(None, 24)
    lines = message.splitlines()
    y = 10
    for line in lines:
        text_surface = font.render(line, True, BLACK)
        screen.blit(text_surface, (10, y))
        y += 30
    pygame.display.flip()
    # Wait until the user closes the window
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
    pygame.quit()
    exit()

# Load assets with error display
try:
    background_img = pygame.image.load("background.jpg")
    rock_img = pygame.image.load("rock.jpg")
    paper_img = pygame.image.load("paper.jpg")
    scissors_img = pygame.image.load("scissors.jpg")
except pygame.error as e:
    display_error(f"Error loading image: {e}")

# Scale images
rock_img = pygame.transform.scale(rock_img, (150, 150))
paper_img = pygame.transform.scale(paper_img, (150, 150))
scissors_img = pygame.transform.scale(scissors_img, (150, 150))

# Function to determine the winner
def get_winner(player, computer):
    rules = {"rock": "scissors", "scissors": "paper", "paper": "rock"}
    if player == computer:
        return "It's a Tie!"
    elif rules[player] == computer:
        return "You Win!"
    else:
        return "Computer Wins!"

# Function to display centered text
def display_text(text, font, color, y_offset=0):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + y_offset))
    screen.blit(text_surface, text_rect)

# Game loop variables
running = True
player_choice = None
computer_choice = None
result = "Choose your move!"
player_pos = (100, HEIGHT - 200)        # Position for player's choices
transition = False
clock = pygame.time.Clock()

# Timer event type for resetting the game
RESET_EVENT = pygame.USEREVENT + 1

try:
    while running:
        screen.fill(WHITE)
        screen.blit(background_img, (0, 0))  # Display the background

        # Show player choices if no selection has been made yet
        if not player_choice:
            screen.blit(rock_img, player_pos)
            screen.blit(paper_img, (player_pos[0] + 160, player_pos[1]))
            screen.blit(scissors_img, (player_pos[0] + 320, player_pos[1]))

        # After a choice is made, show the selections on the screen
        if transition:
            # Display player's choice on the left
            if player_choice == "rock":
                screen.blit(rock_img, (100, HEIGHT // 2 - 75))
            elif player_choice == "paper":
                screen.blit(paper_img, (100, HEIGHT // 2 - 75))
            else:
                screen.blit(scissors_img, (100, HEIGHT // 2 - 75))
            
            # Display computer's choice on the right
            if computer_choice == "rock":
                screen.blit(rock_img, (WIDTH - 250, HEIGHT // 2 - 75))
            elif computer_choice == "paper":
                screen.blit(paper_img, (WIDTH - 250, HEIGHT // 2 - 75))
            else:
                screen.blit(scissors_img, (WIDTH - 250, HEIGHT // 2 - 75))

        font = pygame.font.Font(None, 36)
        display_text(result, font, BLACK, -150)
        if computer_choice:
            display_text(f"Computer chose: {computer_choice}", font, BLACK, 100)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Reset timer event to clear the board and start new round
            elif event.type == RESET_EVENT:
                player_choice = None
                computer_choice = None
                result = "Choose your move!"
                transition = False
                pygame.time.set_timer(RESET_EVENT, 0)  # Disable the timer
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                
                # Check for player's choice by checking image rect boundaries
                if 100 <= x <= 250 and HEIGHT - 200 <= y <= HEIGHT - 50:
                    player_choice = "rock"
                    transition = True
                elif 260 <= x <= 410 and HEIGHT - 200 <= y <= HEIGHT - 50:
                    player_choice = "paper"
                    transition = True
                elif 420 <= x <= 570 and HEIGHT - 200 <= y <= HEIGHT - 50:
                    player_choice = "scissors"
                    transition = True
                
                # در صورتی که کاربر انتخاب کرده باشد و کامپیوتر هنوز انتخاب نکرده باشد
                if player_choice and not computer_choice:
                    computer_choice = random.choice(CHOICES)
                    result = get_winner(player_choice, computer_choice)
                    # به جای wait کردن، یک event timer برای ریست بازی در ۱ ثانیه تنظیم می‌کنیم
                    pygame.time.set_timer(RESET_EVENT, 3000)

        pygame.display.flip()
        clock.tick(60)

except Exception as e:
    error_message = traceback.format_exc()
    display_error(f"An error occurred:\n{error_message}")

pygame.quit()
