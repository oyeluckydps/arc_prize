# File: input_output_pair.py

from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from .matrix import Matrix

class InputOutputPair(BaseModel):
    """
    Represents an input-output pair of matrices in the ARC challenge.
    """
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    input: Matrix = Field(..., description="The input matrix")
    output: Matrix = Field(..., description="The output matrix")

    def print(self) -> str:
        return f"""InputOutputPair:
        Input:
        {self.input}
        Output:
        {self.output}"""

    def show(self):
        """
        Displays the input and output matrices side by side.
        """
        from GUI.matplotlib.create_grid_image import create_grid_image
        import matplotlib.pyplot as plt

        fig, (ax1, ax2) = plt.subplots

