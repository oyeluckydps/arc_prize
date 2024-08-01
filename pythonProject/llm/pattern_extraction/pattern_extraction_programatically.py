import datetime
from typing import List
from custom_types.input_output_pair import InputOutputPair
from custom_types.matrix import Matrix
from ..code_handling.python_code_generation import PythonCodeGenerationClass
from .signatures.pattern_description_signature import PatternDetails
from .signatures.pattern_count_and_description import PatternCountAndDescription, pattern_count_and_description_chat
from .signatures.io_based_pattern_description import IOBasedPatternDescription, io_based_pattern_chat
from ..causation.signatures.probable_causation import ProbableCausation, probable_causation_chat
from ..causation.signatures.causal_input_patterns import RelevantInputPatternMap, CausalInputPatterns, causal_input_patterns_chat
from .signatures.pattern_description_python_code import PatternDescriptionPythonCode, pattern_description_python_code
from ..causation.signatures.mapping_function_python_code import MappingFunctionPythonCode, mapping_function_python_code
from ..challenge_details.challenge_description import ChallengeDescription, challenge_description_obj
from utils.cacher import cached_call
from globals import VERSION

class PatternExtractionProgramatically:
    def __init__(self, training_set: List[InputOutputPair]):
        self.training_set: List[InputOutputPair] = training_set
        self.input_pattern_description: PatternDetails = None
        self.output_pattern_description: PatternDetails = None
        self.relevant_input_patterns_map: List[List[RelevantInputPatternMap]] = []
        self.input_pattern_counts = []
        self.input_pattern_characteristics = []
        self.output_pattern_counts = []
        self.output_pattern_characteristics = []
        self.time = f"{datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}"
        self.log_file = f"logs/pattern_extraction_{self.time}.txt"

    def find_probable_causation(self, page_number: int) -> ProbableCausation:
        probable_causation = cached_call(probable_causation_chat.send_message)\
                            (f"integrated/{VERSION}/{page_number}/probable_causation.pickle", ["causation_description"])
        causation_response = probable_causation(
            challenge_description = challenge_description_obj,
            input_output_pairs = self.training_set,
            question = ProbableCausation.sample_prompt()
        )
        print(causation_response.causation_description)
        self.probable_causation = causation_response.causation_description
        return causation_response.causation_description

    def find_pattern_description(self, page_number: int, grid_type: str) -> PatternDetails:
        if grid_type not in ['input', 'output']:
            raise ValueError(f"Invalid grid type: {grid_type}")

        io_based_pattern = cached_call(io_based_pattern_chat.send_message)\
                        (f"integrated/{VERSION}/{page_number}/pattern_description_{grid_type}.pickle", ["pattern_description"])
        pattern_description_response = io_based_pattern(
            challenge_description = challenge_description_obj,
            question = IOBasedPatternDescription.sample_prompt(grid_type),
            input_ouptut_pairs = self.training_set,
            probable_causation = self.probable_causation,
            FOR_MATRIX_TYPE = grid_type
        )
        print(pattern_description_response.pattern_description)
        
        if grid_type == 'input':
            self.input_pattern_description = pattern_description_response.pattern_description
        else:
            self.output_pattern_description = pattern_description_response.pattern_description
        
        return pattern_description_response.pattern_description

    def count_and_describe_patterns(self, page_number: int, grid_type: str):
        if grid_type not in ['input', 'output']:
            raise ValueError(f"Invalid grid type: {grid_type}")

        pattern_description = self.input_pattern_description if grid_type == 'input' else self.output_pattern_description
        
        for idx, io_pair in enumerate(self.training_set):
            matrix = io_pair.input if grid_type == 'input' else io_pair.output
            
            cache_file = f"integrated/{VERSION}/{page_number}/pattern_count_desc_{grid_type}_{idx}.pickle"
            
            result = cached_call(pattern_count_and_description_chat.send_message)(
                cache_file,
                ["pattern_count", "pattern_characteristics"]
            )(
                challenge_description=challenge_description_obj,
                pattern_description=pattern_description,
                matrix=matrix,
                question=PatternCountAndDescription.sample_prompt()
            )
            
            if grid_type == 'input':
                self.input_pattern_counts.append(result.pattern_count)
                self.input_pattern_characteristics.append(result.pattern_characteristics)
            else:
                self.output_pattern_counts.append(result.pattern_count)
                self.output_pattern_characteristics.append(result.pattern_characteristics)

        print(f"Counted and described pattern characteristics in {grid_type} matrices.")

    def find_python_code(self, page_number: int, grid_type: str):
        if grid_type not in ['input', 'output']:
            raise ValueError(f"Invalid grid type: {grid_type}")

        matrices = [io_pair.input.matrix if grid_type == 'input' else io_pair.output.matrix for io_pair in self.training_set]
        pattern_description = self.input_pattern_description if grid_type == 'input' else self.output_pattern_description
        pattern_counts = self.input_pattern_counts if grid_type == 'input' else self.output_pattern_counts

        def validation_function(index, result, args, kwargs):
            matrix = args[0]
            if len(result) != pattern_counts[index]:
                return f"Expected {pattern_counts[index]} patterns, but got {len(result)}"
            for pattern in result:
                if len(pattern) != len(matrix) or len(pattern[0]) != len(matrix[0]):
                    return "Pattern dimensions do not match input matrix dimensions"
            return True

        code_generator = PythonCodeGenerationClass(
            llm_call_function=pattern_description_python_code.send_message,
            validation_function=validation_function,
            argument_tuples=[(matrix,) for matrix in matrices],
            keyword_argument_dicts=[{} for _ in range(len(matrices))]
        )

        results = code_generator.generate_till_success(
            question=PatternDescriptionPythonCode.sample_prompt(),
            matrices=matrices,
            pattern_description=pattern_description,
            pattern_counts=pattern_counts
        )
        if grid_type == 'input':
            self.input_extraction_python_code = code_generator
        else:
            self.output_extraction_python_code = code_generator
        print(f"Successfully generated and validated Python code for {grid_type} pattern extraction.")
        return results


    def patterns_extractor(self):
        """
        Extract patterns from input and output matrices using the corresponding Python functions.
        """
        self.input_extracted_patterns = self.input_extraction_python_code.execute_code()
        self.output_extracted_patterns = self.output_extraction_python_code.execute_code()
        print("Extracted input and output patterns programmatically.")

    def map_relevant_input_patterns(self, page_number: int):
        self.relevant_input_patterns_map = []

        for io_pair_index, (io_pair, input_patterns, output_patterns) in enumerate(zip(self.training_set, self.input_extracted_patterns, self.output_extracted_patterns)):
            output_pattern_maps = []

            for output_pattern_index, output_pattern in enumerate(output_patterns):
                cache_file = f"integrated/{VERSION}/{page_number}/relevant_input_pattern_map_{io_pair_index}_{output_pattern_index}.pickle"
                
                causal_input_patterns_result = cached_call(causal_input_patterns_chat.send_message)(
                    cache_file,
                    ["relevant_input_pattern_map"]
                )

                result = causal_input_patterns_result(
                    challenge_description=challenge_description_obj,
                    question=CausalInputPatterns.sample_prompt(),
                    probable_causation=self.probable_causation,
                    input_matrix=io_pair.input,
                    output_matrix=io_pair.output,
                    input_patterns=input_patterns,
                    output_pattern=output_pattern
                )

                output_pattern_maps.append(result.relevant_input_pattern_map)

            self.relevant_input_patterns_map.append(output_pattern_maps)

        print("Mapped relevant input patterns to output patterns.")

    # def find_mapping_python_code(self, page_number: int):
    #     def validation_function(index, result, args, kwargs):
    #         input_dict = args[0]
    #         # Basic checks on the result
    #         assert isinstance(result, list), "Output is not a list"
    #         assert all(isinstance(row, list) for row in result), "Output is not a list of lists"
    #         assert all(all(isinstance(item, (int, type(None))) for item in row) for row in result), "Output contains non-int and non-None values"


    #     code_generator = PythonCodeGenerationClass(
    #         llm_call_function=mapping_function_python_code.send_message,
    #         validation_function=validation_function,
    #         argument_tuples=[(relevant_input_pattern_map,) for output_pattern_maps in self.relevant_input_patterns_map for relevant_input_pattern_map in output_pattern_maps],
    #         keyword_argument_dicts=[{} for _ in range(sum(len(maps) for maps in self.relevant_input_patterns_map))]
    #     )

    #     try:
    #         results = code_generator.generate_till_success(
    #             question=MappingFunctionPythonCode.sample_prompt(),
    #             relevant_input_pattern_map=self.relevant_input_patterns_map
    #         )
    #         self.mapping_python_codes = code_generator.generated_code
    #         print("Successfully generated and validated Python code for mapping function.")
    #         return results
    #     except ValueError as e:
    #         print(f"Failed to generate valid code for mapping function: {str(e)}")
    #         return None