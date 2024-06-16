import pygame
import math
pygame.init()
from ..constants import Constants as C
from ..utils.color import Color
from .utils import draw_patterns_in_area, calculate_block_size

def display_patterns(screen, pre_patterns, post_patterns=None):
    """
    Display patterns on a Pygame screen, dividing the play area into grids for each pattern.
    
    Parameters:
    pre_patterns (list): A list of patterns, where each pattern is a list of tuples. Each tuple 
                         contains the coordinates (x, y) and the color of the cell.
    post_patterns (list, optional): A list of patterns similar to pre_patterns to be displayed 
                                    in the POST-AREA. Defaults to None.
    """
    # Calculate the number of columns and rows for the grid
    num_pre_patterns = len(pre_patterns)
    num_pre_columns = math.ceil(num_pre_patterns ** 0.5)
    num_pre_rows = (num_pre_patterns + num_pre_columns - 1) // num_pre_columns
    
    if post_patterns:
        num_post_patterns = len(post_patterns)
        num_post_columns = math.ceil(num_post_patterns ** 0.5)
        num_post_rows = (num_post_patterns + num_post_columns - 1) // num_post_columns
    else:
        num_post_patterns = 0
        num_post_columns = 0
        num_post_rows = 0
    
    # Calculate the size of each grid cell
    cell_width = C.SCREEN_WIDTH // (num_pre_columns + num_post_columns)
    cell_height = C.MIDDLE_PLAY_HEIGHT // max(num_pre_rows, num_post_rows)
    margin = 10
    gap = 1
    
    # Calculate the smallest block size for all patterns
    min_block_size = calculate_block_size(pre_patterns, cell_width, cell_height, margin, gap)
    if post_patterns:
        min_block_size = min(min_block_size, calculate_block_size(post_patterns, cell_width, cell_height, margin, gap))

    # Calculate the width of each area
    if post_patterns:
        pre_area_width = C.SCREEN_WIDTH // 2
        post_area_width = C.SCREEN_WIDTH - pre_area_width
        # Draw the separator
        pygame.draw.line(screen, Color.BLACK, (pre_area_width, C.TOP_MENU_HEIGHT), (pre_area_width, C.SCREEN_HEIGHT - C.BOTTOM_STATUS_HEIGHT), 5)
    else:
        pre_area_width = C.SCREEN_WIDTH
        post_area_width = 0

    # Draw the pre_patterns in the PRE-AREA
    draw_patterns_in_area(screen, pre_patterns, 0, pre_area_width, C.TOP_MENU_HEIGHT, C.MIDDLE_PLAY_HEIGHT, min_block_size)

    # Draw the post_patterns in the POST-AREA
    if post_patterns:
        draw_patterns_in_area(screen, post_patterns, pre_area_width, post_area_width, C.TOP_MENU_HEIGHT, C.MIDDLE_PLAY_HEIGHT, min_block_size)


def display_patterns_list(patterns_list):
    """
    Display patterns from a list of PRE and POST patterns on a Pygame screen with navigation buttons.
    
    Parameters:
    patterns_list (list): A list of tuples, where each tuple contains a list of PRE patterns and a list of POST patterns.
    """
    current_index = 0
    total_patterns = len(patterns_list)
    
    def update_display(screen):
        pre_patterns, post_patterns = patterns_list[current_index]
        display_patterns(screen, pre_patterns, post_patterns)
    
    # Set up the screen
    screen = pygame.display.set_mode((C.SCREEN_WIDTH, C.SCREEN_HEIGHT))
    pygame.display.set_caption("Pattern Display")
    
    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if C.exit_button.collidepoint(event.pos):
                    running = False
                elif C.left_button.collidepoint(event.pos):
                    current_index = max(0, current_index - 1)
                elif C.right_button.collidepoint(event.pos):
                    current_index = min(total_patterns - 1, current_index + 1)
                elif C.double_left_button.collidepoint(event.pos):
                    current_index = 0
                elif C.double_right_button.collidepoint(event.pos):
                    current_index = total_patterns - 1

        # Fill the screen with a background color
        screen.fill(Color.WHITE)

        # Draw the top menu
        pygame.draw.rect(screen, Color.GRAY, (0, 0, C.SCREEN_WIDTH, C.TOP_MENU_HEIGHT))
        
        # Draw the bottom status area
        pygame.draw.rect(screen, Color.GRAY, (0, C.SCREEN_HEIGHT - C.BOTTOM_STATUS_HEIGHT, C.SCREEN_WIDTH, C.BOTTOM_STATUS_HEIGHT))
        
        # Draw the middle play area
        play_area_rect = pygame.Rect(0, C.TOP_MENU_HEIGHT, C.SCREEN_WIDTH, C.MIDDLE_PLAY_HEIGHT)
        pygame.draw.rect(screen, Color.LIGHT_GRAY, play_area_rect)

        update_display(screen)

        # Draw the exit button
        pygame.draw.rect(screen, Color.BUTTON_COLOR, C.exit_button)
        exit_text = C.button_font.render("Exit", True, Color.WHITE)
        screen.blit(exit_text, (C.exit_button.x + 10, C.exit_button.y + 5))
        
        # Draw navigation buttons
        pygame.draw.rect(screen, Color.BUTTON_COLOR, C.double_left_button)
        double_left_text = C.button_font.render("<<", True, Color.WHITE)
        screen.blit(double_left_text, (C.double_left_button.x + 10, C.double_left_button.y + 5))
        
        pygame.draw.rect(screen, Color.BUTTON_COLOR, C.left_button)
        left_text = C.button_font.render("<", True, Color.WHITE)
        screen.blit(left_text, (C.left_button.x + 10, C.left_button.y + 5))
        
        pygame.draw.rect(screen, Color.BUTTON_COLOR, C.right_button)
        right_text = C.button_font.render(">", True, Color.WHITE)
        screen.blit(right_text, (C.right_button.x + 10, C.right_button.y + 5))
        
        pygame.draw.rect(screen, Color.BUTTON_COLOR, C.double_right_button)
        double_right_text = C.button_font.render(">>", True, Color.WHITE)
        screen.blit(double_right_text, (C.double_right_button.x + 10, C.double_right_button.y + 5))
        
        # Draw the current index and total patterns
        index_text = C.button_font.render(f"{current_index + 1}/{total_patterns}", True, Color.BLACK)
        screen.blit(index_text, (C.left_button.x + C.left_button.width + 10, C.left_button.y + 5))
        
        # Update the display
        pygame.display.flip()
    
    pygame.quit()

