import pygame
import sys
import os
import re

# =========================================
# CONFIG GENERAL
# =========================================
pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CyberGuardian - Nivel 2")
clock = pygame.time.Clock()
FPS = 60

# Colores principales
WHITE = (255, 255, 255)
RED = (255, 60, 80)
CYAN = (0, 255, 220)
YELLOW = (255, 210, 90)
DARK_BLUE = (5, 15, 25)
SOFT_TEXT = (215, 240, 245)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# =========================================
# RUTAS SEGURAS
# =========================================
def asset_path(*parts):
    return os.path.join(BASE_DIR, *parts)


def load_image_safe(path, size=None, alpha=True):
    if not os.path.exists(path):
        print(f"No se encontró la imagen: {path}")
        surface = pygame.Surface(size if size else (100, 100), pygame.SRCALPHA)
        surface.fill((20, 20, 30, 255))
        return surface

    image = pygame.image.load(path)

    if alpha:
        image = image.convert_alpha()
    else:
        image = image.convert()

    if size is not None:
        image = pygame.transform.scale(image, size)

    return image


def natural_sort_key(filename):
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r"(\d+)", filename)]


# =========================================
# HUD MEJORADO COMPACTO
# =========================================
def draw_panel(surface, rect, fill_color=(6, 18, 32), alpha=185, border_color=CYAN, radius=10):
    panel = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    pygame.draw.rect(panel, (*fill_color, alpha), panel.get_rect(), border_radius=radius)
    surface.blit(panel, rect.topleft)

    pygame.draw.rect(surface, border_color, rect, width=2, border_radius=radius)

    inner = rect.inflate(-8, -8)
    pygame.draw.rect(surface, (0, 95, 120), inner, width=1, border_radius=max(4, radius - 4))


def draw_heart(surface, x, y, size=8, filled=True):
    color = RED if filled else (55, 60, 70)
    outline = (255, 170, 185) if filled else (105, 110, 120)

    r = size

    pygame.draw.circle(surface, color, (x + r, y + r), r)
    pygame.draw.circle(surface, color, (x + r * 3, y + r), r)

    points = [
        (x, y + r),
        (x + r * 2, y + r * 4),
        (x + r * 4, y + r),
    ]

    pygame.draw.polygon(surface, color, points)

    pygame.draw.circle(surface, outline, (x + r, y + r), r, 1)
    pygame.draw.circle(surface, outline, (x + r * 3, y + r), r, 1)
    pygame.draw.lines(surface, outline, True, points, 1)


def draw_hud(surface, player, challenge_done):
    font_title = pygame.font.Font(None, 22)
    font_text = pygame.font.Font(None, 23)
    font_small = pygame.font.Font(None, 20)

    # -------------------------------------
    # PANEL PEQUEÑO DE VIDAS
    # -------------------------------------
    lives_rect = pygame.Rect(18, 18, 180, 52)
    draw_panel(
        surface,
        lives_rect,
        fill_color=(10, 18, 30),
        alpha=190,
        border_color=RED,
        radius=10
    )

    title = font_title.render("VIDAS", True, WHITE)
    surface.blit(title, (32, 27))

    heart_x = 96
    heart_y = 33

    for i in range(player.max_health):
        draw_heart(
            surface,
            heart_x,
            heart_y,
            size=6,
            filled=(i < player.health)
        )
        heart_x += 27

    # -------------------------------------
    # PANEL PEQUEÑO DE OBJETIVO
    # -------------------------------------
    obj_rect = pygame.Rect(225, 18, 780, 52)

    if challenge_done:
        border = CYAN
        fill = (8, 24, 34)
        objective = "Puerta desbloqueada. Avanza a la salida."
    else:
        border = YELLOW
        fill = (34, 22, 8)
        objective = "Resuelve el reto de contraseñas seguras para abrir la puerta."

    draw_panel(
        surface,
        obj_rect,
        fill_color=fill,
        alpha=185,
        border_color=border,
        radius=10
    )

    obj_title = font_small.render("OBJETIVO", True, border)
    surface.blit(obj_title, (242, 26))

    obj_text = font_text.render(objective, True, WHITE)
    surface.blit(obj_text, (242, 47))


# =========================================
# PARALLAX (2 CAPAS)
# =========================================
class ParallaxBackground:
    def __init__(self, capa1_path, capa2_path):
        self.capa1 = load_image_safe(capa1_path, (WIDTH, HEIGHT), alpha=True)
        self.capa2 = load_image_safe(capa2_path, (WIDTH, HEIGHT), alpha=True)

    def draw(self, screen_surface, player_y):
        offset1 = int(player_y * 0.05)
        offset2 = int(player_y * 0.15)

        y1 = -offset1 % HEIGHT
        y2 = -offset2 % HEIGHT

        screen_surface.blit(self.capa1, (0, y1 - HEIGHT))
        screen_surface.blit(self.capa1, (0, y1))

        screen_surface.blit(self.capa2, (0, y2 - HEIGHT))
        screen_surface.blit(self.capa2, (0, y2))


# =========================================
# PLATAFORMAS
# =========================================
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.image = pygame.Surface((w, h), pygame.SRCALPHA)
        self.image.fill((25, 25, 38))
        pygame.draw.rect(self.image, (0, 180, 255), (0, 0, w, 3))
        pygame.draw.rect(self.image, (0, 70, 100), (0, h - 3, w, 3))
        self.rect = self.image.get_rect(topleft=(x, y))


# =========================================
# TERMINAL
# =========================================
class Terminal:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y - 32, 32, 32)

    def draw(self, screen_surface):
        pygame.draw.rect(screen_surface, (0, 255, 100), self.rect, border_radius=6)
        pygame.draw.rect(screen_surface, WHITE, self.rect, width=2, border_radius=6)

        inner = self.rect.inflate(-10, -10)
        pygame.draw.rect(screen_surface, (0, 80, 55), inner, border_radius=3)

    def can_interact(self, player_rect):
        return self.rect.colliderect(player_rect)


# =========================================
# PUERTA
# =========================================
class Door:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y - 64, 40, 80)

    def draw(self, screen_surface, open_):
        color = (0, 220, 255) if open_ else (50, 50, 60)
        border = CYAN if open_ else (130, 130, 145)

        pygame.draw.rect(screen_surface, color, self.rect, border_radius=6)
        pygame.draw.rect(screen_surface, border, self.rect, width=2, border_radius=6)

        if not open_:
            lock_rect = pygame.Rect(self.rect.centerx - 8, self.rect.centery - 4, 16, 18)
            pygame.draw.rect(screen_surface, (20, 20, 30), lock_rect, border_radius=3)
            pygame.draw.circle(screen_surface, (20, 20, 30), (self.rect.centerx, self.rect.centery - 8), 9, 3)

    def can_exit(self, player, open_):
        return open_ and self.rect.colliderect(player.rect)


# =========================================
# DRONE
# =========================================
class Drone(pygame.sprite.Sprite):
    def __init__(self, x1, x2, y):
        super().__init__()
        self.x1, self.x2 = x1, x2

        self.image = pygame.Surface((32, 20), pygame.SRCALPHA)
        pygame.draw.rect(self.image, (255, 60, 120), (0, 0, 32, 20), border_radius=6)
        pygame.draw.circle(self.image, (0, 255, 255), (10, 10), 4)
        pygame.draw.circle(self.image, (0, 255, 255), (22, 10), 4)
        pygame.draw.rect(self.image, WHITE, (0, 0, 32, 20), width=1, border_radius=6)

        self.rect = self.image.get_rect(midbottom=(x1, y))
        self.speed = 2
        self.dir = 1

    def update(self, player):
        self.rect.x += self.speed * self.dir

        if self.rect.x < self.x1:
            self.rect.x = self.x1
            self.dir = 1

        if self.rect.x > self.x2:
            self.rect.x = self.x2
            self.dir = -1

        if self.rect.colliderect(player.rect):
            player.take_damage(1)


# =========================================
# PLAYER
# =========================================
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, folder):
        super().__init__()

        self.frames = self.load_frames(folder)

        if not self.frames:
            img = pygame.Surface((64, 64), pygame.SRCALPHA)
            img.fill((0, 200, 255))
            self.frames = [img]

        self.image = self.frames[0]
        self.rect = self.image.get_rect(topleft=(x, y))

        self.vel_x = 0
        self.vel_y = 0
        self.speed = 4
        self.jump_power = -12
        self.on_ground = False

        self.anim_index = 0
        self.anim_timer = 0
        self.anim_speed = 0.12
        self.facing_right = True

        self.spawn = (x, y)
        self.max_health = 3
        self.health = 3
        self.invincible = 0

    def load_frames(self, folder):
        frames = []

        if not os.path.exists(folder):
            print(f"No se encontró la carpeta de sprites del jugador: {folder}")
            return frames

        image_names = [
            img_name for img_name in os.listdir(folder)
            if img_name.lower().endswith(".png")
        ]

        image_names.sort(key=natural_sort_key)

        for img_name in image_names:
            path = os.path.join(folder, img_name)
            img = pygame.image.load(path).convert_alpha()
            img = pygame.transform.smoothscale(img, (64, 64))
            frames.append(img)

        return frames

    def take_damage(self, amount):
        if self.invincible > 0:
            return

        self.health -= amount
        self.invincible = 45
        self.rect.y -= 20

        if self.health <= 0:
            self.health = self.max_health
            self.rect.topleft = self.spawn
            self.vel_x = 0
            self.vel_y = 0

    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.vel_x = 0

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.vel_x = -self.speed
            self.facing_right = False

        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.vel_x = self.speed
            self.facing_right = True

        if (keys[pygame.K_w] or keys[pygame.K_SPACE] or keys[pygame.K_UP]) and self.on_ground:
            self.vel_y = self.jump_power

    def apply_gravity(self):
        self.vel_y += 0.5

        if self.vel_y > 12:
            self.vel_y = 12

    def collide(self, vx, vy, platforms):
        for p in platforms:
            if self.rect.colliderect(p.rect):
                if vx > 0:
                    self.rect.right = p.rect.left

                if vx < 0:
                    self.rect.left = p.rect.right

                if vy > 0:
                    self.rect.bottom = p.rect.top
                    self.vel_y = 0
                    self.on_ground = True

                if vy < 0:
                    self.rect.top = p.rect.bottom
                    self.vel_y = 0

    def clamp_to_screen(self):
        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

        if self.rect.top < 0:
            self.rect.top = 0

    def animate(self):
        moving = self.vel_x != 0

        if moving:
            self.anim_timer += self.anim_speed

            if self.anim_timer >= 1:
                self.anim_timer = 0
                self.anim_index = (self.anim_index + 1) % len(self.frames)
        else:
            self.anim_index = 0

        img = self.frames[self.anim_index]

        if not self.facing_right:
            img = pygame.transform.flip(img, True, False)

        if self.invincible > 0 and (self.invincible // 5) % 2 == 0:
            temp = img.copy()
            temp.set_alpha(120)
            self.image = temp
        else:
            self.image = img

    def update(self, platforms):
        if self.invincible > 0:
            self.invincible -= 1

        self.handle_input()
        self.apply_gravity()

        self.rect.x += self.vel_x
        self.collide(self.vel_x, 0, platforms)

        self.rect.y += self.vel_y
        self.on_ground = False
        self.collide(0, self.vel_y, platforms)

        self.clamp_to_screen()
        self.animate()


# =========================================
# RETO DE CONTRASEÑAS
# =========================================
def password_challenge(screen_surface):
    local_clock = pygame.time.Clock()
    font_title = pygame.font.Font(None, 58)
    font = pygame.font.Font(None, 34)
    font_small = pygame.font.Font(None, 28)

    question = "¿Cual de estas contraseñas es la mas segura?"
    options = [
        "1) 12345Juan",
        "2) Luna2024",
        "3) G#92vP!r*7q"
    ]
    correct = 3

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if e.type == pygame.KEYDOWN:
                if e.key in (pygame.K_1, pygame.K_KP1):
                    return 1 == correct
                if e.key in (pygame.K_2, pygame.K_KP2):
                    return 2 == correct
                if e.key in (pygame.K_3, pygame.K_KP3):
                    return 3 == correct

        screen_surface.fill((6, 14, 28))

        # Fondo decorativo simple
        for i in range(0, WIDTH, 80):
            pygame.draw.line(screen_surface, (0, 40, 60), (i, 0), (i, HEIGHT), 1)

        for j in range(0, HEIGHT, 80):
            pygame.draw.line(screen_surface, (0, 40, 60), (0, j), (WIDTH, j), 1)

        panel = pygame.Rect(160, 90, 960, 520)
        draw_panel(screen_surface, panel, fill_color=(3, 18, 32), alpha=230, border_color=CYAN, radius=18)

        title = font_title.render("RETO DE CONTRASENAS SEGURAS", True, CYAN)
        screen_surface.blit(title, (WIDTH // 2 - title.get_width() // 2, 130))

        subtitle = font_small.render("Selecciona la respuesta correcta usando las teclas 1, 2 o 3", True, SOFT_TEXT)
        screen_surface.blit(subtitle, (WIDTH // 2 - subtitle.get_width() // 2, 185))

        qsurf = font.render(question, True, WHITE)
        screen_surface.blit(qsurf, (220, 250))

        y = 320

        for opt in options:
            opt_rect = pygame.Rect(220, y - 10, 840, 50)
            pygame.draw.rect(screen_surface, (8, 26, 42), opt_rect, border_radius=10)
            pygame.draw.rect(screen_surface, (0, 150, 180), opt_rect, width=2, border_radius=10)

            osurf = font.render(opt, True, WHITE)
            screen_surface.blit(osurf, (245, y))
            y += 70

        pygame.display.flip()
        local_clock.tick(30)


# =========================================
# CREAR NIVEL 2
# =========================================
def create_vertical_level():
    plats = pygame.sprite.Group()

    def P(x, y, w, h):
        plats.add(Platform(x, y, w, h))

    P(0, HEIGHT - 40, WIDTH, 40)
    P(20, HEIGHT - 140, 1170, 24)
    P(820, HEIGHT - 230, 180, 24)
    P(600, HEIGHT - 300, 300, 24)
    P(300, HEIGHT - 380, 200, 24)
    P(150, HEIGHT - 460, 200, 24)
    P(430, HEIGHT - 520, 200, 24)
    P(700, HEIGHT - 520, 200, 24)

    final_y = 95
    final_x = 1000
    P(final_x, final_y, 220, 30)

    terminal = Terminal(final_x + 10, final_y)
    door = Door(final_x + 120, final_y)

    drones = [
        Drone(120, 260, HEIGHT - 150),
        Drone(300, 480, HEIGHT - 260),
        Drone(200, 480, HEIGHT - 310),
        Drone(520, 720, HEIGHT - 380),
        Drone(630, 900, HEIGHT - 530),
    ]

    return plats, terminal, door, drones


# =========================================
# PANTALLA FINAL NIVEL 2
# =========================================
def level2_complete_screen(screen_surface):
    local_clock = pygame.time.Clock()
    font_title = pygame.font.Font(None, 60)
    font_btn = pygame.font.Font(None, 40)
    font_msg = pygame.font.Font(None, 36)

    lana_path = asset_path("assets", "sprites", "Lana", "Fin_nivel2.png")
    lana_bg = load_image_safe(lana_path, (WIDTH, HEIGHT), alpha=True)

    btn_width = 320
    btn_height = 70
    next_btn = pygame.Rect(WIDTH // 2 - btn_width // 2, HEIGHT - 220, btn_width, btn_height)
    exit_btn = pygame.Rect(WIDTH // 2 - btn_width // 2, HEIGHT - 130, btn_width, btn_height)

    text1 = "¡Excelente trabajo, Cyber!"
    text2 = "Pero Xenon esta evolucionando. Debemos detenerlo."

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if e.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()

                if next_btn.collidepoint(mx, my):
                    return "next"

                if exit_btn.collidepoint(mx, my):
                    pygame.quit()
                    sys.exit()

            if e.type == pygame.KEYDOWN:
                if e.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    return "next"

                if e.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        screen_surface.blit(lana_bg, (0, 0))

        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 130))
        screen_surface.blit(overlay, (0, 0))

        title = font_title.render("¡NIVEL 2 COMPLETADO!", True, YELLOW)
        screen_surface.blit(title, (WIDTH // 2 - title.get_width() // 2, 60))

        screen_surface.blit(font_msg.render(text1, True, WHITE), (WIDTH // 2 - 280, 200))
        screen_surface.blit(font_msg.render(text2, True, WHITE), (WIDTH // 2 - 360, 240))

        pygame.draw.rect(screen_surface, (0, 200, 255), next_btn, border_radius=12)
        screen_surface.blit(
            font_btn.render("Siguiente Nivel", True, (0, 20, 40)),
            (next_btn.centerx - 120, next_btn.centery - 20)
        )

        pygame.draw.rect(screen_surface, (255, 80, 80), exit_btn, border_radius=12)
        screen_surface.blit(
            font_btn.render("Salir del Juego", True, (40, 0, 0)),
            (exit_btn.centerx - 120, exit_btn.centery - 20)
        )

        pygame.display.flip()
        local_clock.tick(30)


# =========================================
# MAIN NIVEL 2
# =========================================
def main_nivel2():
    music_path = asset_path("assets", "Musica", "Nivel2.mp3")

    if os.path.exists(music_path):
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
    else:
        print(f"No se encontró la música del nivel 2: {music_path}")

    fondo = ParallaxBackground(
        asset_path("assets", "sprites", "Fondos", "Nivel2", "CAPA1.png"),
        asset_path("assets", "sprites", "Fondos", "Nivel2", "CAPA2.png")
    )

    plats, terminal, door, drones = create_vertical_level()
    drones_group = pygame.sprite.Group(drones)

    player = Player(60, HEIGHT - 100, asset_path("assets", "sprites", "Cyber"))

    challenge_done = False
    running = True

    while running:
        clock.tick(FPS)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_e and terminal.can_interact(player.rect):
                    if not challenge_done:
                        success = password_challenge(screen)

                        if success:
                            challenge_done = True

        player.update(plats)
        drones_group.update(player)

        if player.rect.top > HEIGHT + 150:
            player.rect.topleft = player.spawn
            player.vel_x = 0
            player.vel_y = 0

        # Dibujar mundo
        fondo.draw(screen, player.rect.y)
        plats.draw(screen)
        drones_group.draw(screen)
        terminal.draw(screen)
        door.draw(screen, challenge_done)
        screen.blit(player.image, player.rect)

        # HUD compacto sin controles ni terminal
        draw_hud(screen, player, challenge_done)

        # Pasar al siguiente nivel
        if door.can_exit(player, challenge_done):
            pygame.mixer.music.stop()

            result = level2_complete_screen(screen)

            if result == "next":
                running = False
                import nivel3
                nivel3.main_nivel3()

        pygame.display.flip()


if __name__ == "__main__":
    main_nivel2()
