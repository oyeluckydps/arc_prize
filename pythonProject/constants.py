import pygame
import inspect
class Constants():
    # Constants for the game window dimensions
    SCREEN_WIDTH = 1400
    SCREEN_HEIGHT = 700

    # Constants for dividing the screen
    TOP_MENU_HEIGHT = 50
    BOTTOM_STATUS_HEIGHT = 50
    MIDDLE_PLAY_HEIGHT = SCREEN_HEIGHT - TOP_MENU_HEIGHT - BOTTOM_STATUS_HEIGHT

    # Define actions
    COPY_ACTION = 1
    RESET_ACTION = 2
    SUBMIT_ACTION = 3
    MAXIMIZE_ACTION = 4
    MINIMIZE_ACTION = 5

    # Initialize states
    page_number = 1
    FIRST_PAGE = 1
    LAST_PAGE = 20
    status_message = ""
    selected_color = None
    maximized_block = None
    paint_mode = False
    color_palette_rects = []

    # Global list to track button positions and actions
    test_buttons = []
    max_min_buttons = []
    post_grid_params = []

    # Initialize fonts
    font = pygame.font.Font(None, 36)
    small_font = pygame.font.Font(None, 30)
    very_small_font = pygame.font.Font(None, 18)
    matrix_font = pygame.font.Font(None, 14)
    button_font = pygame.font.Font(None, 28)

    # Button definitions
    ARROW_BUTTON_WIDTH = 50
    ARROW_BUTTON_HEIGHT = 30

    double_left_button = pygame.Rect(10, 10, ARROW_BUTTON_WIDTH, ARROW_BUTTON_HEIGHT)
    left_button = pygame.Rect(70, 10, ARROW_BUTTON_WIDTH, ARROW_BUTTON_HEIGHT)
    right_button = pygame.Rect(280, 10, ARROW_BUTTON_WIDTH, ARROW_BUTTON_HEIGHT)
    double_right_button = pygame.Rect(340, 10, ARROW_BUTTON_WIDTH, ARROW_BUTTON_HEIGHT)

    print("Called!")
    # Set up the game window
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Game Layout Example")

