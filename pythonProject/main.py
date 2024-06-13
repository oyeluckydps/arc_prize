import pygame

# Initialize Pygame
pygame.init()

from constants import Constants as C
import actions
from screens.game import draw_top_menu, draw_middle_play, draw_bottom_status
import time
import sys
from utils.color import Color
from utils.grid import paint_post_grid

# Main game loop
def main():
    running = True
    while running:
        # print(f"{time.time()}: LOOP!")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                # Check if top menu navigation buttons are clicked
                if C.double_left_button.collidepoint(pos):
                    actions.go_to_first_page()
                elif C.left_button.collidepoint(pos):
                    actions.update_page(-1)
                elif C.right_button.collidepoint(pos):
                    actions.update_page(1)
                elif C.double_right_button.collidepoint(pos):
                    actions.go_to_last_page()
                # Check if any test block buttons are clicked
                for button, index, action in C.test_buttons:
                    if button.collidepoint(pos):
                        actions.handle_button_click(pos, index, action)
                        break  # Only handle one button click per event

                for max_min_button, action, is_test_block, page, block_index in C.max_min_buttons:
                    if max_min_button.collidepoint(pos):
                        if action == C.MAXIMIZE_ACTION:
                            actions.maximize_block((is_test_block, page, block_index))
                        elif action == C.MINIMIZE_ACTION:
                            actions.minimize_block()
                        break

                for post_matrix, post_rect, gap in C.post_grid_params:
                    if post_rect.collidepoint(pos):
                        paint_post_grid(post_matrix, post_rect, pos, gap)
                    break

                Color.handle_color_selection(pos)


        # Clear the screen
        C.screen.fill(Color.WHITE)

        # Draw the different areas
        draw_top_menu()
        draw_middle_play()
        draw_bottom_status()

        # Update the display
        pygame.display.flip()

    # Quit Pygame
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

