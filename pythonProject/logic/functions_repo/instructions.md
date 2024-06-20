# 1 - INSTRUCTION FOR AGENT

1. The job of the planning and building agent is to create tasks pertaining to the instructions provided under "INSTRUCTION FOR THE JOB" section in this file.
2. The agent must ONLY make changes to the files in this folder and i.e. /logic/functions_repo folder and no other folder at any cost.
3. Always use the best of practices in python for writing the code. Ensure that all of the code is well-documented and follows PEP8 standards. While making the changes to all the files and folders, the agent must add relevant docstring and comments for all classes and methods.
4. Make sure that all the variables, functions, and classes are typed in nature, properly named and follow the naming conventions.
4. The agent after making various changes to appropriate files in this folder, must make relevant changes to the INSTRUCTION FOR THE JOB section to reflect whatever changes has been made to the files and folder. Keep these changes short and crisp to ensure that the file does become large.
5. After completing the tasks and making changes to the instructions.md file, go through the section 3 i.e CONCLUDING INSTRUCTIONS and make the changes mentioned there.

# 2 - INSTRUCTION FOR THE JOB

1. Create a new file `function_repo.py` and add an abstract class named `functionRepo`.
2. Create the following classes derived from `functionRepo` in separate files:
   - `cell_transformation.py`: `cellTransformation`
   - `cell_expansion.py`: `cellExpansion`
   - `pattern_contraction.py`: `patternContraction`
   - `pattern_transformation.py`: `patternTransformation`
   - `pattern_extraction.py`: `patternExtraction`
   - `pattern_expansion.py`: `patternExpansion`
   - `group_contraction.py`: `groupContraction`
   - `group_transformation.py`: `groupTransformation`
   - `group_extraction.py`: `groupExtraction`
   - `group_expansion.py`: `groupExpansion`
3. Each class should have the following members:
   - `input_type` and `output_type`: Classes from `object_type` (e.g., `Cell`, `Pattern`, `Grid`, `Constellation`).
   - `method`: A pointer to a function. The method is not a function so do not define it. Initiate it with None if not provided in init.
   - `description`: A string describing the function.
   - `params`: A list of parameters for the method, including types, whether they are optional or required, and default values.
4. The object of each class is essentially a function (`method`), with other members of the class providing the support required by the method.
5. Descriptions of the classes: Do not implement the functions inside the class. The functions are to be attached to the objects of the class and are not a member of the class.
   - `cellTransformation`: `input_type` = `Cell`, `output_type` = `Cell`. Function acts on a single cell and returns a transformed cell (e.g., color change, translation).
   - `cellExpansion`: `input_type` = `Cell`, `output_type` = `Pattern`. Function expands a single cell into a pattern (e.g., construct a square by replicating the cell).
   - `patternContraction`: `input_type` = `Pattern`, `output_type` = `Cell`. Function reduces a pattern to a single cell (e.g., select top-left cell).
   - `patternTransformation`: `input_type` = `Pattern`, `output_type` = `Pattern`. Function transforms one pattern into another (e.g., affine transformations).
   - `patternExtraction`: `input_type` = `Grid`, `output_type` = `List[Pattern]`. Function extracts patterns from a grid. Add an `iter` member to return list members one by one.
   - `patternExpansion`: `input_type` = `Pattern`, `output_type` = `Group`. Function expands a pattern into a group (e.g., replicate and translate pattern).
   - `groupContraction`: `input_type` = `Group`, `output_type` = `Pattern`. Function extracts a pattern from a group (e.g., select most occurring pattern).
   - `groupTransformation`: `input_type` = `Group`, `output_type` = `Group`. Function transforms a group of patterns (e.g., reflect patterns).
   - `groupExtraction`: `input_type` = `Grid`, `output_type` = `List[Group]`. Function extracts groups from a grid (e.g., extract groups of squares).
   - `groupExpansion`: `input_type` = `Group`, `output_type` = `SuperGroup`. Function expands a group into a super group.
6. Import proper classes from ../object_type/ as required. For example when Grid is requried, use from ../object_type/grid import Grid.

# 3 - CONCLUDING INSTRUCTIONS

1. Ensure all files are saved and committed to the repository.
2. Verify that all classes and methods are properly documented.
3. Ensure that all code follows PEP8 standards.
4. Run any necessary tests to ensure the new classes work as expected.
5. Update any relevant documentation to reflect the changes made.

