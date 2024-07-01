import matplotlib.pyplot as plt
import numpy as np

def create_grid_image(matrix):
    # Define color mapping
    color_map = {
        0: (0, 0, 0),        # Black
        1: (1, 0, 0),        # Red
        2: (0, 1, 0),        # Green
        3: (0, 0, 1),        # Blue
        4: (1, 1, 0),        # Yellow
        5: (1, 0, 1),        # Magenta
        6: (0, 1, 1),        # Cyan
        7: (0.5, 0, 0.5),    # Purple
        8: (1, 0.65, 0),     # Orange
        9: (0, 0.5, 0.5)     # Teal
    }
    
    # Convert matrix to numpy array
    grid = np.array(matrix)
    
    # Create a new figure
    fig, ax = plt.subplots()
    
    # Create the grid
    for (x, y), value in np.ndenumerate(grid):
        color = color_map.get(value, (1, 1, 1))  # Default to white if color not found
        rect = plt.Rectangle([y, x], 1, 1, facecolor=color, edgecolor='white')
        ax.add_patch(rect)
    
    # Set limits and aspect
    ax.set_xlim(0, grid.shape[1])
    ax.set_ylim(grid.shape[0], 0)
    ax.set_aspect('equal')
    
    # Remove axes
    ax.axis('off')
    
    # Add grid dimensions at the top
    plt.title(f"Grid Dimensions: {grid.shape[0]}x{grid.shape[1]}", pad=20)
    
    # Show the plot
    plt.tight_layout()
    plt.show()

# # Example usage:
# matrix = [
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 3, 3, 3, 3, 3, 2, 0, 0, 0],
#     [2, 0, 0, 0, 0, 0, 2, 0, 0, 0],
#     [2, 0, 3, 3, 1, 0, 2, 0, 0, 0],
#     [2, 2, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 3, 3, 3, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# ]

# create_grid_image(matrix)