var WORKING_FOLDER = "./pattern_extraction_repo/"

# 1 - INSTRUCTION FOR AGENT

1. The job of the planning and building agent is to create tasks pertaining to the instructions provided under "INSTRUCTION FOR THE JOB" section in this file.
2. The agent must ONLY make changes to the files in WORKING_FOLDER folder and no other folder at any cost.
3. Always use the best of practices in python for writing the code. Ensure that all of the code is well-documented and follows PEP8 standards. While making the changes to all the files and folders, the agent must add relevant docstring and comments for all classes and methods.
4. Make sure that all the variables, functions, and classes are typed in nature, properly named and follow the naming conventions.
5. After completing the tasks, go through the section 3 i.e CONCLUDING INSTRUCTIONS and make the changes mentioned there.

# 2 - INSTRUCTION FOR THE JOB

1. Create a new file named chromatic_segregation.py in the pattern_extraction_repo folder. Put a function with the same name in it. The function takes a grid and optionally a color betweeen 0 and 9 as input. Your job is is iterate over cells of grid and pick only those that belong to the input color. Create a pattern by collecting these cells that adhere to a color and return a list having that one pattern. However, if color is not provided, then iterate over all colors from 0 to 9 and create a pattern for each color, then put these patterns in a list and return it.

# 3 - CONCLUDING INSTRUCTIONS


1. update the summary of changes made in the WORKING_FOLDER/SUMMARY.md file.

