from .constants import Constants as C
# from randomly_initialize import load_all_test_blocks
from .data_initialize import check_solution
import inspect
import time
import os                                                             
from pathlib import Path   
from .screens import game

import pygame

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

def snapshot():                                                    
    """                                                                   
    Takes a screenshot of the complete game screen and saves it in the ./snapshots/total_page/<working_set>/<page_number>/ folder.                 
    Creates the folder if it doesn't exist.                               
    """                                                                                                                                                                                          
    try:                                                                  
        # Create the folder path                                          
        folder_path = Path(f'./snapshots/total_page/{C.working_set}/{C.page_number}/')            
        folder_path.mkdir(parents=True, exist_ok=True)                    
                                                                            
        # Define the screenshot file path                                 
        screenshot_path = folder_path / f'{time.time()}.png'                  
                                                                            
        # Take the screenshot and save it                                 
        pygame.image.save(C.screen, screenshot_path)                      
                                                                            
        # Update the status message                                       
        C.status_message = f"Screenshot saved to {screenshot_path}"       
    except Exception as e:                                                
        C.status_message = f"Failed to save screenshot: {e}" 

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

from .constants import Constants as C

def snap_all_grids():
    """
    Maximizes each train grid one after another and takes a snapshot of only the input grid first and the output grid then.
    This happens iteratively for all the train blocks and then the test blocks.
    Saves the images in the ./snapshots/<working_set>/<page_number>/<test or train>_<index>_<input or output>.jpg file.
    Creates the folder if it doesn't exist.
    """
    try:
        # Define the folder path
        folder_path = Path(f'./snapshots/{C.working_set}/{C.page_number}/')
        folder_path.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f'Error: {e}')
        raise

    pygame.image.save(C.screen, folder_path/"total_page.jpg") 

    # Function to take a snapshot of a specific grid
    def snapshot_grid(grid, grid_type, index, grid_name):
        new_width, new_height = int(C.SCREEN_WIDTH * 0.8), int(C.MIDDLE_PLAY_HEIGHT * 0.8)
        x_offset = new_width//2 if grid_name == 'output' else 0
        to_capture_width = new_width if grid_name == 'pair' else new_width//2
        block_rect = pygame.Rect((C.SCREEN_WIDTH - new_width) // 2 + x_offset, C.TOP_MENU_HEIGHT + (C.MIDDLE_PLAY_HEIGHT - new_height) // 2, to_capture_width, new_height)
        
        maximize_block((grid_type=="test", C.page_number, index))

        game.draw_middle_play()
        pygame.display.flip()

        snapshot = C.screen.subsurface(block_rect).copy()

        # Define the screenshot file path
        screenshot_path = folder_path / f'{grid_type}_{index}_{grid_name}.jpg'

        # Take the screenshot and save it
        pygame.image.save(snapshot, screenshot_path)

    # Iterate over train blocks
    for index, (pre_matrix, post_matrix) in enumerate(C.train_blocks_mats):
        snapshot_grid(pre_matrix, 'train', index, 'input')
        snapshot_grid(post_matrix, 'train', index, 'output')
        snapshot_grid(post_matrix, 'train', index, 'pair')

    # Iterate over test blocks
    for index, (pre_matrix, post_matrix) in enumerate(C.test_blocks_mats):
        snapshot_grid(pre_matrix, 'test', index, 'input')
        snapshot_grid(post_matrix, 'test', index, 'output')
        snapshot_grid(post_matrix, 'test', index, 'pair')

    # Update the status message
    C.status_message = "Snapshots taken successfully."

    maximize_block(None)

