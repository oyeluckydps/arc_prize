import pygame
import sys
import random
import math

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
LIGHT_GRAY = (240, 240, 240)

# Color palette (9 distinguishable colors + BLACK)
COLOR_PALETTE = [
    (255, 0, 0), (0, 255, 0), (0, 0, 255),  # Red, Green, Blue
    (255, 255, 0), (255, 0, 255), (0, 255, 255),  # Yellow, Magenta, Cyan
    (128, 0, 128), (255, 165, 0), (0, 128, 128),  # Purple, Orange, Teal
    BLACK  # Black
]

# Initialize page counter and page limits
page_number = 1
FIRST_PAGE = 1
LAST_PAGE = 20

# Initialize TRAINING_BLOCKS_COUNT with random numbers between 1 and 10 for each page
TRAINING_BLOCKS_COUNT = [random.randint(1, 10) for _ in range(LAST_PAGE)]

# Initialize fonts
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 30)  # Font for page number
very_small_font = pygame.font.Font(None, 18)  # Font for indices and block dimensions

# Button definitions
ARROW_BUTTON_WIDTH = 50
ARROW_BUTTON_HEIGHT = 30

double_left_button = pygame.Rect(10, 10, ARROW_BUTTON_WIDTH, ARROW_BUTTON_HEIGHT)
left_button = pygame.Rect(70, 10, ARROW_BUTTON_WIDTH, ARROW_BUTTON_HEIGHT)
right_button = pygame.Rect(280, 10, ARROW_BUTTON_WIDTH, ARROW_BUTTON_HEIGHT)
double_right_button = pygame.Rect(340, 10, ARROW_BUTTON_WIDTH, ARROW_BUTTON_HEIGHT)

PALETTE_BLOCK_SIZE = 30  # Size for color palette blocks

def draw_top_menu():
    top_menu_rect = pygame.Rect(0, 0, SCREEN_WIDTH, TOP_MENU_HEIGHT)
    pygame.draw.rect(screen, GRAY, top_menu_rect)

    # Draw double left arrow button
    pygame.draw.rect(screen, BLUE, double_left_button)
    text = small_font.render('<<', True, WHITE)
    screen.blit(text, (double_left_button.x + 5, double_left_button.y))

    # Draw left arrow button
    pygame.draw.rect(screen, BLUE, left_button)
    text = small_font.render('<', True, WHITE)
    screen.blit(text, (left_button.x + 15, left_button.y))

    # Draw right arrow button
    pygame.draw.rect(screen, BLUE, right_button)
    text = small_font.render('>', True, WHITE)
    screen.blit(text, (right_button.x + 15, right_button.y))

    # Draw double right arrow button
    pygame.draw.rect(screen, BLUE, double_right_button)
    text = small_font.render('>>', True, WHITE)
    screen.blit(text, (double_right_button.x + 5, double_right_button.y))

    # Draw page counter (centered between left and right buttons)
    page_counter_position = (left_button.right + right_button.left) // 2
    text = font.render(f'{page_number}/{LAST_PAGE}', True, BLACK)
    text_rect = text.get_rect(center=(page_counter_position, 28))
    screen.blit(text, text_rect.topleft)

    # Draw color palette in 1*10 format with indices above
    palette_start_x = SCREEN_WIDTH - (10 * PALETTE_BLOCK_SIZE) - 20
    palette_start_y = 10  # Moved lower to make space for indices
    index = 0
    for col in range(10):
        color = COLOR_PALETTE[index]
        palette_rect = pygame.Rect(palette_start_x + col * PALETTE_BLOCK_SIZE,
                                   palette_start_y + 8,  # Pushed down
                                   PALETTE_BLOCK_SIZE, PALETTE_BLOCK_SIZE)
        pygame.draw.rect(screen, color, palette_rect)
        pygame.draw.rect(screen, BLACK, palette_rect, 1)

        # Draw the index above the color block
        index_text = very_small_font.render(str(index), True, BLACK)
        text_rect = index_text.get_rect(center=(palette_rect.centerx, palette_start_y))
        screen.blit(index_text, text_rect.topleft)
        index += 1


def draw_middle_play():
    middle_play_rect = pygame.Rect(0, TOP_MENU_HEIGHT, SCREEN_WIDTH, MIDDLE_PLAY_HEIGHT)
    pygame.draw.rect(screen, WHITE, middle_play_rect)

    # Display current page number
    text = small_font.render(f'Page no. {page_number}', True, BLACK)
    screen.blit(text, (10, TOP_MENU_HEIGHT + 10))

    # Determine number of blocks for current page
    blocks_count = TRAINING_BLOCKS_COUNT[page_number - 1]  # Page number is 1-based index
    rows = cols = math.ceil(math.sqrt(blocks_count))

    # Training blocks area (66% of the width on the left side)
    training_area_width = SCREEN_WIDTH * 0.66
    test_area_width = SCREEN_WIDTH - training_area_width

    # Calculate the size of each block in the training area
    if rows * (cols - 1) >= blocks_count:  # More efficient layout considering left-aligned blocks
        cols -= 1

    block_width = training_area_width / cols
    block_height = MIDDLE_PLAY_HEIGHT / rows

    # Draw training blocks
    for i in range(blocks_count):
        row = i // cols
        col = i % cols
        block_rect = pygame.Rect(col * block_width, TOP_MENU_HEIGHT + row * block_height, block_width, block_height)
        pygame.draw.rect(screen, LIGHT_GRAY, block_rect)
        pygame.draw.rect(screen, GRAY, block_rect, 2)  # Draw block with a 2-pixel border

        # Draw the label inside the block
        text = font.render(f'Training {i + 1}', True, BLACK)
        text_rect = text.get_rect(center=block_rect.center)
        screen.blit(text, text_rect)

        # Draw width, height and ratio in lower left corner
        dimension_text = very_small_font.render(
            f'{block_rect.width:.0f}x{block_rect.height:.0f} {block_rect.width / block_rect.height:.2f}',
            True, BLACK)
        screen.blit(dimension_text, (block_rect.x + 5, block_rect.y + block_rect.height - 20))

    # Draw test blocks
    test_block_height = MIDDLE_PLAY_HEIGHT / 2
    for i in range(2):
        test_block_rect = pygame.Rect(training_area_width, TOP_MENU_HEIGHT + i * test_block_height, test_area_width,
                                      test_block_height)
        pygame.draw.rect(screen, LIGHT_GRAY, test_block_rect)
        pygame.draw.rect(screen, GRAY, test_block_rect, 2)

        # Draw the label inside the test block
        text = font.render(f'Test {i + 1}', True, BLACK)
        text_rect = text.get_rect(center=test_block_rect.center)
        screen.blit(text, text_rect)

        # Draw width, height and ratio in lower left corner
        dimension_text = very_small_font.render(
            f'{test_block_rect.width:.0f}x{test_block_rect.height:.0f} {test_block_rect.width / test_block_rect.height:.2f}',
            True, BLACK)
        screen.blit(dimension_text, (test_block_rect.x + 5, test_block_rect.y + test_block_rect.height - 20))


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