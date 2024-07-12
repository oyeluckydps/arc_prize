import matplotlib.pyplot as plt
import numpy as np

def create_grid_image(matrix):
    # Define color mapping
    color_map = {
        '0': (0/255, 0/255, 0/255),        # Black
        '1': (255/255, 0/255, 0/255),      # Red
        '2': (0/255, 255/255, 0/255),      # Green
        '3': (0/255, 0/255, 255/255),      # Blue
        '4': (255/255, 255/255, 0/255),    # Yellow
        '5': (255/255, 0/255, 255/255),    # Magenta
        '6': (0/255, 255/255, 255/255),    # Cyan
        '7': (128/255, 0/255, 128/255),    # Purple
        '8': (255/255, 165/255, 0/255),    # Orange
        '9': (0/255, 128/255, 128/255),    # Teal
        '.': (128/255, 128/255, 128/255)   # Grey
    }
   
    # Convert matrix to numpy array
    grid = np.array(matrix)
   
    # Create a new figure
    fig, ax = plt.subplots()
   
    # Create the grid
    for (x, y), value in np.ndenumerate(grid):
        color = color_map.get(str(value), (128/255, 128/255, 128/255))  # Default to grey if color not found
        rect = plt.Rectangle([y, x], 1, 1, facecolor=color, edgecolor='grey')
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
    pass

# # Example usage:
# matrix = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 4],
#                       [1, 1, 0, 0, 0, 0, 0, 0, 0, 4],
#                       [1, 1, 0, 2, 2, 0, 3, 3, 0, 4],
#                       [1, 1, 0, 2, 2, 0, 3, 3, 0, 4]]


# create_grid_image(matrix)