from llm.pattern_extraction.signatures.pattern_extraction_signature import *
import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from GUI.matplotlib.create_grid_image import create_grid_image

def main():
    background = PatternDescription(name='Background',
                                extraction="""1. Search the most prominent color that acts as the background for the matrices. 
                                2. Look for a large area of contiguous cells with that value and extract the matrix.""",
                                matrices=[1, 2],
                                prominent_reason='It covers the majority of the matrix with a consistent value',
                                location='Throughout the matrix, primarily in the upper and middle sections',
                                unique_identifier='Look for a large area of contiguous cells with value 0',
                                common_features=['Value of 0', 'Covers most of the matrix', 'Primarily in upper and middle sections'],
                                varying_features=['Exact shape and size of the background area'])
   
    matrix = Matrix(matrix=[
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 4],
        [1, 1, 0, 0, 0, 0, 0, 0, 0, 4],
        [1, 1, 0, 2, 2, 0, 3, 3, 0, 4],
        [1, 1, 0, 2, 2, 0, 3, 3, 0, 4]
    ])
   
    prompt = PatternExtractionSignature.sample_prompt()
    claude = dspy.Claude("claude-3-5-sonnet-20240620", api_key=os.environ.get('ANTHROPIC_API_KEY'))
    dspy.settings.configure(lm=claude)
    # Create a predictor using the PatternSignature
    predictor = dspy.TypedPredictor(PatternExtractionSignature)
    # Predict patterns based on the question
    solution = predictor(query=prompt, pattern_description=background, matrix=matrix)
    
    for pattern in solution.output_pattern:
        create_grid_image(pattern.matrix)
        print(pattern)
        print("*"*80)

if __name__ == "__main__":
    main()