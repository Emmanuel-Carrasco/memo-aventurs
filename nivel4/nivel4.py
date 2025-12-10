import pygame
import sys
import random
import cv2
import numpy as np
import math
import os
import subprocess

# --- CONFIGURACIÓN GENERAL ---
pygame.init()
pygame.mixer.init()

ANCHO = 1200
ALTO = 760
FPS = 90

PANTALLA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Nivel 4 - Batalla Final")

# COLORES
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
AMARILLO = (255, 255, 0)
NARANJA = (255, 165, 0)
GRIS_OSCURO = (50, 50, 50)
PURPURA = (128, 0, 128)
CYAN = (0, 255, 255)
VERDE_NEON = (57, 255, 20)
AZUL_ELECTRICO = (0, 191, 255)
ROSA_NEON = (255, 20, 147)
PURPURA_NEON = (180, 0, 255)
CIAN_NEON = (0, 255, 255)

# COLORES BLOQUES TETRIS
COLOR_T = (180, 0, 255)    # Púrpura (Tetromino T)
COLOR_I = (0, 255, 255)    # Cian (Tetromino I)
COLOR_O = (255, 255, 0)    # Amarillo (Tetromino O)
COLOR_J = (0, 0, 255)      # Azul (Tetromino J)
COLOR_L = (255, 165, 0)    # Naranja (Tetromino L)
COLOR_S = (0, 255, 0)      # Verde (Tetromino S)
COLOR_Z = (255, 0, 0)      # Rojo (Tetromino Z)

# FUENTES
FUENTE_GRANDE = pygame.font.SysFont("Arial", 60, bold=True)
FUENTE_MEDIANA = pygame.font.SysFont("Arial", 40, bold=True)
FUENTE_PEQ = pygame.font.SysFont("Arial", 20)
FUENTE_TITULO = pygame.font.SysFont("Arial", 80, bold=True)
FUENTE_ARCADA = pygame.font.SysFont("Courier New", 24, bold=True)
FUENTE_HISTORIA = pygame.font.SysFont("Courier New", 30, bold=True)
FUENTE_SUBTITULO = pygame.font.SysFont("Courier New", 36, bold=True)

# --- CARGA DE RECURSOS ---
def cargar_imagen(nombre, escala=None, alpha=True):
    try:
        ruta_nivel4 = os.path.join("nivel4", nombre)
        if os.path.exists(ruta_nivel4):
            if alpha:
                img = pygame.image.load(ruta_nivel4).convert_alpha()
            else:
                img = pygame.image.load(ruta_nivel4).convert()
        else:
            ruta_nivel2 = os.path.join("nivel2", nombre)
            if os.path.exists(ruta_nivel2):
                if alpha:
                    img = pygame.image.load(ruta_nivel2).convert_alpha()
                else:
                    img = pygame.image.load(ruta_nivel2).convert()
            else:
                if alpha:
                    img = pygame.image.load(nombre).convert_alpha()
                else:
                    img = pygame.image.load(nombre).convert()
        
        if escala:
            img = pygame.transform.scale(img, escala)
        return img
    except Exception as e:
        print(f"Error al cargar imagen {nombre}: {e}")
        if escala:
            surf = pygame.Surface(escala)
        else:
            surf = pygame.Surface((100, 100))
        surf.fill(ROJO)
        return surf

# Imágenes
IMG_NAVE = cargar_imagen("nave.png", (60, 40))
IMG_JEFE = cargar_imagen("jefe_nivel4.png", (300, 300))
IMG_FONDO = cargar_imagen("fondo_nivel4.png")
IMG_WINNER = cargar_imagen("winner.png", (400, 200))
IMG_VIDA_ICONO = cargar_imagen("vidas.png", (30, 30))

# Imágenes para potenciadores
IMG_MISIL = cargar_imagen("misil.png", (50, 25))
IMG_BOMBA = cargar_imagen("bomba.png", (50, 50))
IMG_ESCUDO = cargar_imagen("escudo.png", (60, 60))

# Imágenes para las pantallas de historia
IMG_HISTORIA_INICIO = cargar_imagen("historia_inicio_nivel4.png", (ANCHO, ALTO), alpha=True)
IMG_HISTORIA_FINAL = cargar_imagen("historia_final_nivel4.png", (ANCHO, ALTO), alpha=True)

# Escalar fondo
if IMG_FONDO.get_size() != (ANCHO, ALTO):
    IMG_FONDO = pygame.transform.scale(IMG_FONDO, (ANCHO, ALTO))

# Sonidos
def cargar_sonido(nombre):
    try:
        ruta_nivel4 = os.path.join("nivel4", nombre)
        if os.path.exists(ruta_nivel4):
            return pygame.mixer.Sound(ruta_nivel4)
        else:
            ruta_nivel2 = os.path.join("nivel2", nombre)
            if os.path.exists(ruta_nivel2):
                return pygame.mixer.Sound(ruta_nivel2)
            else:
                return pygame.mixer.Sound(nombre)
    except:
        return None

SND_DISPARO = cargar_sonido("disparo.mp3")
SND_CONTEO = cargar_sonido("conteo.mp3")
SND_COIN = cargar_sonido("coin.mp3")
SND_GAMEOVER = cargar_sonido("gameover.mp3")
SND_EXPLOSION = cargar_sonido("explosion.mp3")
SND_POWERUP = cargar_sonido("powerup.mp3")
SND_VICTORY = cargar_sonido("victory.mp3")
SND_FUEGOS_ARTIFICIALES = cargar_sonido("fuegos_artificiales.mp3")
SND_CAIDA_FUEGO = cargar_sonido("caida_fuego.mp3")
SND_TETRIS_MOVE = cargar_sonido("tetris_move.mp3")
SND_BOSS_HURT = cargar_sonido("boss_hurt.mp3")
SND_BOSS_TRANSFORM = cargar_sonido("boss_transform.mp3")

# --- FUNCIÓN PARA CARGAR SIGUIENTE NIVEL ---
def cargar_siguiente_nivel():
    """Intenta cargar el siguiente nivel (nivel5.py) desde la carpeta nivel5"""
    try:
        # Verificar si existe la carpeta nivel5
        if os.path.exists("nivel5"):
            print("Cargando nivel 5...")
            
            # Buscar el archivo nivel5.py
            archivo_nivel5 = os.path.join("nivel5", "nivel5.py")
            if os.path.exists(archivo_nivel5):
                print(f"Encontrado: {archivo_nivel5}")
                
                # Cerrar Pygame completamente antes de abrir el nuevo nivel
                pygame.quit()
                
                # Usar subprocess para ejecutar el nuevo nivel como un proceso separado
                subprocess.Popen([sys.executable, archivo_nivel5])
                
                # Salir del juego actual
                sys.exit(0)
                
            else:
                print(f"Archivo nivel5.py no encontrado en la carpeta 'nivel5'")
                print(f"Buscando en: {os.path.abspath('nivel5')}")
                
                # Mostrar mensaje de error en pantalla
                mensaje_error = "Nivel 5 no disponible aún"
                return False, mensaje_error
        else:
            print("Carpeta 'nivel5' no encontrada")
            mensaje_error = "Carpeta 'nivel5' no encontrada"
            return False, mensaje_error
            
    except Exception as e:
        print(f"Error al cargar nivel 5: {e}")
        mensaje_error = f"Error: {str(e)[:50]}..."
        return False, mensaje_error
    
    return True, ""

# --- CLASES ---

class PantallaHistoriaDerecha:
    def __init__(self, imagen_fondo, titulo, subtitulo, texto_historia):
        self.imagen_fondo = imagen_fondo
        self.titulo = titulo
        self.subtitulo = subtitulo
        self.texto_historia = texto_historia
        
        self.palabras = texto_historia.split()
        self.palabras_mostradas = 0
        self.temporizador_palabra = 0
        self.intervalo_palabra = 80
        self.tiempo_inicio = 0
        
        self.efecto_brillo = 0
        self.direccion_brillo = 1
        self.particulas = []
        self.generar_particulas()
        
        self.ancho_panel = 550
        self.margen_panel = 40
        
        self.terminada = False
        self.saltar = False
        
        self.sonido_escritura = cargar_sonido("teclado.mp3")
        
        self.alpha_panel = 0
        self.alpha_texto = 0
        self.fase_transicion = 0
    
    def generar_particulas(self):
        self.particulas = []
        for _ in range(30):
            x = random.randint(0, ANCHO)
            y = random.randint(0, ALTO)
            velocidad_x = random.uniform(-0.3, 0.3)
            velocidad_y = random.uniform(-0.3, 0.3)
            tamaño = random.randint(1, 2)
            vida = random.randint(50, 150)
            color = random.choice([AZUL_ELECTRICO, VERDE_NEON, ROSA_NEON, AMARILLO])
            self.particulas.append([x, y, velocidad_x, velocidad_y, tamaño, vida, color])
    
    def actualizar_particulas(self):
        for i, particula in enumerate(self.particulas):
            particula[0] += particula[2]
            particula[1] += particula[3]
            particula[5] -= 1
            
            if particula[5] <= 0:
                x = random.randint(0, ANCHO)
                y = random.randint(0, ALTO)
                velocidad_x = random.uniform(-0.3, 0.3)
                velocidad_y = random.uniform(-0.3, 0.3)
                tamaño = random.randint(1, 2)
                vida = random.randint(50, 150)
                color = random.choice([AZUL_ELECTRICO, VERDE_NEON, ROSA_NEON, AMARILLO])
                self.particulas[i] = [x, y, velocidad_x, velocidad_y, tamaño, vida, color]
    
    def actualizar(self, dt):
        if self.saltar:
            self.terminada = True
            return
        
        self.efecto_brillo += 0.05 * self.direccion_brillo
        if self.efecto_brillo > 1.0 or self.efecto_brillo < 0.0:
            self.direccion_brillo *= -1
        
        self.actualizar_particulas()
        
        if self.fase_transicion == 0:
            self.alpha_panel = min(255, self.alpha_panel + 5)
            if self.alpha_panel >= 255:
                self.fase_transicion = 1
        elif self.fase_transicion == 1:
            self.alpha_texto = min(255, self.alpha_texto + 3)
            if self.alpha_texto >= 255:
                self.fase_transicion = 2
        
        if self.fase_transicion >= 1:
            self.temporizador_palabra += dt
            
            if self.temporizador_palabra >= self.intervalo_palabra:
                if self.palabras_mostradas < len(self.palabras):
                    if self.sonido_escritura and random.random() < 0.3:
                        self.sonido_escritura.play()
                    
                    self.palabras_mostradas += 1
                    self.temporizador_palabra = 0
                else:
                    if self.tiempo_inicio == 0:
                        self.tiempo_inicio = pygame.time.get_ticks()
                    elif pygame.time.get_ticks() - self.tiempo_inicio > 3000:
                        self.terminada = True
    
    def dibujar(self, pantalla):
        pantalla.blit(self.imagen_fondo, (0, 0))
        
        for particula in self.particulas:
            x, y, _, _, tamaño, vida, color = particula
            alpha = min(255, vida * 2)
            s = pygame.Surface((tamaño*2, tamaño*2), pygame.SRCALPHA)
            pygame.draw.circle(s, (*color[:3], alpha), (tamaño, tamaño), tamaño)
            pantalla.blit(s, (int(x), int(y)))
        
        panel_surface = pygame.Surface((self.ancho_panel, ALTO), pygame.SRCALPHA)
        panel_color = (10, 10, 20, int(self.alpha_panel * 0.9))
        pygame.draw.rect(panel_surface, panel_color, (0, 0, self.ancho_panel, ALTO))
        
        borde_color = list(AZUL_ELECTRICO)
        borde_color = [int(c * (0.7 + 0.3 * self.efecto_brillo)) for c in borde_color]
        pygame.draw.rect(panel_surface, (*borde_color, int(self.alpha_panel)), 
                        (0, 0, self.ancho_panel, ALTO), 4)
        
        tiempo = pygame.time.get_ticks() * 0.002
        scan_y = int((math.sin(tiempo) * 0.5 + 0.5) * ALTO)
        pygame.draw.line(panel_surface, (0, 255, 255, 100), 
                        (10, scan_y), (self.ancho_panel - 10, scan_y), 2)
        
        pantalla.blit(panel_surface, (ANCHO - self.ancho_panel, 0))
        
        titulo_color = list(CIAN_NEON)
        titulo_color = [int(c * (0.8 + 0.2 * self.efecto_brillo)) for c in titulo_color]
        titulo_alpha = min(255, int(self.alpha_texto))
        
        titulo_surf = FUENTE_TITULO.render(self.titulo, True, (*titulo_color, titulo_alpha))
        titulo_rect = titulo_surf.get_rect(center=(ANCHO - self.ancho_panel//2, 100))
        
        titulo_sombra = FUENTE_TITULO.render(self.titulo, True, (0, 100, 150, titulo_alpha))
        pantalla.blit(titulo_sombra, (titulo_rect.x + 4, titulo_rect.y + 4))
        pantalla.blit(titulo_surf, titulo_rect)
        
        subtitulo_alpha = min(255, int(self.alpha_texto * 0.9))
        subtitulo_surf = FUENTE_SUBTITULO.render(self.subtitulo, True, (VERDE_NEON[0], VERDE_NEON[1], VERDE_NEON[2], subtitulo_alpha))
        subtitulo_rect = subtitulo_surf.get_rect(center=(ANCHO - self.ancho_panel//2, 170))
        pantalla.blit(subtitulo_surf, subtitulo_rect)
        
        pygame.draw.line(pantalla, (PURPURA_NEON[0], PURPURA_NEON[1], PURPURA_NEON[2], subtitulo_alpha),
                        (ANCHO - self.ancho_panel + 50, 210),
                        (ANCHO - 50, 210), 3)
        
        texto_actual = " ".join(self.palabras[:self.palabras_mostradas])
        texto_x = ANCHO - self.ancho_panel + self.margen_panel
        texto_y = 250
        ancho_texto = self.ancho_panel - 2 * self.margen_panel
        
        palabras_linea = []
        linea_actual = []
        
        for palabra in texto_actual.split():
            linea_actual.append(palabra)
            linea_texto = " ".join(linea_actual)
            ancho_linea = FUENTE_HISTORIA.size(linea_texto)[0]
            
            if ancho_linea > ancho_texto:
                ultima_palabra = linea_actual.pop()
                palabras_linea.append(" ".join(linea_actual))
                linea_actual = [ultima_palabra]
        
        if linea_actual:
            palabras_linea.append(" ".join(linea_actual))
        
        y_pos = texto_y
        for i, linea in enumerate(palabras_linea):
            if y_pos < ALTO - 100:
                linea_alpha = min(255, int(self.alpha_texto * (1.0 - i * 0.1)))
                if linea_alpha > 0:
                    linea_surf = FUENTE_HISTORIA.render(linea, True, (BLANCO[0], BLANCO[1], BLANCO[2], linea_alpha))
                    pantalla.blit(linea_surf, (texto_x, y_pos))
                    y_pos += 40
        
        if self.palabras_mostradas < len(self.palabras) and self.fase_transicion >= 1:
            if (pygame.time.get_ticks() // 500) % 2 == 0:
                texto_hasta_ahora = " ".join(self.palabras[:self.palabras_mostradas])
                if palabras_linea:
                    ultima_linea = palabras_linea[-1]
                    cursor_x = texto_x + FUENTE_HISTORIA.size(ultima_linea)[0]
                    cursor_y = y_pos - 10
                else:
                    cursor_x = texto_x
                    cursor_y = texto_y
                
                cursor_height = 35
                cursor_alpha = min(255, int(self.alpha_texto))
                pygame.draw.rect(pantalla, (VERDE_NEON[0], VERDE_NEON[1], VERDE_NEON[2], cursor_alpha),
                               (cursor_x, cursor_y, 3, cursor_height))
        
        if self.palabras_mostradas >= len(self.palabras) and self.fase_transicion >= 1:
            if (pygame.time.get_ticks() // 500) % 2 == 0:
                continuar_alpha = min(255, int(self.alpha_texto))
                continuar_surf = FUENTE_ARCADA.render("Presiona ESPACIO para continuar", True, 
                                                    (AMARILLO[0], AMARILLO[1], AMARILLO[2], continuar_alpha))
                continuar_rect = continuar_surf.get_rect(center=(ANCHO - self.ancho_panel//2, ALTO - 60))
                
                continuar_sombra = FUENTE_ARCADA.render("Presiona ESPACIO para continuar", True, 
                                                       (NARANJA[0], NARANJA[1], NARANJA[2], continuar_alpha))
                pantalla.blit(continuar_sombra, (continuar_rect.x + 2, continuar_rect.y + 2))
                pantalla.blit(continuar_surf, continuar_rect)
    
    def manejar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    if self.palabras_mostradas < len(self.palabras):
                        self.palabras_mostradas = len(self.palabras)
                        self.tiempo_inicio = pygame.time.get_ticks()
                    else:
                        self.terminada = True
                elif evento.key == pygame.K_ESCAPE:
                    self.saltar = True
                    self.terminada = True
    
    def reiniciar(self):
        self.palabras_mostradas = 0
        self.temporizador_palabra = 0
        self.tiempo_inicio = 0
        self.terminada = False
        self.saltar = False
        self.alpha_panel = 0
        self.alpha_texto = 0
        self.fase_transicion = 0

class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image_original = IMG_NAVE
        self.image = self.image_original.copy()
        self.rect = self.image.get_rect()
        self.rect.center = (100, ALTO // 2)
        self.velocidad = 5
        
        self.vidas = 5
        self.vidas_iniciales = 5
        
        self.invulnerable = False
        self.tiempo_golpe = 0
        self.duracion_invulnerabilidad = 2000
        
        self.animacion_tiempo = 0
        self.offset_y = 0
        
        self.misiles = 0
        self.bombas = 0
        self.escudo_activo = False
        self.tiempo_escudo = 0
        self.duracion_escudo = 5000
        
        self.misiles_temporales_activos = False
        self.tiempo_misiles_temporales = 0
        self.duracion_misiles_temporales = 5000
        
        self.muertes = 0
        self.monedas_gastadas = 0
        
        self.ultimo_disparo = 0
        self.intervalo_disparo = 200

    def update(self):
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.velocidad
        if teclas[pygame.K_DOWN] and self.rect.bottom < ALTO:
            self.rect.y += self.velocidad
        if teclas[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.velocidad
        if teclas[pygame.K_RIGHT] and self.rect.right < ANCHO:
            self.rect.x += self.velocidad

        self.animacion_tiempo += 0.1
        self.offset_y = math.sin(self.animacion_tiempo) * 2
        self.rect.y += int(self.offset_y)
        
        if teclas[pygame.K_UP]:
            self.image = pygame.transform.rotate(self.image_original, 5)
        elif teclas[pygame.K_DOWN]:
            self.image = pygame.transform.rotate(self.image_original, -5)
        else:
            self.image = self.image_original.copy()
        
        nuevo_rect = self.image.get_rect(center=self.rect.center)
        self.rect = nuevo_rect

        if self.invulnerable:
            ahora = pygame.time.get_ticks()
            if ahora - self.tiempo_golpe > self.duracion_invulnerabilidad:
                self.invulnerable = False
                self.image.set_alpha(255)
            else:
                if (ahora // 200) % 2 == 0:
                    self.image.set_alpha(100)
                else:
                    self.image.set_alpha(255)
        else:
            self.image.set_alpha(255)
            
        if self.escudo_activo:
            ahora = pygame.time.get_ticks()
            if ahora - self.tiempo_escudo > self.duracion_escudo:
                self.escudo_activo = False
        
        if self.misiles_temporales_activos:
            ahora = pygame.time.get_ticks()
            if ahora - self.tiempo_misiles_temporales > self.duracion_misiles_temporales:
                self.misiles_temporales_activos = False

        if teclas[pygame.K_SPACE]:
            ahora = pygame.time.get_ticks()
            if ahora - self.ultimo_disparo > self.intervalo_disparo:
                self.disparar()
                self.ultimo_disparo = ahora

    def recibir_dano(self):
        if not self.invulnerable and not self.escudo_activo:
            self.vidas -= 1
            self.muertes += 1
            self.invulnerable = True
            self.tiempo_golpe = pygame.time.get_ticks()
            return True
        return False

    def disparar(self):
        if self.misiles_temporales_activos:
            return self.disparar_misil_temporal()
        else:
            bala = Bala(self.rect.right, self.rect.centery, es_jugador=True)
            all_sprites.add(bala)
            balas_jugador.add(bala)
            if SND_DISPARO: SND_DISPARO.play()
            return True
        
    def activar_escudo(self):
        self.escudo_activo = True
        self.tiempo_escudo = pygame.time.get_ticks()
        
    def activar_misiles_temporales(self):
        self.misiles_temporales_activos = True
        self.tiempo_misiles_temporales = pygame.time.get_ticks()
        
    def disparar_misil_temporal(self):
        objetivo = None
        distancia_minima = float('inf')
        
        if len(jefe_grupo) > 0:
            jefe = jefe_grupo.sprite
            distancia = math.sqrt((jefe.rect.centerx - self.rect.centerx)**2 + 
                                (jefe.rect.centery - self.rect.centery)**2)
            if distancia < distancia_minima:
                objetivo = jefe
        
        if objetivo:
            misil = MisilTeledirigido(self.rect.centerx, self.rect.centery, objetivo)
            all_sprites.add(misil)
            balas_jugador.add(misil)
            if SND_DISPARO: SND_DISPARO.play()
            return True
        return False
        
    def lanzar_bomba(self):
        if self.bombas > 0:
            bomba = Bomba(self.rect.centerx, self.rect.centery)
            all_sprites.add(bomba)
            self.bombas -= 1
            return True
        return False
        
    def resetear_posicion(self):
        """Reinicia la posición del jugador al centro izquierdo"""
        self.rect.center = (100, ALTO // 2)
        self.invulnerable = True
        self.tiempo_golpe = pygame.time.get_ticks()
        self.image.set_alpha(255)

# --- CLASE BALA BÁSICA ---
class Bala(pygame.sprite.Sprite):
    def __init__(self, x, y, es_jugador):
        super().__init__()
        self.es_jugador = es_jugador
        
        if es_jugador:
            self.image = pygame.Surface((15, 4), pygame.SRCALPHA)
            pygame.draw.rect(self.image, (0, 255, 255), (0, 0, 15, 4))
            pygame.draw.rect(self.image, (255, 255, 255), (0, 0, 5, 4))
            self.rect = self.image.get_rect(midleft=(x, y))
            self.velocidad_x = 8
        else:
            self.image = pygame.Surface((10, 10), pygame.SRCALPHA)
            pygame.draw.circle(self.image, (255, 100, 100), (5, 5), 5)
            pygame.draw.circle(self.image, (255, 200, 200), (5, 5), 3)
            self.rect = self.image.get_rect(center=(x, y))
            self.velocidad_x = -8
        
        self.velocidad_y = 0
        
    def update(self):
        self.rect.x += self.velocidad_x
        self.rect.y += self.velocidad_y
        
        if (self.rect.right < 0 or self.rect.left > ANCHO or 
            self.rect.bottom < 0 or self.rect.top > ALTO):
            self.kill()

# --- CLASES DE ATAQUES ESPECIALES SIMPLIFICADAS ---

class BalaEnergia(pygame.sprite.Sprite):
    def __init__(self, x, y, es_jugador, tamaño=30, color=None):
        super().__init__()
        self.es_jugador = es_jugador
        self.tamaño = tamaño
        self.color = color if color else (CIAN_NEON if es_jugador else ROJO)
        
        self.image = pygame.Surface((tamaño, tamaño), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (tamaño//2, tamaño//2), tamaño//2)
        color_interior = tuple(min(255, c + 50) for c in self.color)
        pygame.draw.circle(self.image, color_interior, (tamaño//2, tamaño//2), tamaño//4)
        pygame.draw.circle(self.image, BLANCO, (tamaño//2, tamaño//2), tamaño//8)
        
        self.rect = self.image.get_rect(center=(x, y))
        self.velocidad_x = -6 if not es_jugador else 10
        self.velocidad_y = 0
        
    def update(self):
        self.rect.x += self.velocidad_x
        self.rect.y += self.velocidad_y
        
        if (self.rect.right < 0 or self.rect.left > ANCHO or 
            self.rect.bottom < 0 or self.rect.top > ALTO):
            self.kill()

class BolaFuego(pygame.sprite.Sprite):
    def __init__(self, x, y, tamaño=50):
        super().__init__()
        self.tamaño = tamaño
        self.image = pygame.Surface((tamaño, tamaño), pygame.SRCALPHA)
        
        for i in range(3):
            radio = self.tamaño//2 - i * 5
            color = (255, 150 - i*30, 0, 200 - i*50)
            pygame.draw.circle(self.image, color, (tamaño//2, tamaño//2), radio)
        
        self.rect = self.image.get_rect(center=(x, y))
        self.velocidad_y = 4
        self.velocidad_x = random.uniform(-1, 1)
        
    def update(self):
        self.rect.y += self.velocidad_y
        self.rect.x += self.velocidad_x
        
        if self.rect.top > ALTO:
            self.kill()

class LaserHorizontal(pygame.sprite.Sprite):
    def __init__(self, y):
        super().__init__()
        self.duracion = 100
        self.temporizador = 0
        self.ancho = 8
        self.y = y
        
        self.image = pygame.Surface((ANCHO, self.ancho), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(ANCHO//2, y))
        
    def update(self):
        self.temporizador += 1
        if self.temporizador >= self.duracion:
            self.kill()
            
    def draw(self, surface):
        if self.temporizador < self.duracion - 20:
            brillo = (math.sin(pygame.time.get_ticks() * 0.01) * 0.5 + 0.5) * 200 + 55
            color = (255, int(brillo), 0, 200)
            
            pygame.draw.line(surface, color, (0, self.y), (ANCHO, self.y), self.ancho)
            
            for i in range(2):
                color_brillo = (255, min(255, int(brillo + i*30)), 50, 100)
                pygame.draw.line(surface, color_brillo, (0, self.y), (ANCHO, self.y), 3)

class OndaExpansiva(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.radio = 20
        self.radio_maximo = 350
        self.velocidad_crecimiento = 7
        self.color = (0, 200, 255)
        self.activo = True
        
        self.image = pygame.Surface((self.radio_maximo*2, self.radio_maximo*2), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(x, y))
        
    def update(self):
        self.radio += self.velocidad_crecimiento
        if self.radio >= self.radio_maximo:
            self.kill()
            
    def draw(self, surface):
        if self.activo:
            for i in range(4):
                radio_actual = self.radio - i * 35
                if radio_actual > 0:
                    alpha = 150 - i * 30
                    grosor = 5 - i
                    pygame.draw.circle(surface, (*self.color[:3], alpha), 
                                     self.rect.center, radio_actual, grosor)

# --- CLASES BLOQUES TETRIS ---

class BloqueTetris(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.tamaño = 40
        self.image = self.crear_bloque(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.velocidad = random.randint(5, 7)
        self.color = color
        
    def crear_bloque(self, color):
        bloque = pygame.Surface((self.tamaño, self.tamaño), pygame.SRCALPHA)
        pygame.draw.rect(bloque, color, (2, 2, self.tamaño-4, self.tamaño-4))
        pygame.draw.line(bloque, self.brillar_color(color, 30), (1, 1), (self.tamaño-2, 1), 2)
        pygame.draw.line(bloque, self.brillar_color(color, 30), (1, 1), (1, self.tamaño-2), 2)
        pygame.draw.line(bloque, self.oscurecer_color(color, 30), (2, self.tamaño-2), (self.tamaño-2, self.tamaño-2), 2)
        pygame.draw.line(bloque, self.oscurecer_color(color, 30), (self.tamaño-2, 2), (self.tamaño-2, self.tamaño-2), 2)
        return bloque
    
    def brillar_color(self, color, cantidad):
        return (min(255, color[0] + cantidad), 
                min(255, color[1] + cantidad), 
                min(255, color[2] + cantidad))
    
    def oscurecer_color(self, color, cantidad):
        return (max(0, color[0] - cantidad), 
                max(0, color[1] - cantidad), 
                max(0, color[2] - cantidad))
    
    def update(self):
        self.rect.x -= self.velocidad
        if self.rect.right < 0:
            self.kill()

class Tetromino(pygame.sprite.Group):
    def __init__(self, tipo, x, y):
        super().__init__()
        self.tipo = tipo
        self.color = self.obtener_color(tipo)
        self.velocidad = random.randint(5, 7)
        self.crear_pieza(x, y)
        
    def obtener_color(self, tipo):
        colores = {
            'I': COLOR_I, 'J': COLOR_J, 'L': COLOR_L,
            'O': COLOR_O, 'S': COLOR_S, 'T': COLOR_T, 'Z': COLOR_Z
        }
        return colores.get(tipo, COLOR_T)
    
    def crear_pieza(self, x, y):
        tamaño_bloque = 40
        patrones = {
            'I': [(0, 0), (1, 0), (2, 0), (3, 0)],
            'J': [(0, 0), (0, 1), (1, 1), (2, 1)],
            'L': [(0, 1), (1, 1), (2, 1), (2, 0)],
            'O': [(0, 0), (1, 0), (0, 1), (1, 1)],
            'S': [(1, 0), (2, 0), (0, 1), (1, 1)],
            'T': [(0, 1), (1, 1), (2, 1), (1, 0)],
            'Z': [(0, 0), (1, 0), (1, 1), (2, 1)]
        }
        
        patron = patrones.get(self.tipo, patrones['T'])
        for dx, dy in patron:
            bloque_x = x + (dx * tamaño_bloque)
            bloque_y = y + (dy * tamaño_bloque)
            bloque = BloqueTetris(bloque_x, bloque_y, self.color)
            self.add(bloque)
    
    def update(self):
        for bloque in self.sprites():
            bloque.rect.x -= self.velocidad
            if bloque.rect.right < 0:
                bloque.kill()

# --- CLASE JEFE NIVEL 4 SIMPLIFICADO ---

class JefeNivel4(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = IMG_JEFE
        self.rect = self.image.get_rect()
        self.rect.x = ANCHO - 250
        self.rect.y = ALTO // 2 - 150
        
        # 3 fases
        self.vida = 120
        self.vida_max = 120
        self.fase = 1
        self.velocidad_y = 1.5
        self.direccion_y = 1
        
        # Sistema de ataques
        self.temporizador_ataque = 0
        self.ataque_actual = 0
        self.duracion_ataque = 100
        self.cooldown_ataque = 80
        
        # Ataques especiales
        self.lasers = []
        self.ondas = []
        
        # Tetrominos
        self.tetrominos = []
        self.ultimo_tetromino = 0
        self.intervalo_tetrominos = 12000
        
        # Efectos
        self.tiempo_temblor = 0
        self.intensidad_temblor = 0
        self.animacion_dano = 0
        self.transformando = False

    def update(self):
        # Movimiento vertical
        self.rect.y += self.velocidad_y * self.direccion_y
        
        # Límites
        limite_superior = 50
        limite_inferior = ALTO - self.rect.height - 50
        
        if self.rect.y <= limite_superior:
            self.rect.y = limite_superior
            self.direccion_y = 1
        elif self.rect.y >= limite_inferior:
            self.rect.y = limite_inferior
            self.direccion_y = -1
        
        # Verificar cambio de fase
        self.verificar_fase()
        
        # Sistema de ciclo de ataques
        self.temporizador_ataque += 1
        
        if self.temporizador_ataque > self.duracion_ataque + self.cooldown_ataque:
            self.temporizador_ataque = 0
            self.cambiar_ataque()
        
        # Ejecutar ataque actual
        if self.temporizador_ataque < self.duracion_ataque:
            self.ejecutar_ataque()
        
        # Generar tetrominos
        ahora = pygame.time.get_ticks()
        if ahora - self.ultimo_tetromino > self.intervalo_tetrominos:
            self.generar_tetrominos()
            self.ultimo_tetromino = ahora
        
        # Actualizar efectos
        self.actualizar_efectos()
        
        # Animación de daño
        if self.animacion_dano > 0:
            self.animacion_dano -= 1
            self.image.set_alpha(150 + (self.animacion_dano * 10))
        else:
            self.image.set_alpha(255)

    def verificar_fase(self):
        if self.fase == 1 and self.vida <= 80:
            self.cambiar_fase(2)
        elif self.fase == 2 and self.vida <= 40:
            self.cambiar_fase(3)

    def cambiar_fase(self, nueva_fase):
        self.fase = nueva_fase
        self.transformando = True
        
        if SND_BOSS_TRANSFORM:
            SND_BOSS_TRANSFORM.play()
        
        # Limpiar ataques
        self.lasers = []
        self.ondas = []
        
        # Cambiar color
        if nueva_fase == 2:
            colored = pygame.Surface(self.image.get_size())
            colored.fill((1.2, 0.8, 0.8))
            final = self.image.copy()
            final.blit(colored, (0, 0), special_flags=pygame.BLEND_MULT)
            self.image = final
        elif nueva_fase == 3:
            colored = pygame.Surface(self.image.get_size())
            colored.fill((0.8, 0.6, 1.2))
            final = self.image.copy()
            final.blit(colored, (0, 0), special_flags=pygame.BLEND_MULT)
            self.image = final
        
        self.transformando = False
        self.activar_temblor(10)

    def cambiar_ataque(self):
        if self.fase == 1:
            self.ataque_actual = (self.ataque_actual + 1) % 3
        elif self.fase == 2:
            self.ataque_actual = (self.ataque_actual + 1) % 4
        elif self.fase == 3:
            self.ataque_actual = (self.ataque_actual + 1) % 5
        self.activar_temblor(4)

    def ejecutar_ataque(self):
        if self.fase == 1:
            if self.ataque_actual == 0:
                self.disparo_triple()
            elif self.ataque_actual == 1:
                self.laser_horizontal()
            elif self.ataque_actual == 2:
                self.lluvia_fuego()
        elif self.fase == 2:
            if self.ataque_actual == 0:
                self.disparo_cruz()
            elif self.ataque_actual == 1:
                self.onda_expansiva()
            elif self.ataque_actual == 2:
                self.disparo_espiral()
            elif self.ataque_actual == 3:
                self.laser_horizontal()
        elif self.fase == 3:
            if self.ataque_actual == 0:
                self.disparo_todos_lados()
            elif self.ataque_actual == 1:
                self.onda_expansiva_doble()
            elif self.ataque_actual == 2:
                self.lluvia_fuego_densa()
            elif self.ataque_actual == 3:
                self.disparo_espiral_doble()
            elif self.ataque_actual == 4:
                self.laser_horizontal_doble()

    def disparo_triple(self):
        if self.temporizador_ataque % 40 == 0:
            for i in range(-1, 2):
                bala = BalaEnergia(self.rect.left, 
                                 self.rect.centery + (i*70), 
                                 es_jugador=False, 
                                 tamaño=35,
                                 color=PURPURA_NEON)
                all_sprites.add(bala)
                balas_enemigas.add(bala)

    def laser_horizontal(self):
        if self.temporizador_ataque == 50:
            y_pos = random.randint(100, ALTO - 100)
            laser = LaserHorizontal(y_pos)
            self.lasers.append(laser)

    def lluvia_fuego(self):
        if self.temporizador_ataque % 25 == 0:
            for _ in range(2):
                x = random.randint(200, ANCHO - 200)
                bola = BolaFuego(x, -50, tamaño=55)
                all_sprites.add(bola)
                balas_enemigas.add(bola)

    def disparo_cruz(self):
        if self.temporizador_ataque % 30 == 0:
            for angulo in [0, 90, 180, 270]:
                radianes = math.radians(angulo)
                velocidad_x = math.cos(radianes) * 5
                velocidad_y = math.sin(radianes) * 5
                
                bala = BalaEnergia(self.rect.centerx, self.rect.centery,
                                 es_jugador=False, tamaño=40,
                                 color=VERDE_NEON)
                bala.velocidad_x = velocidad_x
                bala.velocidad_y = velocidad_y
                all_sprites.add(bala)
                balas_enemigas.add(bala)

    def onda_expansiva(self):
        if self.temporizador_ataque % 60 == 0:
            onda = OndaExpansiva(self.rect.centerx, self.rect.centery)
            self.ondas.append(onda)

    def disparo_espiral(self):
        if self.temporizador_ataque % 20 == 0:
            angulo = (self.temporizador_ataque / 20) * 0.3
            for i in range(4):
                angulo_actual = angulo + (i * math.pi / 2)
                velocidad_x = math.cos(angulo_actual) * 4
                velocidad_y = math.sin(angulo_actual) * 4
                
                bala = BalaEnergia(self.rect.centerx, self.rect.centery,
                                 es_jugador=False, tamaño=30,
                                 color=CIAN_NEON)
                bala.velocidad_x = velocidad_x
                bala.velocidad_y = velocidad_y
                all_sprites.add(bala)
                balas_enemigas.add(bala)

    def disparo_todos_lados(self):
        if self.temporizador_ataque % 15 == 0:
            for i in range(8):
                angulo = (i / 8) * 2 * math.pi
                velocidad_x = math.cos(angulo) * 6
                velocidad_y = math.sin(angulo) * 6
                
                bala = BalaEnergia(self.rect.centerx, self.rect.centery,
                                 es_jugador=False, tamaño=45,
                                 color=ROSA_NEON)
                bala.velocidad_x = velocidad_x
                bala.velocidad_y = velocidad_y
                all_sprites.add(bala)
                balas_enemigas.add(bala)

    def onda_expansiva_doble(self):
        if self.temporizador_ataque % 50 == 0:
            for i in range(2):
                offset = random.randint(-100, 100)
                onda = OndaExpansiva(self.rect.centerx + offset,
                                    self.rect.centery + offset)
                self.ondas.append(onda)

    def lluvia_fuego_densa(self):
        if self.temporizador_ataque % 20 == 0:
            for _ in range(3):
                x = random.randint(150, ANCHO - 150)
                bola = BolaFuego(x, -100, tamaño=65)
                # Dirigidas al jugador
                if random.random() < 0.5:
                    dx = jugador.rect.centerx - x
                    dy = jugador.rect.centery + 100
                    distancia = max(1, math.sqrt(dx*dx + dy*dy))
                    bola.velocidad_x = (dx / distancia) * 2
                all_sprites.add(bola)
                balas_enemigas.add(bola)

    def disparo_espiral_doble(self):
        if self.temporizador_ataque % 15 == 0:
            for j in range(2):
                angulo = (self.temporizador_ataque / 15) * 0.3 + (j * math.pi)
                for i in range(4):
                    angulo_actual = angulo + (i * math.pi / 2)
                    velocidad_x = math.cos(angulo_actual) * 5
                    velocidad_y = math.sin(angulo_actual) * 5
                    
                    bala = BalaEnergia(self.rect.centerx, self.rect.centery,
                                     es_jugador=False, tamaño=35,
                                     color=AMARILLO)
                    bala.velocidad_x = velocidad_x
                    bala.velocidad_y = velocidad_y
                    all_sprites.add(bala)
                    balas_enemigas.add(bala)

    def laser_horizontal_doble(self):
        if self.temporizador_ataque == 40:
            for i in range(2):
                y_pos = random.randint(150, ALTO - 150)
                laser = LaserHorizontal(y_pos)
                self.lasers.append(laser)

    def generar_tetrominos(self):
        tipos = ['I', 'J', 'L', 'O', 'S', 'T', 'Z']
        num_piezas = 3 if self.fase >= 2 else 2
        
        if SND_TETRIS_MOVE:
            SND_TETRIS_MOVE.play()
        
        for i in range(num_piezas):
            tipo = random.choice(tipos)
            y = random.randint(50, ALTO - 200)
            x = ANCHO + (i * 250)
            
            tetromino = Tetromino(tipo, x, y)
            self.tetrominos.append(tetromino)
            
            for bloque in tetromino.sprites():
                all_sprites.add(bloque)
                obstaculos.add(bloque)

    def activar_temblor(self, intensidad):
        self.tiempo_temblor = 8
        self.intensidad_temblor = intensidad

    def recibir_dano(self, cantidad=1):
        self.vida -= cantidad
        self.animacion_dano = 8
        
        if SND_BOSS_HURT:
            SND_BOSS_HURT.play()
        
        self.activar_temblor(4)
        return self.vida <= 0

    def actualizar_efectos(self):
        for laser in self.lasers[:]:
            laser.update()
            if laser.temporizador >= laser.duracion:
                self.lasers.remove(laser)
        
        for onda in self.ondas[:]:
            onda.update()
            if onda.radio >= onda.radio_maximo:
                self.ondas.remove(onda)
        
        for tetromino in self.tetrominos[:]:
            tetromino.update()
            if len(tetromino.sprites()) == 0:
                self.tetrominos.remove(tetromino)
        
        if self.tiempo_temblor > 0:
            self.tiempo_temblor -= 1

    def draw_efectos(self, surface):
        for laser in self.lasers:
            laser.draw(surface)
        
        for onda in self.ondas:
            onda.draw(surface)

    def get_temblor_offset(self):
        if self.tiempo_temblor > 0:
            return (random.randint(-self.intensidad_temblor, self.intensidad_temblor),
                   random.randint(-self.intensidad_temblor, self.intensidad_temblor))
        return (0, 0)

# --- OTRAS CLASES NECESARIAS ---

class MisilTeledirigido(pygame.sprite.Sprite):
    def __init__(self, x, y, objetivo):
        super().__init__()
        self.image_original = IMG_MISIL
        self.image = self.image_original.copy()
        self.rect = self.image.get_rect(center=(x, y))
        self.objetivo = objetivo
        self.velocidad = 5
        self.giro_maximo = 0.08
        self.velocidad_x = 0
        self.velocidad_y = 0
        
    def update(self):
        if self.objetivo and self.objetivo.alive():
            dx = self.objetivo.rect.centerx - self.rect.centerx
            dy = self.objetivo.rect.centery - self.rect.centery
            distancia = max(1, math.sqrt(dx*dx + dy*dy))
            
            dx_normal = dx / distancia
            dy_normal = dy / distancia
            
            angulo_actual = math.atan2(self.velocidad_y, self.velocidad_x) if self.velocidad_x != 0 or self.velocidad_y != 0 else 0
            
            angulo_deseado = math.atan2(dy_normal, dx_normal)
            
            diferencia_angulo = angulo_deseado - angulo_actual
            while diferencia_angulo > math.pi:
                diferencia_angulo -= 2 * math.pi
            while diferencia_angulo < -math.pi:
                diferencia_angulo += 2 * math.pi
                
            angulo_actual += max(-self.giro_maximo, min(self.giro_maximo, diferencia_angulo))
            
            self.velocidad_x = math.cos(angulo_actual) * self.velocidad
            self.velocidad_y = math.sin(angulo_actual) * self.velocidad
            
            self.rect.x += self.velocidad_x
            self.rect.y += self.velocidad_y
            
            angulo_grados = math.degrees(angulo_actual)
            self.image = pygame.transform.rotate(self.image_original, -angulo_grados)
            self.rect = self.image.get_rect(center=self.rect.center)
            
            if pygame.sprite.collide_rect(self, self.objetivo):
                if SND_EXPLOSION: SND_EXPLOSION.play()
                self.objetivo.vida -= 1
                if self.objetivo.vida <= 0:
                    self.objetivo.kill()
                self.kill()
        else:
            self.rect.x += self.velocidad_x
            self.rect.y += self.velocidad_y
            
        if (self.rect.right < 0 or self.rect.left > ANCHO or 
            self.rect.bottom < 0 or self.rect.top > ALTO):
            self.kill()

class Bomba(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image_original = IMG_BOMBA
        self.image = self.image_original.copy()
        self.rect = self.image.get_rect(center=(x, y))
        self.velocidad = 4
        self.tiempo_explosion = 80
        self.temporizador = 0
        self.exploto = False
        
    def update(self):
        if not self.exploto:
            self.rect.x += self.velocidad
            self.temporizador += 1
            angulo = self.temporizador * 4
            self.image = pygame.transform.rotate(self.image_original, angulo)
            self.rect = self.image.get_rect(center=self.rect.center)
            
            if self.temporizador >= self.tiempo_explosion:
                self.explotar()
                
            if self.rect.left > ANCHO:
                self.kill()
    
    def explotar(self):
        self.exploto = True
        if SND_EXPLOSION: SND_EXPLOSION.play()
        
        for obstaculo in list(obstaculos):
            if hasattr(obstaculo, 'sprites'):
                for bloque in obstaculo.sprites():
                    distancia = math.sqrt((bloque.rect.centerx - self.rect.centerx)**2 + 
                                        (bloque.rect.centery - self.rect.centery)**2)
                    if distancia < 120:
                        bloque.kill()
            else:
                distancia = math.sqrt((obstaculo.rect.centerx - self.rect.centerx)**2 + 
                                    (obstaculo.rect.centery - self.rect.centery)**2)
                if distancia < 120:
                    obstaculo.kill()
            
        explosion = Explosion(self.rect.centerx, self.rect.centery)
        all_sprites.add(explosion)
        
        self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.radio = 5
        self.radio_maximo = 80
        self.velocidad_crecimiento = 4
        self.image = pygame.Surface((self.radio_maximo*2, self.radio_maximo*2), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(x, y))
        
    def update(self):
        self.radio += self.velocidad_crecimiento
        if self.radio >= self.radio_maximo:
            self.kill()
            
    def draw(self, surface):
        pygame.draw.circle(surface, (255, 200, 0), 
                         self.rect.center, self.radio, 3)
        pygame.draw.circle(surface, (255, 100, 0), 
                         self.rect.center, self.radio-8, 2)

class Escudo(pygame.sprite.Sprite):
    def __init__(self, jugador):
        super().__init__()
        self.jugador = jugador
        self.radio = 35
        self.image = pygame.Surface((self.radio*2, self.radio*2), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=self.jugador.rect.center)
        
    def update(self):
        if self.jugador.alive():
            self.rect.center = self.jugador.rect.center
        else:
            self.kill()
        
    def draw(self, surface):
        tiempo = pygame.time.get_ticks() * 0.008
        pulsacion = math.sin(tiempo) * 2
        radio_actual = self.radio + pulsacion
        
        for i in range(3):
            alpha = 150 - i * 50
            grosor = 3 - i
            pygame.draw.circle(surface, (100, 200, 255, alpha), 
                             self.rect.center, radio_actual - i*4, grosor)

class Potenciador(pygame.sprite.Sprite):
    def __init__(self, tipo):
        super().__init__()
        self.tipo = tipo
        
        if tipo == 1:
            self.image = IMG_MISIL
            self.color = (255, 100, 100)
            self.aura_color = (255, 50, 50)
        elif tipo == 2:
            self.image = IMG_BOMBA
            self.color = (255, 200, 100)
            self.aura_color = (255, 150, 50)
        elif tipo == 3:
            self.image = IMG_ESCUDO
            self.color = (100, 200, 255)
            self.aura_color = (50, 150, 255)
            
        self.rect = self.image.get_rect()
        self.rect.x = ANCHO + random.randint(10, 100)
        self.rect.y = random.randint(50, ALTO - 50)
        self.velocidad_x = -2
        
        self.tiempo_animacion = 0
        self.radio_aura = 35
        
    def update(self):
        self.rect.x += self.velocidad_x
        
        self.tiempo_animacion += 0.08
        self.rect.y += math.sin(self.tiempo_animacion) * 1.5
        
        if self.rect.right < 0:
            self.kill()
            
    def draw_aura(self, surface):
        tiempo = pygame.time.get_ticks() * 0.008
        pulsacion = math.sin(tiempo) * 6
        radio_actual = self.radio_aura + pulsacion
        
        for i in range(3):
            alpha = 150 - i * 50
            pygame.draw.circle(surface, (*self.aura_color, alpha), 
                             self.rect.center, radio_actual - i*4, 3)
            
    def aplicar(self, jugador):
        if SND_POWERUP: SND_POWERUP.play()
        
        if self.tipo == 1:
            jugador.activar_misiles_temporales()
            return "¡MISILES TELEDIRIGIDOS ACTIVADOS!"
        elif self.tipo == 2:
            jugador.bombas += 1
            return "¡BOMBA AGREGADA!"
        elif self.tipo == 3:
            jugador.activar_escudo()
            return "¡ESCUDO ACTIVADO!"

# --- FUNCIONES AUXILIARES ---

def dibujar_barra_arcade(surface, x, y, ancho, alto, progreso, color_fondo, color_relleno, texto=""):
    pygame.draw.rect(surface, color_fondo, (x, y, ancho, alto), border_radius=5)
    
    if progreso > 0:
        ancho_relleno = int((ancho - 4) * progreso)
        pygame.draw.rect(surface, color_relleno, (x + 2, y + 2, ancho_relleno, alto - 4), border_radius=3)
    
    pygame.draw.rect(surface, BLANCO, (x, y, ancho, alto), 2, border_radius=5)
    
    if texto:
        txt = FUENTE_PEQ.render(texto, True, BLANCO)
        surface.blit(txt, (x + ancho + 10, y))

def dibujar_hud(surf, x, y, vidas, puntaje, meta_puntaje, jugador, tiempo_transcurrido, jefe):
    for i in range(vidas):
        surf.blit(IMG_VIDA_ICONO, (x + (i * 35), y))
    
    if len(jefe_grupo) > 0:
        jefe = jefe_grupo.sprite
        progreso_jefe = jefe.vida / jefe.vida_max
        
        if jefe.fase == 1:
            color_fase = VERDE_NEON
        elif jefe.fase == 2:
            color_fase = NARANJA
        else:
            color_fase = ROJO
            
        dibujar_barra_arcade(surf, ANCHO // 2 - 200, 10, 400, 25, progreso_jefe, 
                            (50, 50, 50), color_fase, f"JEFE FASE {jefe.fase}: {jefe.vida}/{jefe.vida_max}")
    
    max_tiempo = 240
    progreso_tiempo = min(tiempo_transcurrido / max_tiempo, 1.0)
    tiempo_restante = max(0, max_tiempo - tiempo_transcurrido)
    minutos = int(tiempo_restante // 60)
    segundos = int(tiempo_restante % 60)
    dibujar_barra_arcade(surf, ANCHO - 210, 50, 200, 20, progreso_tiempo,
                        (50, 50, 50), NARANJA, f"TIME: {minutos:02d}:{segundos:02d}")
    
    y_powerups = 80
    if jugador.misiles_temporales_activos:
        tiempo_restante = max(0, jugador.duracion_misiles_temporales - (pygame.time.get_ticks() - jugador.tiempo_misiles_temporales))
        txt_misil = FUENTE_PEQ.render(f"Misiles Temp: {tiempo_restante/1000:.1f}s", True, (255, 100, 100))
        surf.blit(txt_misil, (10, y_powerups))
        y_powerups += 25
        
    if jugador.bombas > 0:
        txt_bomba = FUENTE_PEQ.render(f"Bombas: {jugador.bombas} (B)", True, (255, 200, 100))
        surf.blit(txt_bomba, (10, y_powerups))
        y_powerups += 25
        
    if jugador.escudo_activo:
        tiempo_restante = max(0, jugador.duracion_escudo - (pygame.time.get_ticks() - jugador.tiempo_escudo))
        txt_escudo = FUENTE_PEQ.render(f"Escudo: {tiempo_restante/1000:.1f}s", True, (100, 200, 255))
        surf.blit(txt_escudo, (10, y_powerups))
    
    if len(jefe_grupo) > 0:
        jefe = jefe_grupo.sprite
        tiempo_restante_tetrominos = max(0, jefe.intervalo_tetrominos - (pygame.time.get_ticks() - jefe.ultimo_tetromino))
        txt_tetrominos = FUENTE_PEQ.render(f"Próx. tetrominos: {tiempo_restante_tetrominos/1000:.1f}s", True, CIAN_NEON)
        surf.blit(txt_tetrominos, (ANCHO - 220, 80))

def dibujar_game_over(surf, puntaje):
    overlay = pygame.Surface((ANCHO, ALTO))
    overlay.set_alpha(200)
    overlay.fill(NEGRO)
    surf.blit(overlay, (0,0))
    
    txt_go = FUENTE_GRANDE.render("GAME OVER", True, ROJO)
    txt_pts = FUENTE_MEDIANA.render(f"Puntaje Final: {puntaje}", True, BLANCO)
    
    txt_op1 = FUENTE_PEQ.render("[C]ontinuar (Regalo: 3 vidas)", True, AMARILLO)
    txt_op2 = FUENTE_PEQ.render("[R]eintentar Nivel", True, BLANCO)
    txt_op3 = FUENTE_PEQ.render("[M]enú Principal", True, BLANCO)
    
    cx, cy = ANCHO // 2, ALTO // 2
    surf.blit(txt_go, txt_go.get_rect(center=(cx, cy - 100)))
    surf.blit(txt_pts, txt_pts.get_rect(center=(cx, cy - 40)))
    surf.blit(txt_op1, txt_op1.get_rect(center=(cx, cy + 40)))
    surf.blit(txt_op2, txt_op2.get_rect(center=(cx, cy + 80)))
    surf.blit(txt_op3, txt_op3.get_rect(center=(cx, cy + 120)))

def dibujar_resultados_finales(surf, estadisticas, mensaje_error=""):
    surf.fill(NEGRO)
    
    for i in range(100):
        x = random.randint(0, ANCHO)
        y = random.randint(0, ALTO)
        tamaño = random.randint(1, 3)
        brillo = random.randint(100, 255)
        pygame.draw.circle(surf, (brillo, brillo, brillo), (x, y), tamaño)
    
    titulo = FUENTE_TITULO.render("¡NIVEL 4 COMPLETADO!", True, PURPURA_NEON)
    titulo_shadow = FUENTE_TITULO.render("¡NIVEL 4 COMPLETADO!", True, PURPURA)
    
    surf.blit(titulo_shadow, (ANCHO//2 - titulo.get_width()//2 + 3, 53))
    surf.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 50))
    
    y_pos = 150
    estadisticas_lista = [
        (f"PUNTAJE TOTAL: {estadisticas['puntaje']}", VERDE_NEON),
        (f"DAÑO INFLIGIDO AL JEFE: {estadisticas['dano_jefe']}", ROJO),
        (f"MUERTES: {estadisticas['muertes']}", ROSA_NEON),
        (f"BOMBAS USADAS: {estadisticas['bombas_usadas']}", NARANJA),
        (f"TIEMPO TOTAL: {estadisticas['tiempo_formateado']}", CYAN),
        (f"VIDAS RESTANTES: {estadisticas['vidas_restantes']}/{estadisticas['vidas_iniciales']}", AZUL),
        (f"FASE MÁXIMA ALCANZADA: {estadisticas['fase_maxima']}", PURPURA_NEON)
    ]
    
    for texto, color in estadisticas_lista:
        txt = FUENTE_MEDIANA.render(texto, True, color)
        surf.blit(txt, (ANCHO//2 - txt.get_width()//2, y_pos))
        y_pos += 60
    
    if mensaje_error:
        error_txt = FUENTE_MEDIANA.render(mensaje_error, True, ROJO)
        surf.blit(error_txt, (ANCHO//2 - error_txt.get_width()//2, y_pos + 20))
        y_pos += 60
        
        alt_txt = FUENTE_ARCADA.render("Presiona R para reiniciar nivel 4", True, AMARILLO)
        surf.blit(alt_txt, (ANCHO//2 - alt_txt.get_width()//2, y_pos + 20))
        y_pos += 40
    
    tiempo_actual = pygame.time.get_ticks()
    if (tiempo_actual // 500) % 2 == 0:
        if not mensaje_error:
            mensaje = FUENTE_ARCADA.render("PRESIONA ESPACIO para avanzar al NIVEL 5 o ESC para salir", True, BLANCO)
        else:
            mensaje = FUENTE_ARCADA.render("PRESIONA R para reiniciar nivel 4 o ESC para salir", True, BLANCO)
        surf.blit(mensaje, (ANCHO//2 - mensaje.get_width()//2, ALTO - 80))

def reproducir_musica(ruta, volumen=0.5):
    try:
        ruta_nivel4 = os.path.join("nivel4", ruta)
        if os.path.exists(ruta_nivel4):
            pygame.mixer.music.load(ruta_nivel4)
        else:
            ruta_nivel2 = os.path.join("nivel2", ruta)
            if os.path.exists(ruta_nivel2):
                pygame.mixer.music.load(ruta_nivel2)
            else:
                pygame.mixer.music.load(ruta)
                
        pygame.mixer.music.stop()
        pygame.mixer.music.set_volume(volumen)
        pygame.mixer.music.play(-1)
        return True
    except:
        print(f"No se pudo cargar la música: {ruta}")
        return False

def detener_musica():
    pygame.mixer.music.stop()

def pausar_musica():
    pygame.mixer.music.pause()

def reanudar_musica():
    pygame.mixer.music.unpause()

# --- GRUPOS DE SPRITES ---
all_sprites = pygame.sprite.Group()
balas_jugador = pygame.sprite.Group()
balas_enemigas = pygame.sprite.Group()
jefe_grupo = pygame.sprite.GroupSingle()
potenciadores = pygame.sprite.Group()
escudo_grupo = pygame.sprite.GroupSingle()
obstaculos = pygame.sprite.Group()
jugador = Jugador()
all_sprites.add(jugador)

# --- FUNCIÓN DE REINICIO ---
def reiniciar_nivel(completo=True):
    balas_jugador.empty()
    balas_enemigas.empty()
    jefe_grupo.empty()
    potenciadores.empty()
    escudo_grupo.empty()
    obstaculos.empty()
    
    jugador.rect.center = (100, ALTO // 2)
    jugador.vidas = 5
    jugador.vidas_iniciales = 5
    jugador.invulnerable = False
    jugador.misiles = 0
    jugador.bombas = 0
    jugador.escudo_activo = False
    jugador.misiles_temporales_activos = False
    jugador.muertes = 0
    jugador.monedas_gastadas = 0
    
    if completo:
        return 0, 1
    else:
        return None

def continuar_juego():
    """Reinicia el estado del juego para continuar después de game over"""
    # Limpiar balas enemigas y obstáculos
    balas_enemigas.empty()
    obstaculos.empty()
    
    # Limpiar potenciadores y escudo
    potenciadores.empty()
    escudo_grupo.empty()
    
    # Limpiar ataques especiales del jefe
    if len(jefe_grupo) > 0:
        jefe = jefe_grupo.sprite
        jefe.lasers = []
        jefe.ondas = []
        jefe.tetrominos = []
    
    # Resetear jugador
    jugador.resetear_posicion()
    jugador.vidas = 3
    
    # Continuar la música
    reanudar_musica()

# --- LOOP PRINCIPAL NIVEL 4 ---

def juego():
    estado = 0 
    # 0: Historia Intro, 1: Cuenta, 2: Juego, 3: Winner, 4: Historia Final, 5: Game Over, 6: Resultados Finales
    
    puntaje = 0
    estado_anterior = 2
    
    fondo_x = 0
    tiempo_inicio_conteo = 0
    tiempo_inicio_nivel = 0
    
    tiempo_inicio_winner = 0
    efecto_salto = 0
    direccion_salto = 1
    
    bombas_usadas = 0
    tiempo_total_nivel = 0
    
    tiempo_temblor = 0
    intensidad_temblor = 0
    mensaje_powerup = ""
    tiempo_mensaje = 0
    
    musica_reproduciendose = False
    musica_pausada = False
    
    # Variable para mensaje de error al cargar nivel 5
    mensaje_error_nivel5 = ""
    
    # Textos para la historia
    titulo_inicio = "EL ING"
    subtitulo_inicio = "NIVEL4"
    
    historia_inicio = (
         "Motocle llega a las calles dominadas por el Inge Julio, un territorio caótico "
    "donde Infinitum impone sus propias reglas. Avanza con cuidado: aquí nada es estable "
    "y Julio no dejará que escapes sin un duro enfrentamiento."
    )
    
    titulo_final = "ESOOO!"
    subtitulo_final = "ADIOS TELMEX"
    
    historia_final = (
         "Motocle derrota al Inge Julio y supera el caos de las calles dominadas por Infinitum. "
    "Con esta victoria asegura otra gran calificación y se acerca al desafío final."
    )
    
    pantalla_historia_inicio = PantallaHistoriaDerecha(IMG_HISTORIA_INICIO, titulo_inicio, subtitulo_inicio, historia_inicio)
    pantalla_historia_final = PantallaHistoriaDerecha(IMG_HISTORIA_FINAL, titulo_final, subtitulo_final, historia_final)
    
    reloj = pygame.time.Clock()
    ejecutando = True

    while ejecutando:
        dt = reloj.tick(FPS)
        
        if estado in [2]:
            tiempo_total_nivel = (pygame.time.get_ticks() - tiempo_inicio_nivel) / 1000.0
        
        eventos = pygame.event.get()
        for event in eventos:
            if event.type == pygame.QUIT:
                ejecutando = False
            
            if estado == 0:
                pantalla_historia_inicio.manejar_eventos([event])
            elif estado == 4:
                pantalla_historia_final.manejar_eventos([event])
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b and estado == 2:
                    if jugador.lanzar_bomba():
                        bombas_usadas += 1
                
                if estado == 5:
                    if event.key == pygame.K_c:
                        if SND_COIN: SND_COIN.play()
                        continuar_juego()
                        estado = estado_anterior
                        musica_pausada = False
                        musica_reproduciendose = True

                    elif event.key == pygame.K_r:
                        puntaje, estado = reiniciar_nivel(completo=True)
                        tiempo_inicio_conteo = pygame.time.get_ticks()
                        tiempo_inicio_nivel = pygame.time.get_ticks()
                        bombas_usadas = 0
                        if SND_CONTEO: SND_CONTEO.play()
                        detener_musica()
                        musica_reproduciendose = False
                        musica_pausada = False

                    elif event.key == pygame.K_m:
                        print("Regresando al menú principal...")
                        ejecutando = False
                
                if estado == 6:
                    if event.key == pygame.K_SPACE and not mensaje_error_nivel5:
                        exito, mensaje = cargar_siguiente_nivel()
                        if not exito:
                            mensaje_error_nivel5 = mensaje
                    
                    elif event.key == pygame.K_r:
                        puntaje, estado = reiniciar_nivel(completo=True)
                        tiempo_inicio_conteo = pygame.time.get_ticks()
                        tiempo_inicio_nivel = pygame.time.get_ticks()
                        bombas_usadas = 0
                        mensaje_error_nivel5 = ""
                        detener_musica()
                        musica_reproduciendose = False
                        musica_pausada = False
                    
                    elif event.key == pygame.K_ESCAPE:
                        print("Saliendo del juego...")
                        ejecutando = False

        # --- MÁQUINA DE ESTADOS ---
        if estado == 0:
            pantalla_historia_inicio.actualizar(dt)
            pantalla_historia_inicio.dibujar(PANTALLA)
            
            if pantalla_historia_inicio.terminada:
                estado = 1
                tiempo_inicio_conteo = pygame.time.get_ticks()
                tiempo_inicio_nivel = pygame.time.get_ticks()
                if SND_CONTEO: SND_CONTEO.play()

        elif estado == 1:
            PANTALLA.blit(IMG_FONDO, (0,0))
            ahora = pygame.time.get_ticks()
            delta = ahora - tiempo_inicio_conteo
            
            texto = ""
            if delta < 500: texto = "3"
            elif delta < 800: texto = "2"
            elif delta < 1000: texto = "1"
            elif delta < 4000: 
                texto = "¡BATALLA FINAL!"
                if not musica_reproduciendose and not musica_pausada:
                    reproducir_musica("musica_batalla_final.mp3", 0.6)
                    musica_reproduciendose = True
            else:
                estado = 2
                jefe = JefeNivel4()
                all_sprites.add(jefe)
                jefe_grupo.add(jefe)
            
            if texto:
                surf = FUENTE_GRANDE.render(texto, True, PURPURA_NEON)
                PANTALLA.blit(surf, surf.get_rect(center=(ANCHO//2, ALTO//2)))

        elif estado == 2:
            # Aplicar efecto de temblor
            offset_x, offset_y = (0, 0)
            if len(jefe_grupo) > 0:
                jefe = jefe_grupo.sprite
                jefe_offset_x, jefe_offset_y = jefe.get_temblor_offset()
                offset_x += jefe_offset_x
                offset_y += jefe_offset_y
            
            if tiempo_temblor > 0:
                offset_x += random.randint(-intensidad_temblor, intensidad_temblor)
                offset_y += random.randint(-intensidad_temblor, intensidad_temblor)
                tiempo_temblor -= 1
            
            # Scroll Fondo
            fondo_x -= 3
            if fondo_x <= -ANCHO: fondo_x = 0
            PANTALLA.blit(IMG_FONDO, (fondo_x + offset_x, offset_y))
            PANTALLA.blit(IMG_FONDO, (fondo_x + ANCHO + offset_x, offset_y))

            # Generar Potenciadores
            if len(potenciadores) == 0 and random.randint(0, 600) < 2:
                tipo = random.randint(1, 3)
                p = Potenciador(tipo)
                all_sprites.add(p)
                potenciadores.add(p)

            # Actualizar y dibujar
            all_sprites.update()
            all_sprites.draw(PANTALLA)
            
            # Dibujar efectos especiales del jefe
            if len(jefe_grupo) > 0:
                jefe_grupo.sprite.draw_efectos(PANTALLA)
            
            # Dibujar auras de potenciadores
            for potenciador in potenciadores:
                potenciador.draw_aura(PANTALLA)
            
            # Dibujar escudo si está activo
            if jugador.escudo_activo:
                if len(escudo_grupo) == 0:
                    escudo = Escudo(jugador)
                    escudo_grupo.add(escudo)
                for escudo in escudo_grupo:
                    escudo.update()
                    escudo.draw(PANTALLA)
            else:
                escudo_grupo.empty()

        elif estado == 3:
            PANTALLA.blit(IMG_FONDO, (0,0))
            efecto_salto += direccion_salto * 2
            if abs(efecto_salto) > 20: direccion_salto *= -1
            
            r = IMG_WINNER.get_rect(center=(ANCHO//2, ALTO//2 + efecto_salto))
            PANTALLA.blit(IMG_WINNER, r)
            
            if pygame.time.get_ticks() - tiempo_inicio_winner > 3000:
                estado = 4
                pantalla_historia_final.reiniciar()

        elif estado == 4:
            detener_musica()
            musica_reproduciendose = False
            musica_pausada = False
            
            pantalla_historia_final.actualizar(dt)
            pantalla_historia_final.dibujar(PANTALLA)
            
            if pantalla_historia_final.terminada:
                estado = 6

        elif estado == 5:
            if musica_reproduciendose and not musica_pausada:
                pausar_musica()
                musica_pausada = True
            
            PANTALLA.blit(IMG_FONDO, (0,0)) 
            dibujar_game_over(PANTALLA, puntaje)
            
        elif estado == 6:
            # Calcular estadísticas
            dano_jefe = 0
            fase_maxima = 1
            if len(jefe_grupo) > 0:
                jefe = jefe_grupo.sprite
                dano_jefe = jefe.vida_max - jefe.vida
                fase_maxima = jefe.fase
            else:
                dano_jefe = 120
                fase_maxima = 3
            
            # Preparar estadísticas
            minutos = int(tiempo_total_nivel // 60)
            segundos = int(tiempo_total_nivel % 60)
            tiempo_formateado = f"{minutos:02d}:{segundos:02d}"
            
            estadisticas = {
                'puntaje': puntaje,
                'dano_jefe': dano_jefe,
                'muertes': jugador.muertes,
                'bombas_usadas': bombas_usadas,
                'tiempo_formateado': tiempo_formateado,
                'vidas_restantes': jugador.vidas,
                'vidas_iniciales': jugador.vidas_iniciales,
                'fase_maxima': fase_maxima
            }
            
            dibujar_resultados_finales(PANTALLA, estadisticas, mensaje_error_nivel5)

        # --- COLISIONES (Estado 2) ---
        if estado == 2:
            # Colisiones con potenciadores
            hits_powerups = pygame.sprite.spritecollide(jugador, potenciadores, True)
            for powerup in hits_powerups:
                mensaje = powerup.aplicar(jugador)
                mensaje_powerup = mensaje
                tiempo_mensaje = pygame.time.get_ticks()
            
            # Colisiones con obstáculos
            hits_obstaculos = pygame.sprite.spritecollide(jugador, obstaculos, True)
            for obstaculo in hits_obstaculos:
                if jugador.recibir_dano():
                    if SND_EXPLOSION: SND_EXPLOSION.play()
                    tiempo_temblor = 12
                    intensidad_temblor = 3
            
            # Balas Jugador -> Jefe
            if len(jefe_grupo) > 0:
                hits_j = pygame.sprite.groupcollide(jefe_grupo, balas_jugador, False, True)
                for j in hits_j:
                    puntaje += 10
                    if j.recibir_dano():
                        j.kill()
                        estado = 3
                        tiempo_inicio_winner = pygame.time.get_ticks()
                        balas_enemigas.empty()
                        if SND_EXPLOSION: SND_EXPLOSION.play()
                        if SND_VICTORY: SND_VICTORY.play()
                    else:
                        tiempo_temblor = 6
                        intensidad_temblor = 2
            
            # Daño al Jugador
            if pygame.sprite.spritecollide(jugador, balas_enemigas, True):
                if jugador.recibir_dano():
                    if SND_EXPLOSION: SND_EXPLOSION.play()
                    tiempo_temblor = 12
                    intensidad_temblor = 2

            if pygame.sprite.spritecollide(jugador, jefe_grupo, False):
                if jugador.recibir_dano():
                    if SND_EXPLOSION: SND_EXPLOSION.play()
                    tiempo_temblor = 20
                    intensidad_temblor = 5
            
            if len(jefe_grupo) > 0:
                jefe = jefe_grupo.sprite
                for laser in jefe.lasers:
                    if laser.temporizador < laser.duracion - 20:
                        laser_rect = pygame.Rect(0, laser.y - laser.ancho//2, ANCHO, laser.ancho)
                        if laser_rect.colliderect(jugador.rect):
                            if jugador.recibir_dano():
                                if SND_EXPLOSION: SND_EXPLOSION.play()
                                tiempo_temblor = 10
                                intensidad_temblor = 2
            
            for onda in jefe.ondas[:]:
                distancia = math.sqrt((onda.rect.centerx - jugador.rect.centerx)**2 + 
                                    (onda.rect.centery - jugador.rect.centery)**2)
                if distancia < onda.radio:
                    if jugador.recibir_dano():
                        if SND_EXPLOSION: SND_EXPLOSION.play()
                        tiempo_temblor = 8
                        intensidad_temblor = 2
            
            # Verificar Muerte
            if jugador.vidas <= 0:
                estado_anterior = estado
                estado = 5
                if musica_reproduciendose and not musica_pausada:
                    pausar_musica()
                    musica_pausada = True
                if SND_GAMEOVER: SND_GAMEOVER.play()

            # HUD
            if len(jefe_grupo) > 0:
                dibujar_hud(PANTALLA, 10, 10, jugador.vidas, puntaje, 120, jugador, tiempo_total_nivel, jefe_grupo.sprite)
            
            # Mostrar mensaje de potenciador
            if mensaje_powerup and pygame.time.get_ticks() - tiempo_mensaje < 2000:
                txt_powerup = FUENTE_MEDIANA.render(mensaje_powerup, True, AMARILLO)
                PANTALLA.blit(txt_powerup, txt_powerup.get_rect(center=(ANCHO//2, 100)))
            elif pygame.time.get_ticks() - tiempo_mensaje >= 2000:
                mensaje_powerup = ""

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    juego()