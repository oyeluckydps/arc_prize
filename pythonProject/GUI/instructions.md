var WORKING_FILE = "./actions/"

The WORKING_FILE define the file@function that the agent should work on.
The WORKING_FOLDER defines the folder that the agent should work on.

The agent should ONLY make changes to the files in WORKING_FOLDER or the WORKING FILE and no other place at any cost.

# 1 - INSTRUCTION FOR AGENT

1. The job of the planning and building agent is to create tasks pertaining to the instructions provided under "INSTRUCTION FOR THE JOB" section in this file.
2. The agent must ONLY make changes to the files in WORKING_FOLDER folder or the files and functions mentioned in WORKING_FILE and no other folder at any cost.
3. Always use the best of practices in python for writing the code. Ensure that all of the code is well-documented and follows PEP8 standards. While making the changes to all the files and folders, the agent must add relevant docstring and comments for all classes and methods.
4. Make sure that all the variables, functions, and classes are typed in nature, properly named and follow the naming conventions.
5. Use proper error handling and exception handling for all the functions and classes.
6. After completing the tasks, go through the section 3 i.e CONCLUDING INSTRUCTIONS and make the changes mentioned there.

# 2 - INSTRUCTION FOR THE JOB

1. Add a new button called SNAPSHOT to the bottom of the game screen in the status bar on the right corner.
2. Write a new function in WORKING_FILE that maximizes each train grids one after another and takes a snapshot of only the input grid first and the output grid then. This should happen iteratively for all the train blocks and then the test blocks. After taking the snapshot save the images in the ./snapshots/<working_set>/<page_number>/<test or train>_<index>_<input or output>.jpg file. Create the folder if it doesn't exist. Use the Path library from the pathlib module to create the folder. You might need to calculate the starting x and y coordinates of the grids to take the snapshots.
These formula are used to calculate the block dimensitons of the maximized grids. You may use them to calculate the starting x and y coordinates of the grids to take the snapshots.
        new_width, new_height = int(C.SCREEN_WIDTH * 0.8), int(C.MIDDLE_PLAY_HEIGHT * 0.8)
        block_rect = pygame.Rect((C.SCREEN_WIDTH - new_width) // 2, C.TOP_MENU_HEIGHT + (C.MIDDLE_PLAY_HEIGHT - new_height) // 2, new_width, new_height)
3. Use proper naming conventions for the files and folders. Write proper docstrings and comments for all functions and classes.

# 3 - CONCLUDING INSTRUCTIONS

1. Add comment whereever required. Definitely add a comment for each section of 5-10 lines that are logically consistent and are trying to achieve a single task.
2. update the summary of changes made in the WORKING_FOLDER/SUMMARY.md file.