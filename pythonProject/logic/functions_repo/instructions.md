var WORKING_FOLDER = "./pattern_transformation_repo/"

# 1 - INSTRUCTION FOR AGENT

1. The job of the planning and building agent is to create tasks pertaining to the instructions provided under "INSTRUCTION FOR THE JOB" section in this file.
2. The agent must ONLY make changes to the files in WORKING_FOLDER folder and no other folder at any cost.
3. Always use the best of practices in python for writing the code. Ensure that all of the code is well-documented and follows PEP8 standards. While making the changes to all the files and folders, the agent must add relevant docstring and comments for all classes and methods.
4. Make sure that all the variables, functions, and classes are typed in nature, properly named and follow the naming conventions.
5. After completing the tasks, go through the section 3 i.e CONCLUDING INSTRUCTIONS and make the changes mentioned there.

# 2 - INSTRUCTION FOR THE JOB

1. Create an __init__ file in pattern_transformation_repo folder.
2. Create a new file named trim_to_arena and make a function of same name in it. The function should take a pattern as input and return a pattern as output. It should remove all the cells outside the arena from the pattern. The height and width of arena is optionally provided to the function. If the height and width are not provided, the function should import it from module named ENV_PARAMS in logic folder. So, width = ENV_PARAMS.width and height = ENV_PARAMS.height. Any cell in the input pattern that has x or y below 0 or above or equal to width or height should be removed from the pattern. Return the pattern after trimming of these cells.

# 3 - CONCLUDING INSTRUCTIONS

1. Add comment whereever required. Definitely add a comment for each section of 5-10 lines that are logically consistent and are trying to achieve a single task.
2. update the summary of changes made in the WORKING_FOLDER/SUMMARY.md file.

