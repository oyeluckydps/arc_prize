from ..constants import Constants as C
from ..utils.color import Color as Color
from pathlib import Path
import pygame

DROPDOWN_WIDTH, DROPDOWN_HEIGHT = 400, 40
BUTTON_WIDTH, BUTTON_HEIGHT = 100, 40

def read_elements_from_folder():
    """
    Reads the folders from the specified directory with names
    ending in '_challenges' or '_solutions'.
    """
    folder_path = Path(C.SAMPLE_FOLDER_PATH)
    relevant_folders = [folder.name for folder in folder_path.iterdir() if
               folder.is_dir() and (folder.name.endswith('_challenges'))]
    return relevant_folders

OPTIONS = read_elements_from_folder()

# Variables
dropdown_rect = pygame.Rect((C.SCREEN_WIDTH-DROPDOWN_WIDTH-BUTTON_WIDTH-10)/2, C.SCREEN_HEIGHT/2-50, DROPDOWN_WIDTH,
                            DROPDOWN_HEIGHT)
button_rect = pygame.Rect(dropdown_rect.right + 10, C.SCREEN_HEIGHT/2-50, BUTTON_WIDTH, BUTTON_HEIGHT)

def draw_rounded_rect(surface, rect, color, radius=10):
    pygame.draw.rect(surface, color, rect, border_radius=radius)


def draw_dropdown(rect, options, selected_index, open_):
    # Draw dropdown rectangle
    draw_rounded_rect(C.screen, rect, Color.GRAY if open_ else Color.WHITE, radius=0)
    selected_text = options[selected_index] if selected_index != -1 else "Select an option"
    text_surface = C.font.render(selected_text, True, Color.BLACK)
    C.screen.blit(text_surface, (rect.x + 5, rect.y + 10))

    if open_:
        for idx, option in enumerate(options):
            option_rect = pygame.Rect(rect.x, rect.y + (rect.height * (idx + 1)), rect.width, rect.height)
            draw_rounded_rect(C.screen, option_rect, Color.WHITE, radius=0)
            option_text_surface = C.font.render(option, True, Color.BLACK)
            C.screen.blit(option_text_surface, (option_rect.x + 5, option_rect.y + 10))

def intro_screen():
    dropdown_open = False
    selected_option_index = -1
    while C.scene == "intro":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                C.scene = "EXIT"
                print("EXIT called!")
                break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if dropdown_rect.collidepoint(event.pos):
                    dropdown_open = not dropdown_open
                elif dropdown_open:
                    for idx, option in enumerate(OPTIONS):
                        option_rect = pygame.Rect(dropdown_rect.x, dropdown_rect.y + (dropdown_rect.height * (idx + 1)),
                                                  dropdown_rect.width, dropdown_rect.height)
                        if option_rect.collidepoint(event.pos):
                            selected_option_index = idx
                            dropdown_open = False
                            break
                    else:
                        dropdown_open = False
                elif button_rect.collidepoint(event.pos):
                    if selected_option_index != -1:
                        C.working_set = OPTIONS[selected_option_index]
                        C.set_pages()
                        C.scene = "game"
                        break
                else:
                    dropdown_open = False

        C.screen.fill(Color.LIGHT_GRAY)
        draw_dropdown(dropdown_rect, OPTIONS, selected_option_index, dropdown_open)
        draw_rounded_rect(C.screen, button_rect, Color.RED)
        button_text_surface = C.button_font.render("Load", True, Color.WHITE)
        C.screen.blit(button_text_surface, (button_rect.x + 20, button_rect.y + 10))
        pygame.display.flip()
    return
