import pygame
pygame.init()

from pathlib import Path
import os

from GUI.constants import Constants as C
from GUI.screens.game import draw_top_menu, draw_middle_play, draw_bottom_status
from GUI.actions import snapshot, snap_all_grids
from GUI.utils.color import Color as Color


def get_snapshots(working_set: str, page_number: int) -> None:
    """
    Function to get snapshots of all grids.
    
    Args:
        working_set (str): The working set to be used.
        page_number (int): The page number to be loaded.
    """
    # Set the working set and page number
    C.working_set = working_set
    C.page_number = page_number

    # Initialize Pygame and set up the screen
    C.screen = pygame.display.set_mode((C.SCREEN_WIDTH, C.SCREEN_HEIGHT))

    # Load the game screen
    C.scene = "game"

    # Clear the screen
    C.screen.fill(Color.WHITE)

    # Draw the different areas
    draw_top_menu()
    draw_middle_play()
    draw_bottom_status()

    # Update the display
    pygame.display.flip()

    # Emulate click on SNAPSHOT button
    snapshot()
    snap_all_grids()

    # Quit Pygame
    pygame.quit()
