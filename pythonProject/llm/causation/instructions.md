var WORKING_FILE = ""
var WORKING_FOLDER = "./"

The WORKING_FILE define the file@function that the agent should work on.
The WORKING_FOLDER defines the folder that the agent should work on.

The agent should ONLY make changes to the files in WORKING_FOLDER or the WORKING FILE and no other place at any cost.

# 1 - INSTRUCTION FOR AGENT

1. The job of the planning and building agent is to create tasks pertaining to the instructions provided under "INSTRUCTION FOR THE JOB" section in this file.
2. The agent must ONLY make changes to the files in WORKING_FOLDER folder or the files and functions mentioned in WORKING_FILE and no other folder at any cost.
3. Always use the best of practices in python for writing the code. Ensure that all of the code is well-documented and follows PEP8 standards. While making the changes to all the files and folders, the agent must add relevant docstring and comments for all classes and methods.
4. Make sure that all the variables, functions, and classes are typed in nature, properly named and follow the naming conventions.
5. After completing the tasks, go through the section 3 i.e CONCLUDING INSTRUCTIONS and make the changes mentioned there.

# 2 - INSTRUCTION FOR THE JOB

1. Create a new file in the WORKING_FOLDER folder with the name single_pair_size_color.py. Create a new function in the file that takes one input and one output image and corresponding input and output matrices, train or test case_type, index, and chat_session/oracle as in ../input_chat.py. Your job is to call the oracle functions sequenctially similar to that in ../input_chat.py@zero_shot_input_chat for the given tasks.
2. Write detailed prompts telling the oracle to be ready for causation task. The oracle will be sent the input image and matrix first and it needs to find the properties related to the grid like dimensions, color, patterns, repetition, and groups of patterns. Then the oracle will be showed the output image and matrix and it needs to find the properties related to the grid like dimensions, color, patterns, repetition, and groups of patterns. Finally, the oracle needs to tell the causation between the two grids. Tell this to the agent in the first primpt. Also tell the agent if it is a test or train case and mention the index of the case.
3. Then send the input image and matrix to the oracle and ask it to analyze the input grids. Ask the dimensions in the format (HEIGHT, WIDTH) and the color in the format of a set of digits {x, y, ...} where x, y are digits in range [0, 9] and as found in the matrix. So basically any color occuring in the matrix is a valid color and should be included in the color set. Ask the oracke to reply in the following JSON format only: {"dimensions": (HEIGHT, WIDTH), "color": [x, y, ...]}
4. Then send the output image and matrix to the oracle and ask it to analyze the output grids. Ask all the same questions as in the previous step for the output grids. Ask it to generate the dimentions in the format (HEIGHT, WIDTH) and the color in the format of a set of digits {x, y, ...}. Ask the oracke to reply in the following JSON format only: {"dimensions": (HEIGHT, WIDTH), "color": [x, y, ...]}
5. Write a function to extract the dimensions and color from the JSON response.
6. Finally, ask the oracle to tell the causation between the dimensions and colors between the input and the output grid. In this step pass the dimensions and color of the input grid and the output grid to the oracle through prompt so that the agent can detect the causation. Tell the agent that you are sending the dimenstions and color of the input grid and the output grid and ask it to find the caudation.
7. Ask oracle to return the causation it has found int the following JSON format only: {"dimension_function" : <A python function that takes in diemnsions and color of the input and returns the output dimenstions.>, "color_function" : <A python function that takes in diemnsions and color of the input and returns the output colors as set.>, "dimension_causation" : Explain the causation leading to the output dimensions in natural language based on the input dimensions and color., "color_causation" : Explain the causation leading to the output colors in natural language based on the input dimensions and color.}
8. Finally I want you to make a dict of input and output dimensions and color and the causations derived by the oracle and return it.
9. Break the task into multiple small functions and call them as required. You may write the complete task into multiple files and give them relevant names, if required.
10. Create pydantic models for all the JSON schemas and if required create functions to convert the JSON to pydantic models and vice versa.
11. Document all the functions and classes in the file. Write proper docstrings for all the functions and classes. Use typed variables and type hints where possible.


# 3 - CONCLUDING INSTRUCTIONS

1. Add comment whereever required. Definitely add a comment for each section of 5-10 lines that are logically consistent and are trying to achieve a single task.
2. update the summary of changes made in the WORKING_FOLDER/SUMMARY.md file. Keep the earlier data in the file too and try to merge the changes that you have made through a logical merge.