import pygame
import random
import cv2
import numpy as np

pygame.init()
WIDTH, HEIGHT = 960, 540
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Battle")

WHITE = (255, 255, 255)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
BLACK = (0, 0, 0)

GROUND = HEIGHT - 60
FPS = 60
FONT = pygame.font.SysFont(None, 30)
BIG_FONT = pygame.font.SysFont(None, 50)
clock = pygame.time.Clock()

# Load and play background music
pygame.mixer.music.load("space-cloud-333647.mp3")
pygame.mixer.music.play(-1)  # Loop forever
pygame.mixer.music.set_volume(0.5)

player_img = pygame.transform.scale(
    pygame.image.load("player_tank.png"), (40, 90))
enemy_img = pygame.transform.rotate(
    pygame.transform.scale(
        pygame.image.load("enemy_tank.png"), (40, 80)), 180)
boss_img = pygame.transform.scale(
    pygame.image.load("boss_tank.png"), (120, 180))
bullet_sound = pygame.mixer.Sound("bulletshot.mp3")

# Initialize OpenCV video capture for background video
cap = cv2.VideoCapture("backvd.mp4")


class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, is_enemy=False):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(RED if is_enemy else WHITE)
        self.rect = self.image.get_rect(center=(x, y))
        self.direction = direction
        self.speed = 10

    def update(self):
        self.rect.y += self.speed * self.direction
        if self.rect.bottom < 0 or self.rect.top > HEIGHT:
            self.kill()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect(midbottom=(WIDTH // 2, GROUND))
        self.lives = 3
        self.score = 0
        self.projectiles = pygame.sprite.Group()
        self.shoot_cooldown = 0
        self.hits_taken = 0

    def update(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += 5
        if keys[pygame.K_SPACE] and self.shoot_cooldown == 0:
            if len(self.projectiles) < 5:
                shell = Projectile(self.rect.centerx, self.rect.top, -1)
                self.projectiles.add(shell)
                bullet_sound.play()
                self.shoot_cooldown = 15
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        self.projectiles.update()


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
        self.attack_rate = 90
        self.projectiles = pygame.sprite.Group()

    def update(self):
        self.rect.y += self.speed
        self.attack_timer += 1
        if self.attack_timer >= self.attack_rate:
            self.attack_timer = 0
            self.shoot()
        self.projectiles.update()

    def shoot(self):
        shell = Projectile(self.rect.centerx,
                           self.rect.bottom, 1, is_enemy=True)
        self.projectiles.add(shell)
        bullet_sound.play()

    def draw_health_bar(self, surface):
        health_percentage = self.health / self.max_health
        bar_width = 75 if self.boss else 40
        pygame.draw.rect(surface, RED, (self.rect.x,
                         self.rect.y - 10, bar_width, 5))
        pygame.draw.rect(surface, GREEN, (self.rect.x,
                         self.rect.y - 10, bar_width * health_percentage, 5))

    def respawn(self):
        self.health = self.max_health
        self.rect.y = -random.randint(60, 300)
        self.rect.x = random.randint(50, WIDTH - 50)


def draw_text(surface, text, x, y, color=WHITE, font=FONT):
    img = font.render(text, True, color)
    surface.blit(img, (x, y))


def draw_hud():
    draw_text(win, f"Lives: {player.lives}", 10, 10)
    draw_text(win, f"Score: {player.score}", 10, 30)
    draw_text(win, f"Hits Taken: {player.hits_taken} / 3", 10, 50)
    draw_text(win, f"Enemies Escaped: {enemy_escape_count} / 4", 10, 70)


def game_over_screen():
    win.fill(BLACK)
    draw_text(win, "GAME OVER", WIDTH // 2 - 70,
              HEIGHT // 2 - 40, RED, BIG_FONT)
    draw_text(win, "Press R to Restart or Q to Quit",
              WIDTH // 2 - 150, HEIGHT // 2, WHITE)
    pygame.display.update()
    wait = True
    while wait:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_r:
                    wait = False
                elif e.key == pygame.K_q:
                    pygame.quit()
                    exit()


def start_screen():
    win.fill(BLACK)
    draw_text(win, "SPACE WAR", WIDTH // 2 - 80,
              HEIGHT // 2 - 80, WHITE, BIG_FONT)
    draw_text(win, "Press any key to Start",
              WIDTH // 2 - 100, HEIGHT // 2 - 20)
    draw_text(win, "Press Q to Quit", WIDTH // 2 - 80, HEIGHT // 2 + 20)
    pygame.display.update()
    waiting = True
    while waiting:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_q:
                    pygame.quit()
                    exit()
                else:
                    waiting = False  # Any other key starts the game


def win_screen():
    victory_sound = pygame.mixer.Sound("victory.mp3")
    victory_sound.play()

    win_timer = pygame.time.get_ticks()
    flash = True

    sparkles = [pygame.Rect(random.randint(0, WIDTH), random.randint(
        0, HEIGHT), 2, 2) for _ in range(100)]

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

        if flash:
            draw_text(win, "CONGRATULATIONS!", WIDTH // 2 -
                      200, HEIGHT // 2 - 60, GREEN, BIG_FONT)

        draw_text(win, "You defeated the boss!", WIDTH //
                  2 - 140, HEIGHT // 2 - 10, WHITE, FONT)
        draw_text(win, "Press R to Restart or Q to Quit",
                  WIDTH // 2 - 150, HEIGHT // 2 + 30, WHITE)

        if pygame.time.get_ticks() - win_timer > 500:
            flash = not flash
            win_timer = pygame.time.get_ticks()

        pygame.display.update()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_r:
                    return
                elif e.key == pygame.K_q:
                    pygame.quit()
                    exit()


def load_level(level):
    enemies.empty()
    if level == 1:
        for _ in range(3):
            enemies.add(Enemy(random.randint(50, WIDTH - 50),
                        random.randint(-300, -60), speed=1))
    elif level == 2:
        for _ in range(5):
            enemies.add(Enemy(random.randint(50, WIDTH - 50),
                        random.randint(-300, -60), speed=1.2))
    elif level == 3:
        for _ in range(3):
            enemies.add(Enemy(random.randint(50, WIDTH - 50),
                        random.randint(-300, -60), speed=1.5))
        enemies.add(Enemy(random.randint(50, WIDTH - 50),
                    random.randint(-300, -60), boss=True, speed=1.2))


start_screen()

player = Player()
enemies = pygame.sprite.Group()
level = 1
load_level(level)
level_up_display_time = 0
enemy_escape_count = 0

run = True
while run:
    clock.tick(FPS)

    # Read video frame from OpenCV
    ret, frame = cap.read()
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        ret, frame = cap.read()

    frame = cv2.resize(frame, (WIDTH, HEIGHT))
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    background_surface = pygame.surfarray.make_surface(np.rot90(frame))
    win.blit(background_surface, (0, 0))

    keys = pygame.key.get_pressed()
    for e in pygame.event.get():
        if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_q):
            run = False

    player.update(keys)
    enemies.update()

    # Bullet collisions
    for p_bullet in player.projectiles:
        for enemy in enemies:
            for e_bullet in enemy.projectiles:
                if pygame.sprite.collide_rect(p_bullet, e_bullet):
                    p_bullet.kill()
                    e_bullet.kill()

    for shell in player.projectiles:
        hit_list = pygame.sprite.spritecollide(shell, enemies, False)
        for enemy in hit_list:
            enemy.health -= 100
            shell.kill()
            if enemy.health <= 0:
                player.score += 20 if enemy.boss else 10
                enemy.respawn()

    for enemy in enemies:
        for e_bullet in enemy.projectiles:
            if player.rect.colliderect(e_bullet.rect):
                player.lives -= 1
                player.hits_taken += 1
                e_bullet.kill()
                if player.lives <= 0 or player.hits_taken >= 3:
                    game_over_screen()
                    player = Player()
                    level = 1
                    load_level(level)

    # Enemy escape check
    for enemy in enemies:
        if enemy.rect.top > HEIGHT:
            enemy_escape_count += 1
            enemy.respawn()

    if enemy_escape_count >= 4:
        game_over_screen()
        player = Player()
        level = 1
        load_level(level)
        enemy_escape_count = 0

    # Draw all sprites
    player.projectiles.draw(win)
    win.blit(player.image, player.rect)
    for enemy in enemies:
        win.blit(enemy.image, enemy.rect)
        enemy.projectiles.draw(win)
        enemy.draw_health_bar(win)

    draw_hud()

    # Level up
    if player.score >= 50 and level == 1:
        level = 2
        load_level(level)
        level_up_display_time = pygame.time.get_ticks()
    if player.score >= 100 and level == 2:
        level = 3
        load_level(level)
        level_up_display_time = pygame.time.get_ticks()
    if player.score >= 150 and level == 3:
        win_screen()
        player = Player()
        level = 1
        load_level(level)

    # Display "Level Up" message for 3 seconds
    if level_up_display_time > 0 and pygame.time.get_ticks() - level_up_display_time < 3000:
        draw_text(win, f"Level {level}", WIDTH // 2 -
                  40, HEIGHT // 2 - 50, WHITE, BIG_FONT)
    else:
        level_up_display_time = 0

    pygame.display.update()

pygame.quit()
cap.release()
