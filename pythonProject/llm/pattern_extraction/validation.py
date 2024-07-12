from typing import List, Dict, Any, Tuple
from .pattern_description_signature import Matrix
import json

class Validator:
    def validate_decomposition(self, original_grid: Matrix, extracted_patterns: List[Matrix], pattern_descriptions: List[Dict[str, Any]]) -> List[str]:
        failure_reports = []
        
        if not self._are_patterns_in_grid(extracted_patterns, original_grid):
            failure_reports.append(self._generate_pattern_not_present_report(original_grid, extracted_patterns, pattern_descriptions))
        
        if not self._do_patterns_form_grid(extracted_patterns, original_grid):
            failure_reports.append(self._generate_incomplete_grid_report(original_grid, extracted_patterns))
        
        overlapping_patterns = self._are_patterns_non_overlapping(extracted_patterns)
        if overlapping_patterns:
            failure_reports.append(self._generate_overlap_report(original_grid, extracted_patterns, pattern_descriptions, overlapping_patterns))
        
        return failure_reports

    def _are_patterns_in_grid(self, patterns: List[Matrix], grid: Matrix) -> bool:
        return all(self._is_pattern_in_grid(pattern, grid) for pattern in patterns)

    def _is_pattern_in_grid(self, pattern: Matrix, grid: Matrix) -> bool:
        for i in range(len(grid.matrix) - len(pattern.matrix) + 1):
            for j in range(len(grid.matrix[0]) - len(pattern.matrix[0]) + 1):
                if self._match_pattern(pattern, grid, i, j):
                    return True
        return False

    def _match_pattern(self, pattern: Matrix, grid: Matrix, start_i: int, start_j: int) -> bool:
        for i in range(len(pattern.matrix)):
            for j in range(len(pattern.matrix[0])):
                if pattern.matrix[i][j] is not None and pattern.matrix[i][j] != grid.matrix[start_i + i][start_j + j]:
                    return False
        return True

    def _do_patterns_form_grid(self, patterns: List[Matrix], grid: Matrix) -> bool:
        combined_grid = [[None for _ in range(len(grid.matrix[0]))] for _ in range(len(grid.matrix))]
        for pattern in patterns:
            for i in range(len(pattern.matrix)):
                for j in range(len(pattern.matrix[0])):
                    if pattern.matrix[i][j] is not None:
                        if combined_grid[i][j] is None:
                            combined_grid[i][j] = pattern.matrix[i][j]
                        elif combined_grid[i][j] != pattern.matrix[i][j]:
                            return False
        return combined_grid == grid.matrix

    def _are_patterns_non_overlapping(self, patterns: List[Matrix]) -> List[Tuple[int, int]]:
        overlapping_patterns = []
        for i in range(len(patterns)):
            for j in range(i + 1, len(patterns)):
                if self._patterns_overlap(patterns[i], patterns[j]):
                    overlapping_patterns.append((i, j))
        return overlapping_patterns

    def _patterns_overlap(self, pattern1: Matrix, pattern2: Matrix) -> bool:
        for i in range(len(pattern1.matrix)):
            for j in range(len(pattern1.matrix[0])):
                if pattern1.matrix[i][j] is not None and pattern2.matrix[i][j] is not None:
                    return True
        return False

    def _generate_pattern_not_present_report(self, original_grid: Matrix, extracted_patterns: List[Matrix], pattern_descriptions: List[Dict[str, Any]]) -> str:
        return f"Pattern not present in the original grid.\n" \
               f"Pattern description: {json.dumps(pattern_descriptions, indent=2)}\n" \
               f"Extracted patterns: {json.dumps([p.matrix for p in extracted_patterns], indent=2)}\n" \
               f"Original grid: {json.dumps(original_grid.matrix, indent=2)}\n" \
               f"The extracted pattern does not match any part of the original grid."

    def _generate_incomplete_grid_report(self, original_grid: Matrix, extracted_patterns: List[Matrix]) -> str:
        return f"Extracted patterns do not combine to form the complete original grid.\n" \
               f"Original grid: {json.dumps(original_grid.matrix, indent=2)}\n" \
               f"Extracted patterns: {json.dumps([p.matrix for p in extracted_patterns], indent=2)}\n" \
               f"The combination of all extracted patterns does not recreate the original grid exactly."

    def _generate_overlap_report(self, original_grid: Matrix, extracted_patterns: List[Matrix], pattern_descriptions: List[Dict[str, Any]], overlapping_patterns: List[Tuple[int, int]]) -> str:
        overlap_report = f"Extracted patterns are overlapping in the following grid:\n"
        overlap_report += f"Original grid: {json.dumps(original_grid.matrix, indent=2)}\n\n"
        overlap_report += "Overlapping patterns:\n"
        for i, j in overlapping_patterns:
            overlap_report += f"Pattern 1:\n"
            overlap_report += f"Description: {json.dumps(pattern_descriptions[i], indent=2)}\n"
            overlap_report += f"Extracted pattern: {json.dumps(extracted_patterns[i].matrix, indent=2)}\n\n"
            overlap_report += f"Pattern 2:\n"
            overlap_report += f"Description: {json.dumps(pattern_descriptions[j], indent=2)}\n"
            overlap_report += f"Extracted pattern: {json.dumps(extracted_patterns[j].matrix, indent=2)}\n\n"
        overlap_report += "These patterns have non-None values in the same position, indicating overlap."
        return overlap_report