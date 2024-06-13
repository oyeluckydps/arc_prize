from constants import Constants as C
from randomly_initialize import load_all_test_blocks
import inspect

def reset_states():
    # print(f"The name of this function is {inspect.currentframe().f_code.co_name}")
    C.test_buttons = []
    C.max_min_buttons = []
    C.post_grid_params = []
    C.status_message = ''

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

def go_to_first_page():
    # print(f"The name of this function is {inspect.currentframe().f_code.co_name}")
    C.page_number = C.FIRST_PAGE
    reset_states()

def go_to_last_page():
    # print(f"The name of this function is {inspect.currentframe().f_code.co_name}")
    C.page_number = C.LAST_PAGE
    reset_states()

def handle_button_click(pos, test_block_index, action):
    """ Handle button click actions for copy, reset, and submit """
    # print(f"The name of this function is {inspect.currentframe().f_code.co_name}")
    _, test_matrices_by_page = load_all_test_blocks()
    pre_matrix, post_matrix = test_matrices_by_page[C.page_number - 1][test_block_index]

    if action == C.COPY_ACTION:
        for i in range(len(pre_matrix)):
            for j in range(len(pre_matrix[i])):
                post_matrix[i][j] = pre_matrix[i][j]
        C.status_message = ""
    elif action == C.RESET_ACTION:
        for i in range(len(post_matrix)):
            for j in range(len(post_matrix[i])):
                post_matrix[i][j] = 0
        C.status_message = ""
    elif action == C.SUBMIT_ACTION:
        C.status_message = f"Submitted Page: {C.page_number}, Block: {test_block_index + 1}"

