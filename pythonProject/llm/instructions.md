var WORKING_FILE = "./pattern_recog.py"
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

1. A custom gemini model is put in the ./connectors/gemini.py file. Instead of using the google.generativeai as genai library, use the connectors/gemini.py file to upload the images and chat with gemini and use the model to generate the output. Replace all the code such that the agent can use the gemini model to generate the output.

# 3 - CONCLUDING INSTRUCTIONS

1. Add comment whereever required. Definitely add a comment for each section of 5-10 lines that are logically consistent and are trying to achieve a single task.
2. update the summary of changes made in the WORKING_FOLDER/SUMMARY.md file. Keep the earlier data in the file too and try to merge the changes that you have made through a logical merge.