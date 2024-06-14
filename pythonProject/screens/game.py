from constants import Constants as C
from utils.color import Color as Color
from randomly_initialize import load_all_training_blocks, load_all_test_blocks
from utils.grid import draw_matrices_and_buttons, draw_matrices_block, paint_post_grid
import actions

import pygame
import math
import inspect
import time
import sys

def draw_top_menu():
    # print(f"The name of this function is {inspect.currentframe().f_code.co_name}")
    top_menu_rect = pygame.Rect(0, 0, C.SCREEN_WIDTH, C.TOP_MENU_HEIGHT)
    pygame.draw.rect(C.screen, Color.GRAY, top_menu_rect)

    # Draw double left arrow button
    pygame.draw.rect(C.screen, Color.BLUE, C.double_left_button)
    C.screen.blit(C.small_font.render('<<', True, Color.WHITE), (C.double_left_button.x + 5, C.double_left_button.y))
    # Draw left arrow button
    pygame.draw.rect(C.screen, Color.BLUE, C.left_button)
    C.screen.blit(C.small_font.render('<', True, Color.WHITE), (C.left_button.x + 15, C.left_button.y))
    # Draw right arrow button
    pygame.draw.rect(C.screen, Color.BLUE, C.right_button)
    C.screen.blit(C.small_font.render('>', True, Color.WHITE), (C.right_button.x + 15, C.right_button.y))
    # Draw double right arrow button
    pygame.draw.rect(C.screen, Color.BLUE, C.double_right_button)
    C.screen.blit(C.small_font.render('>>', True, Color.WHITE), (C.double_right_button.x + 5, C.double_right_button.y))

    # Draw page counter (centered between left and right buttons)
    page_counter_position = (C.left_button.right + C.right_button.left) // 2
    text = C.font.render(f'{C.page_number}/{C.LAST_PAGE}', True, Color.BLACK)
    C.screen.blit(text, text.get_rect(center=(page_counter_position, 28)).topleft)

    # Draw double EXIT button
    pygame.draw.rect(C.screen, Color.BLUE, C.exit_button)
    C.screen.blit(C.small_font.render('EXIT', True, Color.WHITE), (C.exit_button.x + 5,
                                                                   C.exit_button.y))

    # Draw color palette in 1*10 format with indices above
    palette_start_x = C.SCREEN_WIDTH - (10 * Color.PALETTE_BLOCK_SIZE) - 20 - 200
    palette_start_y = 10
    C.color_palette_rects.clear()
    for index in range(10):
        color = Color.COLOR_PALETTE[index]
        palette_rect = pygame.Rect(palette_start_x + index * Color.PALETTE_BLOCK_SIZE, palette_start_y + 8, Color.PALETTE_BLOCK_SIZE, Color.PALETTE_BLOCK_SIZE)
        pygame.draw.rect(C.screen, color, palette_rect)
        pygame.draw.rect(C.screen, Color.BLACK, palette_rect, 1)
        C.color_palette_rects.append(palette_rect)

        # Draw the index above the color block
        index_text = C.very_small_font.render(str(index), True, Color.BLACK)
        C.screen.blit(index_text, index_text.get_rect(center=(palette_rect.centerx, palette_start_y)).topleft)

        if C.selected_color == index:
            contrast = tuple([255-c for c in color])
            pygame.draw.line(C.screen, contrast, (palette_rect.x, palette_rect.y), (palette_rect.x + Color.PALETTE_BLOCK_SIZE, palette_rect.y + Color.PALETTE_BLOCK_SIZE), 2)
            pygame.draw.line(C.screen, contrast, (palette_rect.x + Color.PALETTE_BLOCK_SIZE, palette_rect.y), (palette_rect.x, palette_rect.y + Color.PALETTE_BLOCK_SIZE), 2)


def draw_middle_play():
    # print(f"The name of this function is {inspect.currentframe().f_code.co_name}")
    TRAINING_BLOCKS_COUNT, block_matrices = load_all_training_blocks()
    TEST_BLOCKS_COUNT, test_matrices_by_page = load_all_test_blocks()
    middle_play_rect = pygame.Rect(0, C.TOP_MENU_HEIGHT, C.SCREEN_WIDTH, C.MIDDLE_PLAY_HEIGHT)
    pygame.draw.rect(C.screen, Color.WHITE, middle_play_rect)

    training_area_width, test_area_width = C.SCREEN_WIDTH * 0.66, C.SCREEN_WIDTH * 0.34

    if C.maximized_block is None:
        blocks_count = TRAINING_BLOCKS_COUNT[C.page_number - 1]
        rows, cols = math.ceil(math.sqrt(blocks_count)), math.ceil(math.sqrt(blocks_count))

        block_width = training_area_width / cols
        block_height = C.MIDDLE_PLAY_HEIGHT / rows
        margin = 10

        page_matrices = block_matrices[C.page_number - 1]
        for i in range(blocks_count):
            row, col = i // cols, i % cols
            block_rect = pygame.Rect(col * block_width, C.TOP_MENU_HEIGHT + row * block_height, block_width, block_height)
            pygame.draw.rect(C.screen, Color.LIGHT_GRAY, block_rect)
            pygame.draw.rect(C.screen, Color.GRAY, block_rect, 2)

            pre_matrix, post_matrix = page_matrices[i]
            draw_matrices_block(pre_matrix, post_matrix, block_rect, index=i, draw_plus=True)

        test_block_height = C.MIDDLE_PLAY_HEIGHT / TEST_BLOCKS_COUNT[C.page_number - 1]
        test_block_offset = 0
        if TEST_BLOCKS_COUNT[C.page_number - 1] == 1:
            test_block_height = min(test_area_width / 2 - 1.5 * margin, C.MIDDLE_PLAY_HEIGHT - 2 * margin - 40)
            test_block_height *= 1.35
            test_block_offset = test_block_height / 2

        button_height = 40
        button_width = (test_area_width - 4 * margin) / 3  # Equal gaps around and between buttons

        test_matrices = test_matrices_by_page[C.page_number - 1]

        for i in range(TEST_BLOCKS_COUNT[C.page_number - 1]):
            test_block_rect = pygame.Rect(training_area_width,
                                          C.TOP_MENU_HEIGHT + i * test_block_height + test_block_offset,
                                          test_area_width, test_block_height)
            pygame.draw.rect(C.screen, Color.LIGHT_GRAY, test_block_rect)
            pygame.draw.rect(C.screen, Color.GRAY, test_block_rect, 2)

            pre_matrix, post_matrix = test_matrices[i]
            copy_button, reset_button, submit_button = draw_matrices_and_buttons(test_block_rect, margin, button_height,
                                                                                 button_width, pre_matrix,
                                                                                 post_matrix, index = i,
                                                                                 draw_plus=True)

            C.test_buttons.append((copy_button, i, C.COPY_ACTION))
            C.test_buttons.append((reset_button, i, C.RESET_ACTION))
            C.test_buttons.append((submit_button, i, C.SUBMIT_ACTION))
    else:
        C.screen.set_alpha(150)
        # pygame.draw.rect(screen, GRAY, middle_play_rect)  # Fade background

        original_block = C.maximized_block
        is_test_block, page, block_index = original_block

        # Enlarge to 80% of the play area
        new_width, new_height = int(C.SCREEN_WIDTH * 0.8), int(C.MIDDLE_PLAY_HEIGHT * 0.8)
        block_rect = pygame.Rect((C.SCREEN_WIDTH - new_width) // 2, C.TOP_MENU_HEIGHT + (C.MIDDLE_PLAY_HEIGHT - new_height) // 2, new_width, new_height)
        pygame.draw.rect(C.screen, Color.LIGHT_GRAY, block_rect)
        pre_matrix, post_matrix = (block_matrices if not is_test_block else test_matrices_by_page)[page][block_index]
        if is_test_block:
            margin = 10
            button_height = 40
            button_width = (test_area_width - 4 * margin) / 3  # Equal gaps around and between buttons

            copy_button, reset_button, submit_button = draw_matrices_and_buttons(block_rect, margin, button_height,
                                                                                 button_width, pre_matrix,
                                                                                 post_matrix, index=block_index,
                                                                                 draw_plus=False)

            C.test_buttons.append((copy_button, block_index, C.COPY_ACTION))
            C.test_buttons.append((reset_button, block_index, C.RESET_ACTION))
            C.test_buttons.append((submit_button, block_index, C.SUBMIT_ACTION))
        else:
            draw_matrices_block(pre_matrix, post_matrix, block_rect, index=None, is_test_block=is_test_block, draw_plus=False)

def draw_bottom_status():
    # print(f"The name of this function is {inspect.currentframe().f_code.co_name}")
    bottom_status_rect = pygame.Rect(0, C.SCREEN_HEIGHT - C.BOTTOM_STATUS_HEIGHT, C.SCREEN_WIDTH, C.BOTTOM_STATUS_HEIGHT)
    pygame.draw.rect(C.screen, Color.GRAY, bottom_status_rect)
    text = C.font.render(C.status_message, True, Color.BLACK)
    C.screen.blit(text, (10, C.SCREEN_HEIGHT - C.BOTTOM_STATUS_HEIGHT + 10))

def game_screen():
    while C.scene == "game":
        # print(f"{time.time()}: LOOP!")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                C.scene = "EXIT"
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
                elif C.exit_button.collidepoint(pos):
                    C.scene = "intro"
                    print("Transition from Game -> Intro")
                    break
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

    return