"""
Program: Final Performance Task - Help / Game Manual (Space Wars)
Date: January 17, 2026
Programmer: Sanjith Diddla

Description:
This program implements a multi-page help and instruction screen for the
Space Wars game. It explains the controls, objectives, enemy behavior, and
gameplay tips in a clear and user-friendly format. The help screen is fully
interactive and visually consistent with the main game.

Design & Development Notes:
- A multi-page system was implemented to organize information clearly without
  overwhelming the player with too much text at once.
- I tried to use a scroll bar initially, but it was too complex for the scope of this
  project, so I opted for discrete pages instead.
- Navigation buttons (Next, Previous, Main Menu, Exit) allow the user to move
  through pages intuitively using the mouse.
- The visual style, fonts, colors, and animated star background match the main
  game to maintain a consistent user experience.
- Game settings such as fullscreen mode and FPS display are loaded from a JSON
  file to ensure consistency across all screens.
- The Buttons are created using a class with a cool hover effect.
- An optional FPS counter is included to assist with performance monitoring
  during development and testing and give it a real big game feel.

"""

# Import Statements
import pygame
import random
import sys
import os
import subprocess
import json

# CONFIG
WIDTH, HEIGHT = 1280, 720
FPS = 120
STARS_AMOUNT = 400
BG_COLOR = (8, 24, 32)
STAR_COLOR = (224, 248, 208)
TEXT_COLOR = (224, 248, 208)

# Get the folder path
folder = os.path.dirname(os.path.abspath(__file__))

# Load settings from JSON to stay consistent with the game
def load_settings():
    try:
        path = os.path.join(folder, "settings_data.json")
        with open(path, "r") as f:
            return json.load(f)
    except:
        return {"show_fps": True, "fullscreen": False}

# Star Class
class Star:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.speed = random.randint(1, 3)
        self.size = random.randint(1, 4)

    def move(self):
        self.y += self.speed
        if self.y > HEIGHT:
            self.y, self.x = -20, random.randint(0, WIDTH)

    def draw(self, screen):
        pygame.draw.rect(screen, STAR_COLOR, (self.x, self.y, self.size, self.size))

# Main Help Loop
def run_help():
    pygame.init()
    settings = load_settings()
    
    # Set screen mode
    if settings.get("fullscreen"):
        screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
    else:
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        
    pygame.display.set_caption("Space Wars - Help")
    clock = pygame.time.Clock()

    # Initialize music
    pygame.mixer.init()
    if settings.get("music", True):
        pygame.mixer.music.load(os.path.join(folder, "assets", "mainmenumusic.mp3"))
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)  # loop indefinitely
    else:
        pygame.mixer.music.stop()
    

    # Load Fonts
    title_font = pygame.font.Font(os.path.join(folder, "assets", "upheaval.ttf"), 80)
    ui_font = pygame.font.Font(os.path.join(folder, "assets", "silkscreen.ttf"), 22)
    small_font = pygame.font.Font(os.path.join(folder, "assets", "silkscreen.ttf"), 18)


    # Background Stars
    all_stars = []
    for i in range(STARS_AMOUNT):
        all_stars.append(Star())

    # Button Rectangles (The "Student Way")
    prev_btn = pygame.Rect(WIDTH//2 - 250, HEIGHT - 80, 200, 50)
    next_btn = pygame.Rect(WIDTH//2 + 50, HEIGHT - 80, 200, 50)
    menu_btn = pygame.Rect(30, HEIGHT - 80, 200, 50)
    exit_btn = pygame.Rect(WIDTH - 230, HEIGHT - 80, 200, 50)

    current_page = 0
    running = True

    while running:
        clock.tick(FPS)
        mx, my = pygame.mouse.get_pos()
        click = False

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True

        # Update Stars
        for s in all_stars:
            s.move()

        # Drawing
        screen.fill(BG_COLOR)
        for s in all_stars:
            s.draw(screen)

        # Draw a simple background panel for the text
        panel_rect = pygame.Rect(WIDTH//2 - 500, 120, 1000, 480)
        pygame.draw.rect(screen, (20, 40, 50), panel_rect)
        pygame.draw.rect(screen, STAR_COLOR, panel_rect, 3)

        # Title
        title_txt = title_font.render("GAME MANUAL", True, TEXT_COLOR)
        screen.blit(title_txt, title_txt.get_rect(center=(WIDTH//2, 70)))

        # The Actual Help Text Based on Current Page
        if current_page == 0:
            lines = [
                "HOW TO PLAY:",
                "",
                "- MOVE: USE W, A, S, D OR THE ARROW KEYS",
                "- SHOOT: SPACEBAR OR LEFT MOUSE CLICK",
                "- PAUSE: PRESS THE ESCAPE KEY",
                "",
                "YOUR SHIP HAS 7 HEARTS. IF YOU LOSE THEM ALL,",
                "THE GALAXY IS DOOMED!"
            ]
        elif current_page == 1:
            lines = [
                "THE MISSION:",
                "",
                "- SURVIVE THROUGH 5 WAVES OF INVADERS",
                "- EACH WAVE HAS A UNIQUE BOSS IN THE CENTER",
                "- BOSSES ONLY TAKE DAMAGE ONCE MINIONS ARE GONE",
                "",
                "WATCH OUT! BOSS BULLETS AIM DIRECTLY AT YOU."
            ]
        else:
            lines = [
                "PRO TIPS:",
                "",
                "- YOU CANNOT SPAM BULLETS (1 SECOND COOLDOWN)",
                "- ANY ROW OF MINIONS CAN SHOOT",
                "- MINION BULLETS ARE SLOWER THAN YOURS",
                "- STAY ON THE OPPOSITE SIDE OF ENEMY WHEN THEY ARE ABOUT TO SHOOT",
                "",
                "GO FORTH, PILOT! SAVE THE UNIVERSE!"
            ]

        # Draw each line of text
        y_pos = 160
        for text in lines:
            rendered = ui_font.render(text, True, TEXT_COLOR)
            screen.blit(rendered, (WIDTH//2 - 450, y_pos))
            y_pos += 45

        # Page Indicator
        page_txt = small_font.render(f"PAGE {current_page + 1} / 3", True, (150, 180, 150))
        screen.blit(page_txt, page_txt.get_rect(center=(WIDTH//2, 570)))

        # Draw Buttons
        btn_list = [(prev_btn, "PREVIOUS"), (next_btn, "NEXT"), (menu_btn, "MAIN MENU"), (exit_btn, "EXIT")]
        for rect, label in btn_list:
            # Hover effect
            color = (60, 80, 90) if rect.collidepoint(mx, my) else (40, 56, 64)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, TEXT_COLOR, rect, 2)
            
            txt_surface = ui_font.render(label, True, TEXT_COLOR)
            screen.blit(txt_surface, txt_surface.get_rect(center=rect.center))

        # Button Logic
        if click:
            if next_btn.collidepoint(mx, my):
                current_page = min(2, current_page + 1)
            if prev_btn.collidepoint(mx, my):
                current_page = max(0, current_page - 1)
            if exit_btn.collidepoint(mx, my):
                pygame.quit(); sys.exit()
            if menu_btn.collidepoint(mx, my):
                pygame.quit()
                subprocess.run([sys.executable, os.path.join(folder, "main.py")])
                sys.exit()

        # FPS Counter (Consistent with main game)
        if settings.get("show_fps"):
            fps_t = small_font.render(f"FPS: {int(clock.get_fps())}", True, TEXT_COLOR)
            screen.blit(fps_t, (10, 10))

        pygame.display.flip()

if __name__ == "__main__":
    run_help()