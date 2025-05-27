# Importing libraries
import pygame
import random
import cv2 # OpenCV is used to play a video background
import numpy as np
import os
import sys

pygame.init() # Initialize pygame

# Set screen dimensions and create a window
WIDTH, HEIGHT = 960, 540
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Battle")

# Define some color constants
WHITE = (255, 255, 255)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0) # Added for collectibles
BLUE = (0, 0, 200) # For level complete text

# Ground level (player can't go below this for jumping)
GROUND = HEIGHT - 60

# Frame rate settings
FPS = 60
FONT = pygame.font.SysFont(None, 30)
BIG_FONT = pygame.font.SysFont(None, 50)
clock = pygame.time.Clock()

# Folder where all input files are stored
BASE_PATH = "Input" # Make sure you have this folder with your assets!

# Load background music and set it to loop
pygame.mixer.music.load(os.path.join(BASE_PATH, "space.mp3"))
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.5)

# Load and scale images
player_img = pygame.transform.scale(
    pygame.image.load(os.path.join(BASE_PATH, "player_plane.png")), (40, 90))
enemy_img = pygame.transform.rotate(
    pygame.transform.scale(
        pygame.image.load(os.path.join(BASE_PATH, "enemy_plane.png")), (40, 80)), 180)
boss_img = pygame.transform.scale(
    pygame.image.load(os.path.join(BASE_PATH, "boss_plane.png")), (120, 180))

# Load sound effects
bullet_sound = pygame.mixer.Sound(os.path.join(BASE_PATH, "bulletshot.mp3"))
victory_sound = pygame.mixer.Sound(os.path.join(BASE_PATH, "victory.mp3"))
collect_sound = pygame.mixer.Sound(os.path.join(BASE_PATH, "collect.mp3")) # Make sure you have a collect.mp3
level_up_sound = pygame.mixer.Sound(os.path.join(BASE_PATH, "levelup.mp3")) # New: Level up sound

# Load background video using OpenCV
cap = cv2.VideoCapture(os.path.join(BASE_PATH, "backvd.mp4"))

# Projectile class for both player and enemy bullets
class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, is_enemy=False):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(RED if is_enemy else WHITE)
        self.rect = self.image.get_rect(center=(x, y))
        self.direction = direction
        self.speed = 10

    # Move projectile and destroy it if out of screen bounds
    def update(self):
        self.rect.y += self.speed * self.direction
        if self.rect.bottom < 0 or self.rect.top > HEIGHT:
            self.kill()

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect(midbottom=(WIDTH // 2, GROUND))
        self.lives = 3 # Represents extra lives
        self.max_hits = 3 # Maximum hits before current life is lost
        self.hits_taken = 0 # Hits taken in current life
        self.score = 0
        self.projectiles = pygame.sprite.Group()
        self.shoot_cooldown = 0

        # --- New: Jump variables ---
        self.jump_speed = -12  # Initial upward velocity for jump
        self.gravity = 0.6    # How quickly the player falls
        self.velocity_y = 0   # Current vertical speed
        self.on_ground = True # To prevent multiple jumps in the air

    # Player movements
    def update(self, keys):
        # Horizontal movement
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += 5

        # --- New: Jump logic ---
        # Changed from K_UP to W for jump, assuming common WASD controls. Change to K_UP if preferred.
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.on_ground:
            self.velocity_y = self.jump_speed
            self.on_ground = False

        # Apply gravity
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

        # Prevent falling below ground level
        if self.rect.bottom >= GROUND:
            self.rect.bottom = GROUND
            self.velocity_y = 0
            self.on_ground = True

        # Shooting logic
        if keys[pygame.K_SPACE] and self.shoot_cooldown == 0:
            if len(self.projectiles) < 5: # Limit active projectiles
                shell = Projectile(self.rect.centerx, self.rect.top, -1)
                self.projectiles.add(shell)
                bullet_sound.play()
                self.shoot_cooldown = 15 # Cooldown in frames
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        self.projectiles.update()

    def take_hit(self):
        self.hits_taken += 1
        if self.hits_taken >= self.max_hits:
            self.lives -= 1
            self.hits_taken = 0 # Reset hits taken for the new life

    def heal(self, amount):
        self.hits_taken = max(0, self.hits_taken - amount) # Reduce hits taken, minimum 0

    def add_life(self):
        self.lives += 1


# Enemy class (also used for boss enemies)
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, health=50, boss=False, speed=1.5):
        super().__init__()
        self.boss = boss
        self.image = boss_img if boss else enemy_img
        self.rect = self.image.get_rect(topleft=(x, y))
        self.max_health = 250 if boss else health
        self.health = self.max_health
        self.speed = speed
        self.attack_timer = 0
        self.attack_rate = 90 # How often the enemy shoots
        self.projectiles = pygame.sprite.Group()

    # Move enemy downward and shoot if cooldown is done
    def update(self):
        self.rect.y += self.speed
        self.attack_timer += 1
        if self.attack_timer >= self.attack_rate:
            self.attack_timer = 0
            self.shoot()
        self.projectiles.update()

    def shoot(self):
        # Create a projectile shot by the enemy
        shell = Projectile(self.rect.centerx, self.rect.bottom, 1, is_enemy=True)
        self.projectiles.add(shell)
        bullet_sound.play()

    def draw_health_bar(self, surface):
        # Draw health bar above enemy
        health_percentage = self.health / self.max_health
        bar_width = 75 if self.boss else 40
        pygame.draw.rect(surface, RED, (self.rect.x, self.rect.y - 10, bar_width, 5))
        pygame.draw.rect(surface, GREEN, (self.rect.x, self.rect.y - 10, bar_width * health_percentage, 5))

    def respawn(self):
        # Reset enemy position and health
        self.health = self.max_health
        self.rect.y = -random.randint(60, 300)
        self.rect.x = random.randint(50, WIDTH - 50)

# --- New: Collectible Class ---
class Collectible(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        super().__init__()
        self.type = type # 'health_boost', 'extra_life', 'score_boost'

        # Different visual for each collectible type
        self.image = pygame.Surface((20, 20))
        if self.type == 'health_boost':
            self.image.fill(GREEN) # Green square for health
            self.value = 1 # Amount of health to restore (reduce hits taken)
        elif self.type == 'extra_life':
            self.image.fill(WHITE) # White square for extra life
            self.value = 1 # Amount of extra life
        elif self.type == 'score_boost':
            self.image.fill((0, 255, 255)) # Cyan square for score
            self.value = 100 # Score points
        else: # Default for safety
            self.image.fill(YELLOW)

        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 2 # Collectibles fall slowly

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT: # Remove if off-screen
            self.kill()

# Draw any text to the screen
def draw_text(surface, text, x, y, color=WHITE, font=FONT):
    img = font.render(text, True, color)
    surface.blit(img, (x, y))

# Show HUD(head up display) with lives, score, hits taken, enemies escaped, and player health bar
def draw_hud(player, enemy_escape_count, current_level): # Added current_level
    # Player Health Bar (new)
    bar_width = 100
    bar_height = 10
    # Calculate health based on hits taken (0 hits = full health, max_hits = empty)
    health_percentage = (player.max_hits - player.hits_taken) / player.max_hits
    if health_percentage < 0:
        health_percentage = 0 # Prevent negative health bar

    bar_x = 10
    bar_y = 90 # Adjust position as needed to avoid overlapping other text

    pygame.draw.rect(win, RED, (bar_x, bar_y, bar_width, bar_height)) # Background of bar
    pygame.draw.rect(win, GREEN, (bar_x, bar_y, bar_width * health_percentage, bar_height)) # Actual health
    draw_text(win, "Health:", bar_x + bar_width + 10, bar_y - 5) # Label for health bar

    draw_text(win, f"Lives: {player.lives}", 10, 10)
    draw_text(win, f"Score: {player.score}", 10, 30)
    draw_text(win, f"Hits Taken: {player.hits_taken} / {player.max_hits}", 10, 50)
    draw_text(win, f"Enemies Escaped: {enemy_escape_count} / 6", 10, 70)
    draw_text(win, f"Level: {current_level}", WIDTH - 100, 10) # Display current level

# Utility to wait for specific key presses
def wait_for_key(allowed_keys=None):
    """
    Handles key input and quit events centrally.
    allowed_keys: set or list of pygame key constants that are accepted.
    Returns the key pressed or None if quit requested.
    """
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if allowed_keys is None or event.key in allowed_keys:
                    return event.key

# Display Game Over screen and wait for player to restart or quit
def game_over_screen():
    win.fill(BLACK)
    draw_text(win, "GAME OVER", WIDTH // 2 - 70, HEIGHT // 2 - 40, RED, BIG_FONT)
    draw_text(win, "Press R to Restart or Q to Quit", WIDTH // 2 - 150, HEIGHT // 2, WHITE)
    pygame.display.update()

    while True:
        key = wait_for_key({pygame.K_r, pygame.K_q})
        if key == pygame.K_r:
            return
        elif key == pygame.K_q:
            pygame.quit()
            sys.exit()

# Show the start screen before the game begins
#WASD movement (W-forward or up, A-left,S-backward or down AND D-right.  )
def start_screen():
    win.fill(BLACK)
    draw_text(win, "SPACE WAR", WIDTH // 2 - 80, HEIGHT // 2 - 80, WHITE, BIG_FONT)
    draw_text(win, "Press any key to Start (WASD for movement, Space for Shoot)", WIDTH // 2 - 250, HEIGHT // 2 - 20)
    draw_text(win, "Press Q to Quit", WIDTH // 2 - 80, HEIGHT // 2 + 20)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                else:
                    return

# Show win screen after defeating boss
def win_screen():
    victory_sound.play()
    win_timer = pygame.time.get_ticks()
    flash = True
    sparkles = [pygame.Rect(random.randint(0, WIDTH), random.randint(0, HEIGHT), 2, 2) for _ in range(100)]

    while True:
        ret, frame = cap.read()
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = cap.read()
        frame = cv2.resize(frame, (WIDTH, HEIGHT))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        background_surface = pygame.surfarray.make_surface(np.rot90(frame))
        win.blit(background_surface, (0, 0))

        for sparkle in sparkles:
            pygame.draw.rect(win, (255, 255, 255), sparkle)
            sparkle.y += 1
            if sparkle.y > HEIGHT:
                sparkle.y = 0
                sparkle.x = random.randint(0, WIDTH)

        # Show win text and blinking effect
        if flash:
            draw_text(win, "CONGRATULATIONS!", WIDTH // 2 - 200, HEIGHT // 2 - 60, GREEN, BIG_FONT)
        draw_text(win, "You defeated the boss!", WIDTH // 2 - 140, HEIGHT // 2 - 10, WHITE, FONT)
        draw_text(win, "Press R to Restart or Q to Quit", WIDTH // 2 - 150, HEIGHT // 2 + 30, WHITE)

        if pygame.time.get_ticks() - win_timer > 500:
            flash = not flash
            win_timer = pygame.time.get_ticks()

        pygame.display.update()

        key = wait_for_key({pygame.K_r, pygame.K_q})
        if key == pygame.K_r:
            return
        elif key == pygame.K_q:
            pygame.quit()
            sys.exit()

# New: Function to display "Level Complete" screen
def level_complete_screen(current_level):
    level_up_sound.play() # Play level up sound
    start_time = pygame.time.get_ticks()
    duration = 2000 # Display for 2 seconds

    while pygame.time.get_ticks() - start_time < duration:
        win.fill(BLACK) # Clear screen
        draw_text(win, f"LEVEL {current_level} COMPLETED!", WIDTH // 2 - 180, HEIGHT // 2 - 40, BLUE, BIG_FONT)
        pygame.display.update()

        # Allow quitting during level complete screen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                pygame.quit()
                sys.exit()
    return # Return to main game loop

# Load enemies for each level
# Modified: Now returns the number of enemies to defeat for this level
def load_level(level, enemies):
    enemies.empty() # Clear existing enemies
    if level == 1:
        # Spawn 3 regular enemies with speed 1
        for _ in range(3):
            enemies.add(Enemy(random.randint(50, WIDTH - 50), random.randint(-300, -60), speed=1))
        return 5 # New: Target 5 enemies to defeat for Level 1
    elif level == 2:
        # Spawn 5 regular enemies with slightly increased speed
        for _ in range(5):
            enemies.add(Enemy(random.randint(50, WIDTH - 50), random.randint(-300, -60), speed=1.2))
        return 7 # New: Target 7 enemies to defeat for Level 2
    elif level == 3:
        # Spawn 3 regular enemies and 1 boss enemy
        for _ in range(3):
            enemies.add(Enemy(random.randint(50, WIDTH - 50), random.randint(-300, -60), speed=1.5))
        enemies.add(Enemy(random.randint(50, WIDTH - 50), random.randint(-300, -60), boss=True, speed=1.2))
        return 1 # New: Target 1 (the boss) for Level 3
    return 0 # Default return

# Main game loop
def main():
    start_screen() # Show start screen first
    player = Player()
    enemies = pygame.sprite.Group()
    collectibles = pygame.sprite.Group() # Collectibles Group

    current_level = 1 # Track current level
    enemies_defeated_this_level = 0 # New: Counter for enemies defeated in current level
    level_target_kills = load_level(current_level, enemies) # Load initial level and get target

    enemy_escape_count = 0

    collectible_spawn_timer = 0
    COLLECTIBLE_SPAWN_RATE = 300 # Every 5 seconds (60 FPS * 5 seconds)

    running = True
    while running:
        clock.tick(FPS) # Cap frame rate

        # Read video frame for background
        ret, frame = cap.read()
        if not ret: # If video ends, loop it from the beginning
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = cap.read()
        frame = cv2.resize(frame, (WIDTH, HEIGHT))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        background_surface = pygame.surfarray.make_surface(np.rot90(frame))
        win.blit(background_surface, (0, 0))

        keys = pygame.key.get_pressed() # Get all currently pressed keys

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                running = False # End game loop

        # Update game elements
        player.update(keys)
        enemies.update()
        collectibles.update()

        # Spawn collectibles
        collectible_spawn_timer += 1
        if collectible_spawn_timer >= COLLECTIBLE_SPAWN_RATE:
            collectible_spawn_timer = 0
            collectible_type = random.choice(['health_boost', 'extra_life', 'score_boost'])
            new_collectible = Collectible(random.randint(50, WIDTH - 50), -30, collectible_type)
            collectibles.add(new_collectible)

        # Collision between player and enemy bullets
        for enemy in enemies:
            for e_bullet in enemy.projectiles:
                if player.rect.colliderect(e_bullet.rect):
                    player.take_hit() # Player takes a hit
                    e_bullet.kill() # Destroy enemy bullet
                    if player.lives < 0: # If player runs out of lives
                        game_over_screen()
                        main() # Restart game (recursive call to main)
                        return # Exit current main loop

        # Collision between player bullets and enemies
        for shell in player.projectiles:
            hit_list = pygame.sprite.spritecollide(shell, enemies, False) # False: don't kill enemy immediately
            for enemy in hit_list:
                enemy.health -= 100 # Player bullet deals 100 damage
                shell.kill() # Destroy player bullet on hit
                if enemy.health <= 0:
                    if enemy.boss:
                        win_screen() # Show win screen if boss is defeated (game finished)
                        main() # Restart game
                        return # Exit current main loop
                    player.score += 1 # Increase score for regular enemy
                    enemies_defeated_this_level += 1 # New: Increment level enemy counter
                    enemy.respawn() # Respawn defeated regular enemy

        # Collision between player bullets and enemy bullets (optional, for deflecting/canceling)
        for p_bullet in player.projectiles:
            for enemy in enemies:
                for e_bullet in enemy.projectiles:
                    if pygame.sprite.collide_rect(p_bullet, e_bullet):
                        p_bullet.kill() # Destroy both bullets on collision
                        e_bullet.kill()

        # Collision between player and collectibles
        collected_items = pygame.sprite.spritecollide(player, collectibles, True) # True for auto-kill collectible
        for item in collected_items:
            collect_sound.play() # Play sound when collected
            if item.type == 'health_boost':
                player.heal(item.value) # Use new heal method
            elif item.type == 'extra_life':
                player.add_life() # Use new add_life method
            elif item.type == 'score_boost':
                player.score += item.value

        # Enemy movement and respawn if off screen
        for enemy in enemies:
            enemy.projectiles.draw(win) # Draw enemy bullets
            enemy.draw_health_bar(win) # Draw enemy health bar
            if enemy.rect.top > HEIGHT: # If enemy goes off screen
                enemy_escape_count += 1
                enemy.respawn() # Respawn the escaped enemy
                if enemy_escape_count >= 6 or player.lives < 0: # If too many enemies escape or player has no lives left
                    game_over_screen()
                    main() # Restart game
                    return # Exit current main loop

        # --- New: Level Progression Logic ---
        if current_level < 3 and enemies_defeated_this_level >= level_target_kills:
            level_complete_screen(current_level) # Show "Level Complete" message
            current_level += 1 # Advance to next level
            enemies_defeated_this_level = 0 # Reset counter for next level
            level_target_kills = load_level(current_level, enemies) # Load next level enemies and get its target

        # Draw all elements
        player.projectiles.draw(win) # Draw player bullets
        win.blit(player.image, player.rect) # Draw player
        enemies.draw(win) # Draw enemies
        collectibles.draw(win) # Draw collectibles
        draw_hud(player, enemy_escape_count, current_level) # Pass current_level to head up display(hud)

        pygame.display.update() # Update the display

    pygame.quit() # Quit pygame
    sys.exit() # Exit the system

if __name__ == "__main__":
    main()
