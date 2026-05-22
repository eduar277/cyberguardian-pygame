import pygame
import sys
import os

pygame.init()
pygame.mixer.init()

# ----------------------------------------------------
# CONFIGURACION GENERAL
# ----------------------------------------------------
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CyberGuardian: Amenaza Xenon")
clock = pygame.time.Clock()
FPS = 60

# Colores
WHITE = (255, 255, 255)
CYAN = (0, 255, 220)
CYAN_DARK = (0, 150, 180)
RED = (255, 80, 80)
RED_DARK = (190, 40, 40)
DARK_BLUE = (5, 15, 25)
SOFT_TEXT = (210, 240, 245)
BLACK = (0, 0, 0)
YELLOW = (255, 210, 90)
MAGENTA = (255, 0, 180)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Importar Nivel 1
from nivel1 import main_nivel1


# ----------------------------------------------------
# RUTAS
# ----------------------------------------------------
def asset_path(*parts):
    return os.path.join(BASE_DIR, *parts)


# ----------------------------------------------------
# CARGA SEGURA DE IMAGENES
# ----------------------------------------------------
def load_image_safe(path, size=None):
    if os.path.exists(path):
        img = pygame.image.load(path).convert()
        if size is not None:
            img = pygame.transform.scale(img, size)
        return img

    print(f"No se encontro la imagen: {path}")
    return None


# ----------------------------------------------------
# TEXTO CENTRADO
# ----------------------------------------------------
def draw_text_center(surface, text, font, color, center_x, y):
    rendered = font.render(text, True, color)
    surface.blit(rendered, (center_x - rendered.get_width() // 2, y))
    return rendered


# ----------------------------------------------------
# PANEL TRANSLUCIDO ESTILO CYBER
# ----------------------------------------------------
def draw_panel(surface, rect, color=(3, 18, 32), alpha=210, border_color=CYAN):
    panel = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    panel.fill((*color, alpha))
    surface.blit(panel, rect.topleft)

    # Borde principal
    pygame.draw.rect(surface, border_color, rect, width=2, border_radius=20)

    # Borde interno
    inner = rect.inflate(-18, -18)
    pygame.draw.rect(surface, (0, 100, 130), inner, width=1, border_radius=16)

    # Esquinas decorativas
    corner_len = 34
    x, y, w, h = rect.x, rect.y, rect.width, rect.height

    pygame.draw.line(surface, border_color, (x + 18, y + 18), (x + 18 + corner_len, y + 18), 3)
    pygame.draw.line(surface, border_color, (x + 18, y + 18), (x + 18, y + 18 + corner_len), 3)

    pygame.draw.line(surface, border_color, (x + w - 18, y + 18), (x + w - 18 - corner_len, y + 18), 3)
    pygame.draw.line(surface, border_color, (x + w - 18, y + 18), (x + w - 18, y + 18 + corner_len), 3)

    pygame.draw.line(surface, border_color, (x + 18, y + h - 18), (x + 18 + corner_len, y + h - 18), 3)
    pygame.draw.line(surface, border_color, (x + 18, y + h - 18), (x + 18, y + h - 18 - corner_len), 3)

    pygame.draw.line(surface, border_color, (x + w - 18, y + h - 18), (x + w - 18 - corner_len, y + h - 18), 3)
    pygame.draw.line(surface, border_color, (x + w - 18, y + h - 18), (x + w - 18, y + h - 18 - corner_len), 3)


# ----------------------------------------------------
# BOTON PRINCIPAL MEJORADO
# ----------------------------------------------------
class Button:
    def __init__(self, text, x, y, width, height, color, hover_color, text_color=WHITE):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.font = pygame.font.Font(None, 40)

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        is_hover = self.rect.collidepoint(mouse_pos)

        current_color = self.hover_color if is_hover else self.color
        border_color = WHITE if is_hover else CYAN

        # Sombra
        shadow = self.rect.copy()
        shadow.x += 6
        shadow.y += 6
        pygame.draw.rect(surface, (0, 0, 0), shadow, border_radius=16)

        # Glow externo
        glow_rect = self.rect.inflate(10, 10)
        glow_surface = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(
            glow_surface,
            (*border_color, 45 if is_hover else 25),
            glow_surface.get_rect(),
            border_radius=18
        )
        surface.blit(glow_surface, glow_rect.topleft)

        # Cuerpo del boton
        pygame.draw.rect(surface, current_color, self.rect, border_radius=16)
        pygame.draw.rect(surface, border_color, self.rect, width=2, border_radius=16)

        # Brillo superior
        highlight = pygame.Rect(self.rect.x + 10, self.rect.y + 8, self.rect.width - 20, 3)
        pygame.draw.rect(surface, (180, 255, 255), highlight, border_radius=2)

        txt = self.font.render(self.text, True, self.text_color)
        surface.blit(
            txt,
            (
                self.rect.centerx - txt.get_width() // 2,
                self.rect.centery - txt.get_height() // 2
            )
        )

    def is_clicked(self, event):
        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        )


# ----------------------------------------------------
# DIBUJAR TECLA NORMAL
# ----------------------------------------------------
def draw_key(surface, text, x, y, w=70, h=55):
    key_rect = pygame.Rect(x, y, w, h)

    shadow = key_rect.copy()
    shadow.x += 4
    shadow.y += 4
    pygame.draw.rect(surface, BLACK, shadow, border_radius=12)

    pygame.draw.rect(surface, (7, 32, 48), key_rect, border_radius=12)
    pygame.draw.rect(surface, CYAN, key_rect, width=2, border_radius=12)

    font_key = pygame.font.Font(None, 34)
    key_text = font_key.render(text, True, WHITE)

    surface.blit(
        key_text,
        (
            key_rect.centerx - key_text.get_width() // 2,
            key_rect.centery - key_text.get_height() // 2
        )
    )


# ----------------------------------------------------
# DIBUJAR FLECHAS SIN CARACTERES ESPECIALES
# ----------------------------------------------------
def draw_arrow_key(surface, direction, x, y):
    key_rect = pygame.Rect(x, y, 70, 55)

    shadow = key_rect.copy()
    shadow.x += 4
    shadow.y += 4
    pygame.draw.rect(surface, BLACK, shadow, border_radius=12)

    pygame.draw.rect(surface, (7, 32, 48), key_rect, border_radius=12)
    pygame.draw.rect(surface, CYAN, key_rect, width=2, border_radius=12)

    cx, cy = key_rect.center

    if direction == "left":
        points = [(cx + 14, cy - 15), (cx - 15, cy), (cx + 14, cy + 15)]
    elif direction == "right":
        points = [(cx - 14, cy - 15), (cx + 15, cy), (cx - 14, cy + 15)]
    elif direction == "up":
        points = [(cx, cy - 17), (cx - 16, cy + 12), (cx + 16, cy + 12)]
    else:
        points = [(cx, cy + 17), (cx - 16, cy - 12), (cx + 16, cy - 12)]

    pygame.draw.polygon(surface, WHITE, points)


# ----------------------------------------------------
# FILA DE CONTROL
# ----------------------------------------------------
def draw_control_row(surface, label, y, key_draw_commands):
    font_label = pygame.font.Font(None, 38)
    label_surf = font_label.render(label, True, WHITE)
    surface.blit(label_surf, (150, y))

    for command in key_draw_commands:
        command()


# ----------------------------------------------------
# PANTALLA DE CONTROLES MEJORADA
# ----------------------------------------------------
def controls_screen():
    font_title = pygame.font.Font(None, 78)
    font_subtitle = pygame.font.Font(None, 34)
    font_small = pygame.font.Font(None, 30)

    bg_path = asset_path("assets", "sprites", "Fondos", "menu2.png")
    bg_controls = load_image_safe(bg_path, (WIDTH, HEIGHT))

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                return

        if bg_controls:
            screen.blit(bg_controls, (0, 0))
        else:
            screen.fill(DARK_BLUE)

        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 75))
        screen.blit(overlay, (0, 0))

        panel_rect = pygame.Rect(80, 70, 800, 580)
        draw_panel(screen, panel_rect, color=(3, 18, 32), alpha=215, border_color=CYAN)

        title = font_title.render("CONTROLES", True, CYAN)
        screen.blit(title, (panel_rect.centerx - title.get_width() // 2, 105))

        subtitle = font_subtitle.render("Guia rapida para jugar CyberGuardian", True, SOFT_TEXT)
        screen.blit(subtitle, (panel_rect.centerx - subtitle.get_width() // 2, 170))

        pygame.draw.line(screen, CYAN, (145, 220), (815, 220), 2)
        pygame.draw.circle(screen, CYAN, (145, 220), 5)
        pygame.draw.circle(screen, CYAN, (815, 220), 5)

        draw_control_row(
            screen,
            "Mover personaje",
            255,
            [
                lambda: draw_key(screen, "A", 455, 245),
                lambda: draw_key(screen, "D", 535, 245),
                lambda: draw_arrow_key(screen, "left", 635, 245),
                lambda: draw_arrow_key(screen, "right", 715, 245),
            ]
        )

        draw_control_row(
            screen,
            "Saltar",
            340,
            [
                lambda: draw_key(screen, "W", 455, 330),
                lambda: draw_arrow_key(screen, "up", 535, 330),
                lambda: draw_key(screen, "SPACE", 635, 330, w=150),
            ]
        )

        draw_control_row(
            screen,
            "Interactuar con terminales",
            425,
            [
                lambda: draw_key(screen, "E", 690, 415),
            ]
        )

        draw_control_row(
            screen,
            "Responder retos",
            510,
            [
                lambda: draw_key(screen, "1", 500, 500),
                lambda: draw_key(screen, "2", 580, 500),
                lambda: draw_key(screen, "3", 660, 500),
            ]
        )

        pygame.draw.line(screen, (0, 120, 140), (145, 585), (815, 585), 1)

        back_text = font_small.render("Pulsa ESC para volver al menu principal", True, SOFT_TEXT)
        screen.blit(back_text, (150, 610))

        hint = font_small.render("CyberGuardian Security Interface", True, (0, 190, 210))
        screen.blit(hint, (925, 635))

        pygame.display.flip()
        clock.tick(FPS)


# ----------------------------------------------------
# PANTALLA DE CREDITOS
# ----------------------------------------------------
def credits_screen():
    font_title = pygame.font.Font(None, 78)
    font_section = pygame.font.Font(None, 38)
    font_text = pygame.font.Font(None, 32)
    font_small = pygame.font.Font(None, 26)

    bg_path = asset_path("assets", "sprites", "Fondos", "menu2.png")
    bg_credits = load_image_safe(bg_path, (WIDTH, HEIGHT))

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                return

        if bg_credits:
            screen.blit(bg_credits, (0, 0))
        else:
            screen.fill(DARK_BLUE)

        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 95))
        screen.blit(overlay, (0, 0))

        panel_rect = pygame.Rect(210, 70, 860, 580)
        draw_panel(screen, panel_rect, color=(2, 14, 26), alpha=225, border_color=CYAN)

        title = font_title.render("CREDITOS", True, CYAN)
        screen.blit(title, (panel_rect.centerx - title.get_width() // 2, 105))

        subtitle = font_small.render("CyberGuardian: Amenaza Xenon", True, SOFT_TEXT)
        screen.blit(subtitle, (panel_rect.centerx - subtitle.get_width() // 2, 170))

        pygame.draw.line(screen, CYAN, (280, 220), (1000, 220), 2)
        pygame.draw.circle(screen, CYAN, (280, 220), 5)
        pygame.draw.circle(screen, CYAN, (1000, 220), 5)

        y = 255

        creator_title = font_section.render("CREADOR", True, YELLOW)
        screen.blit(creator_title, (310, y))
        y += 42

        creator = font_text.render("Eduar Ferney Rodriguez Lopez", True, WHITE)
        screen.blit(creator, (350, y))
        y += 70

        tech_title = font_section.render("DESARROLLO", True, YELLOW)
        screen.blit(tech_title, (310, y))
        y += 42

        tech = font_text.render("Videojuego 2D desarrollado con Python y Pygame", True, WHITE)
        screen.blit(tech, (350, y))
        y += 70

        img_title = font_section.render("IMAGENES", True, YELLOW)
        screen.blit(img_title, (310, y))
        y += 42

        img_credit = font_text.render("Imagenes generadas con IA - OpenAI", True, WHITE)
        screen.blit(img_credit, (350, y))
        y += 70

        sound_title = font_section.render("EFECTOS DE SONIDO", True, YELLOW)
        screen.blit(sound_title, (310, y))
        y += 42

        sound_credit = font_text.render("", True, WHITE)
        screen.blit(sound_credit, (350, y))
        y += 65

        footer = font_small.render("", True, SOFT_TEXT)
        screen.blit(footer, (panel_rect.centerx - footer.get_width() // 2, 585))

        back_text = font_small.render("Pulsa ESC para volver al menu principal", True, CYAN)
        screen.blit(back_text, (panel_rect.centerx - back_text.get_width() // 2, 615))

        pygame.display.flip()
        clock.tick(FPS)


# ----------------------------------------------------
# MENU PRINCIPAL MEJORADO
# ----------------------------------------------------
def main_menu():
    font_logo = pygame.font.Font(None, 88)
    font_title_small = pygame.font.Font(None, 42)
    font_subtitle = pygame.font.Font(None, 31)
    font_info = pygame.font.Font(None, 28)

    music_path = asset_path("assets", "Musica", "Manu.mp3")
    if os.path.exists(music_path):
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.set_volume(0.55)
        pygame.mixer.music.play(-1)
    else:
        print(f"No se encontro la musica del menu: {music_path}")

    bg_path = asset_path("assets", "sprites", "Fondos", "menu1.png")
    bg_img = load_image_safe(bg_path, (WIDTH, HEIGHT))

    panel_rect = pygame.Rect(WIDTH // 2 - 315, 75, 630, 585)

    btn_play = Button("INICIAR MISION", WIDTH // 2 - 170, 340, 340, 62, CYAN_DARK, CYAN)
    btn_controls = Button("CONTROLES", WIDTH // 2 - 170, 415, 340, 62, (0, 120, 155), (0, 210, 230))
    btn_credits = Button("CREDITOS", WIDTH // 2 - 170, 490, 340, 62, (90, 40, 150), (160, 80, 230))
    btn_exit = Button("SALIR", WIDTH // 2 - 170, 565, 340, 62, RED_DARK, RED)

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if btn_play.is_clicked(e):
                pygame.mixer.music.stop()
                pygame.time.delay(150)
                main_nivel1()

            if btn_controls.is_clicked(e):
                controls_screen()

            if btn_credits.is_clicked(e):
                credits_screen()

            if btn_exit.is_clicked(e):
                pygame.quit()
                sys.exit()

        # Fondo del menu principal
        if bg_img:
            screen.blit(bg_img, (0, 0))
        else:
            screen.fill(DARK_BLUE)

        # Oscurecer fondo
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 95))
        screen.blit(overlay, (0, 0))

        # Panel central
        draw_panel(screen, panel_rect, color=(2, 14, 26), alpha=215, border_color=CYAN)

        # Titulo principal
        title = font_logo.render("CYBERGUARDIAN", True, WHITE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 115))

        # Subtitulo
        title_2 = font_title_small.render("AMENAZA XENON", True, CYAN)
        screen.blit(title_2, (WIDTH // 2 - title_2.get_width() // 2, 190))

        # Linea decorativa
        pygame.draw.line(screen, CYAN, (WIDTH // 2 - 230, 245), (WIDTH // 2 + 230, 245), 3)
        pygame.draw.circle(screen, CYAN, (WIDTH // 2 - 230, 245), 5)
        pygame.draw.circle(screen, CYAN, (WIDTH // 2 + 230, 245), 5)

        # Texto de historia corto
        story_1 = font_subtitle.render("Cyber debe infiltrarse en la red central", True, SOFT_TEXT)
        story_2 = font_subtitle.render("y detener la propagacion de Xenon.", True, SOFT_TEXT)

        screen.blit(story_1, (WIDTH // 2 - story_1.get_width() // 2, 270))
        screen.blit(story_2, (WIDTH // 2 - story_2.get_width() // 2, 300))

        # Botones
        btn_play.draw(screen)
        btn_controls.draw(screen)
        btn_credits.draw(screen)
        btn_exit.draw(screen)

        # Texto inferior del panel
        footer = font_info.render("Sistema de defensa digital activo", True, (0, 210, 220))
        screen.blit(footer, (WIDTH // 2 - footer.get_width() // 2, 635))

        # Decoraciones laterales
        left_info_rect = pygame.Rect(55, 570, 280, 70)
        right_info_rect = pygame.Rect(945, 570, 280, 70)

        draw_panel(screen, left_info_rect, color=(2, 14, 26), alpha=160, border_color=(0, 150, 180))
        draw_panel(screen, right_info_rect, color=(2, 14, 26), alpha=160, border_color=(0, 150, 180))

        left_info = font_info.render("Atlas: Comando activo", True, SOFT_TEXT)
        right_info = font_info.render("Lana: Enlace seguro", True, SOFT_TEXT)

        screen.blit(left_info, (left_info_rect.centerx - left_info.get_width() // 2, left_info_rect.y + 25))
        screen.blit(right_info, (right_info_rect.centerx - right_info.get_width() // 2, right_info_rect.y + 25))

        pygame.display.flip()
        clock.tick(FPS)


# ----------------------------------------------------
# EJECUTAR MENU
# ----------------------------------------------------
if __name__ == "__main__":
    main_menu()