import pygame
import sys
import subprocess
import time
import math
import random
import os
from pygame.locals import *

# Inicializar pygame y mixer
pygame.init()
pygame.mixer.init()

# Configuración de pantalla moderna
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("El Viaje Escolar de Memo")
clock = pygame.time.Clock()

print("=== VERIFICANDO ARCHIVOS ===")

# Verificar archivos de imágenes
required_files = ["escuela.png", "empresa.png"]
for file in required_files:
    if os.path.exists(file):
        print(f"OK: {file} encontrado")
    else:
        print(f"FALTA: {file} - Se usara placeholder")

# Intentar cargar música de fondo
if os.path.exists("fondo_musical.mp3"):
    try:
        pygame.mixer.music.load("fondo_musical.mp3")
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)
        music_loaded = True
        print("OK: Musica de fondo cargada")
    except:
        music_loaded = False
        print("ERROR: No se pudo cargar la musica")
else:
    music_loaded = False
    print("INFO: fondo_musical.mp3 no encontrado")

# Paleta de colores moderna y profesional
COLORS = {
    "background": (10, 15, 30),
    "dark_blue": (20, 30, 50),
    "medium_blue": (40, 60, 100),
    "light_blue": (70, 130, 220),
    "accent_blue": (30, 150, 255),
    "white": (245, 245, 255),
    "light_gray": (200, 210, 220),
    "gray": (120, 130, 140),
    "gold": (255, 200, 50),
    "light_gold": (255, 220, 100),
    "success_green": (70, 220, 120),
    "error_red": (220, 80, 80)
}

# Cargar fuentes
try:
    title_font_large = pygame.font.SysFont("arial", 72, bold=True)
    title_font = pygame.font.SysFont("arial", 48, bold=True)
    subtitle_font = pygame.font.SysFont("arial", 36, bold=True)
    heading_font = pygame.font.SysFont("arial", 32)
    body_font = pygame.font.SysFont("arial", 24)
    button_font = pygame.font.SysFont("arial", 28, bold=True)
    caption_font = pygame.font.SysFont("arial", 18)
except:
    title_font_large = pygame.font.Font(None, 72)
    title_font = pygame.font.Font(None, 48)
    subtitle_font = pygame.font.Font(None, 36)
    heading_font = pygame.font.Font(None, 32)
    body_font = pygame.font.Font(None, 24)
    button_font = pygame.font.Font(None, 28)
    caption_font = pygame.font.Font(None, 18)

# Clase para botones modernos
class ModernButton:
    def __init__(self, x, y, width, height, text, 
                 color=COLORS["medium_blue"], hover_color=COLORS["light_blue"],
                 text_color=COLORS["white"]):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.hovered = False
        
    def draw(self, surface):
        current_color = self.hover_color if self.hovered else self.color
        
        pygame.draw.rect(surface, current_color, self.rect, border_radius=8)
        pygame.draw.rect(surface, COLORS["accent_blue"], self.rect, 2, border_radius=8)
        
        text_surf = button_font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
        
        if self.hovered:
            highlight = pygame.Surface((self.rect.width, 30), pygame.SRCALPHA)
            highlight.fill((255, 255, 255, 30))
            surface.blit(highlight, (self.rect.x, self.rect.y))
    
    def update(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)
        return self.hovered
    
    def handle_event(self, event):
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            if self.hovered:
                return True
        return False

def draw_text(surface, text, font, color, x, y, centered=True):
    text_surf = font.render(text, True, color)
    if centered:
        text_rect = text_surf.get_rect(center=(x, y))
    else:
        text_rect = text_surf.get_rect(topleft=(x, y))
    surface.blit(text_surf, text_rect)
    return text_rect

def fade_transition(duration=0.5, fade_in=True):
    fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    fade_surface.fill((0, 0, 0))
    
    steps = 30
    for i in range(steps + 1):
        alpha = int(255 * (i / steps))
        if fade_in:
            alpha = 255 - alpha
        
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        pygame.display.flip()
        pygame.time.delay(int(duration * 1000 / steps))

def load_and_scale_image(filename, max_width, max_height):
    try:
        image = pygame.image.load(filename).convert_alpha()
        img_width, img_height = image.get_size()
        
        scale = min(max_width / img_width, max_height / img_height)
        new_width = int(img_width * scale)
        new_height = int(img_height * scale)
        
        scaled_image = pygame.transform.smoothscale(image, (new_width, new_height))
        return scaled_image, new_width, new_height
    except Exception as e:
        print(f"Error cargando {filename}: {e}")
        return None, 0, 0

# Pantalla de créditos
def show_credits():
    screen.fill(COLORS["background"])
    
    # Fondo estrellado
    for _ in range(200):
        x = random.randint(0, SCREEN_WIDTH)
        y = random.randint(0, SCREEN_HEIGHT)
        size = random.randint(1, 3)
        brightness = random.randint(100, 255)
        pygame.draw.circle(screen, (brightness, brightness, brightness), (x, y), size)
    
    # Marco central
    card_width = 800
    card_height = 600
    card_x = (SCREEN_WIDTH - card_width) // 2
    card_y = (SCREEN_HEIGHT - card_height) // 2
    
    pygame.draw.rect(screen, (20, 25, 40), (card_x, card_y, card_width, card_height), border_radius=20)
    pygame.draw.rect(screen, COLORS["accent_blue"], (card_x, card_y, card_width, card_height), 3, border_radius=20)
    
    draw_text(screen, "DESARROLLADO POR", title_font, COLORS["gold"], SCREEN_WIDTH // 2, card_y + 60)
    
    # Línea decorativa
    line_y = card_y + 120
    pygame.draw.line(screen, COLORS["accent_blue"], 
                    (card_x + 100, line_y), 
                    (card_x + card_width - 100, line_y), 4)
    
    # Nombres del equipo
    team_members = [
        "Emmanuel Carrasco Tinoco",
        "Xochitl Perez Flores",
        "Gerson Caleb Salvador Romero",
        "Adan Cancino Mendoza",
        "Francisco Javier Flores Rivera",
        "Jose Manuel Davila Garcia",
        "Diego Ivan Luna Rodriguez"
    ]
    
    y_pos = card_y + 160
    for i, member in enumerate(team_members):
        color = COLORS["light_blue"] if i % 2 == 0 else COLORS["white"]
        draw_text(screen, member, heading_font, color, SCREEN_WIDTH // 2, y_pos)
        y_pos += 50
    
    # Instrucción
    current_time = pygame.time.get_ticks() / 1000.0
    if int(current_time * 2) % 2 == 0:
        draw_text(screen, "Presiona cualquier tecla para continuar", 
                  caption_font, COLORS["light_gray"], SCREEN_WIDTH // 2, card_y + card_height - 60)
    
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN or event.type == MOUSEBUTTONDOWN:
                waiting = False
    
    fade_transition(0.5, fade_in=False)

# Pantalla con imagen
def show_image_screen(title_text, image_filename):
    screen.fill(COLORS["background"])
    
    # Fondo con patrón
    for x in range(0, SCREEN_WIDTH, 80):
        pygame.draw.line(screen, (25, 35, 55), (x, 0), (x, SCREEN_HEIGHT), 1)
    for y in range(0, SCREEN_HEIGHT, 80):
        pygame.draw.line(screen, (25, 35, 55), (0, y), (SCREEN_WIDTH, y), 1)
    
    # Marco principal
    card_width = 900
    card_height = 550
    card_x = (SCREEN_WIDTH - card_width) // 2
    card_y = (SCREEN_HEIGHT - card_height) // 2
    
    pygame.draw.rect(screen, (25, 35, 60), (card_x, card_y, card_width, card_height), border_radius=20)
    pygame.draw.rect(screen, COLORS["accent_blue"], (card_x, card_y, card_width, card_height), 3, border_radius=20)
    
    # Título
    title_color = COLORS["light_blue"] if "ESCUELA" in title_text else COLORS["gold"]
    draw_text(screen, title_text, title_font, title_color, SCREEN_WIDTH // 2, card_y + 60)
    
    # Línea decorativa
    pygame.draw.line(screen, COLORS["accent_blue"], 
                    (card_x + 150, card_y + 120), 
                    (card_x + card_width - 150, card_y + 120), 3)
    
    # Cargar y mostrar imagen
    max_img_width = 700
    max_img_height = 320
    image, img_width, img_height = load_and_scale_image(image_filename, max_img_width, max_img_height)
    
    if image:
        img_x = card_x + (card_width - img_width) // 2
        img_y = card_y + 150
        
        # Marco para la imagen
        frame_padding = 15
        frame_rect = pygame.Rect(
            img_x - frame_padding, 
            img_y - frame_padding, 
            img_width + frame_padding * 2, 
            img_height + frame_padding * 2
        )
        
        pygame.draw.rect(screen, (40, 50, 80), frame_rect, border_radius=12)
        pygame.draw.rect(screen, COLORS["accent_blue"], frame_rect, 3, border_radius=12)
        
        screen.blit(image, (img_x, img_y))
        
        # Etiqueta
        label_y = img_y + img_height + 20
        label_text = "Logotipo Institucional" if "ESCUELA" in title_text else "Logotipo Corporativo"
        draw_text(screen, label_text, caption_font, COLORS["light_gray"], SCREEN_WIDTH // 2, label_y)
    else:
        # Placeholder si no hay imagen
        placeholder = pygame.Rect(card_x + 250, card_y + 150, 400, 250)
        pygame.draw.rect(screen, (40, 50, 80), placeholder, border_radius=12)
        pygame.draw.rect(screen, COLORS["accent_blue"], placeholder, 3, border_radius=12)
        
        draw_text(screen, f"IMAGEN: {image_filename}", body_font, COLORS["gray"], 
                  SCREEN_WIDTH // 2, card_y + 275)
        draw_text(screen, "Coloca la imagen en la carpeta del juego", 
                  caption_font, COLORS["gray"], SCREEN_WIDTH // 2, card_y + 310)
    
    # Instrucción
    current_time = pygame.time.get_ticks() / 1000.0
    if int(current_time * 2) % 2 == 0:
        draw_text(screen, "Presiona cualquier tecla para continuar", 
                  caption_font, COLORS["light_gray"], SCREEN_WIDTH // 2, card_y + card_height - 50)
    
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN or event.type == MOUSEBUTTONDOWN:
                waiting = False
    
    fade_transition(0.5, fade_in=False)

# Pantalla de historia
def show_story():
    story_pages = [
        [
            "En los rincones del vasto Colegio Galactico,",
            "donde la educacion y el combate se mezclan",
            "en un mismo destino, nace la leyenda de Memo,",
            "un estudiante excepcional que esta a un paso",
            "de su graduacion. Pero aqui nada es sencillo:",
            "antes de recibir su diploma, debera enfrentar",
            "la prueba definitiva."
        ],
        [
            "Las materias ya no son simples clases; cada una",
            "ha tomado forma como un campo de batalla espacial.",
            "Los profesores, ahora convertidos en poderosas",
            "entidades, defienden su territorio con desafios unicos.",
            "Memo tendra que cruzar 5 niveles, cada uno mas",
            "exigente que el anterior, donde el conocimiento",
            "se transforma en energia, el aprendizaje en",
            "armamento, y la valentia en la unica forma de avanzar."
        ],
        [
            "El Director del Colegio Galactico lo dejo claro:",
            '"Solo quien supere las cinco guerras academicas"',
            '"podra graduarse con honores."',
            "",
            "Con su nave lista y su determinacion al maximo,",
            "Memo inicia su viaje escolar definitivo.",
            "Lo espera una aventura epica llena de accion,",
            "obstaculos y enfrentamientos memorables."
        ],
        [
            "Su mision: vencer a cada profesor, aprobar sus",
            "materias... y reclamar el titulo que merece.",
            "",
            "Asi comienza El Viaje Escolar de Memo: una historia",
            "donde estudiar nunca habia sido tan peligroso...",
            "ni tan emocionante."
        ]
    ]
    
    current_page = 0
    btn_next = ModernButton(SCREEN_WIDTH - 220, SCREEN_HEIGHT - 80, 200, 50, "SIGUIENTE", COLORS["success_green"])
    btn_prev = ModernButton(20, SCREEN_HEIGHT - 80, 200, 50, "ANTERIOR", COLORS["medium_blue"])
    
    while current_page < len(story_pages):
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == KEYDOWN:
                if event.key == K_RIGHT or event.key == K_SPACE or event.key == K_RETURN:
                    if current_page < len(story_pages) - 1:
                        current_page += 1
                elif event.key == K_LEFT:
                    if current_page > 0:
                        current_page -= 1
            
            if btn_next.handle_event(event):
                if current_page < len(story_pages) - 1:
                    current_page += 1
            
            if btn_prev.handle_event(event):
                if current_page > 0:
                    current_page -= 1
        
        btn_next.update(mouse_pos)
        btn_prev.update(mouse_pos)
        
        # Dibujar pantalla
        screen.fill(COLORS["background"])
        
        # Fondo
        for i in range(100):
            x = (i * 17) % SCREEN_WIDTH
            y = (i * 13) % SCREEN_HEIGHT
            size = (i % 3) + 1
            color = (100, 150, 200) if i % 2 == 0 else (150, 200, 255)
            pygame.draw.circle(screen, color, (x, y), size)
        
        # Marco de la historia
        story_rect = pygame.Rect(50, 50, SCREEN_WIDTH - 100, SCREEN_HEIGHT - 150)
        
        pygame.draw.rect(screen, (20, 30, 50), story_rect, border_radius=20)
        pygame.draw.rect(screen, COLORS["accent_blue"], story_rect, 3, border_radius=20)
        
        # Título
        draw_text(screen, "LA HISTORIA", title_font, COLORS["gold"], SCREEN_WIDTH // 2, 100)
        
        # Línea decorativa
        pygame.draw.line(screen, COLORS["accent_blue"], 
                        (100, 150), (SCREEN_WIDTH - 100, 150), 3)
        
        # Texto de la historia
        story_lines = story_pages[current_page]
        y_pos = 180
        
        for line in story_lines:
            draw_text(screen, line, body_font, COLORS["white"], SCREEN_WIDTH // 2, y_pos)
            y_pos += 40
        
        # Indicador de página
        page_text = f"Pagina {current_page + 1} de {len(story_pages)}"
        draw_text(screen, page_text, caption_font, COLORS["light_gray"], SCREEN_WIDTH // 2, SCREEN_HEIGHT - 130)
        
        # Botones
        if current_page > 0:
            btn_prev.draw(screen)
        
        if current_page < len(story_pages) - 1:
            btn_next.draw(screen)
        else:
            btn_finish = ModernButton(SCREEN_WIDTH - 220, SCREEN_HEIGHT - 80, 200, 50, "CONTINUAR", COLORS["success_green"])
            btn_finish.update(mouse_pos)
            btn_finish.draw(screen)
            
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    if btn_finish.rect.collidepoint(mouse_pos):
                        fade_transition(0.5, fade_in=False)
                        return
        
        # Instrucciones
        draw_text(screen, "Usa flechas izquierda/derecha o los botones", 
                  caption_font, COLORS["gray"], SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
        
        pygame.display.flip()
        clock.tick(60)

# Menú principal
def show_main_menu():
    btn_start = ModernButton(SCREEN_WIDTH // 2 - 150, 400, 300, 60, "INICIAR AVENTURA", COLORS["success_green"])
    btn_exit = ModernButton(SCREEN_WIDTH // 2 - 150, 480, 300, 60, "SALIR", COLORS["error_red"])
    
    running = True
    start_time = pygame.time.get_ticks()
    
    while running:
        current_time = (pygame.time.get_ticks() - start_time) / 1000.0
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
                pygame.quit()
                sys.exit()
            
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                    pygame.quit()
                    sys.exit()
                elif event.key == K_RETURN or event.key == K_SPACE:
                    fade_transition(0.5, fade_in=False)
                    if music_loaded:
                        pygame.mixer.music.fadeout(500)
                    
                    try:
                        subprocess.run([sys.executable, "nivel1.py"])
                    except:
                        print("No se pudo ejecutar nivel1.py")
                        show_error_message("No se encontro nivel1.py")
                        pygame.time.delay(2000)
                    
                    if music_loaded:
                        pygame.mixer.music.play(-1)
                    return
            
            if btn_start.handle_event(event):
                fade_transition(0.5, fade_in=False)
                if music_loaded:
                    pygame.mixer.music.fadeout(500)
                
                try:
                    subprocess.run([sys.executable, "nivel1.py"])
                except:
                    print("No se pudo ejecutar nivel1.py")
                    show_error_message("No se encontro nivel1.py")
                    pygame.time.delay(2000)
                
                if music_loaded:
                    pygame.mixer.music.play(-1)
                return
            
            if btn_exit.handle_event(event):
                running = False
                pygame.quit()
                sys.exit()
        
        btn_start.update(mouse_pos)
        btn_exit.update(mouse_pos)
        
        # Dibujar fondo
        screen.fill(COLORS["background"])
        
        # Estrellas animadas
        for i in range(150):
            x = (i * 23 + current_time * 50) % SCREEN_WIDTH
            y = (i * 17 + current_time * 30) % SCREEN_HEIGHT
            size = 1 + math.sin(current_time + i) * 0.5
            brightness = 150 + int(100 * math.sin(current_time * 2 + i))
            pygame.draw.circle(screen, (brightness, brightness, brightness), (int(x), int(y)), int(size))
        
        # Marco del menú
        menu_rect = pygame.Rect(SCREEN_WIDTH // 2 - 350, 80, 700, 600)
        
        pygame.draw.rect(screen, (20, 30, 50, 200), menu_rect, border_radius=25)
        pygame.draw.rect(screen, COLORS["accent_blue"], menu_rect, 3, border_radius=25)
        
        # Título principal
        pulse = 0.5 + 0.5 * math.sin(current_time * 2)
        title_color = (
            int(COLORS["light_blue"][0] * pulse),
            int(COLORS["light_blue"][1] * pulse),
            int(COLORS["light_blue"][2] * pulse)
        )
        
        draw_text(screen, "EL VIAJE ESCOLAR", title_font_large, title_color, SCREEN_WIDTH // 2, 150)
        draw_text(screen, "DE MEMO", subtitle_font, COLORS["gold"], SCREEN_WIDTH // 2, 220)
        
        # Icono de nave
        ship_x, ship_y = SCREEN_WIDTH // 2, 320
        ship_angle = math.sin(current_time) * 10
        
        # Cuerpo de la nave
        pygame.draw.polygon(screen, COLORS["accent_blue"], [
            (ship_x, ship_y - 40),
            (ship_x + 50, ship_y + 20),
            (ship_x, ship_y + 40),
            (ship_x - 50, ship_y + 20)
        ])
        
        # Motor animado
        flame_size = 15 + 10 * math.sin(current_time * 5)
        pygame.draw.polygon(screen, COLORS["gold"], [
            (ship_x - 50, ship_y - 15),
            (ship_x - 50 - flame_size, ship_y),
            (ship_x - 50, ship_y + 15)
        ])
        
        # Línea decorativa
        line_y = 370
        pygame.draw.line(screen, COLORS["accent_blue"], 
                        (SCREEN_WIDTH // 2 - 200, line_y),
                        (SCREEN_WIDTH // 2 + 200, line_y), 2)
        
        # Botones
        btn_start.draw(screen)
        btn_exit.draw(screen)
        
        # Instrucciones
        if int(current_time * 2) % 2 == 0:
            draw_text(screen, "Presiona ENTER o haz clic para iniciar", 
                      caption_font, COLORS["light_gray"], SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60)
        
        # Créditos
        draw_text(screen, "(c) 2024 Colegio Galactico Interactive", 
                  caption_font, COLORS["gray"], SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30)
        
        pygame.display.flip()
        clock.tick(60)

def show_error_message(message):
    screen.fill(COLORS["error_red"])
    draw_text(screen, "ERROR", title_font, COLORS["white"], SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)
    draw_text(screen, message, body_font, COLORS["white"], SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20)
    pygame.display.flip()

def show_loading():
    screen.fill(COLORS["background"])
    
    draw_text(screen, "INICIALIZANDO SISTEMA...", title_font, COLORS["white"],
              SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100)
    
    bar_width = 500
    bar_height = 25
    bar_x = (SCREEN_WIDTH - bar_width) // 2
    bar_y = SCREEN_HEIGHT // 2
    
    for progress in range(101):
        screen.fill(COLORS["background"])
        
        draw_text(screen, "INICIALIZANDO SISTEMA...", title_font, COLORS["white"],
                  SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100)
        
        pygame.draw.rect(screen, COLORS["dark_blue"], 
                        (bar_x, bar_y, bar_width, bar_height), 
                        border_radius=12)
        
        progress_width = int(bar_width * (progress / 100))
        pygame.draw.rect(screen, COLORS["accent_blue"], 
                        (bar_x, bar_y, progress_width, bar_height), 
                        border_radius=12)
        
        draw_text(screen, f"{progress}%", caption_font, COLORS["white"],
                  SCREEN_WIDTH // 2, bar_y + bar_height + 20)
        
        if progress < 30:
            status = "Cargando recursos graficos..."
        elif progress < 60:
            status = "Inicializando sistema de audio..."
        elif progress < 90:
            status = "Preparando interfaz..."
        else:
            status = "Listo para iniciar..."
        
        draw_text(screen, status, body_font, COLORS["light_gray"],
                  SCREEN_WIDTH // 2, bar_y + bar_height + 60)
        
        pygame.display.flip()
        pygame.time.delay(20)

def main():
    print("\n" + "="*50)
    print("EL VIAJE ESCOLAR DE MEMO - MENU PRINCIPAL")
    print("="*50)
    
    try:
        # Animación de carga
        show_loading()
        pygame.time.delay(500)
        
        # Pantalla de créditos
        fade_transition(0.8, fade_in=True)
        show_credits()
        fade_transition(0.8, fade_in=True)
        
        # Pantalla ESCUELA con imagen
        print("\nMostrando pantalla: ESCUELA")
        show_image_screen("ESCUELA", "escuela.png")
        fade_transition(0.8, fade_in=True)
        
        # Pantalla EMPRESA con imagen
        print("Mostrando pantalla: EMPRESA")
        show_image_screen("EMPRESA", "empresa.png")
        fade_transition(0.8, fade_in=True)
        
        # Historia
        print("Mostrando historia...")
        show_story()
        fade_transition(0.8, fade_in=True)
        
        # Menú principal
        print("Mostrando menu principal...")
        show_main_menu()
        
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        
        screen.fill(COLORS["error_red"])
        draw_text(screen, "ERROR CRITICO", title_font, COLORS["white"],
                  SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)
        draw_text(screen, str(e), body_font, COLORS["white"],
                  SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20)
        draw_text(screen, "Presiona cualquier tecla para salir", 
                  caption_font, COLORS["white"],
                  SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80)
        pygame.display.flip()
        
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type in (QUIT, KEYDOWN, MOUSEBUTTONDOWN):
                    waiting = False
    
    finally:
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()