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
BUTTON_COLOR = (100, 149, 237)  # Cornflower Blue

# Define copy, reset, and submit actions
COPY_ACTION = 1
RESET_ACTION = 2
SUBMIT_ACTION = 3

# Color palette (9 distinguishable colors + BLACK)
COLOR_PALETTE = [
    BLACK,  # Black
    (255, 0, 0), (0, 255, 0), (0, 0, 255),  # Red, Green, Blue
    (255, 255, 0), (255, 0, 255), (0, 255, 255),  # Yellow, Magenta, Cyan
    (128, 0, 128), (255, 165, 0), (0, 128, 128),  # Purple, Orange, Teal
]

# Initialize page counter and page limits
page_number = 1
FIRST_PAGE = 1
LAST_PAGE = 20

# Initialize status message
status_message = ""

# Initialize TRAINING_BLOCKS_COUNT with random numbers between 1 and 10 for each page
TRAINING_BLOCKS_COUNT = [random.randint(1, 10) for _ in range(LAST_PAGE)]

# Initialize test blocks count with random numbers either 1 or 2 for each page
TEST_BLOCKS_COUNT = [random.randint(1, 2) for _ in range(LAST_PAGE)]

# Initialize fonts
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 30)  # Font for page number
very_small_font = pygame.font.Font(None, 18)  # Font for indices and block dimensions
matrix_font = pygame.font.Font(None, 14)  # Font for matrix display
button_font = pygame.font.Font(None, 28)  # Font for buttons

# Button definitions
ARROW_BUTTON_WIDTH = 50
ARROW_BUTTON_HEIGHT = 30

double_left_button = pygame.Rect(10, 10, ARROW_BUTTON_WIDTH, ARROW_BUTTON_HEIGHT)
left_button = pygame.Rect(70, 10, ARROW_BUTTON_WIDTH, ARROW_BUTTON_HEIGHT)
right_button = pygame.Rect(280, 10, ARROW_BUTTON_WIDTH, ARROW_BUTTON_HEIGHT)
double_right_button = pygame.Rect(340, 10, ARROW_BUTTON_WIDTH, ARROW_BUTTON_HEIGHT)

PALETTE_BLOCK_SIZE = 30  # Size for color palette blocks

# Generate matrices for each block
block_matrices = []
for page_blocks in TRAINING_BLOCKS_COUNT:
    page_matrix = []
    for block in range(page_blocks):
        n = random.randint(2, 30)
        pre_matrix = [[random.randint(0, 9) for _ in range(n)] for _ in range(n)]
        post_matrix = [[random.randint(0, 9) for _ in range(n)] for _ in range(n)]
        page_matrix.append((pre_matrix, post_matrix))
    block_matrices.append(page_matrix)

# Generate pre matrices for test blocks and initialize post matrices to 0
test_matrices_by_page = []
for test_blocks in TEST_BLOCKS_COUNT:
    page_test_matrices = []
    for _ in range(test_blocks):
        n = random.randint(10, 20)  # Reasonable range for display purposes
        pre_matrix = [[random.randint(0, 9) for _ in range(n)] for _ in range(n)]
        post_matrix = [[0 for _ in range(n)] for _ in range(n)]  # Initialize post matrix to 0
        page_test_matrices.append((pre_matrix, post_matrix))
    test_matrices_by_page.append(page_test_matrices)

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
    palette_start_y = 10
    index = 0
    for col in range(10):
        color = COLOR_PALETTE[index]
        palette_rect = pygame.Rect(palette_start_x + col * PALETTE_BLOCK_SIZE,
                                   palette_start_y + 8,
                                   PALETTE_BLOCK_SIZE, PALETTE_BLOCK_SIZE)
        pygame.draw.rect(screen, color, palette_rect)
        pygame.draw.rect(screen, BLACK, palette_rect, 1)

        # Draw the index above the color block
        index_text = very_small_font.render(str(index), True, BLACK)
        text_rect = index_text.get_rect(center=(palette_rect.centerx, palette_start_y))
        screen.blit(index_text, text_rect.topleft)
        index += 1

def draw_grids_in_block(matrix, start_x, start_y, block_width, block_height):
    """ Helper function to draw a grid inside a block """
    n = len(matrix)
    gap = 1  # 1-pixel gap between grid elements
    cell_size = min((block_width - (n - 1) * gap) / n, (block_height - (n - 1) * gap) / n)
    for i in range(n):
        for j in range(n):
            color = COLOR_PALETTE[matrix[i][j]]
            cell_rect = pygame.Rect(start_x + j * (cell_size + gap), start_y + i * (cell_size + gap), cell_size, cell_size)
            pygame.draw.rect(screen, color, cell_rect)

def draw_matrices_block(pre_matrix, post_matrix, block_rect, is_test_block=False):
    """ Helper function to draw pre and post matrices inside a block """
    margin = 10
    button_height = 40 if is_test_block else 0

    # Ensure that the grids are squares
    max_grid_size = min(block_rect.width / 2 - 1.5 * margin, block_rect.height - 2 * margin - button_height)
    inner_height = inner_width = max_grid_size

    # Center align horizontally and vertically
    start_x = block_rect.x + (block_rect.width - 2 * inner_width - 3 * margin) / 2
    start_y = block_rect.y + (block_rect.height - inner_height - 2 * margin - button_height) / 2

    pre_rect = pygame.Rect(start_x + margin, start_y + margin, inner_width, inner_height)
    post_rect = pygame.Rect(start_x + 2 * margin + inner_width, start_y + margin, inner_width, inner_height)

    pygame.draw.rect(screen, BLACK, pre_rect, 2)
    pygame.draw.rect(screen, BLACK, post_rect, 2)

    draw_grids_in_block(pre_matrix, pre_rect.x, pre_rect.y, pre_rect.width, pre_rect.height)
    draw_grids_in_block(post_matrix, post_rect.x, post_rect.y, post_rect.width, post_rect.height)

    # Draw arrow between pre and post grids
    arrow_start = (post_rect.x - margin, post_rect.y + inner_height / 2)
    arrow_end = (post_rect.x, post_rect.y + inner_height / 2)

    pygame.draw.line(screen, BLACK, arrow_start, arrow_end, 2)
    pygame.draw.polygon(screen, BLACK, [(arrow_end[0] - 5, arrow_end[1] - 5), (arrow_end[0], arrow_end[1]),
                                        (arrow_end[0] - 5, arrow_end[1] + 5)])

    return is_test_block, pre_rect, post_rect

def draw_matrices_and_buttons(test_block_rect, margin, button_height, button_width, pre_matrix, post_matrix):
    """ Helper function to draw matrices and buttons inside a test block """

    # Draw matrices
    _, pre_rect, post_rect = draw_matrices_block(pre_matrix, post_matrix, test_block_rect, is_test_block=True)

    # Draw buttons
    button_y = test_block_rect.y + test_block_rect.height - button_height - margin

    copy_button = pygame.Rect(test_block_rect.x + margin, button_y, button_width, button_height)
    reset_button = pygame.Rect(test_block_rect.x + 2 * margin + button_width, button_y, button_width, button_height)
    submit_button = pygame.Rect(test_block_rect.x + 3 * margin + 2 * button_width, button_y, button_width, button_height)

    pygame.draw.rect(screen, BUTTON_COLOR, copy_button, border_radius=10)
    pygame.draw.rect(screen, BUTTON_COLOR, reset_button, border_radius=10)
    pygame.draw.rect(screen, BUTTON_COLOR, submit_button, border_radius=10)

    pygame.draw.rect(screen, BLACK, copy_button, 2, border_radius=10)
    pygame.draw.rect(screen, BLACK, reset_button, 2, border_radius=10)
    pygame.draw.rect(screen, BLACK, submit_button, 2, border_radius=10)

    # Draw button text
    copy_text = button_font.render('Copy', True, WHITE)
    reset_text = button_font.render('Reset', True, WHITE)
    submit_text = button_font.render('Submit', True, WHITE)

    copy_text_rect = copy_text.get_rect(center=copy_button.center)
    reset_text_rect = reset_text.get_rect(center=reset_button.center)
    submit_text_rect = submit_text.get_rect(center=submit_button.center)

    screen.blit(copy_text, copy_text_rect)
    screen.blit(reset_text, reset_text_rect)
    screen.blit(submit_text, submit_text_rect)

    return copy_button, reset_button, submit_button

def handle_button_click(pos, test_block_index, action):
    """ Handle button click actions for copy, reset, and submit """
    global status_message
    pre_matrix, post_matrix = test_matrices_by_page[page_number - 1][test_block_index]

    if action == COPY_ACTION:
        for i in range(len(pre_matrix)):
            for j in range(len(pre_matrix[i])):
                post_matrix[i][j] = pre_matrix[i][j]
    elif action == RESET_ACTION:
        for i in range(len(post_matrix)):
            for j in range(len(post_matrix[i])):
                post_matrix[i][j] = 0
    elif action == SUBMIT_ACTION:
        status_message = f"Submitted Page: {page_number}, Block: {test_block_index + 1}"

def draw_middle_play():
    global test_buttons
    middle_play_rect = pygame.Rect(0, TOP_MENU_HEIGHT, SCREEN_WIDTH, MIDDLE_PLAY_HEIGHT)
    pygame.draw.rect(screen, WHITE, middle_play_rect)

    # Determine number of blocks for current page
    blocks_count = TRAINING_BLOCKS_COUNT[page_number - 1]  # Page number is 1-based index
    rows = cols = math.ceil(math.sqrt(blocks_count))

    # Training blocks area (66% of the width on the left side)
    training_area_width = SCREEN_WIDTH * 0.66
    test_area_width = SCREEN_WIDTH - training_area_width

    # Calculate the size of each block in the training area
    if rows * (cols - 1) >= blocks_count:
        cols -= 1

    block_width = training_area_width / cols
    block_height = MIDDLE_PLAY_HEIGHT / rows
    margin = 10

    # Draw training blocks with grids
    page_matrices = block_matrices[page_number - 1]
    for i in range(blocks_count):
        row = i // cols
        col = i % cols
        block_rect = pygame.Rect(col * block_width, TOP_MENU_HEIGHT + row * block_height, block_width, block_height)
        pygame.draw.rect(screen, LIGHT_GRAY, block_rect)
        pygame.draw.rect(screen, GRAY, block_rect, 2)  # Draw block with a 2-pixel border

        pre_matrix, post_matrix = page_matrices[i]
        draw_matrices_block(pre_matrix, post_matrix, block_rect)

    # Draw test blocks with grids and buttons
    test_block_height = MIDDLE_PLAY_HEIGHT / TEST_BLOCKS_COUNT[page_number - 1]
    test_block_offset = 0
    if TEST_BLOCKS_COUNT[page_number - 1] == 1:
        test_block_height = min(test_area_width / 2 - 1.5 * margin, MIDDLE_PLAY_HEIGHT - 2 * margin - 40)
        # Increase the height by 35% for better visibility
        test_block_height *= 1.35
        test_block_offset = test_block_height / 2

    button_height = 40
    button_width = (test_area_width - 4 * margin) / 3  # Equal gaps around and between buttons

    test_matrices = test_matrices_by_page[page_number - 1]

    for i in range(TEST_BLOCKS_COUNT[page_number - 1]):
        test_block_rect = pygame.Rect(training_area_width,
                                      TOP_MENU_HEIGHT + i * test_block_height + test_block_offset,
                                      test_area_width, test_block_height)
        pygame.draw.rect(screen, LIGHT_GRAY, test_block_rect)
        pygame.draw.rect(screen, GRAY, test_block_rect, 2)

        pre_matrix, post_matrix = test_matrices[i]
        copy_button, reset_button, submit_button = draw_matrices_and_buttons(test_block_rect, margin, button_height,
                                                                             button_width, pre_matrix, post_matrix)

        # Store button positions and related actions
        test_buttons.append((copy_button, i, COPY_ACTION))
        test_buttons.append((reset_button, i, RESET_ACTION))
        test_buttons.append((submit_button, i, SUBMIT_ACTION))

def draw_bottom_status():
    bottom_status_rect = pygame.Rect(0, SCREEN_HEIGHT - BOTTOM_STATUS_HEIGHT, SCREEN_WIDTH, BOTTOM_STATUS_HEIGHT)
    pygame.draw.rect(screen, GRAY, bottom_status_rect)
    text = font.render(status_message, True, BLACK)
    screen.blit(text, (10, SCREEN_HEIGHT - BOTTOM_STATUS_HEIGHT + 10))

def update_page(delta):
    global page_number
    global test_buttons
    page_number += delta
    if page_number < FIRST_PAGE:
        page_number = FIRST_PAGE
    elif page_number > LAST_PAGE:
        page_number = LAST_PAGE
    # Clear previous button states
    test_buttons = []

def go_to_first_page():
    global page_number
    global test_buttons
    page_number = FIRST_PAGE
    # Clear previous button states
    test_buttons = []

def go_to_last_page():
    global page_number
    global test_buttons
    page_number = LAST_PAGE
    # Clear previous button states
    test_buttons = []

# Global list to track button positions and actions
test_buttons = []

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            # Check if top menu navigation buttons are clicked
            if double_left_button.collidepoint(pos):
                go_to_first_page()
            elif left_button.collidepoint(pos):
                update_page(-1)
            elif right_button.collidepoint(pos):
                update_page(1)
            elif double_right_button.collidepoint(pos):
                go_to_last_page()
            # Check if any test block buttons are clicked
            for button, index, action in test_buttons:
                if button.collidepoint(pos):
                    handle_button_click(pos, index, action)
                    break  # Only handle one button click per event

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