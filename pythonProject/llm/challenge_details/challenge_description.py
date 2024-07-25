# File: challenge_description.py

from pydantic import BaseModel, Field, ConfigDict
from components_description import ComponentsDescription, components_description_obj
from character_description import CharacterDescription, characters
from typing import List

class ChallengeDescription(BaseModel):
    """
    Describes the overall ARC challenge, including its explanation, components, and characters.
    """
    model_config = ConfigDict(populate_by_name=True)
    
    explanation: str = Field(..., description="Explanation of the ARC challenge")
    components: ComponentsDescription = Field(..., description="Description of all components in the challenge")
    characters: List[CharacterDescription] = Field(..., description="Description of characters involved in the challenge")

    def __str__(self) -> str:
        return f"""ChallengeDescription:
        Explanation: {self.explanation}
        Components: {self.components}
        Characters: {self.characters}"""

# Create an object of the ChallengeDescription class
challenge_description_obj = ChallengeDescription(
    explanation="""This challenge is a part of ARC PRIZE where a computer program would be provided with a challenge that is expected to be very easily solvable by humans 
    due to their visual cognitive abilities but turn out to be significantly difficult for computer programs to solve. These challenges are essentially puzzles. 
    You shall be provided training set consisting of input output pair of grids. It is assumed that there is an underlying transformation rule that would transform 
    the provided input matrix into the corresponding output matrix. As an expert puzzle solver, 
    the job of solver program is to work on the training set where only the input matrix will be provided. Based on the causation and 
    other understanding drawn from the input-output pair of the training set, 
    it is your job to find the most likely output grid corresponding to the input grid in the test set.""",
    components=components_description_obj,
    characters=characters
)

# # Print the object to verify
# print(challenge_description_obj)

