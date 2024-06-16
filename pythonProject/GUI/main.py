import pygame
import sys
# Initialize Pygame
pygame.init()

from constants import Constants as C
from screens.game import game_screen
from screens.intro import intro_screen

# Main game loop
if __name__ == "__main__":
    while C.scene != "EXIT":
        print(f"{C.scene=}")
        if C.scene == "intro":
            intro_screen()
        elif C.scene == "game":
            game_screen()
    pygame.quit()
    sys.exit()


