from constants import Constants as C
import inspect

class Color():
    # Define colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (200, 200, 200)
    BLUE = (0, 0, 255)
    LIGHT_GRAY = (240, 240, 240)
    BUTTON_COLOR = (100, 149, 237)  # Cornflower Blue

    # Color palette (9 distinguishable colors + BLACK)
    COLOR_PALETTE = [
        BLACK,  # Black
        (255, 0, 0), (0, 255, 0), (0, 0, 255),  # Red, Green, Blue
        (255, 255, 0), (255, 0, 255), (0, 255, 255),  # Yellow, Magenta, Cyan
        (128, 0, 128), (255, 165, 0), (0, 128, 128),  # Purple, Orange, Teal
    ]

    PALETTE_BLOCK_SIZE = 30  # Size for color palette blocks

    def handle_color_selection(pos):
        # print(f"The name of this function is {inspect.currentframe().f_code.co_name}")
        for index, palette_rect in enumerate(C.color_palette_rects):
            if palette_rect.collidepoint(pos):
                if C.selected_color == index:
                    C.selected_color = None
                    C.paint_mode = False
                else:
                    C.selected_color = index
                    C.paint_mode = True
                break

