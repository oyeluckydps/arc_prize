import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants for the game window dimensions
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 700

# Constants for dividing the screen
TOP_MENU_HEIGHT = 50
BOTTOM_STATUS_HEIGHT = 50
MIDDLE_PLAY_HEIGHT = SCREEN_HEIGHT - TOP_MENU_HEIGHT - BOTTOM_STATUS_HEIGHT

# Set up the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game Layout Example")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)

# Initialize page counter and page limits
page_number = 1
FIRST_PAGE = 1
LAST_PAGE = 20

# Initialize fonts
font = pygame.font.Font(None, 36)

# Button definitions
ARROW_BUTTON_WIDTH = 50
ARROW_BUTTON_HEIGHT = 30

double_left_button = pygame.Rect(10, 10, ARROW_BUTTON_WIDTH, ARROW_BUTTON_HEIGHT)
left_button = pygame.Rect(70, 10, ARROW_BUTTON_WIDTH, ARROW_BUTTON_HEIGHT)
right_button = pygame.Rect(200, 10, ARROW_BUTTON_WIDTH, ARROW_BUTTON_HEIGHT)
double_right_button = pygame.Rect(260, 10, ARROW_BUTTON_WIDTH, ARROW_BUTTON_HEIGHT)


def draw_top_menu():
    top_menu_rect = pygame.Rect(0, 0, SCREEN_WIDTH, TOP_MENU_HEIGHT)
    pygame.draw.rect(screen, GRAY, top_menu_rect)

    # Draw double left arrow button
    pygame.draw.rect(screen, BLUE, double_left_button)
    text = font.render('<<', True, WHITE)
    screen.blit(text, (double_left_button.x + 5, double_left_button.y))

    # Draw left arrow button
    pygame.draw.rect(screen, BLUE, left_button)
    text = font.render('<', True, WHITE)
    screen.blit(text, (left_button.x + 10, left_button.y))

    # Draw page counter
    text = font.render(f'{page_number}/{LAST_PAGE}', True, BLACK)
    screen.blit(text, (130, 10))

    # Draw right arrow button
    pygame.draw.rect(screen, BLUE, right_button)
    text = font.render('>', True, WHITE)
    screen.blit(text, (right_button.x + 10, right_button.y))

    # Draw double right arrow button
    pygame.draw.rect(screen, BLUE, double_right_button)
    text = font.render('>>', True, WHITE)
    screen.blit(text, (double_right_button.x + 5, double_right_button.y))


def draw_middle_play():
    middle_play_rect = pygame.Rect(0, TOP_MENU_HEIGHT, SCREEN_WIDTH, MIDDLE_PLAY_HEIGHT)
    pygame.draw.rect(screen, WHITE, middle_play_rect)

    # Display current page number
    text = font.render(f'Page no. {page_number}', True, BLACK)
    screen.blit(text, (10, TOP_MENU_HEIGHT + 10))


def draw_bottom_status():
    bottom_status_rect = pygame.Rect(0, SCREEN_HEIGHT - BOTTOM_STATUS_HEIGHT, SCREEN_WIDTH, BOTTOM_STATUS_HEIGHT)
    pygame.draw.rect(screen, GRAY, bottom_status_rect)
    text = font.render('Status Area', True, BLACK)
    screen.blit(text, (10, SCREEN_HEIGHT - BOTTOM_STATUS_HEIGHT + 10))


def update_page(delta):
    global page_number
    page_number += delta
    if page_number < FIRST_PAGE:
        page_number = FIRST_PAGE
    elif page_number > LAST_PAGE:
        page_number = LAST_PAGE


def go_to_first_page():
    global page_number
    page_number = FIRST_PAGE


def go_to_last_page():
    global page_number
    page_number = LAST_PAGE


# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if left or right buttons are clicked
            if double_left_button.collidepoint(event.pos):
                go_to_first_page()
            elif left_button.collidepoint(event.pos):
                update_page(-1)
            elif right_button.collidepoint(event.pos):
                update_page(1)
            elif double_right_button.collidepoint(event.pos):
                go_to_last_page()

    # Clear the screen
    screen.fill(WHITE)

    # Draw the different areas
    draw_top_menu()
    draw_middle_play()
    draw_bottom_status()

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()