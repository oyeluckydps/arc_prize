from constants import Constants as C
# from randomly_initialize import load_all_test_blocks
from data_initialize import check_solution
import inspect

def reset_states():
    # print(f"The name of this function is {inspect.currentframe().f_code.co_name}")
    C.test_buttons = []
    C.max_min_buttons = []
    C.post_grid_params = []
    C.status_message = ''

def reset_blocks():
    C.test_blocks_num = None
    C.test_blocks_mats = None
    C.train_blocks_num = None
    C.train_blocks_mats = None

def maximize_block(original_block):
    # print(f"The name of this function is {inspect.currentframe().f_code.co_name}")
    C.maximized_block = original_block
    reset_states()

def minimize_block():
    # print(f"The name of this function is {inspect.currentframe().f_code.co_name}")
    C.maximized_block = None
    reset_states()

def update_page(delta):
    # print(f"The name of this function is {inspect.currentframe().f_code.co_name}")
    C.page_number += delta
    if C.page_number < C.FIRST_PAGE:
        C.page_number = C.FIRST_PAGE
    elif C.page_number > C.LAST_PAGE:
        C.page_number = C.LAST_PAGE
    reset_states()
    reset_blocks()

def go_to_first_page():
    # print(f"The name of this function is {inspect.currentframe().f_code.co_name}")
    C.page_number = C.FIRST_PAGE
    reset_states()
    reset_blocks()

def go_to_last_page():
    # print(f"The name of this function is {inspect.currentframe().f_code.co_name}")
    C.page_number = C.LAST_PAGE
    reset_states()
    reset_blocks()

def handle_button_click(pos, test_block_index, action):
    """ Handle button click actions for copy, reset, and submit """
    # print(f"The name of this function is {inspect.currentframe().f_code.co_name}")
    pre_matrix, post_matrix = C.test_blocks_mats[test_block_index]

    if action == C.COPY_ACTION:
        if len(pre_matrix) == len(post_matrix) and len(pre_matrix[0]) == len(post_matrix[0]):
            for i in range(len(pre_matrix)):
                for j in range(len(pre_matrix[i])):
                    post_matrix[i][j] = pre_matrix[i][j]
            C.status_message = ""
        else:
            C.status_message = "COPY not possible as dimensions mismatch!"
    elif action == C.RESET_ACTION:
        for i in range(len(post_matrix)):
            for j in range(len(post_matrix[i])):
                post_matrix[i][j] = 0
        C.status_message = ""
    elif action == C.SUBMIT_ACTION:
        correct, actual_solution = check_solution(C.page_number, test_block_index, post_matrix)
        if correct:
            C.status_message = f"CORRECT ANSWER!"
        else:
            C.status_message = "INCORRECT ANSWER! - Showing Solution now."
            C.test_blocks_mats[test_block_index] = (C.test_blocks_mats[test_block_index][0], actual_solution)
            C.post_grid_params[test_block_index] = (actual_solution, C.post_grid_params[test_block_index][1],
                                                    C.post_grid_params[test_block_index][2])


