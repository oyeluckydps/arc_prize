from llm.pattern_extraction.pattern_description_signature import *

def identify_patterns(question: str, matrices: Dict[str, List[List[int]]]) -> PatternList:
    """
    Identifies patterns in matrices based on the given question.

    Args:
        question (str): The question describing the matrices and pattern identification task.

    Returns:
        PatternList: A list of identified patterns.
    """
    # Initialize Claude model
    claude = dspy.Claude("claude-3-5-sonnet-20240620", api_key=os.environ.get('ANTHROPIC_API_KEY'))
    dspy.settings.configure(lm=claude)

    # Create a predictor using the PatternSignature
    predictor = dspy.TypedPredictor(DetailedPatternDescriptionSignature)

    # Predict patterns based on the question
    solution = predictor(question=question, matrices=matrices)

    return solution.patterns_description

def main():
    """
    Main function to demonstrate pattern identification.
    """
    # Sample question describing the matrices and pattern identification task
    sample_question = DetailedPatternDescriptionSignature.sample_prompt()

    sample_matrices = {
        "Matrix 2": Matrix(matrix=
                    [
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [8, 8, 8, 0, 0, 0, 0, 0, 0, 0],
                    [8, 8, 8, 0, 0, 0, 0, 0, 0, 0],
                    [8, 8, 8, 0, 7, 7, 0, 2, 2, 2],
                    [8, 8, 8, 0, 7, 7, 0, 2, 2, 2]
                    ]),
        "Matrix 1": Matrix(matrix=
                    [ [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 4],
                      [1, 1, 0, 0, 0, 0, 0, 0, 0, 4],
                      [1, 1, 0, 2, 2, 0, 3, 3, 0, 4],
                      [1, 1, 0, 2, 2, 0, 3, 3, 0, 4]]
                    )
    }

    # Identify patterns
    patterns = identify_patterns(sample_question, sample_matrices)

    # Print identified patterns
    for pattern in patterns.list_of_patterns:
        print(f"Pattern: {pattern.name}")
        print(f"Location: {pattern.location}")
        print(f"Prominent reason: {pattern.prominent_reason}")
        print(f"Unique identifier: {pattern.unique_identifier}")
        print("---")

if __name__ == "__main__":
    main()