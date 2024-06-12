from pathlib import Path
import json
import pprint
from collections import namedtuple
import os

CWD = Path(os.getcwd())

RAW_JSON_DIR = Path("../samples/")
PROCESSED_JSON_DIR = Path("processed_json/")

Problem_Setup_details = namedtuple('ProblemType', ['name'])

TRAINING = Problem_Setup_details(name = "training")
TEST = Problem_Setup_details(name = "test")
EVALUATION = Problem_Setup_details(name = "evaluation")

def is_list_of_lists_of_ints(obj):
    if not isinstance(obj, list):
        return False
    is_child_list = [isinstance(sublist, list) for sublist in obj]
    if not all(is_child_list):
        return False
    is_child_of_child_int = [isinstance(item, int) for sublist in obj for item in sublist]
    return all(is_child_of_child_int)

def contains_list_of_lists_of_ints(json_obj):
    if isinstance(json_obj, list):
        if is_list_of_lists_of_ints(json_obj):
            return True
        for item in json_obj:
            if contains_list_of_lists_of_ints(item):
                return True
    elif isinstance(json_obj, dict):
        for value in json_obj.values():
            if contains_list_of_lists_of_ints(value):
                return True
    return False

class SingleLinePrettyPrinter(pprint.PrettyPrinter):
    def _format(self, object, stream, indent, allowance, context, level):
        # super()._format(object, stream, indent, allowance, context, level)
        if is_list_of_lists_of_ints(object):
            # Convert the list to a single line string representation
            stream.write('[')
            for i, item in enumerate(object):
                if i > 0:
                    stream.write(',\n')
                    stream.write(' '*(indent+1))
                # self._format(item, stream, indent, allowance if i == len(object) - 1 else 1, context, level)
                self._format(item, stream, indent, 1, context, level)
            stream.write(']')
        elif contains_list_of_lists_of_ints(object):
            super()._format(object, stream, indent, self._width, context, level)
        else:
            super()._format(object, stream, indent, allowance, context, level)

pp = SingleLinePrettyPrinter(width=180)

def preprocess_samples(problem_name):
    challenges_detail = {
            'raw_file': RAW_JSON_DIR / Path(f"arc-agi_{problem_name.name}_challenges.json"),
            'processed_folder': PROCESSED_JSON_DIR / Path(f"{problem_name.name}_challenges/"),
            'summary_file': PROCESSED_JSON_DIR / Path(f"{problem_name.name}_challenges/000_summary.json")
    }
    solutions_detail = {
        'raw_file': RAW_JSON_DIR / Path(f"arc-agi_{problem_name.name}_solutions.json"),
        'processed_folder': PROCESSED_JSON_DIR / Path(f"{problem_name.name}_solutions/"),
        'summary_file': PROCESSED_JSON_DIR / Path(f"{problem_name.name}_solutions/000_summary.json")
    }
    summary= {
        'Total cases': None,
        'Min Train Count': float('inf'),
        'Max Train Count': float('-inf'),
        'Max Test Count': float('-inf'),
        'Min Train Size': float('inf'),
        'Max Train Size': float('-inf')
    }

    challenges_detail["processed_folder"].mkdir(parents=True, exist_ok=True)
    with open(challenges_detail["raw_file"]) as f:
        all_json = json.load(f)
    summary['Total cases'] = len(all_json)
    for idx, (key, val) in enumerate(all_json.items(), start=1):
        filename = f"{idx:03}_"+key+".json"
        filepath = challenges_detail["processed_folder"]/Path(filename)
        # print(f"Working on {filepath}")
        summary['Min Train Count'] = len(val['train']) if len(val['train']) < summary['Min Train Count'] else \
                                        summary['Min Train Count']
        summary['Max Train Count'] = len(val['train']) if len(val['train']) > summary['Max Train Count'] else \
                                        summary['Max Train Count']
        summary['Max Test Count'] = len(val['test']) if len(val['test']) > summary['Max Test Count'] else \
            summary['Max Test Count']
        grid_sizes = [len(elem['input']) for elem in val['train']]
        summary['Min Train Size'] = min(grid_sizes) if min(grid_sizes) < summary['Min Train Size'] else \
            summary['Min Train Size']
        summary['Max Train Size'] = max(grid_sizes) if max(grid_sizes) > summary['Max Train Size'] else \
            summary['Max Train Size']

        with open(filepath, 'w') as file:
            pp = SingleLinePrettyPrinter(width=180, stream=file)
            pp.pprint(val)
    with open(challenges_detail['summary_file'], 'w') as file:
        pp = SingleLinePrettyPrinter(width=180, stream=file)
        pp.pprint(summary)


    try:
        with open(solutions_detail["raw_file"]) as f:
            all_json = json.load(f)
    except FileNotFoundError:
        print("Solutions not present!")
        return
    summary = {
        'Total cases': None,
        'Max Test Count': float('-inf'),
        'Min Test Size': float('inf'),
        'Max Test Size': float('-inf')
    }
    solutions_detail["processed_folder"].mkdir(parents=True, exist_ok=True)
    summary['Total cases'] = len(all_json)
    for idx, (key, val) in enumerate(all_json.items(), start=1):
        filename = f"{idx:03}_" + key + ".json"
        filepath = solutions_detail["processed_folder"] / Path(filename)
        # print(f"Working on {filepath}")
        summary['Max Test Count'] = len(val) if len(val) > summary['Max Test Count'] else \
            summary['Max Test Count']
        grid_sizes = [len(elem) for elem in val]
        summary['Min Test Size'] = min(grid_sizes) if min(grid_sizes) < summary['Min Test Size'] else \
            summary['Min Test Size']
        summary['Max Test Size'] = max(grid_sizes) if max(grid_sizes) > summary['Max Test Size'] else \
            summary['Max Test Size']
        with open(filepath, 'w') as file:
            pp = SingleLinePrettyPrinter(width=180, stream=file)
            pp.pprint(val)
    with open(solutions_detail['summary_file'], 'w') as file:
        pp = SingleLinePrettyPrinter(width=180, stream=file)
        pp.pprint(summary)



if __name__ == "__main__":
    # with open(test_challenges_file) as f:
    #     training_challenges = json.load(f)
    # pp.pprint(training_challenges)
    preprocess_samples(EVALUATION)
    pass