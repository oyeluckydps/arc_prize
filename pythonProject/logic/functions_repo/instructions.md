# 1 - INSTRUCTION FOR AGENT

1. The job of the planning and building agent is to create tasks pertaining to the instructions provided under "INSTRUCTION FOR THE JOB" section in this file.
2. The agent must ONLY make changes to the files in this folder and i.e. /logic/functions_repo folder and no other folder at any cost.
3. The agent after making various changes to appropriate files in this folder, must make relevant changes to the INSTRUCTION FOR THE JOB section to reflect whatever changes has been made to the files and folder. Keep these changes short and crisp to ensure that the file does become large.
4. After completing the tasks and making changes to the instructions.md file, go through the section 3 i.e CONCLUDING INSTRUCTIONS and make the changes mentioned there.

# 2 - INSTRUCTION FOR THE JOB

1. Create a new file and add an abstract class named `functionRepo`.
1-A. Provide relevant docstrings and comments for all classes and methods.
2. Create the following classes derived from `functionRepo`: `cell_transformation`, `cell_expansion`, `pattern_contraction`, `pattern_transformation`, `pattern_extraction`, `pattern_expansion`, `group_contraction`, `group_transformation`, `group_extraction`, `group_expansion`.
3. Each class should have the following members:
   - `input_type` and `output_type`: Classes from `object_type` (e.g., `Cell`, `Pattern`, `Grid`, `Constellation`).
   - `method`: A function to be applied on the input type.
   - `description`: A string describing the function.
   - `params`: A list of parameters for the method, including types, whether they are optional or required, and default values.
4. The object of each class is essentially a function (`method`), with other members supporting the method.
5. Descriptions of the classes:
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



