"""
Program: Final Performance Task - Main Menu & Program Launcher (Space Wars)
Date: January 4, 2026
Programmer: Sanjith Diddla

Description:
This file serves as the main entry point for the Space Wars game. It displays
the animated title screen and main menu, allowing the user to start the game,
access the help screen, open the settings menu, or exit the program. This file
is responsible for initializing Pygame, loading user settings, and launching
the appropriate game modules.

Design & Development Notes:
- A centralized main menu was created to improve usability and navigation.
- The program uses modular design by separating gameplay, settings, and help
  into individual files that are launched from this main menu.
- User preferences such as fullscreen mode, music, and FPS display are loaded
  from a JSON file to ensure consistency across all parts of the game.
- Animated background stars are implemented using object-oriented programming
  to enhance visual appeal without affecting gameplay logic.
- A reusable Button class is used to handle mouse interaction, hover effects,
  and menu selection logic.

"""


# Import Statements
import pygame
import random
import sys
import os
import subprocess
import json  # <-- needed for reading settings_data.json


# Get the directory where this script is located
folder = os.path.dirname(os.path.abspath(__file__))


# Configuration
BASE_WIDTH, BASE_HEIGHT = 1280, 720
FPS = 120
NUM_STARS = 400
BACKGROUND_COLOR = (8, 24, 32)
STAR_COLOR = (224, 248, 208)


# Star Class
class Star:
    def __init__(self, width, height):  
        self.x = random.randint(0, width)
        self.y = random.randint(0, height)
        self.speed = random.randint(1, 3)
        self.size = random.randint(1, 4)
        self.alpha = 0  
        self.alpha_increment = random.uniform(1, 3)

    def update(self):
        self.y += self.speed
        if self.y > BASE_HEIGHT:
            self.y = random.randint(-20, 0)
            self.x = random.randint(0, BASE_WIDTH)
            self.speed = random.randint(1, 3)
            self.size = random.randint(1, 4)
            self.alpha = 0
        self.alpha = min(255, self.alpha + self.alpha_increment)

    def draw(self, screen):
        star_surface = pygame.Surface((self.size, self.size))
        star_surface.set_alpha(self.alpha)
        star_surface.fill(STAR_COLOR)
        screen.blit(star_surface, (self.x, self.y))


# Button Class
class Button:
    def __init__(self, text, y_pos):
        self.text = text
        self.width = 220
        self.height = 55
        self.x = BASE_WIDTH // 2 - self.width // 2
        self.y = y_pos
        self.hovered = False
        self.font = pygame.font.Font(os.path.join(folder, "assets", "silkscreen.ttf"), 22)
        
    def draw(self, screen):
        if self.hovered:
            bg_color = (224, 248, 208)
            text_color = (8, 24, 32)
            border_color = (255, 255, 255)
        else:
            bg_color = (40, 56, 64)
            text_color = (224, 248, 208)
            border_color = (224, 248, 208)

        pygame.draw.rect(screen, bg_color, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, border_color, (self.x, self.y, self.width, self.height), 2)
        text_surface = self.font.render(self.text, True, text_color)
        text_rect = text_surface.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        screen.blit(text_surface, text_rect)

    def check_hover(self, mouse_pos):
        self.hovered = self.x <= mouse_pos[0] <= self.x + self.width and self.y <= mouse_pos[1] <= self.y + self.height
        return self.hovered

    def is_clicked(self, mouse_pos, mouse_click):
        return mouse_click and self.hovered


# Title Screen
def title_screen(screen, clock, stars, show_fps):
    buttons = [
        Button("PLAY", 270),
        Button("HELP", 345),
        Button("SETTINGS", 420),
        Button("STORY", 495),  
        Button("EXIT", 570)   
    ]
    title_font = pygame.font.Font(os.path.join(folder, "assets", "upheaval.ttf"), 85)
    subtitle_font = pygame.font.Font(os.path.join(folder, "assets", "silkscreen.ttf"), 28)

    running = True
    while running:
        clock.tick(FPS)
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_click = True

        for star in stars:
            star.update()

        screen.fill(BACKGROUND_COLOR)
        for star in stars:
            star.draw(screen)

        title_text = title_font.render("SPACE WARS", True, (224, 248, 208))
        screen.blit(title_text, title_text.get_rect(center=(BASE_WIDTH // 2, 100)))

        subtitle_text = subtitle_font.render("Fight for Survival", True, (180, 200, 180))
        screen.blit(subtitle_text, subtitle_text.get_rect(center=(BASE_WIDTH // 2, 165)))

        for button in buttons:
            button.check_hover(mouse_pos)
            button.draw(screen)
            if button.is_clicked(mouse_pos, mouse_click):
                pygame.mixer.music.stop()
                pygame.quit()
                if button.text == "PLAY":
                    subprocess.run([sys.executable, os.path.join(folder, "play.py")])
                elif button.text == "HELP":
                    subprocess.run([sys.executable, os.path.join(folder, "help.py")])
                elif button.text == "SETTINGS":
                    subprocess.run([sys.executable, os.path.join(folder, "settings.py")])
                elif button.text == "STORY":   # <-- New condition
                    subprocess.run([sys.executable, os.path.join(folder, "story.py")])
                elif button.text == "EXIT":
                    sys.exit()

        # Show FPS if enabled
        if show_fps:
            fps_font = pygame.font.Font(os.path.join(folder, "assets", "silkscreen.ttf"), 18)
            fps_text = fps_font.render(f"FPS: {int(clock.get_fps())}", True, (224, 248, 208))
            screen.blit(fps_text, (10, 10))

        pygame.display.flip()


# Main Loop
def main(settings):
    # Fullscreen flag
    flags = pygame.SCALED
    if settings.get("fullscreen", False):
        flags |= pygame.FULLSCREEN

    screen = pygame.display.set_mode((BASE_WIDTH, BASE_HEIGHT), flags)
    pygame.display.set_caption("Starship Sprout – Space Wars")

    clock = pygame.time.Clock()
    stars = [Star(BASE_WIDTH, BASE_HEIGHT) for _ in range(NUM_STARS)]

    show_fps = settings.get("show_fps", True)

    title_screen(screen, clock, stars, show_fps)


# Running the Program
if __name__ == "__main__":
    with open(os.path.join(folder, "settings_data.json")) as f:
        settings = json.load(f)

    pygame.init()
    pygame.mixer.init()

    if settings.get("music", True):
        pygame.mixer.music.load(os.path.join(folder, "assets", "mainmenumusic.mp3"))
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

    main(settings)
