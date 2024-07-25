# File: character_description.py

from pydantic import BaseModel, Field, ConfigDict
from typing import List

class CharacterDescription(BaseModel):
    """
    Describes a character in the ARC challenge, including their name and job description.
    """
    model_config = ConfigDict(populate_by_name=True)
    
    name: str = Field(..., description="Name of the character")
    job_description: str = Field(..., description="Description of the character's job")

    def __str__(self) -> str:
        return f"""CharacterDescription:
Name: {self.name}
Job Description: {self.job_description}"""

# Create CHALLENGER character
challenger = CharacterDescription(
    name="CHALLENGER",
    job_description="""The CHALLENGER is responsible for posing puzzles for the SOLVER to solve. They design and provide the training set and test set for each puzzle. 
    The final answer to the problem is known only to the CHALLENGER and not to the SOLVER. 
    The CHALLENGER's role is to create challenging yet solvable puzzles that test the SOLVER's ability to recognize patterns and apply transformations."""
)

# Create SOLVER character
solver = CharacterDescription(
    name="SOLVER",
    job_description="""The SOLVER's task is to analyze and solve the puzzles posed by the CHALLENGER. 
    They must examine the input-output pairs in the training set to deduce the underlying transformation or causation that leads from the input matrix to the output matrix. 
    The SOLVER is expected to understand this undescribed transformation and apply it to the input matrices of the test set to generate the puzzle's output matrix. 
    This requires pattern recognition, logical reasoning, and the ability to generalize from examples to solve new, unseen problems."""
)

# List of characters
characters: List[CharacterDescription] = [challenger, solver]

# # Print the characters to verify
# for character in characters:
#     print(character)
#     print()

