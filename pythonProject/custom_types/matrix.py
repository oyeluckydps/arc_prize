from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from GUI.matplotlib.create_grid_image import create_grid_image
from preprocess_sample_json import pp

# Define the Pydantic model for matrix
class Matrix(BaseModel):
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)
    matrix: List[List[Optional[int]]] = Field(description="The grid with integers representing colors or None representing absence of anything.")

    def show(self):
        create_grid_image(self.matrix)
    
    def print(self):
        return pp.pformat(self.matrix)
    
    