"""
Program: Final Performance Task - SPACE WARS (Inspired by Space Invaders)
Date: January 17, 2026
Programmer: Sanjith Diddla

Description:
This program is a 2D arcade-style shooter created using Pygame. The game features
a player-controlled spaceship, wave-based enemy encounters, and a final boss
for each wave. Enemies move together as an army, and any minion can shoot.
Difficulty increases each wave through adjusted enemy speed, fire rate, and
boss health. A second wave spawns only after the first wave is fully defeated.

Design & Development Notes:
- A wave-based difficulty system was implemented to make debugging, testing,
  and balancing enemy behavior easier and more organized.
- Enemy army movement logic was inspired by classic Space Invaders-style games,
  where enemies share a direction and reverse together at screen edges.
- Smooth movement is achieved using float-based position tracking.
- Diagonal enemy bullets are used to increase difficulty and target the player
  more dynamically.
- An FPS counter was added to help monitor performance during development.

References & Learning Resources:

- Classes, game structure, and core Pygame concepts were learned from:
  https://youtu.be/dDQyZp3qQI8?si=R9EjsEcZhBR_0KdX  
  This resource helped me understand how to organize a large program using
  classes, how to separate responsibilities (player, enemies, bullets, UI),
  and how to manage the main game loop effectively.

- Pixel-perfect collision detection using masks was learned from:
  https://youtu.be/tJiKYMQJnYg?si=yTIi6eIahdvaTzkf  
  From this tutorial, I learned how Pygame masks work and why they are more
  accurate than rectangle-based collisions. I applied this technique to
  ensure fair and precise hit detection between the player, enemies, and
  projectiles. Without this, collisions would feel off and frustrating.

- AI assistance was used during development to support problem-solving and
  optimization.  
  AI was used to help implement an FPS counter for performance monitoring
  and to assist with the mathematical logic required for diagonal enemy
  bullet movement (calculating direction vectors and normalizing speed).

- The Damage Vignette effect was inspired by:
  https://stackoverflow.com/questions/56333344/how-to-create-a-taken-damage-red-vignette-effect-in-pygame
  I basically took this code and modified it to fit my game's needs. It adds a
  nice visual effect when the player takes damage, enhancing the feedback and gameplay experience.  

"""


# Import Statements
import pygame
import random
import sys
import os
import json
import math
import subprocess # Allows us to open main.py when a button is clicked


# --- CONFIG OF GAME ---
# I put all the important numbers here at the top. 
# This is like a "Control Panel" so I can balance the game difficulty
# without searching through 500 lines of code.

# Player Settings
PLAYER_START_LIVES = 7  # Total hearts the player starts with
PLAYER_SPEED = 6
PLAYER_BULLET_SPEED = -6
PLAYER_SHOOT_DELAY = 500 # Time in milliseconds (1 second) between shots

# WAVE STATS
# I created separate stats for every wave so the game gets 
# progressively harder. Wave 1 is slow, Wave 5 is fast.
# W1 = Wave 1, W2 = Wave 2, W3 = Wave 3, etc.
# M = Minion enemies (the army grid), B = Boss enemy (big center enemy)
# 
# Stats explained:
#   M_SPEED     = Minion horizontal movement speed (pixels per frame)
#   M_B_SPEED   = Minion bullet speed (vertical)
#   M_DELAY     = Minion firing cooldown (milliseconds between shots)
#   B_HEALTH    = Boss hit points (how many player bullets to destroy)
#   B_SPEED     = Boss horizontal patrol speed (pixels per frame) 
#   B_B_SPEED   = Boss bullet speed (vertical, used for diagonal shots)
#   B_LIMIT     = Boss shooting cooldown timer (frames between shots)

# Wave 1 (Easy Start)
W1_M_SPEED = 0.8
W1_M_B_SPEED = 2
W1_M_DELAY = 6000
W1_B_HEALTH = 5
W1_B_SPEED = 1.5
W1_B_B_SPEED = 2
W1_B_LIMIT = 150

# Wave 2
W2_M_SPEED = 1.1
W2_M_B_SPEED = 2.5
W2_M_DELAY = 5000
W2_B_HEALTH = 8
W2_B_SPEED = 2.0
W2_B_B_SPEED = 3
W2_B_LIMIT = 120

# Wave 3
W3_M_SPEED = 1.4
W3_M_B_SPEED = 3.0
W3_M_DELAY = 4500
W3_B_HEALTH = 12
W3_B_SPEED = 2.5
W3_B_B_SPEED = 4
W3_B_LIMIT = 100

# Wave 4
W4_M_SPEED = 1.8
W4_M_B_SPEED = 3.5
W4_M_DELAY = 3500
W4_B_HEALTH = 15 
W4_B_SPEED = 3.0
W4_B_B_SPEED = 5
W4_B_LIMIT = 80

# Wave 5 (Final Boss)
W5_M_SPEED = 2.2
W5_M_B_SPEED = 4.0
W5_M_DELAY = 2500
W5_B_HEALTH = 20 
W5_B_SPEED = 3.5
W5_B_B_SPEED = 6
W5_B_LIMIT = 60

# Window Settings - These are best not to change as this will mess the other .py files
WIDTH = 1280
HEIGHT = 720
FPS_CAP = 120 
STARS_AMOUNT = 400 
BG_COLOR = (8, 24, 32)
STAR_COLOR = (224, 248, 208)
TEXT_COLOR = (224, 248, 208)


# Initializing Pygame and Screen
pygame.init()
pygame.mixer.init() # Start sound engine
folder = os.path.dirname(os.path.abspath(__file__)) 

# Load settings from JSON file if it exists
def load_my_settings():
    try:
        settings_path = os.path.join(folder, "settings_data.json")
        with open(settings_path, "r") as f:
            data = json.load(f)
            return data
    except:
        return {"show_fps": True, "fullscreen": False}

game_settings = load_my_settings()
is_fullscreen = game_settings.get("fullscreen", False)
show_fps_setting = game_settings.get("show_fps", True)

# Set screen mode
if is_fullscreen == True:
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
else:
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Space Wars - Final Project")
clock = pygame.time.Clock()


# Loading Assets
def get_font_silkscreen(size):
    path = os.path.join(folder, "assets", "silkscreen.ttf")
    return pygame.font.Font(path, size)

def get_font_upheaval(size):
    path = os.path.join(folder, "assets", "upheaval.ttf")
    return pygame.font.Font(path, size)

# Try to load sounds. Use volume controls to keep music quiet and SFX loud.
try:
    snd_shoot = pygame.mixer.Sound(os.path.join(folder, "assets", "shootingsound.wav"))
    snd_hit = pygame.mixer.Sound(os.path.join(folder, "assets", "enemyhit.wav"))
    pygame.mixer.music.load(os.path.join(folder, "assets", "mainmenumusic.mp3"))
    
    pygame.mixer.music.set_volume(0.1) # Music is quiet
    snd_shoot.set_volume(0.5)          # Lasers are audible
    snd_hit.set_volume(0.5)            # Impacts are audible
    
    pygame.mixer.music.play(-1) # Loop music
except:
    snd_shoot = snd_hit = None


# CLASSES
class Star:
    # Small squares that fall down the screen to create a space effect
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.speed = random.randint(1, 3)
        self.size = random.randint(1, 4)
    def move(self):
        self.y += self.speed
        if self.y > HEIGHT:
            self.y = -20
            self.x = random.randint(0, WIDTH)
    def draw(self):
        pygame.draw.rect(screen, STAR_COLOR, (self.x, self.y, self.size, self.size))

class Player:
    # The player ship with keyboard controls and mask collision
    def __init__(self, ship_num):
        path = os.path.join(folder, "assets", f"spaceship{ship_num}.png")
        raw_img = pygame.image.load(path)
        self.image = pygame.transform.scale(raw_img, (130, 130))
        self.rect = self.image.get_rect(midbottom=(WIDTH // 2, HEIGHT - 20))
        self.mask = pygame.mask.from_surface(self.image)
    def move(self, keys):
        if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and self.rect.left > 0:
            self.rect.x -= PLAYER_SPEED
        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and self.rect.right < WIDTH:
            self.rect.x += PLAYER_SPEED
        if (keys[pygame.K_w] or keys[pygame.K_UP]) and self.rect.top > HEIGHT * 0.6:
            self.rect.y -= PLAYER_SPEED
        if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and self.rect.bottom < HEIGHT:
            self.rect.y += PLAYER_SPEED
    def draw(self):
        screen.blit(self.image, self.rect)

class Bullet:
    # Tracks projectiles. Uses floats for smooth diagonal travel.
    def __init__(self, x, y, img, dx, dy):
        self.image = img
        self.rect = self.image.get_rect(center=(x, y))
        self.dx = float(dx)
        self.dy = float(dy)
        self.fx = float(self.rect.x) # I used floats here as without them the bullet movement was very choppy.  
        self.fy = float(self.rect.y)
        self.mask = pygame.mask.from_surface(self.image)
    def move(self):
        self.fx += self.dx
        self.fy += self.dy
        self.rect.x = int(self.fx)
        self.rect.y = int(self.fy)
    def draw(self):
        screen.blit(self.image, self.rect)

class Enemy:
    # Handles Boss (centered) and Minions (grid based)
    def __init__(self, x, y, img, hp, speed, is_boss):
        self.image = img
        if is_boss:
            self.rect = self.image.get_rect(center=(x, y))
        else:
            self.rect = self.image.get_rect(topleft=(x, y))
        self.fx = float(self.rect.x)
        self.health = hp
        self.speed = speed
        self.is_boss = is_boss
        self.dir = 1
        self.last_shot = pygame.time.get_ticks() + random.randint(0, 3000)
        self.mask = pygame.mask.from_surface(self.image)
    def move(self, army_direction, can_boss_move):
        if self.is_boss == True and can_boss_move == True:
            self.fx += (self.speed * self.dir)
            self.rect.x = int(self.fx)
            if self.dir == 1 and self.rect.right >= WIDTH - 100:
                self.dir = -1
            elif self.dir == -1 and self.rect.left <= 100:
                self.dir = 1
        elif not self.is_boss:
            self.fx += (self.speed * army_direction)
            self.rect.x = int(self.fx)
    def draw(self):
        screen.blit(self.image, self.rect)


# Win Lore Screens to connect with Torsten's game
def show_win_lore():
    lore_images = []
    for i in range(1, 4):  # WinLore1.png -> WinLore3.png
        img_path = os.path.join(folder, "assets", f"WinLore{i}.png")
        img = pygame.image.load(img_path).convert_alpha()
        img = pygame.transform.scale(img, (WIDTH, HEIGHT))
        lore_images.append(img)

    current_page = 0
    next_btn = pygame.Rect(WIDTH - 150, HEIGHT // 2 - 40, 130, 35)
    prev_btn = pygame.Rect(WIDTH - 150, HEIGHT // 2 + 10, 130, 35)

    while True:
        clock.tick(FPS_CAP)
        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if next_btn.collidepoint(mx, my):
                    if current_page < len(lore_images) - 1:
                        current_page += 1
                    else:
                        # After last lore image, go to victory menu
                        show_end_menu("VICTORY", "You saved the universe!", (0, 255, 0))
                        return
                if prev_btn.collidepoint(mx, my) and current_page > 0:
                    current_page -= 1

        screen.fill(BG_COLOR)
        screen.blit(lore_images[current_page], (0, 0))

        # Draw next/prev buttons
        for rect, text in [(next_btn, "NEXT"), (prev_btn, "PREVIOUS")]:
            color = (60, 80, 90) if rect.collidepoint(mx, my) else (40, 56, 64)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, TEXT_COLOR, rect, 2)
            txt = get_font_silkscreen(20).render(text, True, TEXT_COLOR)
            screen.blit(txt, txt.get_rect(center=rect.center))

        pygame.display.flip()


# MENU SYSTEMS 
def show_end_menu(title, subtitle, color):
    # Full screen menu for Victory or Death
    menu_btn = pygame.Rect(WIDTH//2 - 250, HEIGHT//2 + 100, 200, 50)
    exit_btn = pygame.Rect(WIDTH//2 + 50, HEIGHT//2 + 100, 200, 50)
    while True:
        mx = pygame.mouse.get_pos()[0]
        my = pygame.mouse.get_pos()[1]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if menu_btn.collidepoint(mx, my):
                    pygame.quit()
                    subprocess.run([sys.executable, os.path.join(folder, "main.py")])
                    sys.exit()
                if exit_btn.collidepoint(mx, my):
                    pygame.quit()
                    sys.exit()
        screen.fill(BG_COLOR)
        t1 = get_font_upheaval(100).render(title, True, color)
        t2 = get_font_silkscreen(30).render(subtitle, True, TEXT_COLOR)
        t1_rect = t1.get_rect(center=(WIDTH//2, HEIGHT//2 - 50))
        screen.blit(t1, t1_rect)
        t2_rect = t2.get_rect(center=(WIDTH//2, HEIGHT//2 + 50))
        screen.blit(t2, t2_rect)
        for btn, label in [(menu_btn, "MAIN MENU"), (exit_btn, "EXIT")]:
            if btn.collidepoint(mx, my):
                c = (60, 80, 90)
            else:
                c = (40, 56, 64)
            pygame.draw.rect(screen, c, btn)
            pygame.draw.rect(screen, TEXT_COLOR, btn, 2)
            txt = get_font_silkscreen(20).render(label, True, TEXT_COLOR)
            txt_rect = txt.get_rect(center=btn.center)
            screen.blit(txt, txt_rect)
        pygame.display.flip()

def run_selection_screen(stars_list):
    # Setup ship pick icons
    icons = []
    for i in range(1, 7):
        ship_path = os.path.join(folder, "assets", f"spaceship{i}.png")
        ship_img = pygame.image.load(ship_path)
        scaled_ship = pygame.transform.scale(ship_img, (170, 170))
        icons.append(scaled_ship)
    btns = []
    for i in range(6):
        btn_x = (WIDTH-(3*120+2*40))//2 + (i%3)*160
        btn_y = 200 + (i//3)*160
        btn_rect = pygame.Rect(btn_x, btn_y, 120, 120)
        btns.append(btn_rect)
    while True:
        clock.tick(FPS_CAP)
        mx = pygame.mouse.get_pos()[0]
        my = pygame.mouse.get_pos()[1]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, b in enumerate(btns):
                    if b.collidepoint(mx, my):
                        return i + 1
        screen.fill(BG_COLOR)
        for s in stars_list:
            s.move()
            s.draw()
        t1 = get_font_upheaval(70).render("SELECT SPACESHIP", True, TEXT_COLOR)
        t2 = get_font_silkscreen(24).render("Choose your ship to begin", True, (180, 200, 180))
        t1_rect = t1.get_rect(center=(WIDTH//2, 80))
        screen.blit(t1, t1_rect)
        t2_rect = t2.get_rect(center=(WIDTH//2, 140))
        screen.blit(t2, t2_rect)
        for i, b in enumerate(btns):
            if b.collidepoint(mx, my):
                c = (60, 80, 90)
            else:
                c = (40, 56, 64)
            pygame.draw.rect(screen, c, b)
            pygame.draw.rect(screen, TEXT_COLOR, b, 2)
            icon_rect = icons[i].get_rect(center=b.center)
            screen.blit(icons[i], icon_rect)
        pygame.display.flip()


# Main Game Loop
def start_the_game():
    all_stars = []
    for _ in range(STARS_AMOUNT):
        star = Star()
        all_stars.append(star)
    ship_id = run_selection_screen(all_stars)
    player = Player(ship_id)

    # Load enemy assets
    boss_images = []
    minion_images = []
    for i in range(1, 6):
        if i == 5:
            m_file = f"enemyboss{i}_minion.png"
        else:
            m_file = f"enemyboss{i}_minion.png"
        boss_path = os.path.join(folder, "assets", f"enemyboss{i}.png")
        boss_img = pygame.image.load(boss_path)
        boss_scaled = pygame.transform.scale(boss_img, (120, 120))
        boss_images.append(boss_scaled)
        minion_path = os.path.join(folder, "assets", m_file)
        minion_img = pygame.image.load(minion_path)
        minion_scaled = pygame.transform.scale(minion_img, (80, 80))
        minion_images.append(minion_scaled)

    bullet_img = pygame.image.load(os.path.join(folder, "assets", "shooting.png"))
    ebullet_img = pygame.image.load(os.path.join(folder, "assets", "enemyshooting.png"))
    heart_path = os.path.join(folder, "assets", "heart.png")
    heart_img = pygame.image.load(heart_path)
    heart_pic = pygame.transform.scale(heart_img, (30, 30))

    # Corner Menu Buttons
    side_menu_btn = pygame.Rect(10, 40, 130, 30)
    side_exit_btn = pygame.Rect(10, 80, 130, 30)

    current_wave = 1
    player_lives = PLAYER_START_LIVES
    army_dir = 1
    bullets = []
    enemy_bullets = []
    player_last_shot = 0
    boss_shoot_timer = 0


    # Damage Vignette - Red screen flash when player gets hit
    # Creates a radial gradient from center to edges using alpha transparency.
    # I calculate the maximum radius using Pythagorean theorem (diagonal of screen),
    # then draw concentric circles with increasing transparency.
    # The 0.7 and 0.3 control where the fade starts/ends (AI helped with this formula).
    damage_overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    cx = WIDTH // 2
    cy = HEIGHT // 2
    max_r = int(math.sqrt(cx * cx + cy * cy))
    for r in range(max_r):
        alpha = int(max(0, min(255, (r - 0.7 * max_r) / (0.3 * max_r) * 255)))
        if alpha > 0:
            pygame.draw.circle(damage_overlay, (255, 0, 0, alpha), (cx, cy), r, 1)
    damage_effect = False
    damage_timer = 0
    DAMAGE_DURATION = 20

    # Spawn the current wave's boss and minions using the correct images (idx = zero-based index)
    # boss stats and minion movement speed to increase difficulty.
    # A wave-based system is used to make testing and debugging easier.
    # Creates and returns the boss and a grid of minion enemies for the given wave.
    # 1) Uses the wave number (num) to pick the correct stats (health, speed, etc.)
    #    for that boss and its minions.
    # 2) Builds a single boss Enemy positioned near the top-center of the screen.
    # 3) Builds a 3x5 grid (rows x columns) of minion Enemy objects using a
    #    nested loop so their positions form a tight army.
    # 4) Packs the boss and the full minion list and returns them,
    #    so the main game loop can easily spawn or reset an entire wave at once.
    def spawn_current_wave(num):
        """
    Creates and returns the boss and a grid of minion enemies for the given wave.
    
    How it works:
    1. Uses the wave number to pick the correct stats (health, speed, etc.)
    2. Creates a single boss Enemy positioned near the top-center
    3. Builds a 3x5 grid of minion Enemy objects using nested loops
    4. Returns both the boss and the minion list so the main loop can use them
    
    I designed this function to avoid repeating enemy creation code 
    and make it easy to restart waves or test different difficulties.
    
        """
        idx = num - 1
        if num == 1:
            bh = W1_B_HEALTH
            bs = W1_B_SPEED
            ms = W1_M_SPEED
        elif num == 2:
            bh = W2_B_HEALTH
            bs = W2_B_SPEED
            ms = W2_M_SPEED
        elif num == 3:
            bh = W3_B_HEALTH
            bs = W3_B_SPEED
            ms = W3_M_SPEED
        elif num == 4:
            bh = W4_B_HEALTH
            bs = W4_B_SPEED
            ms = W4_M_SPEED
        else:
            bh = W5_B_HEALTH
            bs = W5_B_SPEED
            ms = W5_M_SPEED
        b_obj = Enemy(WIDTH // 2, 110, boss_images[idx], bh, bs, True)
        m_list = []
        for r in range(3):
            for c in range(5):
                x_pos = (WIDTH - (5 * 120)) // 2 + (c * 120)
                y_pos = 180 + (r * 90)
                minion = Enemy(x_pos, y_pos, minion_images[idx], 1, ms, False)
                m_list.append(minion)
        return b_obj, m_list

    boss, minions = spawn_current_wave(current_wave)

    while True:
        clock.tick(FPS_CAP)
        now = pygame.time.get_ticks()
        mx = pygame.mouse.get_pos()[0]
        my = pygame.mouse.get_pos()[1]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if side_menu_btn.collidepoint(mx, my):
                    pygame.quit()
                    subprocess.run([sys.executable, os.path.join(folder, "main.py")])
                    sys.exit()
                if side_exit_btn.collidepoint(mx, my):
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if now - player_last_shot > PLAYER_SHOOT_DELAY:
                    new_bullet = Bullet(player.rect.centerx, player.rect.top, bullet_img, 0, PLAYER_BULLET_SPEED)
                    bullets.append(new_bullet)
                    player_last_shot = now
                    if snd_shoot:
                        snd_shoot.play()

        player.move(pygame.key.get_pressed())
        for s in all_stars:
            s.move()

        # Stats Checker
        if current_wave == 1:
            b_lim = W1_B_LIMIT
            b_b_spd = W1_B_B_SPEED
            m_del = W1_M_DELAY
            m_b_spd = W1_M_B_SPEED
        elif current_wave == 2:
            b_lim = W2_B_LIMIT
            b_b_spd = W2_B_B_SPEED
            m_del = W2_M_DELAY
            m_b_spd = W2_M_B_SPEED
        elif current_wave == 3:
            b_lim = W3_B_LIMIT
            b_b_spd = W3_B_B_SPEED
            m_del = W3_M_DELAY
            m_b_spd = W3_M_B_SPEED
        elif current_wave == 4:
            b_lim = W4_B_LIMIT
            b_b_spd = W4_B_B_SPEED
            m_del = W4_M_DELAY
            m_b_spd = W4_M_B_SPEED
        else:
            b_lim = W5_B_LIMIT
            b_b_spd = W5_B_B_SPEED
            m_del = W5_M_DELAY
            m_b_spd = W5_M_B_SPEED

        # Boss logic
        if boss:
            m_gone = (len(minions) == 0)
            boss.move(0, m_gone)
            if m_gone:
                boss_shoot_timer += 1
                if boss_shoot_timer > b_lim:
                    # Calculate direction vector from boss to player
                    # This was tricky - I needed bullets to aim at the player
                    # but move at consistent speed regardless of angle.
                    # AI helped me understand vector normalization:
                    # 1. Find dx and dy (direction components)
                    # 2. Calculate distance using Pythagorean theorem  
                    # 3. Divide each component by distance to "normalize"
                    # This makes the bullet travel at exactly b_b_spd pixels/frame
                    # toward the player no matter which direction it goes.
                    dx = player.rect.centerx - boss.rect.centerx
                    dy = player.rect.centery - boss.rect.bottom
                    dist = math.sqrt(dx * dx + dy * dy)
                    boss_bullet = Bullet(boss.rect.centerx, boss.rect.bottom, ebullet_img, (dx / dist) * b_b_spd, (dy / dist) * b_b_spd)
                    enemy_bullets.append(boss_bullet)
                    boss_shoot_timer = 0

        # Army Pivot logic
        if army_dir == 1:
            hit_right_edge = False
            for m in minions:
                if m.rect.right >= WIDTH - 100:
                    hit_right_edge = True
                    break
            if hit_right_edge:
                army_dir = -1
        else:
            hit_left_edge = False
            for m in minions:
                if m.rect.left <= 100:
                    hit_left_edge = True
                    break
            if hit_left_edge:
                army_dir = 1

        for m in minions:
            m.move(army_dir, False)
            if now - m.last_shot > m_del:
                minion_bullet = Bullet(m.rect.centerx, m.rect.bottom, ebullet_img, 0, m_b_spd)
                enemy_bullets.append(minion_bullet)
                m.last_shot = now

        for b in bullets:
            b.move()
        for eb in enemy_bullets:
            eb.move()

        # Collisions
        for b in bullets[:]:
            for m in minions[:]:
                if b.rect.colliderect(m.rect):
                    # Pixel-perfect collision using masks (learned from YouTube tutorial)
                    # Rects are just boxes, but masks check actual pixel overlap
                    # This prevents unfair hits on transparent parts of sprites
                    offset_x = b.rect.x - m.rect.x
                    offset_y = b.rect.y - m.rect.y
                    if m.mask.overlap(b.mask, (offset_x, offset_y)):
                        if snd_hit:
                            snd_hit.play()
                        minions.remove(m)
                        bullets.remove(b)
                        break
            if boss and b.rect.colliderect(boss.rect) and len(minions) == 0:
                offset_x = b.rect.x - boss.rect.x
                offset_y = b.rect.y - boss.rect.y
                if boss.mask.overlap(b.mask, (offset_x, offset_y)):
                    if snd_hit:
                        snd_hit.play()
                    boss.health -= 1
                    bullets.remove(b)
                    if boss.health <= 0:
                        boss = None

        for eb in enemy_bullets[:]:
            if eb.rect.colliderect(player.rect):
                offset_x = eb.rect.x - player.rect.x
                offset_y = eb.rect.y - player.rect.y
                if player.mask.overlap(eb.mask, (offset_x, offset_y)):
                    player_lives -= 1
                    enemy_bullets.remove(eb)
                    damage_effect = True
                    damage_timer = 0
                    if player_lives <= 0:
                        show_end_menu("GAME OVER", "The galaxy has fallen...", (255, 0, 0))
                        start_the_game()

        if boss is None and len(minions) == 0:
            if current_wave < 5:
                current_wave += 1
                player_lives = PLAYER_START_LIVES
                bullets.clear()
                enemy_bullets.clear()
                boss, minions = spawn_current_wave(current_wave)
            else:
                show_win_lore()  
                start_the_game()

        # Drawing
        screen.fill(BG_COLOR)
        for s in all_stars:
            s.draw()
        player.draw()
        if boss:
            boss.draw()
        for m in minions:
            m.draw()
        for b in bullets:
            b.draw()
        for eb in enemy_bullets:
            eb.draw()

        ui_f = get_font_silkscreen(18)
        txt = ui_f.render(f"WAVE {current_wave}   HEALTH:", True, TEXT_COLOR)
        hearts_width = player_lives * 35
        spacing = 20
        total_width = txt.get_width() + spacing + hearts_width
        ux = (WIDTH // 2) - (total_width // 2)
        screen.blit(txt, (ux, 15))
        for i in range(player_lives):
            heart_x = ux + txt.get_width() + spacing + i * 35
            screen.blit(heart_pic, (heart_x, 10))

        if show_fps_setting:
            fps_text = ui_f.render(f"FPS: {int(clock.get_fps())}", True, TEXT_COLOR)
            screen.blit(fps_text, (10, 10))

        for r, label in [(side_menu_btn, "MENU"), (side_exit_btn, "EXIT")]:
            if r.collidepoint(mx, my):
                c = (60, 80, 90)
            else:
                c = (40, 56, 64)
            pygame.draw.rect(screen, c, r)
            pygame.draw.rect(screen, TEXT_COLOR, r, 1)
            btnt = get_font_silkscreen(14).render(label, True, TEXT_COLOR)
            btnt_rect = btnt.get_rect(center=r.center)
            screen.blit(btnt, btnt_rect)

        if damage_effect:
            fade = math.sin((damage_timer / DAMAGE_DURATION) * math.pi)
            temp = damage_overlay.copy()
            temp.set_alpha(int(255 * fade))
            screen.blit(temp, (0, 0))
            damage_timer += 1
            if damage_timer >= DAMAGE_DURATION:
                damage_effect = False

        pygame.display.flip()


# Running the program 
if __name__ == "__main__": 
    start_the_game()

#Debugging purposees to see win screen
#if __name__ == "__main__":
    #pygame.init()
    #screen = pygame.display.set_mode((WIDTH, HEIGHT))
    #show_win_lore()  # Directly jump to the win lore screen
