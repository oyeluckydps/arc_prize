from constants import Constants as C
import random
import inspect

def load_all_training_blocks():
    """
    Using closure method to ensure that a new block_matrices is not generated everytime this matrix is called.
    :return: a new block_matrices on first call and same block_matrices on every subsequent call.
    """
    # print(f"The name of this function is {inspect.currentframe().f_code.co_name}")
    if not hasattr(load_all_training_blocks, "TRAINING_BLOCKS_COUNT"):
        load_all_training_blocks.block_matrices = []
        load_all_training_blocks.TRAINING_BLOCKS_COUNT = [random.randint(1, 10) for _ in range(C.LAST_PAGE)]
        for page_blocks in load_all_training_blocks.TRAINING_BLOCKS_COUNT:
            page_matrix = []
            for block in range(page_blocks):
                n = random.randint(2, 30)
                pre_matrix = [[random.randint(0, 9) for _ in range(n)] for _ in range(n)]
                post_matrix = [[random.randint(0, 9) for _ in range(n)] for _ in range(n)]
                page_matrix.append((pre_matrix, post_matrix))
            load_all_training_blocks.block_matrices.append(page_matrix)
    return load_all_training_blocks.TRAINING_BLOCKS_COUNT, load_all_training_blocks.block_matrices

def load_all_test_blocks():
    """
    Using closure method to ensure that a new test_matrices_by_page is not generated everytime this matrix is called.
    :return: a new test_matrices_by_page on first call and same test_matrices_by_page on every subsequent call.
    """
    # print(f"The name of this function is {inspect.currentframe().f_code.co_name}")
    # Generate pre matrices for test blocks and initialize post matrices to 0
    if not hasattr(load_all_test_blocks, "TEST_BLOCKS_COUNT"):
        load_all_test_blocks.test_matrices_by_page = []
        load_all_test_blocks.TEST_BLOCKS_COUNT = [random.randint(1, 2) for _ in range(C.LAST_PAGE)]
        for test_blocks in load_all_test_blocks.TEST_BLOCKS_COUNT:
            page_test_matrices = []
            for _ in range(test_blocks):
                n = random.randint(10, 20)
                pre_matrix = [[random.randint(0, 9) for _ in range(n)] for _ in range(n)]
                post_matrix = [[0 for _ in range(n)] for _ in range(n)]
                page_test_matrices.append((pre_matrix, post_matrix))
            load_all_test_blocks.test_matrices_by_page.append(page_test_matrices)
    return load_all_test_blocks.TEST_BLOCKS_COUNT, load_all_test_blocks.test_matrices_by_page

