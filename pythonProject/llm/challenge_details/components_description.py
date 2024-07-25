from pydantic import BaseModel, Field, ConfigDict
from .training_set_description import TrainingSetDescription, training_set_description_obj
from .test_set_description import TestSetDescription, test_set_description_obj
from .input_output_pair_description import InputOutputPairDescription, input_output_pair_description_obj
from .input_grid_description import InputGridDescription, input_grid_description_obj
from .output_grid_description import OutputGridDescription, output_grid_description_obj
from .color_schema_description import ColorSchemaDescription, color_schema_description_obj

class ComponentsDescription(BaseModel):
    """
    Describes all components used in the ARC challenge.
    """
    model_config = ConfigDict(populate_by_name=True)

    training_set: TrainingSetDescription = Field(..., description="Description of the training set")
    test_set: TestSetDescription = Field(..., description="Description of the test set")
    input_output_pair: InputOutputPairDescription = Field(..., description="Description of input-output pairs")
    input_grid: InputGridDescription = Field(..., description="Description of input grids")
    output_grid: OutputGridDescription = Field(..., description="Description of output grids")
    color_schema: ColorSchemaDescription = Field(..., description="Description of the color schema")

    def __str__(self) -> str:
        return f"""ComponentsDescription:
        Training Set: {self.training_set}
        Test Set: {self.test_set}
        Input-Output Pair: {self.input_output_pair}
        Input Grid: {self.input_grid}
        Output Grid: {self.output_grid}
        Color Schema: {self.color_schema}"""

# Sample object
components_description_obj = ComponentsDescription(
    training_set=training_set_description_obj,
    test_set=test_set_description_obj,
    input_output_pair=input_output_pair_description_obj,
    input_grid=input_grid_description_obj,
    output_grid=output_grid_description_obj,
    color_schema=color_schema_description_obj
)

