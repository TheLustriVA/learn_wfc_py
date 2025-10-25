# ──  my_pygame_app.py  ────────────────────────────────────────────────
#   A minimal Pygame demo with a 1080p window and a “File → Quit” menu.
#   Python 3.12   –   Pygame 2.1 (or any recent 2.x release)
#
#   Installation:
#       pip install pygame
#   Run:
#       python my_pygame_app.py
# ────────────────────────────────────────────────────────────────────────

import pygame
import sys

# ----------------------------------------------------------------------
#  Configuration
# ----------------------------------------------------------------------
SCREEN_WIDTH   = 1920            # window width  (1080p width)
SCREEN_HEIGHT  = 1080            # window height (1080p height)
FPS           = 60              # frames per second
MENU_HEIGHT   = 30              # height of the menu bar
BUTTON_WIDTH  = 80              # width of the “Quit” button
BUTTON_HEIGHT = 30              # height of the “Quit” button

# ----------------------------------------------------------------------
#  Initialise Pygame & Create Window
# ----------------------------------------------------------------------
pygame.init()
pygame.display.set_caption('Pygame 1080p demo')
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# ----------------------------------------------------------------------
#  Font & Colours
# ----------------------------------------------------------------------
FONT = pygame.font.SysFont('Arial', 20)
COL_MENU_BG   = (50, 50, 50)   # dark‑grey menu bar
COL_BUTTON_BG = (100, 100, 200)  # blue‑ish button
COL_TEXT      = (255, 255, 255)  # white text

# ----------------------------------------------------------------------
#  Define simple menu objects
# ----------------------------------------------------------------------
# Menu bar rectangle
menu_rect = pygame.Rect(0, 0, SCREEN_WIDTH, MENU_HEIGHT)

# “Quit” button rectangle – placed a little inside the menu bar
quit_button_rect = pygame.Rect(
    SCREEN_WIDTH - BUTTON_WIDTH - 10,   # 10 px right padding
    0,                                 # y‑coordinate (top of the window)
    BUTTON_WIDTH,
    BUTTON_HEIGHT)

# ----------------------------------------------------------------------
#  Helper: draw the menu bar & quit button
# ----------------------------------------------------------------------
def draw_menu():
    """Draws the menu bar and the Quit button."""
    # 1. Menu bar background
    pygame.draw.rect(screen, COL_MENU_BG, menu_rect)

    # 2. “Quit” button background
    pygame.draw.rect(screen, COL_BUTTON_BG, quit_button_rect)

    # 3. Render the “Quit” text
    quit_text_surf = FONT.render('Quit', True, COL_TEXT)
    # Center the text vertically inside the button
    text_rect = quit_text_surf.get_rect()
    text_rect.center = (
        quit_button_rect.centerx,
        quit_button_rect.centery,
    )
    screen.blit(quit_text_surf, text_rect)

# ----------------------------------------------------------------------
#  Main event loop
# ----------------------------------------------------------------------
clock = pygame.time.Clock()
running = True

while running:
    # 1. Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Quit button click
        if event.type == pygame.MOUSEBUTTONDOWN:
            if quit_button_rect.collidepoint(event.pos):
                running = False

    # 2. Draw everything
    screen.fill((30, 30, 30))          # clear screen with a dark background
    draw_menu()

    # 3. Update display & tick the clock
    pygame.display.flip()
    clock.tick(FPS)

# ----------------------------------------------------------------------
#  Gracefully exit
# ----------------------------------------------------------------------
pygame.quit()
sys.exit()
# ────────────────────────────────────────────────────────────────────────────────

