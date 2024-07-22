from typing import List, Any, get_origin, get_args, Union
from pydantic import BaseModel
from preprocess_sample_json import pp
import types

from pydantic import BaseModel
from typing import Dict, Any


def replace_model_dump_json_recursive(obj: Any) -> Any:
    if isinstance(obj, BaseModel):
        # Monkey patch the model_dump_json method
        obj.__dict__['model_dump_json'] = types.MethodType(model_dump_json, obj)
        obj.__str__ = types.MethodType(model_dump_json, obj)
        obj.__repr_str__ = types.MethodType(model_dump_json, obj)
        # Recursively process all fields of the model
        for field_name, field_value in obj.model_fields.items():
            setattr(obj, field_name, replace_model_dump_json_recursive(getattr(obj, field_name)))
        
        return obj
    elif isinstance(obj, dict):
        return {k: replace_model_dump_json_recursive(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [replace_model_dump_json_recursive(item) for item in obj]
    else:
        return obj


def replace_model_dump_json(self, kwargs: Dict) -> Dict:
    new_kwargs = {}
    for key, value in kwargs.items():
        if key in self.io_signature.input_fields:
            new_kwargs[key] = replace_model_dump_json_recursive(value)
        else:
            new_kwargs[key] = value
    return new_kwargs


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

