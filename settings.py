"""
Program: Final Performance Task - Settings Menu 
Date: January 17, 2026
Programmer: Sanjith Diddla

Description:
This program controls the settings screen for the Space Wars game. It allows
the user to toggle sound, fullscreen mode, and the FPS display using an
interactive button-based menu. All settings are saved to and loaded from
a JSON file (settings_data.json) so that user preferences persist between different parts of the game.

Design & Development Notes:
- A separate settings module was created to keep the main game file organized
  and to demonstrate modular program design.
- JSON file handling is used to store and retrieve user preferences, allowing
  changes to remain effective after the program is closed.
- A custom Button class was implemented to handle rendering, hover detection,
  and mouse-click interaction in a reusable way.
- A dynamic starfield background is used to maintain visual consistency with
  the main game while demonstrating animation using object-oriented design.
- Fullscreen mode is applied only when its value changes to prevent unnecessary
  window recreation and performance issues.
- An optional FPS counter is included to assist with performance testing and
  debugging during development.

References & Learning Resources:
- AI assistance was used to help with FPS counter logic, JSON settings handling,
  and overall menu structure optimization. All code was reviewed, understood,
  and adapted to fit the project requirements.
  
"""


# Import Statements
import pygame
import random
import sys
import os
import subprocess
import json


# Get the directory where this script is located
folder = os.path.dirname(os.path.abspath(__file__))
SETTINGS_FILE = os.path.join(folder, "settings_data.json")


# Configuration


BASE_WIDTH, BASE_HEIGHT = 1280, 720
FPS = 120
NUM_STARS = 300
BACKGROUND_COLOR = (8, 24, 32)
STAR_COLOR = (224, 248, 208)


# Load and Save settings
def load_settings():
    with open(SETTINGS_FILE, "r") as f:
        return json.load(f)

def save_settings(settings):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=2)


# Star Class
class Star:
    def __init__(self, width, height):
        self.x = random.randint(0, width)
        self.y = random.randint(0, height)
        self.speed = random.randint(1, 3)
        self.size = random.randint(1, 3)
        self.alpha = 0
        self.alpha_increment = random.uniform(1, 3)

    def update(self):
        self.y += self.speed
        if self.y > BASE_HEIGHT:
            self.y = random.randint(-20, 0)
            self.x = random.randint(0, BASE_WIDTH)
            self.speed = random.randint(1, 3)
            self.size = random.randint(1, 3)
            self.alpha = 0
        self.alpha = min(255, self.alpha + self.alpha_increment)

    def draw(self, screen):
        surf = pygame.Surface((self.size, self.size))
        surf.set_alpha(self.alpha)
        surf.fill(STAR_COLOR)
        screen.blit(surf, (self.x, self.y))


# Button Class
class Button:
    def __init__(self, text, x, y, width=55, height=55):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hovered = False
        self.font = pygame.font.Font(os.path.join(folder, "assets", "silkscreen.ttf"), 20)

    def draw(self, screen):
        bg = (224, 248, 208) if self.hovered else (40, 56, 64)
        tc = (8, 24, 32) if self.hovered else (224, 248, 208)
        bc = (255, 255, 255) if self.hovered else (224, 248, 208)

        pygame.draw.rect(screen, bg, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, bc, (self.x, self.y, self.width, self.height), 2)

        text = self.font.render(self.text, True, tc)
        rect = text.get_rect(center=(self.x + self.width//2, self.y + self.height//2))
        screen.blit(text, rect)

    def check_hover(self, pos):
        self.hovered = self.x <= pos[0] <= self.x+self.width and self.y <= pos[1] <= self.y+self.height

    def is_clicked(self, pos, click):
        return click and self.hovered


# Settings Screen
def settings_screen(screen, clock, stars):
    settings = load_settings()

    # Buttons
    main_menu_btn = Button("MAIN MENU", 30, BASE_HEIGHT - 70, width=180, height=50)
    exit_btn = Button("EXIT", BASE_WIDTH - 210, BASE_HEIGHT - 70, width=180, height=50)

    # Toggle buttons
    sound_btn = Button("ON" if settings.get("music", True) else "OFF", BASE_WIDTH//2 + 90, 160)
    fullscreen_btn = Button("ON" if settings.get("fullscreen", False) else "OFF", BASE_WIDTH//2 + 90, 240)
    fps_btn = Button("ON" if settings.get("show_fps", True) else "OFF", BASE_WIDTH//2 + 90, 320)

    # Fonts
    title_font = pygame.font.Font(os.path.join(folder, "assets", "upheaval.ttf"), 70)
    label_font = pygame.font.Font(os.path.join(folder, "assets", "silkscreen.ttf"), 28)

    # Initialize music
    pygame.mixer.init()
    if settings.get("music", True):
        pygame.mixer.music.load(os.path.join(folder, "assets", "mainmenumusic.mp3"))
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

    # Track last fullscreen state to prevent recreating window every frame
    last_fullscreen = settings.get("fullscreen", False)
    if last_fullscreen:
        screen = pygame.display.set_mode((BASE_WIDTH, BASE_HEIGHT), pygame.SCALED | pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((BASE_WIDTH, BASE_HEIGHT), pygame.SCALED)

    running = True
    while running:
        clock.tick(FPS)
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = False

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                mouse_click = True

        for s in stars:
            s.update()

        # Apply fullscreen only when it changes
        if settings.get("fullscreen", False) != last_fullscreen:
            last_fullscreen = settings["fullscreen"]
            if last_fullscreen:
                screen = pygame.display.set_mode((BASE_WIDTH, BASE_HEIGHT), pygame.SCALED | pygame.FULLSCREEN)
            else:
                screen = pygame.display.set_mode((BASE_WIDTH, BASE_HEIGHT), pygame.SCALED)

        screen.fill(BACKGROUND_COLOR)
        for s in stars:
            s.draw(screen)

        # Title & Labels
        screen.blit(title_font.render("SETTINGS", True, STAR_COLOR), (BASE_WIDTH//2 - 170, 30))
        screen.blit(label_font.render("Sound:", True, STAR_COLOR), (BASE_WIDTH//2 - 140, 170))
        screen.blit(label_font.render("Fullscreen:", True, STAR_COLOR), (BASE_WIDTH//2 - 140, 250))
        screen.blit(label_font.render("Show FPS:", True, STAR_COLOR), (BASE_WIDTH//2 - 140, 330))

        # Update buttons
        for btn in [sound_btn, fullscreen_btn, fps_btn, main_menu_btn, exit_btn]:
            btn.check_hover(mouse_pos)
            btn.draw(screen)

        # Toggle logic
        if sound_btn.is_clicked(mouse_pos, mouse_click):
            settings["music"] = not settings.get("music", True)
            sound_btn.text = "ON" if settings["music"] else "OFF"
            if settings["music"]:
                pygame.mixer.music.load(os.path.join(folder, "assets", "mainmenumusic.mp3"))
                pygame.mixer.music.play(-1)
            else:
                pygame.mixer.music.stop()
            save_settings(settings)

        if fullscreen_btn.is_clicked(mouse_pos, mouse_click):
            settings["fullscreen"] = not settings.get("fullscreen", False)
            fullscreen_btn.text = "ON" if settings["fullscreen"] else "OFF"
            save_settings(settings)

        if fps_btn.is_clicked(mouse_pos, mouse_click):
            settings["show_fps"] = not settings.get("show_fps", True)
            fps_btn.text = "ON" if settings["show_fps"] else "OFF"
            save_settings(settings)

        # Draw FPS counter if enabled
        if settings.get("show_fps", True):
            fps_display = label_font.render(f"FPS: {int(clock.get_fps())}", True, STAR_COLOR)
            screen.blit(fps_display, (10, 10))

        # Main menu and exit buttons
        if main_menu_btn.is_clicked(mouse_pos, mouse_click):
            pygame.quit()
            subprocess.run([sys.executable, os.path.join(folder, "main.py")])
            sys.exit()

        if exit_btn.is_clicked(mouse_pos, mouse_click):
            pygame.quit()
            sys.exit()

        pygame.display.flip()

# Main
def main():
    pygame.init()
    screen = pygame.display.set_mode((BASE_WIDTH, BASE_HEIGHT), pygame.SCALED)
    pygame.display.set_caption("Settings")

    clock = pygame.time.Clock()
    stars = [Star(BASE_WIDTH, BASE_HEIGHT) for _ in range(NUM_STARS)]

    settings_screen(screen, clock, stars)

# Running the program
if __name__ == "__main__":
    main()
