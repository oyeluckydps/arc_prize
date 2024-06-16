import pygame
import math
pygame.init()
from ..constants import Constants as C
from ..utils.color import Color
from .utils import draw_patterns_in_area, calculate_block_size

def display_patterns(pre_patterns, post_patterns=None):
    """
    Display patterns on a Pygame screen, dividing the play area into grids for each pattern.
    
    Parameters:
    pre_patterns (list): A list of patterns, where each pattern is a list of tuples. Each tuple 
                         contains the coordinates (x, y) and the color of the cell.
    post_patterns (list, optional): A list of patterns similar to pre_patterns to be displayed 
                                    in the POST-AREA. Defaults to None.
    """
    # Set up the screen
    screen = pygame.display.set_mode((C.SCREEN_WIDTH, C.SCREEN_HEIGHT))
    pygame.display.set_caption("Pattern Display")
    
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
    
    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if C.exit_button.collidepoint(event.pos):
                    running = False
        
        # Fill the screen with a background color
        screen.fill(Color.WHITE)
        
        # Draw the top menu
        pygame.draw.rect(screen, Color.GRAY, (0, 0, C.SCREEN_WIDTH, C.TOP_MENU_HEIGHT))
        
        # Draw the bottom status area
        pygame.draw.rect(screen, Color.GRAY, (0, C.SCREEN_HEIGHT - C.BOTTOM_STATUS_HEIGHT, C.SCREEN_WIDTH, C.BOTTOM_STATUS_HEIGHT))
        
        # Draw the middle play area
        play_area_rect = pygame.Rect(0, C.TOP_MENU_HEIGHT, C.SCREEN_WIDTH, C.MIDDLE_PLAY_HEIGHT)
        pygame.draw.rect(screen, Color.LIGHT_GRAY, play_area_rect)
        
        # Draw the exit button
        pygame.draw.rect(screen, Color.BUTTON_COLOR, C.exit_button)
        exit_text = C.button_font.render("Exit", True, Color.WHITE)
        screen.blit(exit_text, (C.exit_button.x + 10, C.exit_button.y + 5))
        
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
        
        # Update the display
        pygame.display.flip()
    
    pygame.quit()

