# nivel3/nivel3.py (versión con ataques direccionales hacia el jugador)

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
pygame.display.set_caption("Nivel 3 - La Fortaleza Cibernética")

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
LIMA = (191, 255, 0)
MAGENTA = (255, 0, 191)
DORADO = (255, 215, 0)

# COLORES BLOQUES TETRIS (nivel 3 los usa también)
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
        ruta_nivel3 = os.path.join("nivel3", nombre)
        if os.path.exists(ruta_nivel3):
            if alpha:
                img = pygame.image.load(ruta_nivel3).convert_alpha()
            else:
                img = pygame.image.load(ruta_nivel3).convert()
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
IMG_JEFE = cargar_imagen("jefe_nivel3.png", (250, 250))
IMG_FONDO = cargar_imagen("fondo_nivel3.png")
IMG_WINNER = cargar_imagen("winner.png", (400, 200))
IMG_VIDA_ICONO = cargar_imagen("vidas.png", (30, 30))

# Imágenes para potenciadores
IMG_MISIL = cargar_imagen("misil.png", (50, 25))
IMG_BOMBA = cargar_imagen("bomba.png", (50, 50))
IMG_ESCUDO = cargar_imagen("escudo.png", (60, 60))

# Imágenes para las pantallas de historia
IMG_HISTORIA_INICIO = cargar_imagen("historia_inicio_nivel3.png", (ANCHO, ALTO), alpha=True)
IMG_HISTORIA_FINAL = cargar_imagen("historia_final_nivel3.png", (ANCHO, ALTO), alpha=True)

# Escalar fondo
if IMG_FONDO.get_size() != (ANCHO, ALTO):
    IMG_FONDO = pygame.transform.scale(IMG_FONDO, (ANCHO, ALTO))

# Sonidos
def cargar_sonido(nombre):
    try:
        ruta_nivel3 = os.path.join("nivel3", nombre)
        if os.path.exists(ruta_nivel3):
            return pygame.mixer.Sound(ruta_nivel3)
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
    """Intenta cargar el siguiente nivel (nivel4.py) desde la carpeta nivel4"""
    try:
        # Verificar si existe la carpeta nivel4
        if os.path.exists("nivel4"):
            print("Cargando nivel 4...")
            
            # Buscar el archivo nivel4.py
            archivo_nivel4 = os.path.join("nivel4", "nivel4.py")
            if os.path.exists(archivo_nivel4):
                print(f"Encontrado: {archivo_nivel4}")
                
                # Cerrar Pygame completamente antes de abrir el nuevo nivel
                pygame.quit()
                
                # Usar subprocess para ejecutar el nuevo nivel como un proceso separado
                subprocess.Popen([sys.executable, archivo_nivel4])
                
                # Salir del juego actual
                sys.exit(0)
                
            else:
                print(f"Archivo nivel4.py no encontrado en la carpeta 'nivel4'")
                print(f"Buscando en: {os.path.abspath('nivel4')}")
                
                # Mostrar mensaje de error en pantalla
                mensaje_error = "Nivel 4 no disponible aún"
                return False, mensaje_error
        else:
            print("Carpeta 'nivel4' no encontrada")
            mensaje_error = "Carpeta 'nivel4' no encontrada"
            return False, mensaje_error
            
    except Exception as e:
        print(f"Error al cargar nivel 4: {e}")
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

# --- NUEVAS CLASES DE ATAQUES DIRECCIONALES ---

class DisparoDireccional(pygame.sprite.Sprite):
    """Disparo que va en dirección al jugador cuando se dispara"""
    def __init__(self, x, y, jugador_x, jugador_y, color=None, tamaño=25):
        super().__init__()
        self.tamaño = tamaño
        self.color = color or ROSA_NEON
        
        # Calcular dirección hacia el jugador
        dx = jugador_x - x
        dy = jugador_y - y
        distancia = max(1, math.sqrt(dx*dx + dy*dy))
        
        self.velocidad = 7
        self.velocidad_x = (dx / distancia) * self.velocidad
        self.velocidad_y = (dy / distancia) * self.velocidad
        
        # Crear imagen del disparo
        self.image = pygame.Surface((tamaño, tamaño), pygame.SRCALPHA)
        
        # Triángulo que apunta hacia el jugador
        pygame.draw.polygon(self.image, self.color, [
            (tamaño, tamaño//2),  # Punta
            (0, 0),  # Esquina superior izquierda
            (0, tamaño)  # Esquina inferior izquierda
        ])
        
        # Efecto de brillo
        pygame.draw.polygon(self.image, self.brillo_color(self.color, 50), [
            (tamaño-5, tamaño//2),
            (5, 5),
            (5, tamaño-5)
        ])
        
        self.rect = self.image.get_rect(center=(x, y))
        
        # Rotar imagen para que apunte en la dirección correcta
        angulo = math.degrees(math.atan2(dy, dx))
        self.image = pygame.transform.rotate(self.image, -angulo)
        self.rect = self.image.get_rect(center=self.rect.center)
        
    def brillo_color(self, color, cambio):
        return tuple(max(0, min(255, c + cambio)) for c in color)
        
    def update(self):
        self.rect.x += self.velocidad_x
        self.rect.y += self.velocidad_y
        
        if (self.rect.right < 0 or self.rect.left > ANCHO or 
            self.rect.bottom < 0 or self.rect.top > ALTO):
            self.kill()

class RafagaDireccional(pygame.sprite.Sprite):
    """Ráfaga de 3 disparos que apuntan al jugador con pequeñas variaciones"""
    def __init__(self, x, y, jugador_x, jugador_y, color_base=None):
        super().__init__()
        self.x = x
        self.y = y
        self.jugador_x = jugador_x
        self.jugador_y = jugador_y
        self.color_base = color_base or CIAN_NEON
        self.disparos = []
        
        # Crear 3 disparos con variaciones
        variaciones = [-0.2, 0, 0.2]  # Pequeñas variaciones en el ángulo
        
        for variacion in variaciones:
            dx = jugador_x - x
            dy = jugador_y - y
            distancia = max(1, math.sqrt(dx*dx + dy*dy))
            
            # Aplicar variación al ángulo
            angulo = math.atan2(dy, dx) + variacion
            
            velocidad = 6
            velocidad_x = math.cos(angulo) * velocidad
            velocidad_y = math.sin(angulo) * velocidad
            
            color = self.color_base
            
            self.disparos.append({
                'x': x, 'y': y,
                'vel_x': velocidad_x, 'vel_y': velocidad_y,
                'color': color,
                'tamaño': 20,
                'vida': 100  # Tiempo de vida en frames
            })
        
        self.rect = pygame.Rect(x, y, 10, 10)
        
    def update(self):
        for disparo in self.disparos:
            disparo['x'] += disparo['vel_x']
            disparo['y'] += disparo['vel_y']
            disparo['vida'] -= 1
        
        # Eliminar disparos que han salido de la pantalla o han muerto
        self.disparos = [d for d in self.disparos if 
                        0 <= d['x'] <= ANCHO and 
                        0 <= d['y'] <= ALTO and 
                        d['vida'] > 0]
        
        if len(self.disparos) == 0:
            self.kill()
            
    def draw(self, surface):
        for disparo in self.disparos:
            x, y = int(disparo['x']), int(disparo['y'])
            tamaño = disparo['tamaño']
            color = disparo['color']
            
            # Dibujar círculo principal
            pygame.draw.circle(surface, color, (x, y), tamaño//2)
            
            # Efecto de brillo interior
            pygame.draw.circle(surface, self.brillo_color(color, 60), (x, y), tamaño//4)
            
            # Estela
            for i in range(3):
                alpha = 100 - i * 30
                radio = tamaño//2 - i * 3
                if radio > 0:
                    pygame.draw.circle(surface, (*color[:3], alpha), 
                                     (int(x - disparo['vel_x'] * i), 
                                      int(y - disparo['vel_y'] * i)), 
                                     radio)
    
    def brillo_color(self, color, cambio):
        return tuple(max(0, min(255, c + cambio)) for c in color)

class AtaqueCruz(pygame.sprite.Sprite):
    """4 disparos en cruz que apuntan a las 4 direcciones desde el jugador"""
    def __init__(self, x, y, jugador_x, jugador_y, color=None):
        super().__init__()
        self.x = x
        self.y = y
        self.jugador_x = jugador_x
        self.jugador_y = jugador_y
        self.color = color or AMARILLO
        self.disparos = []
        
        # Crear 4 disparos en cruz
        angulos = [0, math.pi/2, math.pi, 3*math.pi/2]  # Derecha, abajo, izquierda, arriba
        
        for angulo in angulos:
            velocidad = 5
            velocidad_x = math.cos(angulo) * velocidad
            velocidad_y = math.sin(angulo) * velocidad
            
            self.disparos.append({
                'x': x, 'y': y,
                'vel_x': velocidad_x, 'vel_y': velocidad_y,
                'color': color,
                'tamaño': 25,
                'vida': 120
            })
        
        self.rect = pygame.Rect(x, y, 10, 10)
        
    def update(self):
        for disparo in self.disparos:
            disparo['x'] += disparo['vel_x']
            disparo['y'] += disparo['vel_y']
            disparo['vida'] -= 1
        
        # Eliminar disparos que han salido de la pantalla o han muerto
        self.disparos = [d for d in self.disparos if 
                        0 <= d['x'] <= ANCHO and 
                        0 <= d['y'] <= ALTO and 
                        d['vida'] > 0]
        
        if len(self.disparos) == 0:
            self.kill()
            
    def draw(self, surface):
        for disparo in self.disparos:
            x, y = int(disparo['x']), int(disparo['y'])
            tamaño = disparo['tamaño']
            color = disparo['color']
            
            # Dibujar cuadrado giratorio
            angulo = pygame.time.get_ticks() * 0.01
            puntos = []
            for i in range(4):
                ang = angulo + i * math.pi/2
                px = x + math.cos(ang) * tamaño//2
                py = y + math.sin(ang) * tamaño//2
                puntos.append((px, py))
            
            pygame.draw.polygon(surface, color, puntos)
            pygame.draw.polygon(surface, self.brillo_color(color, 50), 
                              [(p[0]*0.8 + x*0.2, p[1]*0.8 + y*0.2) for p in puntos])
    
    def brillo_color(self, color, cambio):
        return tuple(max(0, min(255, c + cambio)) for c in color)

class AtaqueDiamante(pygame.sprite.Sprite):
    """8 disparos en forma de diamante que se expanden"""
    def __init__(self, x, y, jugador_x, jugador_y, color=None):
        super().__init__()
        self.x = x
        self.y = y
        self.jugador_x = jugador_x
        self.jugador_y = jugador_y
        self.color = color or VERDE_NEON
        self.disparos = []
        
        # Crear 8 disparos en forma de diamante
        for i in range(8):
            angulo = (i / 8) * 2 * math.pi
            
            # Calcular dirección hacia el jugador con pequeña variación
            dx = jugador_x - x
            dy = jugador_y - y
            angulo_base = math.atan2(dy, dx)
            
            # Combinar dirección al jugador con patrón de diamante
            angulo_final = angulo_base + angulo * 0.3
            
            velocidad = 4
            velocidad_x = math.cos(angulo_final) * velocidad
            velocidad_y = math.sin(angulo_final) * velocidad
            
            # Alternar colores para efecto visual
            if i % 2 == 0:
                color_disparo = self.color
            else:
                color_disparo = self.brillo_color(self.color, 50)
            
            self.disparos.append({
                'x': x, 'y': y,
                'vel_x': velocidad_x, 'vel_y': velocidad_y,
                'color': color_disparo,
                'tamaño': 18,
                'vida': 150
            })
        
        self.rect = pygame.Rect(x, y, 10, 10)
        
    def update(self):
        for disparo in self.disparos:
            disparo['x'] += disparo['vel_x']
            disparo['y'] += disparo['vel_y']
            disparo['vida'] -= 1
        
        # Eliminar disparos que han salido de la pantalla o han muerto
        self.disparos = [d for d in self.disparos if 
                        0 <= d['x'] <= ANCHO and 
                        0 <= d['y'] <= ALTO and 
                        d['vida'] > 0]
        
        if len(self.disparos) == 0:
            self.kill()
            
    def draw(self, surface):
        for disparo in self.disparos:
            x, y = int(disparo['x']), int(disparo['y'])
            tamaño = disparo['tamaño']
            color = disparo['color']
            
            # Dibujar diamante
            puntos = [
                (x, y - tamaño//2),  # Arriba
                (x + tamaño//2, y),  # Derecha
                (x, y + tamaño//2),  # Abajo
                (x - tamaño//2, y)   # Izquierda
            ]
            
            pygame.draw.polygon(surface, color, puntos)
            
            # Efecto de rotación
            angulo = pygame.time.get_ticks() * 0.02
            radio_interno = tamaño//3
            puntos_internos = [
                (x + math.cos(angulo) * radio_interno, 
                 y + math.sin(angulo) * radio_interno),
                (x + math.cos(angulo + math.pi/2) * radio_interno, 
                 y + math.sin(angulo + math.pi/2) * radio_interno),
                (x + math.cos(angulo + math.pi) * radio_interno, 
                 y + math.sin(angulo + math.pi) * radio_interno),
                (x + math.cos(angulo + 3*math.pi/2) * radio_interno, 
                 y + math.sin(angulo + 3*math.pi/2) * radio_interno)
            ]
            
            pygame.draw.polygon(surface, self.brillo_color(color, 70), puntos_internos)
    
    def brillo_color(self, color, cambio):
        return tuple(max(0, min(255, c + cambio)) for c in color)

class AtaqueSeguimientoPrediccion(pygame.sprite.Sprite):
    """Disparo que predice la posición del jugador basándose en su velocidad actual"""
    def __init__(self, x, y, jugador, color=None):
        super().__init__()
        self.tamaño = 30
        self.color = color or MAGENTA
        self.jugador = jugador
        
        # Predecir posición futura del jugador basándose en su movimiento actual
        # Asumimos que el jugador continuará moviéndose en la misma dirección
        tiempo_prediccion = 40  # Frames en el futuro para predecir
        
        # Obtener velocidad aproximada del jugador (basada en posición anterior)
        if hasattr(self.jugador, 'pos_anterior'):
            vel_x = jugador.rect.x - jugador.pos_anterior[0]
            vel_y = jugador.rect.y - jugador.pos_anterior[1]
        else:
            vel_x, vel_y = 0, 0
        
        # Posición predicha
        jugador_x_pred = jugador.rect.centerx + vel_x * tiempo_prediccion
        jugador_y_pred = jugador.rect.centery + vel_y * tiempo_prediccion
        
        # Calcular dirección hacia la posición predicha
        dx = jugador_x_pred - x
        dy = jugador_y_pred - y
        distancia = max(1, math.sqrt(dx*dx + dy*dy))
        
        self.velocidad = 6
        self.velocidad_x = (dx / distancia) * self.velocidad
        self.velocidad_y = (dy / distancia) * self.velocidad
        
        # Guardar posición actual del jugador
        self.jugador.pos_anterior = (jugador.rect.x, jugador.rect.y)
        
        # Crear imagen del disparo
        self.image = pygame.Surface((self.tamaño, self.tamaño), pygame.SRCALPHA)
        
        # Círculo con efecto de anillos
        pygame.draw.circle(self.image, self.color, 
                          (self.tamaño//2, self.tamaño//2), self.tamaño//2)
        pygame.draw.circle(self.image, self.brillo_color(self.color, 40), 
                          (self.tamaño//2, self.tamaño//2), self.tamaño//3)
        pygame.draw.circle(self.image, BLANCO, 
                          (self.tamaño//2, self.tamaño//2), self.tamaño//6)
        
        # Flecha que indica dirección
        pygame.draw.polygon(self.image, self.brillo_color(self.color, 80), [
            (self.tamaño, self.tamaño//2),
            (self.tamaño//2, self.tamaño//4),
            (self.tamaño//2, 3*self.tamaño//4)
        ])
        
        self.rect = self.image.get_rect(center=(x, y))
        
        # Rotar para que la flecha apunte en la dirección correcta
        angulo = math.degrees(math.atan2(dy, dx))
        self.image = pygame.transform.rotate(self.image, -angulo)
        self.rect = self.image.get_rect(center=self.rect.center)
        
    def brillo_color(self, color, cambio):
        return tuple(max(0, min(255, c + cambio)) for c in color)
        
    def update(self):
        self.rect.x += self.velocidad_x
        self.rect.y += self.velocidad_y
        
        # Efecto de pulsación
        tiempo = pygame.time.get_ticks() * 0.01
        tamaño_actual = self.tamaño + math.sin(tiempo) * 3
        self.image = pygame.transform.scale(self.image, 
                                          (int(tamaño_actual), int(tamaño_actual)))
        self.rect = self.image.get_rect(center=self.rect.center)
        
        if (self.rect.right < 0 or self.rect.left > ANCHO or 
            self.rect.bottom < 0 or self.rect.top > ALTO):
            self.kill()

class AtaqueBarrido(pygame.sprite.Sprite):
    """Barrido de disparos que cubren un área donde está el jugador"""
    def __init__(self, x, y, jugador_y, color=None):
        super().__init__()
        self.x = x
        self.y = y
        self.jugador_y = jugador_y
        self.color = color or AZUL_ELECTRICO
        self.disparos = []
        
        # Crear 5 disparos que cubren el área vertical del jugador
        for i in range(5):
            # Calcular posición Y objetivo con variación
            objetivo_y = jugador_y + (i - 2) * 40
            
            dx = 100  # Distancia fija hacia la izquierda
            dy = objetivo_y - y
            distancia = max(1, math.sqrt(dx*dx + dy*dy))
            
            velocidad = 5
            velocidad_x = (-dx / distancia) * velocidad  # Siempre hacia la izquierda
            velocidad_y = (dy / distancia) * velocidad
            
            # Variar colores para efecto de arcoíris
            colores = [AZUL_ELECTRICO, CIAN_NEON, VERDE_NEON, AMARILLO, ROSA_NEON]
            color_disparo = colores[i % len(colores)]
            
            self.disparos.append({
                'x': x, 'y': y,
                'vel_x': velocidad_x, 'vel_y': velocidad_y,
                'color': color_disparo,
                'tamaño': 22,
                'vida': 120
            })
        
        self.rect = pygame.Rect(x, y, 10, 10)
        
    def update(self):
        for disparo in self.disparos:
            disparo['x'] += disparo['vel_x']
            disparo['y'] += disparo['vel_y']
            disparo['vida'] -= 1
        
        # Eliminar disparos que han salido de la pantalla o han muerto
        self.disparos = [d for d in self.disparos if 
                        0 <= d['x'] <= ANCHO and 
                        0 <= d['y'] <= ALTO and 
                        d['vida'] > 0]
        
        if len(self.disparos) == 0:
            self.kill()
            
    def draw(self, surface):
        for disparo in self.disparos:
            x, y = int(disparo['x']), int(disparo['y'])
            tamaño = disparo['tamaño']
            color = disparo['color']
            
            # Dibujar hexágono
            puntos = []
            for i in range(6):
                angulo = i * math.pi / 3
                px = x + math.cos(angulo) * tamaño//2
                py = y + math.sin(angulo) * tamaño//2
                puntos.append((px, py))
            
            pygame.draw.polygon(surface, color, puntos)
            
            # Efecto de rotación interna
            angulo_rot = pygame.time.get_ticks() * 0.015
            puntos_internos = []
            for i in range(6):
                angulo = i * math.pi / 3 + angulo_rot
                px = x + math.cos(angulo) * tamaño//4
                py = y + math.sin(angulo) * tamaño//4
                puntos_internos.append((px, py))
            
            pygame.draw.polygon(surface, self.brillo_color(color, 60), puntos_internos)
    
    def brillo_color(self, color, cambio):
        return tuple(max(0, min(255, c + cambio)) for c in color)

# --- CLASES DE ATAQUES EXISTENTES (mantenidas para compatibilidad) ---

class BalaEnergia(pygame.sprite.Sprite):
    def __init__(self, x, y, es_jugador, tamaño=25, color=None):
        super().__init__()
        self.es_jugador = es_jugador
        self.tamaño = tamaño
        self.color = color if color else (CIAN_NEON if es_jugador else ROJO)
        
        # Crear bala de energía con efecto de brillo
        self.image = pygame.Surface((tamaño, tamaño), pygame.SRCALPHA)
        
        # Círculo principal
        pygame.draw.circle(self.image, self.color, (tamaño//2, tamaño//2), tamaño//2)
        
        # Círculo interior brillante
        color_interior = tuple(min(255, c + 100) for c in self.color)
        pygame.draw.circle(self.image, color_interior, (tamaño//2, tamaño//2), tamaño//4)
        
        # Centro blanco brillante
        pygame.draw.circle(self.image, BLANCO, (tamaño//2, tamaño//2), tamaño//8)
        
        self.rect = self.image.get_rect(center=(x, y))
        self.velocidad_x = -7 if not es_jugador else 10
        self.velocidad_y = 0
        self.tiempo_vida = 0
        
    def update(self):
        self.rect.x += self.velocidad_x
        self.rect.y += self.velocidad_y
        self.tiempo_vida += 1
        
        # Efecto de pulsación
        if self.tiempo_vida % 5 == 0:
            tamaño_actual = self.tamaño + random.randint(-3, 3)
            self.image = pygame.transform.scale(self.image, (tamaño_actual, tamaño_actual))
            self.rect = self.image.get_rect(center=self.rect.center)
        
        if (self.rect.right < 0 or self.rect.left > ANCHO or 
            self.rect.bottom < 0 or self.rect.top > ALTO):
            self.kill()

class MisilGuia(pygame.sprite.Sprite):
    def __init__(self, x, y, color=None):
        super().__init__()
        self.tamaño = 35
        self.color = color or NARANJA
        
        # Crear imagen con colores vivos
        self.image = pygame.Surface((self.tamaño, self.tamaño), pygame.SRCALPHA)
        
        # Cuerpo del misil con colores vivos
        pygame.draw.rect(self.image, self.color, (5, 10, 25, 15))
        pygame.draw.polygon(self.image, self.brillo_color(self.color, 50), 
                           [(30, 10), (35, 17), (30, 25)])
        
        # Ala con efecto brillante
        pygame.draw.polygon(self.image, self.brillo_color(self.color, -50), 
                           [(15, 10), (10, 0), (20, 0)])
        
        # Efecto de propulsión
        pygame.draw.polygon(self.image, AMARILLO, 
                           [(5, 15), (0, 12), (0, 18)])
        
        self.rect = self.image.get_rect(center=(x, y))
        self.velocidad_x = -5
        self.velocidad_y = 0
        self.objetivo_y = random.randint(100, ALTO - 100)
        
    def brillo_color(self, color, cambio):
        return tuple(max(0, min(255, c + cambio)) for c in color)
        
    def update(self):
        self.rect.x += self.velocidad_x
        
        # Movimiento hacia el objetivo Y
        if self.rect.centery < self.objetivo_y:
            self.rect.y += 2
        elif self.rect.centery > self.objetivo_y:
            self.rect.y -= 2
            
        if self.rect.right < 0:
            self.kill()

class LaserHorizontal(pygame.sprite.Sprite):
    def __init__(self, y, color=None):
        super().__init__()
        self.duracion = 120
        self.temporizador = 0
        self.ancho = 10
        self.y = y
        self.color = color or (255, 100, 0)  # Naranja por defecto
        
        self.image = pygame.Surface((ANCHO, self.ancho), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(ANCHO//2, y))
        
    def update(self):
        self.temporizador += 1
        if self.temporizador >= self.duracion:
            self.kill()
            
    def draw(self, surface):
        if self.temporizador < self.duracion - 20:
            # Efecto de láser pulsante con colores vivos
            brillo = (math.sin(pygame.time.get_ticks() * 0.01) * 0.5 + 0.5) * 200 + 55
            color = (self.color[0], int(brillo), self.color[2], 200)
            
            # Línea principal con gradiente
            for i in range(5):
                ancho_actual = self.ancho - i * 2
                if ancho_actual > 0:
                    alpha = 200 - i * 40
                    color_layer = (color[0], min(255, color[1] + i*20), color[2], alpha)
                    pygame.draw.line(surface, color_layer, (0, self.y), (ANCHO, self.y), ancho_actual)
            
            # Efectos de partículas en los extremos
            if random.random() < 0.3:
                for _ in range(3):
                    x_pos = 0 if random.random() < 0.5 else ANCHO
                    tamaño = random.randint(3, 8)
                    pygame.draw.circle(surface, AMARILLO, (x_pos, self.y), tamaño)

class DisparoRebote(pygame.sprite.Sprite):
    def __init__(self, x, y, angulo, color=None):
        super().__init__()
        self.tamaño = 20
        self.color = color or VERDE_NEON
        
        # Crear imagen con colores vivos
        self.image = pygame.Surface((self.tamaño, self.tamaño), pygame.SRCALPHA)
        
        # Crear disparo que rebota con colores brillantes
        pygame.draw.circle(self.image, self.color, (self.tamaño//2, self.tamaño//2), self.tamaño//2)
        pygame.draw.circle(self.image, self.brillo_color(self.color, 60), 
                          (self.tamaño//2, self.tamaño//2), self.tamaño//3)
        pygame.draw.circle(self.image, BLANCO, (self.tamaño//2, self.tamaño//2), self.tamaño//6)
        
        self.rect = self.image.get_rect(center=(x, y))
        self.velocidad = 5
        self.angulo = angulo
        self.rebotes = 0
        self.max_rebotes = 3
        
    def brillo_color(self, color, cambio):
        return tuple(max(0, min(255, c + cambio)) for c in color)
        
    def update(self):
        self.rect.x += math.cos(self.angulo) * self.velocidad
        self.rect.y += math.sin(self.angulo) * self.velocidad
        
        # Rebote en bordes superior/inferior
        if self.rect.top <= 0:
            self.rect.top = 0
            self.angulo = -self.angulo
            self.rebotes += 1
            # Cambiar color al rebotar
            self.color = random.choice([VERDE_NEON, CIAN_NEON, AMARILLO, ROSA_NEON])
        elif self.rect.bottom >= ALTO:
            self.rect.bottom = ALTO
            self.angulo = -self.angulo
            self.rebotes += 1
            # Cambiar color al rebotar
            self.color = random.choice([VERDE_NEON, CIAN_NEON, AMARILLO, ROSA_NEON])
            
        if self.rebotes >= self.max_rebotes or self.rect.right < 0 or self.rect.left > ANCHO:
            self.kill()

class OndaSonica(pygame.sprite.Sprite):
    def __init__(self, x, y, color=None):
        super().__init__()
        self.radio = 20
        self.radio_maximo = 400
        self.velocidad_crecimiento = 6
        self.color = color or (0, 200, 255)  # Cian por defecto
        self.activo = True
        
        self.image = pygame.Surface((self.radio_maximo*2, self.radio_maximo*2), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(x, y))
        
    def update(self):
        self.radio += self.velocidad_crecimiento
        if self.radio >= self.radio_maximo:
            self.kill()
            
    def draw(self, surface):
        if self.activo:
            # Dibujar onda sónica con múltiples anillos coloridos
            for i in range(8):  # Más anillos para mejor efecto visual
                radio_actual = self.radio - i * 30
                if radio_actual > 0:
                    alpha = 150 - i * 15  # Más transparente gradualmente
                    grosor = 6 - i // 2
                    # Alternar colores para efecto arcoiris
                    if i % 4 == 0:
                        color_anillo = (self.color[0], self.color[1], self.color[2], alpha)
                    elif i % 4 == 1:
                        color_anillo = (self.color[2], self.color[0], self.color[1], alpha)
                    elif i % 4 == 2:
                        color_anillo = (self.color[1], self.color[2], self.color[0], alpha)
                    else:
                        color_anillo = (255, 255, 255, alpha)
                    
                    pygame.draw.circle(surface, color_anillo, 
                                     self.rect.center, radio_actual, grosor)

class TormentaRayos(pygame.sprite.Sprite):
    def __init__(self, x, y, objetivo_x, objetivo_y, color=None):
        super().__init__()
        self.duracion = 80
        self.temporizador = 0
        self.activo = True
        self.color = color or (150, 220, 255)  # Azul claro por defecto
        
        # Calcular dirección
        dx = objetivo_x - x
        dy = objetivo_y - y
        self.distancia = max(1, math.sqrt(dx*dx + dy*dy))
        self.dx = dx / self.distancia
        self.dy = dy / self.distancia
        
        self.rect = pygame.Rect(x, y, 20, 20)
        
    def update(self):
        self.temporizador += 1
        if self.temporizador >= self.duracion:
            self.kill()
            
    def draw(self, surface):
        if self.activo:
            end_x = self.rect.x + self.dx * self.distancia
            end_y = self.rect.y + self.dy * self.distancia
            
            # Dibujar rayo principal con múltiples capas coloridas
            for i in range(6):  # Más capas para mejor efecto
                offset_x = random.randint(-6, 6)
                offset_y = random.randint(-6, 6)
                
                # Alternar entre colores para efecto eléctrico
                if i % 3 == 0:
                    color = self.color  # Color base
                elif i % 3 == 1:
                    color = (255, 255, 200)  # Blanco amarillento
                else:
                    color = (200, 255, 255)  # Blanco azulado
                    
                grosor = 8 - i  # Capas más delgadas hacia afuera
                if grosor > 0:
                    pygame.draw.line(surface, color, 
                                   (self.rect.x + offset_x, self.rect.y + offset_y), 
                                   (end_x + offset_x, end_y + offset_y), grosor)
            
            # Efectos de chispas en los extremos
            for _ in range(5):
                spark_x = end_x + random.randint(-15, 15)
                spark_y = end_y + random.randint(-15, 15)
                pygame.draw.circle(surface, AMARILLO, (int(spark_x), int(spark_y)), 3)

class AtaqueEspiral(pygame.sprite.Sprite):
    def __init__(self, x, y, color_base=None):
        super().__init__()
        self.duracion = 150
        self.temporizador = 0
        self.activo = True
        self.color_base = color_base or PURPURA_NEON
        self.particulas = []
        
        self.rect = pygame.Rect(x, y, 10, 10)
        
    def update(self):
        self.temporizador += 1
        
        # Generar partículas en espiral
        if self.temporizador < self.duracion:
            angulo = self.temporizador * 0.1
            radio = self.temporizador * 0.5
            
            # Crear partícula
            px = self.rect.x + math.cos(angulo) * radio
            py = self.rect.y + math.sin(angulo) * radio
            
            # Variar color en la espiral
            color_index = int(self.temporizador / 10) % 7
            colores_arcoiris = [
                ROJO, NARANJA, AMARILLO, VERDE, 
                AZUL, PURPURA_NEON, ROSA_NEON
            ]
            color_particula = colores_arcoiris[color_index]
            
            self.particulas.append([px, py, color_particula])
        
        # Limitar tamaño de partículas
        if len(self.particulas) > 100:
            self.particulas = self.particulas[-100:]
            
        if self.temporizador >= self.duracion:
            self.kill()
            
    def draw(self, surface):
        for px, py, color in self.particulas:
            tamaño = random.randint(2, 5)
            pygame.draw.circle(surface, color, (int(px), int(py)), tamaño)

class AtaqueOrbital(pygame.sprite.Sprite):
    def __init__(self, x, y, num_orbitas=8):
        super().__init__()
        self.x = x
        self.y = y
        self.num_orbitas = num_orbitas
        self.angulo = 0
        self.radio = 50
        self.velocidad = 0.05
        self.duracion = 200
        self.temporizador = 0
        
        self.orbitas = []
        colores = [ROSA_NEON, CIAN_NEON, VERDE_NEON, AMARILLO, 
                  AZUL_ELECTRICO, MAGENTA, LIMA, DORADO]
        
        for i in range(num_orbitas):
            color = colores[i % len(colores)]
            self.orbitas.append({
                'angulo': (2 * math.pi / num_orbitas) * i,
                'radio': self.radio,
                'color': color,
                'tamaño': 15
            })
        
    def update(self):
        self.temporizador += 1
        self.angulo += self.velocidad
        
        # Expandir órbitas gradualmente
        if self.temporizador < self.duracion // 2:
            self.radio += 0.5
            
        if self.temporizador >= self.duracion:
            self.kill()
            
    def draw(self, surface):
        for orbita in self.orbitas:
            angulo_total = orbita['angulo'] + self.angulo
            ox = self.x + math.cos(angulo_total) * self.radio
            oy = self.y + math.sin(angulo_total) * orbita['radio']
            
            # Dibujar órbita principal con efecto de brillo
            pygame.draw.circle(surface, orbita['color'], 
                             (int(ox), int(oy)), orbita['tamaño'])
            
            # Efecto de brillo interior
            pygame.draw.circle(surface, self.brillo_color(orbita['color'], 80), 
                             (int(ox), int(oy)), orbita['tamaño'] // 2)
            
            # Traza de la órbita (línea tenue)
            puntos = []
            for i in range(20):
                a = angulo_total - i * 0.05
                px = self.x + math.cos(a) * self.radio
                py = self.y + math.sin(a) * orbita['radio']
                puntos.append((px, py))
            
            if len(puntos) > 1:
                pygame.draw.lines(surface, (*orbita['color'][:3], 50), 
                                False, puntos, 2)
    
    def brillo_color(self, color, cambio):
        return tuple(max(0, min(255, c + cambio)) for c in color)

class AtaqueArcoiris(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.duracion = 100
        self.temporizador = 0
        self.angulo = 0
        
    def update(self):
        self.temporizador += 1
        self.angulo += 0.1
        
        if self.temporizador >= self.duracion:
            self.kill()
            
    def draw(self, surface):
        if self.temporizador < self.duracion:
            # Disparar balas en todas direcciones con colores arcoíris
            num_disparos = 12
            colores_arcoiris = [
                ROJO, NARANJA, AMARILLO, VERDE_NEON,
                AZUL_ELECTRICO, PURPURA_NEON, ROSA_NEON
            ]
            
            for i in range(num_disparos):
                angulo = self.angulo + (2 * math.pi / num_disparos) * i
                color_idx = i % len(colores_arcoiris)
                
                # Calcular posición final
                distancia = 50 + (self.temporizador * 3)
                end_x = self.x + math.cos(angulo) * distancia
                end_y = self.y + math.sin(angulo) * distancia
                
                # Dibujar línea del disparo
                color = colores_arcoiris[color_idx]
                alpha = max(0, 255 - self.temporizador * 2)
                pygame.draw.line(surface, (*color[:3], alpha), 
                               (self.x, self.y), (end_x, end_y), 4)
                
                # Efecto de partícula en el extremo
                pygame.draw.circle(surface, BLANCO, 
                                 (int(end_x), int(end_y)), 3)

# --- CLASES BLOQUES TETRIS ---

class BloqueTetris(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.tamaño = 40
        self.image = self.crear_bloque(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.velocidad = random.randint(4, 7)
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
        self.velocidad = random.randint(4, 7)
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

# --- CLASE JEFE NIVEL 3 MEJORADA CON NUEVOS ATAQUES DIRECCIONALES ---

class JefeNivel3(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = IMG_JEFE
        self.rect = self.image.get_rect()
        # Posición inicial
        self.rect.x = ANCHO - 250
        self.rect.y = ALTO // 2 - 125
        
        # ¡AUMENTAR VIDA A 200!
        self.vida = 200  # ¡Más vida!
        self.vida_max = 200
        
        self.fase = 1
        self.velocidad_y = 1.5
        self.direccion_y = 1
        
        # Sistema de ataques mejorado
        self.temporizador_ataque = 0
        self.ataque_actual = 0
        self.duracion_ataque = 100
        self.cooldown_ataque = 80
        
        # Ataques especiales
        self.lasers_horizontales = []
        self.ondas_sonicas = []
        self.tormentas_rayos = []
        self.disparos_rebote = []
        self.ataques_espirales = []
        self.ataques_orbitales = []
        self.ataques_arcoiris = []
        
        # NUEVOS ATAQUES DIRECCIONALES
        self.disparos_direccionales = []
        self.rafagas_direccionales = []
        self.ataques_cruz = []
        self.ataques_diamante = []
        self.ataques_seguimiento = []
        self.ataques_barrido = []
        
        # Tetrominos
        self.tetrominos = []
        self.ultimo_tetromino = 0
        self.intervalo_tetrominos = 15000
        
        # Efectos de pantalla
        self.tiempo_temblor = 0
        self.intensidad_temblor = 0
        self.animacion_dano = 0
        self.transformando = False
        
        # Control de parpadeo intenso
        self.tiempo_inicio_nivel = 0
        self.parpadeo_intenso = False
        self.parpadeo_contador = 0
        
        # Colores para ataques
        self.colores_fase1 = [ROSA_NEON, CIAN_NEON, VERDE_NEON, AMARILLO, AZUL_ELECTRICO]
        self.colores_fase2 = [PURPURA_NEON, MAGENTA, LIMA, DORADO, ROJO]

    def update(self):
        # Iniciar temporizador para parpadeo intenso
        if self.tiempo_inicio_nivel == 0:
            self.tiempo_inicio_nivel = pygame.time.get_ticks()
        
        # Movimiento vertical
        self.rect.y += self.velocidad_y * self.direccion_y
        
        # Límites ajustados
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
        
        # Sistema de ciclo de ataques por fase
        self.temporizador_ataque += 1
        
        if self.temporizador_ataque > self.duracion_ataque + self.cooldown_ataque:
            self.temporizador_ataque = 0
            self.cambiar_ataque()
        
        # Ejecutar ataque actual según fase
        if self.temporizador_ataque < self.duracion_ataque:
            if self.fase == 1:
                self.ataque_fase_1()
            elif self.fase == 2:
                self.ataque_fase_2()
        
        # Generar tetrominos cada 15 segundos
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
            
        # Control de parpadeo intenso a los 40 segundos
        tiempo_actual = pygame.time.get_ticks()
        tiempo_transcurrido = (tiempo_actual - self.tiempo_inicio_nivel) / 1000.0
        
        if tiempo_transcurrido > 40 and tiempo_transcurrido < 43:
            # Parpadeo intenso por 3 segundos
            self.parpadeo_intenso = True
            self.parpadeo_contador += 1
            self.intensidad_temblor = 10
            self.tiempo_temblor = 3
        elif tiempo_transcurrido >= 43:
            # Parpadeo menos intenso pero continuo
            self.parpadeo_intenso = False
            if random.random() < 0.1:  # 10% de probabilidad de parpadear
                self.intensidad_temblor = 3
                self.tiempo_temblor = 2

    def verificar_fase(self):
        if self.fase == 1 and self.vida <= 100:  # Cambio a mitad de vida (100/200)
            self.cambiar_fase(2)

    def cambiar_fase(self, nueva_fase):
        self.fase = nueva_fase
        self.transformando = True
        
        if SND_BOSS_TRANSFORM:
            SND_BOSS_TRANSFORM.play()
        
        # Limpiar todos los ataques
        self.limpiar_ataques()
        
        # Cambiar color según fase
        if nueva_fase == 2:
            # Fase 2: Colores más intensos
            colored = pygame.Surface(self.image.get_size())
            colored.fill((1.2, 0.8, 1.0))  # Tono púrpura
            final = self.image.copy()
            final.blit(colored, (0, 0), special_flags=pygame.BLEND_MULT)
            self.image = final
        
        self.transformando = False
        self.activar_temblor(12)

    def limpiar_ataques(self):
        """Limpiar todos los ataques activos"""
        self.lasers_horizontales = []
        self.ondas_sonicas = []
        self.tormentas_rayos = []
        self.disparos_rebote = []
        self.ataques_espirales = []
        self.ataques_orbitales = []
        self.ataques_arcoiris = []
        self.disparos_direccionales = []
        self.rafagas_direccionales = []
        self.ataques_cruz = []
        self.ataques_diamante = []
        self.ataques_seguimiento = []
        self.ataques_barrido = []

    def cambiar_ataque(self):
        if self.fase == 1:
            self.ataque_actual = (self.ataque_actual + 1) % 7  # Más ataques en fase 1
        elif self.fase == 2:
            self.ataque_actual = (self.ataque_actual + 1) % 10  # Muchos más ataques en fase 2
        self.activar_temblor(5)

    # --- FASE 1: ATAQUES BÁSICOS CON DIRECCIONALES ---
    def ataque_fase_1(self):
        if self.ataque_actual == 0:
            self.disparo_arcoiris()
        elif self.ataque_actual == 1:
            self.disparos_direccionales_basicos()
        elif self.ataque_actual == 2:
            self.rafaga_direccional()
        elif self.ataque_actual == 3:
            self.laser_horizontal_colorido()
        elif self.ataque_actual == 4:
            self.ataque_cruz()
        elif self.ataque_actual == 5:
            self.ataque_barrido_vertical()
        elif self.ataque_actual == 6:
            self.disparos_espirales()

    def disparos_direccionales_basicos(self):
        if self.temporizador_ataque % 25 == 0:
            # Obtener posición del jugador si existe
            if len(jugador_grupo) > 0:
                jugador = jugador_grupo.sprite
                for i in range(2):
                    color = random.choice(self.colores_fase1)
                    disparo = DisparoDireccional(
                        self.rect.left, 
                        self.rect.centery + random.randint(-50, 50),
                        jugador.rect.centerx,
                        jugador.rect.centery,
                        color,
                        30
                    )
                    all_sprites.add(disparo)
                    balas_enemigas.add(disparo)

    def rafaga_direccional(self):
        if self.temporizador_ataque % 40 == 0:
            # Obtener posición del jugador si existe
            if len(jugador_grupo) > 0:
                jugador = jugador_grupo.sprite
                color = random.choice(self.colores_fase1)
                rafaga = RafagaDireccional(
                    self.rect.centerx,
                    self.rect.centery,
                    jugador.rect.centerx,
                    jugador.rect.centery,
                    color
                )
                self.rafagas_direccionales.append(rafaga)

    def ataque_cruz(self):
        if self.temporizador_ataque % 50 == 0:
            # Obtener posición del jugador si existe
            if len(jugador_grupo) > 0:
                jugador = jugador_grupo.sprite
                color = random.choice(self.colores_fase1)
                cruz = AtaqueCruz(
                    self.rect.centerx,
                    self.rect.centery,
                    jugador.rect.centerx,
                    jugador.rect.centery,
                    color
                )
                self.ataques_cruz.append(cruz)

    def ataque_barrido_vertical(self):
        if self.temporizador_ataque % 35 == 0:
            # Obtener posición del jugador si existe
            if len(jugador_grupo) > 0:
                jugador = jugador_grupo.sprite
                color = random.choice(self.colores_fase1)
                barrido = AtaqueBarrido(
                    self.rect.centerx,
                    self.rect.centery,
                    jugador.rect.centery,
                    color
                )
                self.ataques_barrido.append(barrido)

    def disparo_arcoiris(self):
        if self.temporizador_ataque % 30 == 0:
            colores = self.colores_fase1
            for i in range(5):
                y_pos = self.rect.centery + (i-2)*40
                color = colores[i % len(colores)]
                bala = BalaEnergia(self.rect.left, y_pos, es_jugador=False, 
                                  tamaño=35, color=color)
                bala.velocidad_y = random.uniform(-1, 1)
                all_sprites.add(bala)
                balas_enemigas.add(bala)

    def laser_horizontal_colorido(self):
        if self.temporizador_ataque == 50:
            y_pos = random.randint(100, ALTO - 100)
            color = random.choice(self.colores_fase1)
            laser = LaserHorizontal(y_pos, color)
            self.lasers_horizontales.append(laser)

    def disparos_espirales(self):
        if self.temporizador_ataque % 60 == 0:
            color = random.choice(self.colores_fase1)
            espiral = AtaqueEspiral(self.rect.centerx, self.rect.centery, color)
            self.ataques_espirales.append(espiral)

    # --- FASE 2: ATAQUES AVANZADOS CON MÁS DIRECCIONALES ---
    def ataque_fase_2(self):
        if self.ataque_actual == 0:
            self.ataque_seguimiento_prediccion()
        elif self.ataque_actual == 1:
            self.ataque_diamante_direccional()
        elif self.ataque_actual == 2:
            self.rafaga_direccional_mejorada()
        elif self.ataque_actual == 3:
            self.onda_sonica_colorida()
        elif self.ataque_actual == 4:
            self.disparos_rebote_multicolor()
        elif self.ataque_actual == 5:
            self.tormenta_rayos_colorida()
        elif self.ataque_actual == 6:
            self.lluvia_energia_arcoiris()
        elif self.ataque_actual == 7:
            self.ataque_arcoiris_completo()
        elif self.ataque_actual == 8:
            self.espiral_multicolor()
        elif self.ataque_actual == 9:
            self.ataque_combinado_explosivo()

    def ataque_seguimiento_prediccion(self):
        if self.temporizador_ataque % 30 == 0:
            # Obtener jugador si existe
            if len(jugador_grupo) > 0:
                jugador = jugador_grupo.sprite
                for i in range(2):
                    color = random.choice(self.colores_fase2)
                    seguimiento = AtaqueSeguimientoPrediccion(
                        self.rect.centerx + random.randint(-20, 20),
                        self.rect.centery + random.randint(-20, 20),
                        jugador,
                        color
                    )
                    all_sprites.add(seguimiento)
                    balas_enemigas.add(seguimiento)

    def ataque_diamante_direccional(self):
        if self.temporizador_ataque % 45 == 0:
            # Obtener posición del jugador si existe
            if len(jugador_grupo) > 0:
                jugador = jugador_grupo.sprite
                color = random.choice(self.colores_fase2)
                diamante = AtaqueDiamante(
                    self.rect.centerx,
                    self.rect.centery,
                    jugador.rect.centerx,
                    jugador.rect.centery,
                    color
                )
                self.ataques_diamante.append(diamante)

    def rafaga_direccional_mejorada(self):
        if self.temporizador_ataque % 20 == 0:
            # Obtener posición del jugador si existe
            if len(jugador_grupo) > 0:
                jugador = jugador_grupo.sprite
                for i in range(2):
                    color = random.choice(self.colores_fase2)
                    rafaga = RafagaDireccional(
                        self.rect.left,
                        self.rect.centery + (i-0.5)*60,
                        jugador.rect.centerx,
                        jugador.rect.centery,
                        color
                    )
                    self.rafagas_direccionales.append(rafaga)

    def onda_sonica_colorida(self):
        if self.temporizador_ataque % 50 == 0:
            color = random.choice(self.colores_fase2)
            onda = OndaSonica(self.rect.centerx, self.rect.centery, color)
            self.ondas_sonicas.append(onda)

    def disparos_rebote_multicolor(self):
        if self.temporizador_ataque % 20 == 0:
            for i in range(4):
                angulo = random.uniform(-1.0, 1.0)
                color = random.choice(self.colores_fase2)
                disparo = DisparoRebote(self.rect.left, 
                                       self.rect.centery + (i-1.5)*40,
                                       angulo, color)
                all_sprites.add(disparo)
                balas_enemigas.add(disparo)

    def tormenta_rayos_colorida(self):
        if self.temporizador_ataque % 35 == 0:
            for _ in range(3):
                objetivo_x = random.randint(50, ANCHO - 50)
                objetivo_y = random.randint(50, ALTO - 50)
                color = random.choice(self.colores_fase2)
                rayo = TormentaRayos(self.rect.centerx, self.rect.centery,
                                    objetivo_x, objetivo_y, color)
                self.tormentas_rayos.append(rayo)

    def lluvia_energia_arcoiris(self):
        if self.temporizador_ataque % 15 == 0:
            for _ in range(4):
                x = random.randint(200, ANCHO - 200)
                colores = [ROJO, NARANJA, AMARILLO, VERDE_NEON, AZUL_ELECTRICO, PURPURA_NEON]
                color = random.choice(colores)
                bala = BalaEnergia(x, -50, es_jugador=False, 
                                  tamaño=40, color=color)
                bala.velocidad_y = 5
                bala.velocidad_x = random.uniform(-2, 2)
                all_sprites.add(bala)
                balas_enemigas.add(bala)

    def ataque_arcoiris_completo(self):
        if self.temporizador_ataque == 1:
            arcoiris = AtaqueArcoiris(self.rect.centerx, self.rect.centery)
            self.ataques_arcoiris.append(arcoiris)

    def espiral_multicolor(self):
        if self.temporizador_ataque % 45 == 0:
            for i in range(2):
                color = self.colores_fase2[i % len(self.colores_fase2)]
                espiral = AtaqueEspiral(self.rect.centerx + (i-0.5)*60, 
                                       self.rect.centery, color)
                self.ataques_espirales.append(espiral)

    def ataque_combinado_explosivo(self):
        if self.temporizador_ataque % 10 == 0:
            for i in range(12):
                angulo = (i / 12) * 2 * math.pi
                velocidad_x = math.cos(angulo) * 5
                velocidad_y = math.sin(angulo) * 5
                
                colores = [ROSA_NEON, CIAN_NEON, VERDE_NEON, AMARILLO, 
                          AZUL_ELECTRICO, PURPURA_NEON, MAGENTA]
                color = colores[i % len(colores)]
                
                bala = BalaEnergia(self.rect.centerx, self.rect.centery,
                                  es_jugador=False, tamaño=35,
                                  color=color)
                bala.velocidad_x = velocidad_x
                bala.velocidad_y = velocidad_y
                all_sprites.add(bala)
                balas_enemigas.add(bala)

    def generar_tetrominos(self):
        tipos = ['I', 'J', 'L', 'O', 'S', 'T', 'Z']
        num_piezas = 3  # Más piezas para mayor desafío
        
        if SND_TETRIS_MOVE:
            SND_TETRIS_MOVE.play()
        
        for i in range(num_piezas):
            tipo = random.choice(tipos)
            y = random.randint(50, ALTO - 200)
            x = ANCHO + (i * 300)
            
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
        
        self.activar_temblor(5)
        return self.vida <= 0

    def actualizar_efectos(self):
        # Actualizar efectos existentes
        for laser in self.lasers_horizontales[:]:
            laser.update()
            if laser.temporizador >= laser.duracion:
                self.lasers_horizontales.remove(laser)
        
        for onda in self.ondas_sonicas[:]:
            onda.update()
            if onda.radio >= onda.radio_maximo:
                self.ondas_sonicas.remove(onda)
        
        for rayo in self.tormentas_rayos[:]:
            rayo.update()
            if rayo.temporizador >= rayo.duracion:
                self.tormentas_rayos.remove(rayo)
        
        for espiral in self.ataques_espirales[:]:
            espiral.update()
            if espiral.temporizador >= espiral.duracion:
                self.ataques_espirales.remove(espiral)
        
        for orbital in self.ataques_orbitales[:]:
            orbital.update()
            if orbital.temporizador >= orbital.duracion:
                self.ataques_orbitales.remove(orbital)
        
        for arcoiris in self.ataques_arcoiris[:]:
            arcoiris.update()
            if arcoiris.temporizador >= arcoiris.duracion:
                self.ataques_arcoiris.remove(arcoiris)
        
        # Actualizar nuevos efectos direccionales
        for rafaga in self.rafagas_direccionales[:]:
            rafaga.update()
            if len(rafaga.disparos) == 0:
                self.rafagas_direccionales.remove(rafaga)
        
        for cruz in self.ataques_cruz[:]:
            cruz.update()
            if len(cruz.disparos) == 0:
                self.ataques_cruz.remove(cruz)
        
        for diamante in self.ataques_diamante[:]:
            diamante.update()
            if len(diamante.disparos) == 0:
                self.ataques_diamante.remove(diamante)
        
        for barrido in self.ataques_barrido[:]:
            barrido.update()
            if len(barrido.disparos) == 0:
                self.ataques_barrido.remove(barrido)
        
        for tetromino in self.tetrominos[:]:
            tetromino.update()
            if len(tetromino.sprites()) == 0:
                self.tetrominos.remove(tetromino)
        
        if self.tiempo_temblor > 0:
            self.tiempo_temblor -= 1

    def draw_efectos(self, surface):
        # Dibujar efectos existentes
        for laser in self.lasers_horizontales:
            laser.draw(surface)
        
        for onda in self.ondas_sonicas:
            onda.draw(surface)
        
        for rayo in self.tormentas_rayos:
            rayo.draw(surface)
        
        for espiral in self.ataques_espirales:
            espiral.draw(surface)
        
        for orbital in self.ataques_orbitales:
            orbital.draw(surface)
        
        for arcoiris in self.ataques_arcoiris:
            arcoiris.draw(surface)
        
        # Dibujar nuevos efectos direccionales
        for rafaga in self.rafagas_direccionales:
            rafaga.draw(surface)
        
        for cruz in self.ataques_cruz:
            cruz.draw(surface)
        
        for diamante in self.ataques_diamante:
            diamante.draw(surface)
        
        for barrido in self.ataques_barrido:
            barrido.draw(surface)

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
        # Explosión colorida
        for i in range(3):
            color = [(255, 200, 0), (255, 100, 0), (255, 50, 0)][i]
            radio_actual = self.radio - i * 15
            if radio_actual > 0:
                pygame.draw.circle(surface, color, 
                                 self.rect.center, radio_actual, 4 - i)

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
        
        # Escudo colorido con múltiples capas
        colores = [(100, 200, 255, 150), (50, 150, 255, 100), (0, 100, 255, 50)]
        
        for i, color in enumerate(colores):
            pygame.draw.circle(surface, color, 
                             self.rect.center, radio_actual - i*8, 3 - i)

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
        
        # Aura colorida
        for i in range(4):
            alpha = 150 - i * 30
            color_aura = (*self.aura_color[:3], alpha)
            pygame.draw.circle(surface, color_aura, 
                             self.rect.center, radio_actual - i*3, 2)
            
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
            color_fase = AZUL_ELECTRICO
        elif jefe.fase == 2:
            color_fase = PURPURA_NEON
            
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
        
        # Mostrar temporizador de parpadeo
        tiempo_actual = pygame.time.get_ticks()
        tiempo_transcurrido = (tiempo_actual - jefe.tiempo_inicio_nivel) / 1000.0
        if tiempo_transcurrido < 43:
            txt_parpadeo = FUENTE_PEQ.render(f"Parpadeo intenso en: {max(0, 40-tiempo_transcurrido):.0f}s", True, AMARILLO)
            surf.blit(txt_parpadeo, (ANCHO - 220, 110))

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
    surf.blit(txt_op2, txt_op2.get_rect(center=(cx, cy + 80)))  # CORREGIDO: cambio rect por center
    surf.blit(txt_op3, txt_op3.get_rect(center=(cx, cy + 120)))
    surf.blit(txt_op3, txt_op3.get_rect(center=(cx, cy + 120)))

def dibujar_resultados_finales(surf, estadisticas, mensaje_error=""):
    """Dibuja la pantalla de resultados finales estilo arcade"""
    surf.fill(NEGRO)
    
    for i in range(100):
        x = random.randint(0, ANCHO)
        y = random.randint(0, ALTO)
        tamaño = random.randint(1, 3)
        brillo = random.randint(100, 255)
        pygame.draw.circle(surf, (brillo, brillo, brillo), (x, y), tamaño)
    
    titulo = FUENTE_TITULO.render("¡NIVEL 3 COMPLETADO!", True, AZUL_ELECTRICO)
    titulo_shadow = FUENTE_TITULO.render("¡NIVEL 3 COMPLETADO!", True, AZUL)
    
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
        (f"FASE MÁXIMA ALCANZADA: {estadisticas['fase_maxima']}", AZUL_ELECTRICO)
    ]
    
    for texto, color in estadisticas_lista:
        txt = FUENTE_MEDIANA.render(texto, True, color)
        surf.blit(txt, (ANCHO//2 - txt.get_width()//2, y_pos))
        y_pos += 60
    
    # Mostrar mensaje de error si existe
    if mensaje_error:
        error_txt = FUENTE_MEDIANA.render(mensaje_error, True, ROJO)
        surf.blit(error_txt, (ANCHO//2 - error_txt.get_width()//2, y_pos + 20))
        y_pos += 60
        
        # Instrucción alternativa
        alt_txt = FUENTE_ARCADA.render("Presiona R para reiniciar nivel 3", True, AMARILLO)
        surf.blit(alt_txt, (ANCHO//2 - alt_txt.get_width()//2, y_pos + 20))
        y_pos += 40
    
    # Mensaje parpadeante estilo arcade
    tiempo_actual = pygame.time.get_ticks()
    if (tiempo_actual // 500) % 2 == 0:  # Parpadeo cada 500ms
        if not mensaje_error:
            mensaje = FUENTE_ARCADA.render("PRESIONA ESPACIO para avanzar al NIVEL 4 o ESC para salir", True, BLANCO)
        else:
            mensaje = FUENTE_ARCADA.render("PRESIONA R para reiniciar nivel 3 o ESC para salir", True, BLANCO)
        surf.blit(mensaje, (ANCHO//2 - mensaje.get_width()//2, ALTO - 80))

def reproducir_musica(ruta, volumen=0.5):
    try:
        ruta_nivel3 = os.path.join("nivel3", ruta)
        if os.path.exists(ruta_nivel3):
            pygame.mixer.music.load(ruta_nivel3)
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
jugador_grupo = pygame.sprite.GroupSingle(jugador)  # Nuevo grupo para fácil acceso al jugador

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
    balas_enemigas.empty()
    obstaculos.empty()
    potenciadores.empty()
    escudo_grupo.empty()
    
    if len(jefe_grupo) > 0:
        jefe = jefe_grupo.sprite
        jefe.limpiar_ataques()
    
    jugador.resetear_posicion()
    jugador.vidas = 3
    
    reanudar_musica()

# --- LOOP PRINCIPAL NIVEL 3 ---

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
    
    # Variable para mensaje de error al cargar nivel 4
    mensaje_error_nivel4 = ""
    
    # Textos para la historia
    titulo_inicio = "PERVERSO"
    subtitulo_inicio = "NIVEL3"
    
    historia_inicio = (
        "Motocle se aproxima al Cubo del Profe Juan Carlos. "
    "Este nivel es conocido por sus trampas inesperadas, así que avanza con cautela. "
    "Prepárate: Juan Carlos no permitirá que pases sin un verdadero reto."
    )
    
    titulo_final = "NEL"
    subtitulo_final = "LE GANE"
    
    historia_final = (
        "Motocle vence al Profe Juan Carlos y supera las trampas del Cubo. "
    "Con esta victoria obtiene una gran calificación y continúa firme rumbo a su graduación."
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
                
                if estado == 6:  # Estado de resultados finales
                    if event.key == pygame.K_SPACE and not mensaje_error_nivel4:
                        # Intentar cargar nivel 4
                        exito, mensaje = cargar_siguiente_nivel()
                        if not exito:
                            mensaje_error_nivel4 = mensaje
                    
                    elif event.key == pygame.K_r:  # Reiniciar nivel 3
                        puntaje, estado = reiniciar_nivel(completo=True)
                        tiempo_inicio_conteo = pygame.time.get_ticks()
                        tiempo_inicio_nivel = pygame.time.get_ticks()
                        bombas_usadas = 0
                        mensaje_error_nivel4 = ""  # Limpiar mensaje de error
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
                texto = "¡FORMA DE ATAQUE!"
                if not musica_reproduciendose and not musica_pausada:
                    reproducir_musica("musica_batalla_final.mp3", 0.6)
                    musica_reproduciendose = True
            else:
                estado = 2
                jefe = JefeNivel3()
                all_sprites.add(jefe)
                jefe_grupo.add(jefe)
            
            if texto:
                surf = FUENTE_GRANDE.render(texto, True, AZUL_ELECTRICO)
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
            
            # Aplicar efecto de parpadeo intenso del jefe
            tiempo_actual = pygame.time.get_ticks()
            tiempo_transcurrido = (tiempo_actual - tiempo_inicio_nivel) / 1000.0
            
            if tiempo_transcurrido > 40 and tiempo_transcurrido < 43:
                # Parpadeo intenso por 3 segundos
                if (pygame.time.get_ticks() // 100) % 2 == 0:  # Parpadeo rápido
                    overlay = pygame.Surface((ANCHO, ALTO))
                    overlay.set_alpha(100)
                    overlay.fill(BLANCO)
                    PANTALLA.blit(overlay, (0, 0))
            
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
                estado = 6  # Ir directamente a resultados finales

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
                dano_jefe = 200
                fase_maxima = 2
            
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
            
            dibujar_resultados_finales(PANTALLA, estadisticas, mensaje_error_nivel4)

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
                for laser in jefe.lasers_horizontales:
                    if laser.temporizador < laser.duracion - 20:
                        laser_rect = pygame.Rect(0, laser.y - laser.ancho//2, ANCHO, laser.ancho)
                        if laser_rect.colliderect(jugador.rect):
                            if jugador.recibir_dano():
                                if SND_EXPLOSION: SND_EXPLOSION.play()
                                tiempo_temblor = 10
                                intensidad_temblor = 2
            
            for onda in jefe.ondas_sonicas[:]:
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
                dibujar_hud(PANTALLA, 10, 10, jugador.vidas, puntaje, 100, jugador, tiempo_total_nivel, jefe_grupo.sprite)
            
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