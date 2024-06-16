import pygame
import math
from ..constants import Constants as C
from ..utils.color import Color


def draw_patterns_in_area(screen, patterns, start_x, area_width, start_y, area_height):
    """
    Draw patterns in a specified area on the screen.
    
    Parameters:
    screen (pygame.Surface): The Pygame screen surface to draw on.
    patterns (list): A list of patterns, where each pattern is a list of tuples. Each tuple 
                     contains the coordinates (x, y) and the color of the cell.
    start_x (int): The starting x-coordinate of the area.
    area_width (int): The width of the area.
    start_y (int): The starting y-coordinate of the area.
    area_height (int): The height of the area.
    """
    num_patterns = len(patterns)
    num_columns = math.ceil(num_patterns ** 0.5)
    num_rows = (num_patterns + num_columns - 1) // num_columns
    
    cell_width = area_width // num_columns
    cell_height = area_height // num_rows
    margin = 10
    gap = 1
    
    for index, pattern in enumerate(patterns):
        col = index % num_columns
        row = index // num_columns
        cell_x = start_x + col * cell_width
        cell_y = start_y + row * cell_height
        
        if pattern:
            max_x = max(x for x, y, color in pattern)
            min_x = min(x for x, y, color in pattern)
            max_y = max(y for x, y, color in pattern)
            min_y = min(y for x, y, color in pattern)
            
            num_rows_in_pattern = max_x - min_x + 1
            num_cols_in_pattern = max_y - min_y + 1
            
            block_size = min((cell_height - margin - (num_rows_in_pattern - 1) * gap) // num_rows_in_pattern, 
                             (cell_width - margin - (num_cols_in_pattern - 1) * gap) // num_cols_in_pattern)
        
        for x in range(num_rows_in_pattern):
            for y in range(num_cols_in_pattern):
                color_rgb = Color.BLACK
                for (px, py, color) in pattern:
                    if px == min_x + x and py == min_y + y:
                        color_rgb = Color.COLOR_PALETTE[color]
                        break
                pygame.draw.rect(screen, color_rgb, (cell_x + x * (block_size + gap), cell_y + y * (block_size + gap), block_size, block_size))
        
        if pattern:
            first_cell = pattern[0]
            text_surface = C.very_small_font.render(f"({first_cell[0]}, {first_cell[1]})", True, Color.BLACK)
            screen.blit(text_surface, (cell_x, cell_y + cell_height - margin))

