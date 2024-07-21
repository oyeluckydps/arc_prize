from typing import List
import pydantic
import json
import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from preprocess_sample_json import pp

class BaseModel(pydantic.BaseModel):
    def model_dump_json(self, *args, **kwargs) -> str:
        data = self.model_dump()
        for field_name, field in self.model_fields.items():
            if field.description:
                data[field_name] = {
                    "value": data[field_name],
                    "description": field.description
                }
        model_dump = pp.pformat(data)
        model_dump = model_dump.replace("\'", "\"")
        return model_dump


class SamplePydanticModel(BaseModel):
    """
    A sample pydantic model to test the model_dump_json method. Here we implement a class to store and represent a sequence of numbers.
    """
    model_config = pydantic.ConfigDict(populate_by_name=True)
    
    name: str = pydantic.Field(..., description="Give a suitable name to this sequence of numbers.")
    matrix: List[List[int]] = pydantic.Field(..., description="Mention the first few numbers of the sequence.")


if __name__ == "__main__":
    nat_num_seq_dict  = {'name': 'Natural Numbers', 'matrix': [[1, 2], [3, 4], [5, 6], [7, 8], [9, 10]]}
    nat_num_seq = SamplePydanticModel(**nat_num_seq_dict)
    as_json = nat_num_seq.model_dump_json()
    print(as_json)
    json.loads(as_json)
    pass