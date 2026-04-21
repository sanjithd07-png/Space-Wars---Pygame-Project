"""
Program: Final Performance Task - Story / Background (Space Wars)
Date: January 22, 2026
Programmer: Sanjith Diddla

Description:
This program displays the story and background lore for the Space Wars game.
It shows multi-page story slides with background images, gradient text boxes,
and interactive buttons to navigate through the story or return to the main menu.
This lore is designed to connect my game to Torsten's game False Reality.
A similar kind of story presentation is also shown in my game once it is completed
on the victory screen.

Design & Development Notes:
- Each slide has a background image with a gradient box for readable story text.
- The gradient box height and position are dynamically adjusted for each slide.
- Text is split into multiple lines to fit neatly within the gradient box.
- Buttons for MENU, EXIT, PREVIOUS, and NEXT are interactive and have hover effects.
- Sound and fullscreen settings are loaded from a JSON file for consistency with the game.
- Background music plays if enabled in the settings.
- Gradient boxes and text are positioned to avoid overlapping buttons.

References & Learning Resources:
- https://youtu.be/8_HVdxBqJmE was used to create gradient boxes to make text more readable.
- All code was reviewed and adapted to match project requirements.
"""

# Import Statements
import pygame
import sys
import os
import subprocess
import json

# Window and UI settings
WIDTH, HEIGHT = 1280, 720
FPS = 120
TEXT_COLOR = (224, 248, 208)
BG_BTN = (40, 56, 64)
HOVER_BTN = (60, 80, 90)

# Folder paths
folder = os.path.dirname(os.path.abspath(__file__))
assets_folder = os.path.join(folder, "assets")

# Initialize pygame and mixer
pygame.init()
pygame.mixer.init()

# Load settings for sound and fullscreen
def load_settings():
    settings_file = os.path.join(folder, "settings_data.json")
    settings = {"sound": True, "fullscreen": False}
    if os.path.exists(settings_file):
        try:
            with open(settings_file, "r") as f:
                settings.update(json.load(f))
        except:
            pass
    return settings

settings = load_settings()
is_fullscreen = settings.get("fullscreen", False)
sound_on = settings.get("sound", True)

# Create the game window
flags = pygame.SCALED
if is_fullscreen:
    flags |= pygame.FULLSCREEN
screen = pygame.display.set_mode((WIDTH, HEIGHT), flags)
pygame.display.set_caption("Space Wars - Story")
clock = pygame.time.Clock()

# Play background music if enabled
if sound_on:
    try:
        pygame.mixer.music.load(os.path.join(assets_folder, "mainmenumusic.mp3"))
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1)
    except:
        pass

# Load font
def get_font(size):
    return pygame.font.Font(os.path.join(assets_folder, "silkscreen.ttf"), size)

font_story = get_font(28)
font_btn = get_font(14)

# Load background images for story slides
story_images = []
for i in range(1, 5):
    img_path = os.path.join(assets_folder, f"{i}.png")
    img = pygame.image.load(img_path).convert_alpha()
    img = pygame.transform.scale(img, (WIDTH, HEIGHT))
    story_images.append(img)

# Polished story text
story_texts = [
    "Chapter 1 – The AI Uprising\n\n"
    "In the near future, schools became fully automated. AIs designed to help teachers "
    "grew too powerful and challenged the world’s greatest minds.\n"
    "One teacher, Mr. Bawa, refused to surrender, winning each fight but facing rising danger.",

    "Chapter 2 – Earth on the Brink\n\n"
    "After defeating the last AI, Mr. Bawa ended the uprising—but at a cost. "
    "Earth’s environment collapsed, forcing humanity to flee and leaving Mr. Bawa trapped, "
    "sending a faint distress signal into space.",

    "Chapter 3 – The Space Rescue\n\n"
    "Far away, your ship intercepts the signal. Your mission: travel to the now-hostile Earth "
    "and rescue Mr. Bawa. Remnants of AI forces orbit, ready to challenge you.\n"
    "Survive five waves to reach Earth and save the last teacher protecting humanity.",

    "Chapter 4 – The Beginning\n\n"
    "The battle begins in space for the survival of one man and the hope of returning humanity home. "
    "Every enemy defeated brings you closer to Earth, Mr. Bawa, and restoring what was lost."
]

# Define buttons
menu_btn = pygame.Rect(15, 70, 130, 30)
exit_btn = pygame.Rect(15, 115, 130, 30)
prev_btn = pygame.Rect(20, HEIGHT - 50, 150, 35)
next_btn = pygame.Rect(WIDTH - 170, HEIGHT - 50, 150, 35)

# Draw a button with hover effect
def draw_button(rect, text):
    mx, my = pygame.mouse.get_pos()
    color = HOVER_BTN if rect.collidepoint(mx, my) else BG_BTN
    pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, TEXT_COLOR, rect, 1)
    label = font_btn.render(text, True, TEXT_COLOR)
    screen.blit(label, label.get_rect(center=rect.center))

# Render multiline text inside gradient box
def render_multiline(text, x, y, font, color, line_spacing=6, max_width=WIDTH-100):
    lines = []
    words = text.split()
    line = ""
    for word in words:
        test_line = line + word + " "
        if font.size(test_line)[0] > max_width - 20:
            lines.append(line)
            line = word + " "
        else:
            line = test_line
    lines.append(line)

    # Calculate gradient box height based on number of lines
    box_height = len(lines) * (font.get_height() + line_spacing) + 20
    grad_rect = pygame.Surface((max_width, box_height))
    grad_rect.set_alpha(200)  # lighter gradient
    grad_rect.fill((0, 0, 0))
    screen.blit(grad_rect, (x, y))

    # Draw text lines
    y_offset = y + 10
    for line in lines:
        rendered = font.render(line.strip(), True, color)
        screen.blit(rendered, (x + 10, y_offset))
        y_offset += font.get_height() + line_spacing

# Y-position for gradient box per slide
box_positions = [
    HEIGHT - 280,   # Slide 1: bottom buttons
    150,            # Slide 2: below top buttons
    HEIGHT - 280,   # Slide 3: bottom buttons
    HEIGHT - 250    # Slide 4: right above bottom buttons
]

# Main loop
current_page = 0
running = True
while running:
    clock.tick(FPS)
    mx, my = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if menu_btn.collidepoint(mx, my):
                subprocess.Popen([sys.executable, os.path.join(folder, "main.py")])
                pygame.quit()
                sys.exit()
            if exit_btn.collidepoint(mx, my):
                pygame.quit()
                sys.exit()
            if prev_btn.collidepoint(mx, my) and current_page > 0:
                current_page -= 1
            if next_btn.collidepoint(mx, my) and current_page < len(story_images) - 1:
                current_page += 1

    # Draw current slide
    screen.blit(story_images[current_page], (0, 0))

    # Draw buttons
    draw_button(menu_btn, "MENU")
    draw_button(exit_btn, "EXIT")
    if current_page > 0:
        draw_button(prev_btn, "PREVIOUS")
    if current_page < len(story_images) - 1:
        draw_button(next_btn, "NEXT")

    # Draw story text with gradient box in dynamic y-position
    render_multiline(story_texts[current_page], 50, box_positions[current_page], font_story, TEXT_COLOR)

    pygame.display.flip()
