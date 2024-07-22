from typing import List, Any, get_origin, get_args, Union
import pydantic
import json
import os, sys

from preprocess_sample_json import pp
from llm.pattern_extraction.utils_pattern_extraction import claude
from llm.connectors.dspy import DSPy

import dspy

class BaseModel(pydantic.BaseModel):

    def model_dump_json(self, *args, **kwargs) -> str:
        def process_field(value: Any, field: Any) -> Any:
            if isinstance(value, BaseModel):
                # This is a nested Pydantic model
                processed_val = process_data(value.model_dump(), value.model_fields)
            elif isinstance(value, list):
                # This is a list, process each item
                processed_val = [process_field(item, None) for item in value]
            elif isinstance(value, dict):
                # This is a dict, process each item
                processed_val = {k: process_field(v, None) for k, v in value.items()}
            else:
                processed_val = value
            if hasattr(field, 'description') and field.description:
                return {
                    "value": processed_val,
                    "description": field.description
                }
            else:
                return processed_val

        def process_data(data: dict, fields: dict) -> dict:
            result = {}
            for field_name, value in data.items():
                if field_name in fields:
                    result[field_name] = process_field(value, fields[field_name])
                else:
                    result[field_name] = value
            return result

        data = self.model_dump()
        processed_data = process_data(data, self.model_fields)
        model_dump = pp.pformat(processed_data)
        model_dump = model_dump.replace("\'", "\"")
        return model_dump

class SamplePydanticModel(pydantic.BaseModel):
        """
        A sample pydantic model to test the model_dump_json method.
        """
        model_config = pydantic.ConfigDict(populate_by_name=True, from_attributes=True)
        
        name: str = pydantic.Field(..., description="Give a suitable name to this matrix.")
        matrix: List[List[int]] = pydantic.Field(..., description="Mention the matrix.")

# The output_class function remains the same
def get_output_class(original_class):
    output_class = original_class
    output_class.__name__ = original_class.__name__+"Output"
    output_class.model_config['io_type'] = "output"
    return output_class

def get_pydantic_class(original_class, io_type):
    assert issubclass(original_class, pydantic.BaseModel)

    new_fields = {}
    for field_name, field_info in original_class.model_fields.items():
        annotation = field_info.annotation
        
        # Handle Optional types
        if get_origin(annotation) is Union:
            args = get_args(annotation)
            if len(args) == 2 and type(None) in args:
                annotation = next(arg for arg in args if arg is not type(None))
        
        if isinstance(annotation, type) and issubclass(annotation, pydantic.BaseModel):
            # Recursively apply get_pydantic_class to nested BaseModel fields
            new_annotation = get_pydantic_class(annotation, io_type)
        else:
            new_annotation = annotation
        
        new_fields[field_name] = (new_annotation, field_info)
    
    # Create a new model with the processed fields
    input_class = pydantic.create_model(
        original_class.__name__+"Input",
        __base__=BaseModel,
        **new_fields
    )
    input_class.model_config['io_type'] = "input"

    output_class = pydantic.create_model(
        original_class.__name__+"Output",
        __base__=pydantic.BaseModel,
        **new_fields
    )
    output_class.model_config['io_type'] = "output"

    if io_type == "input":
        return input_class
    elif io_type == "output":
        return output_class
    else:
        raise ValueError("io_type must be either 'input' or 'output'")


SamplePydanticModelOutput = get_pydantic_class(SamplePydanticModel, 'output')
SamplePydanticModelInput = get_pydantic_class(SamplePydanticModel, 'input')

class SampleSignature(dspy.Signature):
    """
    Defines the input and output fields for the pattern identification task.
    """
    query: str = dspy.InputField()
    input_matrix: SamplePydanticModelInput = dspy.InputField()
    output_matrix: SamplePydanticModelOutput = dspy.OutputField()

sample_DSPy = DSPy(strategy_method='one_shot', system_info='', model=claude, io_signature=SampleSignature)

if __name__ == "__main__":
    mat1_dict  = {'name': 'Matrix', 'matrix': [[1, 2, 3], [3, 4, 5], [5, 6, 7]]}
    mat1 = SamplePydanticModelInput(**mat1_dict)

    mat2_dict  = {'name': 'Matrix', 'matrix': [[1, 2, 4], [3, 4, 8], [5, 6, 12]]}
    mat2 = SamplePydanticModelOutput(**mat2_dict)

    mat1_json = mat1.model_dump_json()
    print("mat1_json = ")
    print(mat1_json)
    print()
    json.loads(mat1_json)

    mat2_json = mat2.model_dump_json()
    print("mat2_json = ")
    print(mat2_json)
    print()
    json.loads(mat2_json)

    response = sample_DSPy.send_message(query="What is the inversion of the provided input matrix?", input_matrix=mat1)
    print(response.output_matrix)
    pass