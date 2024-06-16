import pygame
from GUI.constants import Constants as C
from GUI.utils.color import Color

def display_patterns(patterns):
    """
    Display patterns on a Pygame screen, dividing the play area into grids for each pattern.
    
    Parameters:
    patterns (list): A list of patterns, where each pattern is a list of tuples. Each tuple 
                     contains the coordinates (x, y) and the color of the cell.
    """
    pygame.init()
    
    # Set up the screen
    screen = pygame.display.set_mode((C.SCREEN_WIDTH, C.SCREEN_HEIGHT))
    pygame.display.set_caption("Pattern Display")
    
    # Calculate the number of columns and rows for the grid
    num_patterns = len(patterns)
    num_columns = int(num_patterns ** 0.5)
    num_rows = (num_patterns + num_columns - 1) // num_columns
    
    # Calculate the size of each grid cell
    cell_width = C.SCREEN_WIDTH // num_columns
    cell_height = C.MIDDLE_PLAY_HEIGHT // num_rows
    margin = 10
    gap = 1
    
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
        
        # Display the patterns in the middle play area
        for index, pattern in enumerate(patterns):
            # Calculate the position of the grid cell
            col = index % num_columns
            row = index // num_columns
            cell_x = col * cell_width
            cell_y = row * cell_height + C.TOP_MENU_HEIGHT
            
            # Calculate the size of each block in the pattern
            if pattern:
                max_x = max(x for x, y, color in pattern)
                min_x = min(x for x, y, color in pattern)
                max_y = max(y for x, y, color in pattern)
                min_y = min(y for x, y, color in pattern)
                
                num_rows_in_pattern = max_x - min_x + 1
                num_cols_in_pattern = max_y - min_y + 1
                
                block_size = min((cell_height - margin - (num_rows_in_pattern - 1) * gap) // num_rows_in_pattern, 
                                 (cell_width - margin - (num_cols_in_pattern - 1) * gap) // num_cols_in_pattern)
            
            # Draw the pattern inside the grid cell
            for x in range(num_rows_in_pattern):
                for y in range(num_cols_in_pattern):
                    color_rgb = Color.BLACK  # Default color for non-pattern cells
                    for (px, py, color) in pattern:
                        if px == min_x + x and py == min_y + y:
                            color_rgb = Color.COLOR_PALETTE[color]
                            break
                    pygame.draw.rect(screen, color_rgb, (cell_x + x * (block_size + gap), cell_y + y * (block_size + gap), block_size, block_size))
            
            # Write the location of the first cell below the pattern
            if pattern:
                first_cell = pattern[0]
                text_surface = C.very_small_font.render(f"({first_cell[0]}, {first_cell[1]})", True, Color.BLACK)
                screen.blit(text_surface, (cell_x, cell_y + cell_height - margin))
        
        # Update the display
        pygame.display.flip()
    
    pygame.quit()
