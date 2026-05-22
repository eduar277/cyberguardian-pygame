import pygame

# ---------------------------------------------------
# COLORES
# ---------------------------------------------------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

CYAN = (0, 255, 220)
CYAN_SOFT = (120, 255, 240)
RED = (255, 70, 90)
RED_DARK = (170, 30, 50)
GRAY = (180, 180, 180)
DARK_BG = (10, 18, 28)
PANEL_BG = (8, 16, 28, 185)
PANEL_BORDER = (0, 220, 220)


# ---------------------------------------------------
# PANEL REDONDEADO TRANSLÚCIDO
# ---------------------------------------------------
def draw_panel(surface, rect, border_color=CYAN, fill_color=(8, 16, 28), alpha=185, radius=16):
    panel = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    pygame.draw.rect(panel, (*fill_color, alpha), panel.get_rect(), border_radius=radius)
    surface.blit(panel, rect.topleft)
    pygame.draw.rect(surface, border_color, rect, width=2, border_radius=radius)


# ---------------------------------------------------
# DIBUJAR CORAZÓN
# ---------------------------------------------------
def draw_heart(surface, x, y, size=18, filled=True):
    color = RED if filled else (70, 70, 70)
    outline = (255, 180, 190) if filled else (120, 120, 120)

    radius = size // 2

    # Círculos superiores
    pygame.draw.circle(surface, color, (x + radius, y + radius), radius)
    pygame.draw.circle(surface, color, (x + radius * 3, y + radius), radius)

    # Parte inferior
    points = [
        (x, y + radius),
        (x + radius * 2, y + size * 2),
        (x + radius * 4, y + radius)
    ]
    pygame.draw.polygon(surface, color, points)

    # Contorno
    pygame.draw.circle(surface, outline, (x + radius, y + radius), radius, 2)
    pygame.draw.circle(surface, outline, (x + radius * 3, y + radius), radius, 2)
    pygame.draw.lines(surface, outline, False, points, 2)


# ---------------------------------------------------
# TECLA VISUAL
# ---------------------------------------------------
def draw_key(surface, text, x, y, font):
    key_rect = pygame.Rect(x, y, 42, 34)

    shadow = key_rect.copy()
    shadow.x += 2
    shadow.y += 2
    pygame.draw.rect(surface, (0, 0, 0), shadow, border_radius=8)

    pygame.draw.rect(surface, (20, 35, 52), key_rect, border_radius=8)
    pygame.draw.rect(surface, CYAN_SOFT, key_rect, width=2, border_radius=8)

    txt = font.render(text, True, WHITE)
    surface.blit(
        txt,
        (key_rect.centerx - txt.get_width() // 2,
         key_rect.centery - txt.get_height() // 2)
    )


# ---------------------------------------------------
# FLECHAS VISUALES
# ---------------------------------------------------
def draw_arrow_key(surface, direction, x, y):
    rect = pygame.Rect(x, y, 42, 34)

    shadow = rect.copy()
    shadow.x += 2
    shadow.y += 2
    pygame.draw.rect(surface, (0, 0, 0), shadow, border_radius=8)

    pygame.draw.rect(surface, (20, 35, 52), rect, border_radius=8)
    pygame.draw.rect(surface, CYAN_SOFT, rect, width=2, border_radius=8)

    cx, cy = rect.center

    if direction == "left":
        pts = [(cx + 8, cy - 8), (cx - 8, cy), (cx + 8, cy + 8)]
    elif direction == "right":
        pts = [(cx - 8, cy - 8), (cx + 8, cy), (cx - 8, cy + 8)]
    elif direction == "up":
        pts = [(cx, cy - 9), (cx - 9, cy + 7), (cx + 9, cy + 7)]
    else:
        pts = [(cx, cy + 9), (cx - 9, cy - 7), (cx + 9, cy - 7)]

    pygame.draw.polygon(surface, WHITE, pts)


# ---------------------------------------------------
# DIBUJAR HUD COMPLETO
# ---------------------------------------------------
def draw_hud(screen, vidas_actuales, max_vidas, objective_text):
    width, height = screen.get_size()

    font_title = pygame.font.Font(None, 30)
    font_text = pygame.font.Font(None, 28)
    font_small = pygame.font.Font(None, 24)

    # ------------------------------------------------
    # PANEL DE VIDAS
    # ------------------------------------------------
    lives_rect = pygame.Rect(20, 20, 240, 74)
    draw_panel(screen, lives_rect)

    title = font_title.render("VIDAS", True, WHITE)
    screen.blit(title, (35, 28))

    heart_x = 35
    for i in range(max_vidas):
        draw_heart(screen, heart_x, 52, size=12, filled=(i < vidas_actuales))
        heart_x += 38

    # ------------------------------------------------
    # PANEL DE CONTROLES
    # ------------------------------------------------
    controls_rect = pygame.Rect(280, 20, 650, 74)
    draw_panel(screen, controls_rect)

    controls_title = font_small.render("CONTROLES", True, CYAN_SOFT)
    screen.blit(controls_title, (300, 28))

    # Movimiento
    label_move = font_small.render("Mover", True, WHITE)
    screen.blit(label_move, (300, 55))
    draw_key(screen, "A", 365, 48, font_small)
    draw_key(screen, "D", 412, 48, font_small)
    draw_arrow_key(screen, "left", 470, 48)
    draw_arrow_key(screen, "right", 517, 48)

    # Saltar
    label_jump = font_small.render("Saltar", True, WHITE)
    screen.blit(label_jump, (580, 55))
    draw_key(screen, "W", 645, 48, font_small)
    draw_key(screen, "SP", 692, 48, font_small)

    # Interactuar
    label_interact = font_small.render("Interactuar", True, WHITE)
    screen.blit(label_interact, (760, 55))
    draw_key(screen, "E", 860, 48, font_small)

    # ------------------------------------------------
    # PANEL DE OBJETIVO
    # ------------------------------------------------
    obj_rect = pygame.Rect(20, 105, 560, 58)
    draw_panel(screen, obj_rect, border_color=(255, 180, 80), fill_color=(32, 18, 8), alpha=190)

    obj_title = font_small.render("OBJETIVO", True, (255, 220, 130))
    screen.blit(obj_title, (35, 113))

    obj_text = font_text.render(objective_text, True, WHITE)
    screen.blit(obj_text, (130, 128))