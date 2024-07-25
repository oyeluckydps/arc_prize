

## 2

### LLM corrected version of (2). 

Please identify non-overlapping and distinct common patterns or features across the given input matrices. List any unique patterns or exceptions that do not conform to these common patterns. Ensure that the patterns are exhaustive such that if one were to remove the patterns one by one from a matrix, nothing should remain.

Provide your findings in the following JSON format:

    {
    "list_of_patterns": [
        {
        "First pattern identified": {
            "in which input matrices is it found?": [1, 2, ...],
            "What makes it a prominent and outstanding pattern?": "",
            "Where is the pattern to be found?": "",
            "How to uniquely identify this pattern if an input matrix is provided?": "",
            "If the pattern is found across multiple inputs then what features of the pattern are common across these inputs?": [],
            "If the pattern is found across multiple inputs then what features of the pattern vary across these inputs?": []
        }
        },
        {
        "Second pattern identified": {
            "in which input matrices is it found?": [1, 2, ...],
            "What makes it a prominent and outstanding pattern?": "",
            "Where is the pattern to be found?": "",
            "How to uniquely identify this pattern if an input matrix is provided?": "","If the pattern is found across multiple inputs then what features of the pattern are common across these inputs?": [],
            "If the pattern is found across multiple inputs then what features of the pattern vary across these inputs?": []
        }
        }
        // Add more patterns as necessary
    ]
    }

In this list of patterns:

    Focus only on describing the physical patterns or features you observe in the matrices.
    Ensure that the patterns identified are non-overlapping, distinct, and exhaustive such that if one were to remove all identified patterns one by one from any matrix, nothing should remain.

Examples:

    If you see a background across all the input matrices, mention "background" as a single pattern.
    If you see square shapes of different sizes that can be generalized, mention "squares."
    If you observe random patterns at the same location in the matrices, mention "random pattern at the particular corner of matrix."


## 3

### Get JSON object provided the patterns identified in a JSON and the input matrix.

Given the following JSON object containing a list of patterns and an input matrix along with the input matrix index:

>>>> The JSON containing the list of patterns:
>>>>
>>>>

>>>> The input matrix:
>>>>
>>>>


    1. Iterate over the list of patterns to see if a pattern applies to the provided input matrix index.
    2. If a pattern applies, identify the specified pattern within the input matrix and return the matrix with all other entries replaced by a dot (".").
    3. Maintain the original values in the matrix for the pattern and replace all non-pattern entries with dots (".").
    4. If a pattern does not apply to the input matrix index, simply skip to the next pattern.
    5. Finally, in the Combined patterns: overlap all the patterns that you have identifies and create a new matrix with union of all the patterns.
    6. While printing the matrix as list of lists aginst "the identified pattern" and "the combined pattern" make sure you print each interior list on new line as:
    [
        [2, 6],
        [3, 7]
    ]
Please provide your findings in the following JSON format:


    {
    "list_of_patterns": [
        {
            "First pattern identified": {
                "matrix_index": index of the input matrix,
                "the identified pattern": [
                // a matrix with non-adhering patterns replaced with "."
                ]
            }
        },
        {
            "Second pattern identified": {
                "matrix_index": index of the input matrix,
                "the identified pattern": [
                // a matrix with non-adhering patterns replaced with "."
                ]
            }
        }
        // Add more patterns as necessary
        {
            "Combined patterns": {
                "matrix_index": index of the input matrix,
                "the combined pattern": [
            }
        }
    ]
    }


## 4

### A prompt to get the right set of questions to extract pattern

Write a prompt using below mentioned JSON knowledge such that the prompt instructs the LLM to identify the pattern using the properties mentioned in the JSON and returns the pattern extracted from the input matrix that will be provided along with the JSON file. The pattern's digits and position must be preserved and all other entries in the matrix should be replaced with "." when the LLM outputs its result. 

Here is the JSON:
{ "Background": { "in which input matrices is it found?": [1, 2, 3, 4, 5], "What makes it a prominent and outstanding pattern?": "It's the most common element, filling most of the matrix", "Where is the pattern to be found?": "Throughout the entire matrix", "If the pattern is found across multiple inputs then what features of the pattern are common across these inputs?": ["Represented by 0s", "Covers majority of the matrix"], "If the pattern is found across multiple inputs then what features of the pattern vary across these inputs?": ["Exact arrangement of 0s varies"] } }

## 5

### A sample prompt generated from the above query.

Given the following pattern description in JSON format:

>>>> Pattern description in JSON format:
>>>>
>>>>

Your task is to identify this pattern in the input matrix that will be provided. Extract the pattern from the matrix, preserving its digits and positions. Replace all other entries in the matrix with ".".
Present your result as a list of lists, with each inner list on a new line, like this:
[
[0, ".", ".", 0],
[".", 0, 0, "."],
[0, ".", ".", 0]
]

Here's the input matrix:

>>>> Insert input matrix here
>>>>
>>>>

Please process this matrix and output the result showing only the identified Background pattern.

If there are multiple patterns to be found in the matrix that satisfy the description for the pattern then output all of these matrices as a list.

## 6

### Collapse two patterns extracted from the same matrix into a group.

I have a grid with two different patterns. The cells of pattern are denoted by a digit while the cells not belonging to the pattern are denoted by a ".". I will show you two pattern at a time and it is your job to tell me if you think the two patterns belong to a group for their similarity. The similarity might have any basis like color, shape, size position feature or anything else. 

>>>>
>>>> First pattern on a grid:
>>>>

>>>>
>>>> Second pattern on a grid:
>>>>

Note that the two patterns must have something in common that along the lines of "shape, color, size, position" etc.

## 7

### Group the patterns extracted together if they are similar.

Let me provide you fice different patterns that I want you to store:

>>>>
>>>> PATTERN_1_3
>>>> PATTERN_2_3
>>>> PATTERN_3_3
>>>> PATTERN_4_3
>>>> PATTERN_5_3
>>>>

Now I want you to classify these patterns into one or more groups. The patterns in the same group must have some feature in common. These feature may be based on shape, color, size, position" etc. Try to be as rational as possible to group the matrices that look similar into same group. Do not write the whole matrix in the result. Instead, just write the variable name against the group number. Also share your rationale behind forming the groups.


## 8

### Write python code for the identified pattern.

I want you to go through the input matrices: 

>>>>
>>>>INPUT_004_1
>>>>INPUT_004_2
>>>>INPUT_004_3. 
>>>>

Then I want you to write two functions in python for detecting the presence of particular pattern and for extracting the pattern if it is found in a provided input matrix.

Pattern description: 

>>>>
>>>> PATTERN_004_2
>>>>

Make sure that the code is properly formatted, typed, and commented.

It is understood that any patten description will always have some generalization, specification, and constraint based on the features of the pattern assumptions underlying it. I would like you to write the Python code specifying these assumptions in the arguments and the code should either generalize or not if the argument is set or not. Similarly, it should be more specific based on the specification argument. For example: If the pattern is square, then a generalization can its sides being of an arbitrary size. While fixing the size is an specification. Similarly one of the constraints regarding a square can be: The number of rows and columns occupied are equal.

Use this knowledge to write the python code by mentioning the generalizations, specifications, and constraints. If you find any other such feature then mention that too.

Finally write a JSON file in the following format:
{
    pattern_name: ""
    generalizations: [
        {
            "name": "",
            "description": ""
            permissible_values: List of permissible values or range or a python code.
        }
        ... more generalizations
    ],
    specifications: [
        {
            "name": "",
            "description": ""
            permissible_values: List of permissible values or range or a python code.
        }
        ... more specifications
    ],
    constraints: [
        {
            "name": "",
            "description": ""
        }
        ... more constraints
    ]
}

mentioning all the generalizations, specifications, and constraints that are applicable to the pattern.

