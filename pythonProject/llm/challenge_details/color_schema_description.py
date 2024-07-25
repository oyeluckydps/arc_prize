from pydantic import BaseModel, Field, ConfigDict
from typing import Dict

class ColorSchemaDescription(BaseModel):
    """
    Describes the color schema used in the ARC challenge.
    """
    model_config = ConfigDict(populate_by_name=True)
    
    explanation: str = Field(..., description="Explanation of the color schema")
    example: Dict[int, str] = Field(..., description="Example of a color schema")

    def __str__(self) -> str:
        return f"""ColorSchemaDescription:
Explanation: {self.explanation}
Example: {self.example}"""

# Sample object
color_schema_description_obj = ColorSchemaDescription(
    explanation="""The color schema in the ARC challenge maps integer values (0-9) to specific colors. This mapping is used to visualize the grids, 
    where each integer in the grid represents a color according to this schema. 
    Understanding this color representation is crucial for identifying patterns and transformations in the puzzles.""",
    example={
        0: "Black",
        1: "Red",
        2: "Green",
        3: "Blue",
        4: "Yellow",
        5: "Magenta",
        6: "Cyan",
        7: "Purple",
        8: "Orange",
        9: "Teal"
    }
)

