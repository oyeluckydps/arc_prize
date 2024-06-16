import numpy as np

def input_based(matrix):
    """
    Segregates patterns/shapes from a given 2D numpy matrix.
    
    Parameters:
    matrix (np.ndarray): A 2D numpy array where 0 represents the background and 
                         numbers 1-9 represent different colors/patterns.
    
    Returns:
    list: A list of patterns, where each pattern is a list of tuples. Each tuple 
          contains the coordinates (x, y) and the color of the cell.
    """
    
    def get_neighbors(x, y):
        """
        Get the valid neighboring cells for a given cell (x, y).
        
        Parameters:
        x (int): The x-coordinate of the cell.
        y (int): The y-coordinate of the cell.
        
        Returns:
        list: A list of tuples representing the coordinates of valid neighboring cells.
        """
        neighbors = [
            (x-1, y-1), (x-1, y), (x-1, y+1),
            (x, y-1),           (x, y+1),
            (x+1, y-1), (x+1, y), (x+1, y+1)
        ]
        # Filter out neighbors that are out of bounds
        return [(i, j) for i, j in neighbors if 0 <= i < matrix.shape[0] and 0 <= j < matrix.shape[1]]

    def dfs(x, y, color, pattern):
        """
        Depth-First Search (DFS) to find all connected cells of the same color.
        
        Parameters:
        x (int): The x-coordinate of the starting cell.
        y (int): The y-coordinate of the starting cell.
        color (int): The color of the pattern to be found.
        pattern (list): The list to store the coordinates and color of the cells in the pattern.
        """
        stack = [(x, y)]
        while stack:
            cx, cy = stack.pop()
            if (cx, cy) not in visited:
                visited.add((cx, cy))
                pattern.append((cx, cy, color))
                for nx, ny in get_neighbors(cx, cy):
                    if matrix[nx, ny] == color and (nx, ny) not in visited:
                        stack.append((nx, ny))

    visited = set()  # Set to keep track of visited cells
    patterns = []    # List to store all the patterns

    # Iterate through each cell in the matrix
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            # If the cell is not background and not visited, start a new pattern
            if matrix[i, j] != 0 and (i, j) not in visited:
                pattern = []
                dfs(i, j, matrix[i, j], pattern)
                patterns.append(pattern)

    return patterns

