# import pygame
# pygame.init()
from .constants import Constants as C
from utils.file_handling import load_json_by_page
import inspect
from pathlib import Path

def load_all_training_blocks(page):
    """
    Using closure method to ensure that a new block_matrices is not generated everytime this matrix is called.
    :return: a new block_matrices on first call and same block_matrices on every subsequent call.
    """
    # print(f"The name of this function is {inspect.currentframe().f_code.co_name}")
    page = page+1
    challenges_folder = Path(C.SAMPLE_FOLDER_PATH)/Path(C.working_set)
    solution_folder_name = C.working_set.split("_")[0] + "_solutions"
    solution_folder = Path(C.SAMPLE_FOLDER_PATH)/Path(solution_folder_name)
    challenges_json = load_json_by_page(challenges_folder, page)
    solution_json = load_json_by_page(solution_folder, page)
    page_matrix = []
    for entry in challenges_json["train"]:
        pre_matrix = entry["input"]
        post_matrix = entry["output"]
        page_matrix.append((pre_matrix, post_matrix))
    return len(page_matrix), page_matrix


def load_all_test_blocks(page):
    """
    Using closure method to ensure that a new test_matrices_by_page is not generated everytime this matrix is called.
    :return: a new test_matrices_by_page on first call and same test_matrices_by_page on every subsequent call.
    """
    # print(f"The name of this function is {inspect.currentframe().f_code.co_name}")
    page = page + 1
    challenges_folder = Path(C.SAMPLE_FOLDER_PATH) / Path(C.working_set)
    solution_folder_name = C.working_set.split("_")[0] + "_solutions"
    solution_folder = Path(C.SAMPLE_FOLDER_PATH) / Path(solution_folder_name)
    challenges_entries = load_json_by_page(challenges_folder, page)["test"]
    if not solution_folder.exists():
        solution_entries = [[[0]] for _ in range(len(challenges_entries))]
    else:
        solution_entries = load_json_by_page(solution_folder, page)
    page_matrix = []
    for pre, post in zip(challenges_entries, solution_entries):
        pre_matrix = pre["input"]
        post_matrix = [[0 for _ in row] for row in post]
        page_matrix.append((pre_matrix, post_matrix))
    return len(page_matrix), page_matrix

def check_solution(page, index, provided_sol):
    """
    Using closure method to ensure that a new test_matrices_by_page is not generated everytime this matrix is called.
    :return: a new test_matrices_by_page on first call and same test_matrices_by_page on every subsequent call.
    """
    # print(f"The name of this function is {inspect.currentframe().f_code.co_name}")
    page = page
    challenges_folder = Path(C.SAMPLE_FOLDER_PATH) / Path(C.working_set)
    solution_folder_name = C.working_set.split("_")[0] + "_solutions"
    solution_folder = Path(C.SAMPLE_FOLDER_PATH) / Path(solution_folder_name)
    if not solution_folder.exists():
        return None
    else:
        solution_entries = load_json_by_page(solution_folder, page)
    actual_sol = solution_entries[index]
    return (actual_sol == provided_sol, actual_sol)


# if __name__ == "__main__":
#     # C.working_set = "evaluation_challenges"
#     # C.working_set = "test_challenges"
#     C.working_set = "training_challenges"
#     num, mats = load_all_training_blocks(page = 35)
#     num_test, mats_test = load_all_test_blocks(page=35)
#     pass