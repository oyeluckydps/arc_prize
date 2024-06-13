from constants import Constants as C
from utils.color import Color as Color
import inspect
import pygame

def paint_post_grid(post_matrix, post_rec, pos, gap):
    # print(f"The name of this function is {inspect.currentframe().f_code.co_name}")
    if C.paint_mode and C.selected_color is not None:
        n = len(post_matrix)
        cell_size = int(min((post_rec.width - (n - 1) * gap) / n, (post_rec.height - (n - 1) * gap) / n))
        start_x = post_rec.x
        start_y = post_rec.y
        j = int((pos[0] - start_x) // (cell_size + gap))
        i = int((pos[1] - start_y) // (cell_size + gap))
        if 0 <= i < len(post_matrix) and 0 <= j < len(post_matrix[0]):
            post_matrix[i][j] = C.selected_color


def draw_grids_in_block(matrix, start_x, start_y, block_width, block_height, gap = 1):
    # print(f"The name of this function is {inspect.currentframe().f_code.co_name}")
    n = len(matrix)
    cell_size = int(min((block_width - (n - 1) * gap) / n, (block_height - (n - 1) * gap) / n))
    for i in range(n):
        for j in range(n):
            color = Color.COLOR_PALETTE[matrix[i][j]]
            cell_rect = pygame.Rect(start_x + j * (cell_size + gap), start_y + i * (cell_size + gap), cell_size,
                                     cell_size)
            pygame.draw.rect(C.screen, color, cell_rect)

def draw_matrices_block(pre_matrix, post_matrix, block_rect, index, is_test_block=False, draw_plus=True):
    # print(f"The name of this function is {inspect.currentframe().f_code.co_name}")
    margin = 10
    button_height = 40 if is_test_block else 0

    max_grid_size = min(block_rect.width / 2 - 1.5 * margin, block_rect.height - 3 * margin - button_height)
    inner_height = inner_width = max_grid_size

    start_x = block_rect.x + (block_rect.width - 2 * inner_width - 3 * margin) / 2
    start_y = block_rect.y + (block_rect.height - inner_height - 2 * margin - button_height) / 2

    pre_rect = pygame.Rect(start_x + margin, start_y + margin, inner_width, inner_height)
    post_rect = pygame.Rect(start_x + 2 * margin + inner_width, start_y + margin, inner_width, inner_height)

    # pygame.draw.rect(screen, BLACK, pre_rect, 2)
    # pygame.draw.rect(screen, BLACK, post_rect, 2)

    gap = 1  # 1-pixel gap between grid elements

    draw_grids_in_block(pre_matrix, pre_rect.x, pre_rect.y, pre_rect.width, pre_rect.height, gap)
    draw_grids_in_block(post_matrix, post_rect.x, post_rect.y, post_rect.width, post_rect.height, gap)

    if is_test_block:
        C.post_grid_params.append((post_matrix, post_rect, gap))

    arrow_start = (post_rect.x - margin, post_rect.y + inner_height / 2)
    arrow_end = (post_rect.x, post_rect.y + inner_height / 2)

    pygame.draw.line(C.screen, Color.BLACK, arrow_start, arrow_end, 2)
    pygame.draw.polygon(C.screen, Color.BLACK, [(arrow_end[0] - 5, arrow_end[1] - 5), (arrow_end[0], arrow_end[1]),
                                         (arrow_end[0] - 5, arrow_end[1] + 5)])

    if draw_plus:
        maximize_rect = pygame.Rect(block_rect.right - 20, block_rect.top, 20, 20)
        pygame.draw.line(C.screen, Color.BLACK, (block_rect.right - 15, block_rect.top + 10), (block_rect.right - 5,
                                                                                    block_rect.top + 10), 2)
        pygame.draw.line(C.screen, Color.BLACK, (block_rect.right - 10, block_rect.top + 5), (block_rect.right - 10,
                                                                                   block_rect.top + 15), 2)
        C.max_min_buttons.append((maximize_rect, C.MAXIMIZE_ACTION, is_test_block, C.page_number-1, index))
    else:
        minimize_rect = pygame.Rect(block_rect.right - 20, block_rect.top, 20, 20)
        pygame.draw.line(C.screen, Color.BLACK, (block_rect.right - 15, block_rect.top + 5), (block_rect.right - 5,
                                                                                      block_rect.top + 5), 2)
        C.max_min_buttons.append((minimize_rect, C.MINIMIZE_ACTION, is_test_block, C.page_number-1, index))
    return is_test_block, pre_rect, post_rect

def draw_matrices_and_buttons(test_block_rect, margin, button_height, button_width, pre_matrix, post_matrix, index,
                              draw_plus=True):
    # print(f"The name of this function is {inspect.currentframe().f_code.co_name}")
    _, pre_rect, post_rect = draw_matrices_block(pre_matrix, post_matrix, test_block_rect, index, is_test_block=True,
                                                 draw_plus=draw_plus)

    button_y = test_block_rect.y + test_block_rect.height - button_height - margin
    button_x_offset = (test_block_rect.width - (button_width*3 + margin*4))/2

    copy_button = pygame.Rect(test_block_rect.x + margin + button_x_offset, button_y, button_width, button_height)
    reset_button = pygame.Rect(test_block_rect.x + 2 * margin + button_width + button_x_offset, button_y, button_width, button_height)
    submit_button = pygame.Rect(test_block_rect.x + 3 * margin + 2 * button_width + button_x_offset, button_y, button_width, button_height)

    pygame.draw.rect(C.screen, Color.BUTTON_COLOR, copy_button, border_radius=10)
    pygame.draw.rect(C.screen, Color.BUTTON_COLOR, reset_button, border_radius=10)
    pygame.draw.rect(C.screen, Color.BUTTON_COLOR, submit_button, border_radius=10)

    pygame.draw.rect(C.screen, Color.BLACK, copy_button, 2, border_radius=10)
    pygame.draw.rect(C.screen, Color.BLACK, reset_button, 2, border_radius=10)
    pygame.draw.rect(C.screen, Color.BLACK, submit_button, 2, border_radius=10)

    copy_text = C.button_font.render('Copy', True, Color.WHITE)
    reset_text = C.button_font.render('Reset', True, Color.WHITE)
    submit_text = C.button_font.render('Submit', True, Color.WHITE)

    copy_text_rect = copy_text.get_rect(center=copy_button.center)
    reset_text_rect = reset_text.get_rect(center=reset_button.center)
    submit_text_rect = submit_text.get_rect(center=submit_button.center)

    C.screen.blit(copy_text, copy_text_rect)
    C.screen.blit(reset_text, reset_text_rect)
    C.screen.blit(submit_text, submit_text_rect)

    return copy_button, reset_button, submit_button

