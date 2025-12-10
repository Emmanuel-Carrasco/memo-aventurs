# nivel1.py

import pygame
import sys
import random
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
pygame.display.set_caption("Nivel 1 - El Archivo Perdido")

# COLORES VIVOS Y LLAMATIVOS
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
AMARILLO = (255, 255, 0)
NARANJA = (255, 165, 0)

# COLORES NEON PARA NIVEL 1
VERDE_NEON = (57, 255, 20)
AZUL_ELECTRICO = (0, 191, 255)
ROSA_NEON = (255, 20, 147)
PURPURA_NEON = (180, 0, 255)
CIAN_NEON = (0, 255, 255)
AMARILLO_NEON = (255, 255, 0)
NARANJA_NEON = (255, 100, 0)
ROJO_NEON = (255, 40, 40)
CYAN_NEON = (0, 255, 255)

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
        # Buscar en la misma carpeta
        if os.path.exists(nombre):
            if alpha:
                img = pygame.image.load(nombre).convert_alpha()
            else:
                img = pygame.image.load(nombre).convert()
        else:
            # Crear imagen de respaldo
            if escala:
                img = pygame.Surface(escala)
            else:
                img = pygame.Surface((100, 100))
            img.fill(ROJO_NEON)
        
        if escala:
            img = pygame.transform.scale(img, escala)
        return img
    except Exception as e:
        print(f"Error al cargar imagen {nombre}: {e}")
        if escala:
            surf = pygame.Surface(escala)
        else:
            surf = pygame.Surface((100, 100))
        surf.fill(ROJO_NEON)
        return surf

# Imágenes (todos en la misma carpeta)
IMG_NAVE = cargar_imagen("nave.png", (60, 40))
IMG_JEFE = cargar_imagen("jefe_nivel1.png", (200, 200))
IMG_FONDO = cargar_imagen("fondo_nivel1.png")
IMG_WINNER = cargar_imagen("winner.png", (400, 200))
IMG_VIDA_ICONO = cargar_imagen("vidas.png", (30, 30))

# Imágenes para potenciadores
IMG_MISIL = cargar_imagen("misil.png", (50, 25))
IMG_BOMBA = cargar_imagen("bomba.png", (50, 50))
IMG_ESCUDO = cargar_imagen("escudo.png", (60, 60))

# Crear imágenes de respaldo si no existen
if IMG_FONDO.get_size() != (ANCHO, ALTO):
    IMG_FONDO = pygame.transform.scale(IMG_FONDO, (ANCHO, ALTO))

# Sonidos
def cargar_sonido(nombre):
    try:
        if os.path.exists(nombre):
            return pygame.mixer.Sound(nombre)
        else:
            # Crear sonido de respaldo (silencioso)
            sound = pygame.mixer.Sound(buffer=bytes([0]*1000))
            return sound
    except:
        sound = pygame.mixer.Sound(buffer=bytes([0]*1000))
        return sound

# Cargar sonidos
SND_DISPARO = cargar_sonido("disparo.mp3")
SND_CONTEO = cargar_sonido("conteo.mp3")
SND_COIN = cargar_sonido("coin.mp3")
SND_GAMEOVER = cargar_sonido("gameover.mp3")
SND_EXPLOSION = cargar_sonido("explosion.mp3")
SND_POWERUP = cargar_sonido("powerup.mp3")
SND_VICTORY = cargar_sonido("victory.mp3")

# Música de fondo
def cargar_musica(nombre):
    try:
        if os.path.exists(nombre):
            pygame.mixer.music.load(nombre)
            return True
        return False
    except:
        return False

# --- FUNCIÓN PARA CARGAR SIGUIENTE NIVEL ---
def cargar_siguiente_nivel():
    """Intenta cargar el siguiente nivel (nivel2.py) desde la carpeta nivel2"""
    try:
        # Verificar si existe la carpeta nivel2
        if os.path.exists("nivel2"):
            print("Cargando nivel 2...")
            
            # Buscar el archivo nivel2.py
            archivo_nivel2 = os.path.join("nivel2", "nivel2.py")
            if os.path.exists(archivo_nivel2):
                print(f"Encontrado: {archivo_nivel2}")
                
                # Cerrar Pygame completamente antes de abrir el nuevo nivel
                pygame.quit()
                
                # Usar subprocess para ejecutar el nuevo nivel como un proceso separado
                subprocess.Popen([sys.executable, archivo_nivel2])
                
                # Salir del juego actual
                sys.exit(0)
                
            else:
                print(f"Archivo nivel2.py no encontrado en la carpeta 'nivel2'")
                print(f"Buscando en: {os.path.abspath('nivel2')}")
                
                # Mostrar mensaje de error en pantalla
                mensaje_error = "Nivel 2 no disponible aún"
                return False, mensaje_error
        else:
            print("Carpeta 'nivel2' no encontrada")
            mensaje_error = "Carpeta 'nivel2' no encontrada"
            return False, mensaje_error
            
    except Exception as e:
        print(f"Error al cargar nivel 2: {e}")
        mensaje_error = f"Error: {str(e)[:50]}..."
        return False, mensaje_error
    
    return True, ""

# --- CLASES ---

class PantallaHistoria:
    def __init__(self, titulo, subtitulo, texto_historia):
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
            color = random.choice([AZUL_ELECTRICO, VERDE_NEON, ROSA_NEON, AMARILLO_NEON])
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
                color = random.choice([AZUL_ELECTRICO, VERDE_NEON, ROSA_NEON, AMARILLO_NEON])
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
                    self.palabras_mostradas += 1
                    self.temporizador_palabra = 0
                else:
                    if self.tiempo_inicio == 0:
                        self.tiempo_inicio = pygame.time.get_ticks()
                    elif pygame.time.get_ticks() - self.tiempo_inicio > 3000:
                        self.terminada = True
    
    def dibujar(self, pantalla):
        # Fondo negro con estrellas
        pantalla.fill(NEGRO)
        for i in range(100):
            x = random.randint(0, ANCHO)
            y = random.randint(0, ALTO)
            tamaño = random.randint(1, 3)
            brillo = random.randint(100, 255)
            pygame.draw.circle(pantalla, (brillo, brillo, brillo), (x, y), tamaño)
        
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
        
        pantalla.blit(panel_surface, (ANCHO - self.ancho_panel, 0))
        
        titulo_color = list(CIAN_NEON)
        titulo_color = [int(c * (0.8 + 0.2 * self.efecto_brillo)) for c in titulo_color]
        titulo_alpha = min(255, int(self.alpha_texto))
        
        titulo_surf = FUENTE_TITULO.render(self.titulo, True, (*titulo_color, titulo_alpha))
        titulo_rect = titulo_surf.get_rect(center=(ANCHO - self.ancho_panel//2, 100))
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
                                                    (AMARILLO_NEON[0], AMARILLO_NEON[1], AMARILLO_NEON[2], continuar_alpha))
                continuar_rect = continuar_surf.get_rect(center=(ANCHO - self.ancho_panel//2, ALTO - 60))
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
        bala = Bala(self.rect.right, self.rect.centery, es_jugador=True)
        all_sprites.add(bala)
        balas_jugador.add(bala)
        if SND_DISPARO: SND_DISPARO.play()
        
    def activar_escudo(self):
        self.escudo_activo = True
        self.tiempo_escudo = pygame.time.get_ticks()
        
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

# --- CLASES DE ATAQUES ESPECIALES ---

class BalaEnergia(pygame.sprite.Sprite):
    def __init__(self, x, y, es_jugador, tamaño=25, color=None):
        super().__init__()
        self.es_jugador = es_jugador
        self.tamaño = tamaño
        # Asegurar que el color sea válido
        if color:
            self.color = tuple(max(0, min(255, c)) for c in color)
        else:
            self.color = CIAN_NEON if es_jugador else ROJO_NEON
        
        self.image = pygame.Surface((tamaño, tamaño), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (tamaño//2, tamaño//2), tamaño//2)
        
        color_interior = tuple(min(255, c + 100) for c in self.color)
        pygame.draw.circle(self.image, color_interior, (tamaño//2, tamaño//2), tamaño//4)
        
        pygame.draw.circle(self.image, BLANCO, (tamaño//2, tamaño//2), tamaño//8)
        
        self.rect = self.image.get_rect(center=(x, y))
        self.velocidad_x = -7 if not es_jugador else 10
        self.velocidad_y = 0
        
    def update(self):
        self.rect.x += self.velocidad_x
        self.rect.y += self.velocidad_y
        
        if (self.rect.right < 0 or self.rect.left > ANCHO or 
            self.rect.bottom < 0 or self.rect.top > ALTO):
            self.kill()

class LaserHorizontal:
    def __init__(self, y, color=ROJO_NEON):
        self.y = y
        self.color = color
        self.duracion = 120
        self.temporizador = 0
        self.activo = True
        
    def update(self):
        self.temporizador += 1
        if self.temporizador >= self.duracion:
            self.activo = False
            
    def dibujar(self, superficie):
        if self.activo:
            # Láser con efecto pulsante
            brillo = (math.sin(pygame.time.get_ticks() * 0.01) * 0.5 + 0.5) * 200 + 55
            # Asegurar valores válidos de color
            r = min(255, max(0, self.color[0]))
            g = min(255, max(0, int(brillo)))
            b = min(255, max(0, self.color[2]))
            
            pygame.draw.line(superficie, (r, g, b), (0, self.y), (ANCHO, self.y), 10)

class OndaSonica:
    def __init__(self, x, y, color=(0, 200, 255)):
        self.x = x
        self.y = y
        self.color = color
        self.radio = 20
        self.radio_maximo = 300
        self.velocidad_crecimiento = 6
        self.activo = True
        
    def update(self):
        self.radio += self.velocidad_crecimiento
        if self.radio >= self.radio_maximo:
            self.activo = False
            
    def dibujar(self, superficie):
        if self.activo:
            # Asegurar valores válidos de color
            r = min(255, max(0, self.color[0]))
            g = min(255, max(0, self.color[1]))
            b = min(255, max(0, self.color[2]))
            
            alpha = 150
            pygame.draw.circle(superficie, (r, g, b, alpha), 
                             (self.x, self.y), int(self.radio), 3)

class TormentaRayos:
    def __init__(self, x, y, objetivo_x, objetivo_y, color=(150, 220, 255)):
        self.x = x
        self.y = y
        self.objetivo_x = objetivo_x
        self.objetivo_y = objetivo_y
        self.color = color
        self.duracion = 80
        self.temporizador = 0
        self.activo = True
        
    def update(self):
        self.temporizador += 1
        if self.temporizador >= self.duracion:
            self.activo = False
            
    def dibujar(self, superficie):
        if self.activo:
            # Asegurar valores válidos de color
            r = min(255, max(0, self.color[0]))
            g = min(255, max(0, self.color[1]))
            b = min(255, max(0, self.color[2]))
            
            color_principal = (r, g, b)
            
            # Rayo principal
            pygame.draw.line(superficie, color_principal, 
                           (self.x, self.y), (self.objetivo_x, self.objetivo_y), 4)
            
            # Efecto de electricidad
            for i in range(3):
                offset_x = random.randint(-5, 5)
                offset_y = random.randint(-5, 5)
                color_elec = (min(255, r + 50), min(255, g + 50), 255)
                pygame.draw.line(superficie, color_elec, 
                               (self.x + offset_x, self.y + offset_y), 
                               (self.objetivo_x + offset_x, self.objetivo_y + offset_y), 2)

# --- CLASE JEFE NIVEL 1 MEJORADO Y MÁS AGRESIVO ---

class JefeNivel1(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = IMG_JEFE
        self.rect = self.image.get_rect()
        self.rect.x = ANCHO - 220
        self.rect.y = ALTO // 2 - 100
        
        # VIDA AUMENTADA: 150 puntos de vida (más difícil)
        self.vida = 150
        self.vida_max = 150
        self.fase = 1
        self.velocidad_y = 1.0
        self.direccion_y = 1
        
        # Sistema de ataques mejorado - MÁS AGRESIVO
        self.temporizador_ataque = 0
        self.ataque_actual = 0
        self.duracion_ataque = 100
        self.cooldown_ataque = 100
        
        # Nuevo: Contador de tiempo para cambio de comportamiento
        self.tiempo_inicio = pygame.time.get_ticks()
        self.fase_agresiva = False  # Fase normal por 24 segundos
        self.fase_extrema = False   # Fase extrema después
        
        # Ataques especiales
        self.lasers_horizontales = []
        self.ondas_sonicas = []
        self.tormentas_rayos = []
        
        # Efectos visuales
        self.tiempo_temblor = 0
        self.intensidad_temblor = 0
        self.animacion_dano = 0
        self.animacion_color = 0
        self.parpadeo_pantalla = False
        self.intensidad_parpadeo = 0
        self.contador_parpadeos = 0
        self.parpadeo_activo = False
        
        # Colores vibrantes
        self.colores_fase = [
            ROSA_NEON,      # Ataque 1
            VERDE_NEON,     # Ataque 2
            AZUL_ELECTRICO, # Ataque 3
            AMARILLO_NEON,  # Ataque 4
            PURPURA_NEON    # Ataque 5
        ]

    def update(self):
        # Movimiento vertical MÁS AGRESIVO
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
        
        # Verificar cambio de fase por vida
        if self.vida <= 75 and self.fase == 1:  # 75/150 = 50% de vida
            self.cambiar_fase(2)
        
        # Sistema de cambio de comportamiento por tiempo - 24 SEGUNDOS
        tiempo_actual = pygame.time.get_ticks()
        tiempo_transcurrido = (tiempo_actual - self.tiempo_inicio) / 1000.0
        
        if tiempo_transcurrido > 24 and not self.fase_agresiva:
            self.activar_fase_agresiva()
        
        # Sistema de ciclo de ataques
        self.temporizador_ataque += 1
        self.animacion_color += 0.02
        
        if self.temporizador_ataque > self.duracion_ataque + self.cooldown_ataque:
            self.temporizador_ataque = 0
            self.cambiar_ataque()
        
        # Ejecutar ataque según fase y comportamiento - MÁS FRECUENTES
        if self.temporizador_ataque < self.duracion_ataque:
            if not self.fase_agresiva:
                self.ataque_fase_tranquila()
            elif self.fase == 1:
                self.ataque_fase_1_agresiva()
            elif self.fase == 2:
                self.ataque_fase_2_agresiva()
        
        # Actualizar efectos
        self.actualizar_efectos()
        
        # Animación de daño y color
        if self.animacion_dano > 0:
            self.animacion_dano -= 1
            brillo = 150 + (self.animacion_dano * 10)
            self.image.set_alpha(brillo)
        else:
            # Efecto de cambio de color en fase 2
            if self.fase == 2:
                color_factor = (math.sin(self.animacion_color) * 0.3 + 0.7)
                colored = pygame.Surface(self.image.get_size())
                colored.fill((color_factor, 1.5 * color_factor, color_factor))
                final = self.image.copy()
                final.blit(colored, (0, 0), special_flags=pygame.BLEND_MULT)
                self.image = final
            self.image.set_alpha(255)
    
    def activar_fase_agresiva(self):
        """Activa la fase agresiva después de 24 segundos"""
        self.fase_agresiva = True
        self.velocidad_y = 2.5  # Movimiento MÁS rápido
        self.duracion_ataque = 70  # Ataques MÁS frecuentes
        self.cooldown_ataque = 50
        
        # Activar parpadeo de pantalla PERMANENTE
        self.parpadeo_pantalla = True
        self.parpadeo_activo = True
        self.intensidad_parpadeo = 8  # MÁS intenso
        
        # Temblor constante MÁS fuerte
        self.tiempo_temblor = 9999  # Temblor permanente
        self.intensidad_temblor = 5  # MÁS fuerte

    def cambiar_fase(self, nueva_fase):
        self.fase = nueva_fase
        self.velocidad_y = 2.0  # Movimiento más rápido en fase 2
        
        # Limpiar ataques anteriores
        self.lasers_horizontales = []
        self.ondas_sonicas = []
        self.tormentas_rayos = []
        
        # Aumentar intensidad si ya está en fase agresiva
        if self.fase_agresiva:
            self.intensidad_temblor = 8  # MÁS fuerte
            self.intensidad_parpadeo = 12  # MÁS intenso
        
        self.activar_temblor(20)  # Temblor MÁS fuerte

    def cambiar_ataque(self):
        if self.fase == 1:
            self.ataque_actual = (self.ataque_actual + 1) % 4
        elif self.fase == 2:
            self.ataque_actual = (self.ataque_actual + 1) % 5
        self.activar_temblor(8)  # Temblor MÁS fuerte

    # --- FASE TRANQUILA (primeros 24 segundos) ---
    def ataque_fase_tranquila(self):
        """Ataques simples durante los primeros 24 segundos"""
        if self.ataque_actual == 0:
            self.disparo_simple()
        elif self.ataque_actual == 1:
            self.disparo_doble()
        elif self.ataque_actual == 2:
            self.disparo_triple()
        elif self.ataque_actual == 3:
            self.laser_simple()

    def disparo_simple(self):
        if self.temporizador_ataque % 70 == 0:  # Más lento al inicio
            bala = BalaEnergia(self.rect.left, self.rect.centery, 
                              es_jugador=False, tamaño=20, color=AZUL_ELECTRICO)
            all_sprites.add(bala)
            balas_enemigas.add(bala)

    def disparo_doble(self):
        if self.temporizador_ataque % 80 == 0:  # Más lento al inicio
            for i in range(2):
                y_pos = self.rect.centery + (i-0.5)*60
                bala = BalaEnergia(self.rect.left, y_pos, 
                                  es_jugador=False, tamaño=20, color=VERDE_NEON)
                all_sprites.add(bala)
                balas_enemigas.add(bala)

    def disparo_triple(self):
        if self.temporizador_ataque % 90 == 0:  # Más lento al inicio
            for i in range(3):
                y_pos = self.rect.centery + (i-1)*50
                bala = BalaEnergia(self.rect.left, y_pos, 
                                  es_jugador=False, tamaño=20, color=ROSA_NEON)
                bala.velocidad_y = random.uniform(-1, 1)
                all_sprites.add(bala)
                balas_enemigas.add(bala)

    def laser_simple(self):
        if self.temporizador_ataque == 50:
            y_pos = random.randint(100, ALTO - 100)
            laser = LaserHorizontal(y_pos, ROJO_NEON)
            self.lasers_horizontales.append(laser)

    # --- FASE 1 AGRESIVA (después de 24 segundos) ---
    def ataque_fase_1_agresiva(self):
        """Ataques más intensos después de 24 segundos (fase 1) - MÁS AGRESIVOS"""
        color_actual = self.colores_fase[self.ataque_actual]
        
        if self.ataque_actual == 0:
            self.disparo_rapido(color_actual)
        elif self.ataque_actual == 1:
            self.disparo_arcoiris()
        elif self.ataque_actual == 2:
            self.laser_multiple(color_actual)
        elif self.ataque_actual == 3:
            self.onda_expansiva(color_actual)

    def disparo_rapido(self, color):
        if self.temporizador_ataque % 25 == 0:  # MÁS rápido
            for i in range(5):  # MÁS balas
                y_pos = self.rect.centery + (i-2)*40
                bala = BalaEnergia(self.rect.left, y_pos, 
                                  es_jugador=False, tamaño=25, color=color)
                bala.velocidad_x = -10  # MÁS rápido
                all_sprites.add(bala)
                balas_enemigas.add(bala)

    def disparo_arcoiris(self):
        if self.temporizador_ataque % 35 == 0:  # MÁS rápido
            colores = [ROSA_NEON, VERDE_NEON, AZUL_ELECTRICO, AMARILLO_NEON, PURPURA_NEON, CIAN_NEON]
            for i, color in enumerate(colores):
                y_pos = self.rect.centery + (i-2.5)*30
                bala = BalaEnergia(self.rect.left, y_pos, 
                                  es_jugador=False, tamaño=22, color=color)
                bala.velocidad_y = random.uniform(-3, 3)  # MÁS variación
                all_sprites.add(bala)
                balas_enemigas.add(bala)

    def laser_multiple(self, color):
        if self.temporizador_ataque % 80 == 0:  # MÁS rápido
            for _ in range(3):  # MÁS láseres
                y_pos = random.randint(150, ALTO - 150)
                laser = LaserHorizontal(y_pos, color)
                self.lasers_horizontales.append(laser)

    def onda_expansiva(self, color):
        if self.temporizador_ataque % 90 == 0:  # MÁS rápido
            onda = OndaSonica(self.rect.centerx, self.rect.centery, color)
            self.ondas_sonicas.append(onda)

    # --- FASE 2 AGRESIVA (vida baja + después de 24 segundos) ---
    def ataque_fase_2_agresiva(self):
        """Ataques extremos cuando tiene poca vida y han pasado 24 segundos - MÁS AGRESIVOS"""
        color_actual = self.colores_fase[self.ataque_actual]
        
        if self.ataque_actual == 0:
            self.tormenta_rayos(color_actual)
        elif self.ataque_actual == 1:
            self.lluvia_meteoritos()
        elif self.ataque_actual == 2:
            self.ataque_circulo(color_actual)
        elif self.ataque_actual == 3:
            self.ataque_espiral()
        elif self.ataque_actual == 4:
            self.ataque_saturacion()

    def tormenta_rayos(self, color):
        if self.temporizador_ataque % 40 == 0:  # MÁS rápido
            for _ in range(4):  # MÁS rayos
                objetivo_x = random.randint(100, ANCHO - 100)
                objetivo_y = random.randint(100, ALTO - 100)
                rayo = TormentaRayos(self.rect.centerx, self.rect.centery,
                                    objetivo_x, objetivo_y, color)
                self.tormentas_rayos.append(rayo)

    def lluvia_meteoritos(self):
        if self.temporizador_ataque % 15 == 0:  # MÁS rápido
            for _ in range(4):  # MÁS meteoritos
                x = random.randint(200, ANCHO - 200)
                color = random.choice(self.colores_fase)
                bala = BalaEnergia(x, -50, es_jugador=False, 
                                  tamaño=35, color=color)  # MÁS grande
                bala.velocidad_y = 6  # MÁS rápido
                bala.velocidad_x = random.uniform(-3, 3)  # MÁS variación
                all_sprites.add(bala)
                balas_enemigas.add(bala)

    def ataque_circulo(self, color):
        if self.temporizador_ataque % 50 == 0:  # MÁS rápido
            for i in range(16):  # MÁS balas
                angulo = (i / 16) * 2 * math.pi
                velocidad_x = math.cos(angulo) * 5  # MÁS rápido
                velocidad_y = math.sin(angulo) * 5  # MÁS rápido
                
                bala = BalaEnergia(self.rect.centerx, self.rect.centery,
                                  es_jugador=False, tamaño=25, color=color)
                bala.velocidad_x = velocidad_x
                bala.velocidad_y = velocidad_y
                all_sprites.add(bala)
                balas_enemigas.add(bala)

    def ataque_espiral(self):
        if self.temporizador_ataque % 30 == 0:  # MÁS rápido
            tiempo = pygame.time.get_ticks() * 0.001
            for i in range(10):  # MÁS balas
                angulo = tiempo + (i / 10) * 2 * math.pi
                radio = 120  # MÁS grande
                x = self.rect.centerx + math.cos(angulo) * radio
                y = self.rect.centery + math.sin(angulo) * radio
                
                color_index = i % len(self.colores_fase)
                bala = BalaEnergia(x, y, es_jugador=False, 
                                  tamaño=22, color=self.colores_fase[color_index])
                bala.velocidad_x = math.cos(angulo + math.pi/2) * 4  # MÁS rápido
                bala.velocidad_y = math.sin(angulo + math.pi/2) * 4  # MÁS rápido
                all_sprites.add(bala)
                balas_enemigas.add(bala)

    def ataque_saturacion(self):
        """Ataque masivo que satura la pantalla - MÁS AGRESIVO"""
        if self.temporizador_ataque % 12 == 0:  # MÁS rápido
            # Disparos desde múltiples ángulos
            for i in range(8):  # MÁS balas
                angulo = random.uniform(0, 2*math.pi)
                distancia = random.randint(50, 250)  # MÁS lejos
                x = self.rect.centerx + math.cos(angulo) * distancia
                y = self.rect.centery + math.sin(angulo) * distancia
                
                color = random.choice(self.colores_fase)
                bala = BalaEnergia(x, y, es_jugador=False, 
                                  tamaño=random.randint(20, 30), color=color)  # MÁS grande
                
                # Dirigido hacia el jugador si está vivo
                if jugador.alive():
                    dx = jugador.rect.centerx - x
                    dy = jugador.rect.centery - y
                    distancia_obj = max(1, math.sqrt(dx*dx + dy*dy))
                    bala.velocidad_x = (dx / distancia_obj) * 6  # MÁS rápido
                    bala.velocidad_y = (dy / distancia_obj) * 6  # MÁS rápido
                else:
                    bala.velocidad_x = random.uniform(-6, -3)  # MÁS rápido
                    bala.velocidad_y = random.uniform(-4, 4)   # MÁS variación
                
                all_sprites.add(bala)
                balas_enemigas.add(bala)

    def activar_temblor(self, intensidad):
        self.tiempo_temblor = 15  # MÁS tiempo
        self.intensidad_temblor = intensidad

    def recibir_dano(self, cantidad=1):
        self.vida -= cantidad
        self.animacion_dano = 10
        
        # Aumentar intensidad si está en fase agresiva
        if self.fase_agresiva and self.vida < 75:
            self.intensidad_temblor = min(10, self.intensidad_temblor + 1)  # MÁXIMO 10
            self.intensidad_parpadeo = min(15, self.intensidad_parpadeo + 1)  # MÁXIMO 15
        
        self.activar_temblor(8)  # MÁS fuerte
        return self.vida <= 0

    def actualizar_efectos(self):
        for laser in self.lasers_horizontales[:]:
            laser.update()
            if not laser.activo:
                self.lasers_horizontales.remove(laser)
        
        for onda in self.ondas_sonicas[:]:
            onda.update()
            if not onda.activo:
                self.ondas_sonicas.remove(onda)
        
        for rayo in self.tormentas_rayos[:]:
            rayo.update()
            if not rayo.activo:
                self.tormentas_rayos.remove(rayo)
        
        if self.tiempo_temblor > 0 and self.tiempo_temblor != 9999:
            self.tiempo_temblor -= 1
            
        # Contador de parpadeos para efecto más intenso
        if self.parpadeo_activo:
            self.contador_parpadeos += 1
            if self.contador_parpadeos > 100:  # Cada 100 frames
                self.contador_parpadeos = 0

    def dibujar_efectos(self, superficie):
        for laser in self.lasers_horizontales:
            laser.dibujar(superficie)
        
        for onda in self.ondas_sonicas:
            onda.dibujar(superficie)
        
        for rayo in self.tormentas_rayos:
            rayo.dibujar(superficie)

    def get_temblor_offset(self):
        if self.tiempo_temblor > 0:
            return (random.randint(-self.intensidad_temblor, self.intensidad_temblor),
                   random.randint(-self.intensidad_temblor, self.intensidad_temblor))
        return (0, 0)
    
    def get_parpadeo_alpha(self):
        """Calcula el alpha para el efecto de parpadeo"""
        if self.parpadeo_activo:
            # Parpadeo más intenso y rápido
            tiempo = pygame.time.get_ticks() * 0.01
            # Patrón de parpadeo más caótico
            alpha = (math.sin(tiempo) * 0.5 + 0.5) * self.intensidad_parpadeo * 10
            # Añadir variación aleatoria para mayor intensidad
            alpha += random.randint(0, 20)
            return min(100, alpha)
        return 0

class Bomba(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image_original = IMG_BOMBA
        self.image = self.image_original.copy()
        self.rect = self.image.get_rect(center=(x, y))
        self.velocidad = 3
        self.tiempo_explosion = 100
        self.temporizador = 0
        self.exploto = False
        
    def update(self):
        if not self.exploto:
            self.rect.x += self.velocidad
            self.temporizador += 1
            angulo = self.temporizador * 3
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
                    if distancia < 100:
                        bloque.kill()
            else:
                distancia = math.sqrt((obstaculo.rect.centerx - self.rect.centerx)**2 + 
                                    (obstaculo.rect.centery - self.rect.centery)**2)
                if distancia < 100:
                    obstaculo.kill()
            
        explosion = Explosion(self.rect.centerx, self.rect.centery)
        all_sprites.add(explosion)
        
        self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.radio = 5
        self.radio_maximo = 60
        self.velocidad_crecimiento = 3
        self.image = pygame.Surface((self.radio_maximo*2, self.radio_maximo*2), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(x, y))
        
    def update(self):
        self.radio += self.velocidad_crecimiento
        if self.radio >= self.radio_maximo:
            self.kill()
            
    def draw(self, surface):
        pygame.draw.circle(surface, (255, 220, 0), 
                         self.rect.center, self.radio, 4)
        pygame.draw.circle(surface, (255, 140, 0), 
                         self.rect.center, self.radio-6, 3)
        pygame.draw.circle(surface, (255, 80, 0), 
                         self.rect.center, self.radio-12, 2)

class Potenciador(pygame.sprite.Sprite):
    def __init__(self, tipo):
        super().__init__()
        self.tipo = tipo
        
        if tipo == 1:
            self.image = IMG_MISIL
            self.color = (255, 100, 100)
            self.aura_color = ROJO_NEON
        elif tipo == 2:
            self.image = IMG_BOMBA
            self.color = (255, 200, 100)
            self.aura_color = NARANJA_NEON
        elif tipo == 3:
            self.image = IMG_ESCUDO
            self.color = (100, 200, 255)
            self.aura_color = AZUL_ELECTRICO
            
        self.rect = self.image.get_rect()
        self.rect.x = ANCHO + random.randint(10, 100)
        self.rect.y = random.randint(50, ALTO - 50)
        self.velocidad_x = -1.5
        
        self.tiempo_animacion = 0
        
    def update(self):
        self.rect.x += self.velocidad_x
        
        self.tiempo_animacion += 0.1
        self.rect.y += math.sin(self.tiempo_animacion) * 2
        
        if self.rect.right < 0:
            self.kill()
            
    def aplicar(self, jugador):
        if SND_POWERUP: SND_POWERUP.play()
        
        if self.tipo == 1:
            jugador.bombas += 1
            return "¡BOMBA AGREGADA!"
        elif self.tipo == 2:
            jugador.activar_escudo()
            return "¡ESCUDO ACTIVADO!"
        elif self.tipo == 3:
            jugador.vidas = min(5, jugador.vidas + 1)
            return "¡VIDA EXTRA!"

# --- FUNCIONES AUXILIARES ---

def dibujar_barra_vida(surface, x, y, ancho, alto, progreso, color_fondo, color_relleno):
    pygame.draw.rect(surface, color_fondo, (x, y, ancho, alto))
    
    if progreso > 0:
        ancho_relleno = int(ancho * progreso)
        pygame.draw.rect(surface, color_relleno, (x, y, ancho_relleno, alto))
    
    pygame.draw.rect(surface, BLANCO, (x, y, ancho, alto), 2)

def dibujar_hud(surf, x, y, vidas, puntaje, jugador, tiempo_transcurrido, jefe):
    # Vidas
    for i in range(vidas):
        surf.blit(IMG_VIDA_ICONO, (x + (i * 35), y))
    
    # Barra de vida del jefe
    if len(jefe_grupo) > 0:
        jefe = jefe_grupo.sprite
        progreso_jefe = jefe.vida / jefe.vida_max
        
        if jefe.fase == 1:
            color_fase = ROSA_NEON if not jefe.fase_agresiva else ROJO_NEON
        elif jefe.fase == 2:
            color_fase = VERDE_NEON if not jefe.fase_agresiva else AMARILLO_NEON
            
        dibujar_barra_vida(surf, ANCHO // 2 - 200, 10, 400, 25, progreso_jefe, 
                          (50, 50, 50), color_fase)
        
        # Texto de fase
        fase_texto = f"FASE {jefe.fase}"
        if jefe.fase_agresiva:
            tiempo_fase = (pygame.time.get_ticks() - jefe.tiempo_inicio) / 1000.0
            if tiempo_fase > 24:
                fase_texto += " - ¡MODO AGRESIVO ACTIVADO!"
        fase_surf = FUENTE_PEQ.render(fase_texto, True, BLANCO)
        surf.blit(fase_surf, (ANCHO // 2 - fase_surf.get_width()//2, 40))
    
    # Temporizador
    tiempo_restante = max(0, 300 - tiempo_transcurrido)
    minutos = int(tiempo_restante // 60)
    segundos = int(tiempo_restante % 60)
    tiempo_surf = FUENTE_PEQ.render(f"Tiempo: {minutos:02d}:{segundos:02d}", True, BLANCO)
    surf.blit(tiempo_surf, (ANCHO - 150, 10))
    
    # Power-ups
    y_powerups = 80
    if jugador.bombas > 0:
        txt_bomba = FUENTE_PEQ.render(f"Bombas: {jugador.bombas} (B)", True, NARANJA_NEON)
        surf.blit(txt_bomba, (10, y_powerups))
        y_powerups += 25
        
    if jugador.escudo_activo:
        tiempo_restante = max(0, jugador.duracion_escudo - (pygame.time.get_ticks() - jugador.tiempo_escudo))
        txt_escudo = FUENTE_PEQ.render(f"Escudo: {tiempo_restante/1000:.1f}s", True, AZUL_ELECTRICO)
        surf.blit(txt_escudo, (10, y_powerups))
        y_powerups += 25

def dibujar_game_over(surf, puntaje):
    overlay = pygame.Surface((ANCHO, ALTO))
    overlay.set_alpha(200)
    overlay.fill(NEGRO)
    surf.blit(overlay, (0,0))
    
    txt_go = FUENTE_GRANDE.render("GAME OVER", True, ROJO_NEON)
    txt_pts = FUENTE_MEDIANA.render(f"Puntaje Final: {puntaje}", True, BLANCO)
    
    txt_op1 = FUENTE_PEQ.render("[C]ontinuar (3 vidas)", True, AMARILLO_NEON)
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
    
    for i in range(150):
        x = random.randint(0, ANCHO)
        y = random.randint(0, ALTO)
        tamaño = random.randint(1, 3)
        color = random.choice([AZUL_ELECTRICO, VERDE_NEON, ROSA_NEON, AMARILLO_NEON, CIAN_NEON])
        brillo = random.randint(100, 255)
        pygame.draw.circle(surf, color, (x, y), tamaño)
    
    titulo = FUENTE_TITULO.render("¡NIVEL 1 COMPLETADO!", True, ROSA_NEON)
    surf.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 50))
    
    y_pos = 150
    estadisticas_lista = [
        (f"PUNTAJE TOTAL: {estadisticas['puntaje']}", VERDE_NEON),
        (f"DAÑO INFLIGIDO AL JEFE: {estadisticas['dano_jefe']}", ROJO_NEON),
        (f"MUERTES: {estadisticas['muertes']}", ROSA_NEON),
        (f"TIEMPO TOTAL: {estadisticas['tiempo_formateado']}", CIAN_NEON),
        (f"VIDAS RESTANTES: {estadisticas['vidas_restantes']}/{estadisticas['vidas_iniciales']}", AZUL_ELECTRICO)
    ]
    
    for texto, color in estadisticas_lista:
        txt = FUENTE_MEDIANA.render(texto, True, color)
        surf.blit(txt, (ANCHO//2 - txt.get_width()//2, y_pos))
        y_pos += 60
    
    if mensaje_error:
        error_txt = FUENTE_MEDIANA.render(mensaje_error, True, ROJO_NEON)
        surf.blit(error_txt, (ANCHO//2 - error_txt.get_width()//2, y_pos + 20))
        y_pos += 60
        
        alt_txt = FUENTE_ARCADA.render("Presiona R para reiniciar nivel 1", True, AMARILLO_NEON)
        surf.blit(alt_txt, (ANCHO//2 - alt_txt.get_width()//2, y_pos + 20))
        y_pos += 40
    
    tiempo_actual = pygame.time.get_ticks()
    if (tiempo_actual // 500) % 2 == 0:
        if not mensaje_error:
            mensaje = FUENTE_ARCADA.render("PRESIONA ESPACIO para avanzar al NIVEL 2 o ESC para salir", True, BLANCO)
        else:
            mensaje = FUENTE_ARCADA.render("PRESIONA R para reiniciar nivel 1 o ESC para salir", True, BLANCO)
        surf.blit(mensaje, (ANCHO//2 - mensaje.get_width()//2, ALTO - 80))

def reproducir_musica_fondo():
    """Reproduce música de fondo para el nivel 1"""
    try:
        # Intentar cargar diferentes nombres de archivo de música
        posibles_musicas = [
            "musica_nivel1.mp3",
            "musica_fondo.mp3", 
            "background_music.mp3",
            "music.mp3"
        ]
        
        for musica in posibles_musicas:
            if os.path.exists(musica):
                pygame.mixer.music.load(musica)
                pygame.mixer.music.set_volume(0.5)  # Volumen al 50%
                pygame.mixer.music.play(-1)  # Repetir indefinidamente
                print(f"Reproduciendo música: {musica}")
                return True
        
        print("No se encontró archivo de música de fondo")
        return False
        
    except Exception as e:
        print(f"Error al reproducir música: {e}")
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
obstaculos = pygame.sprite.Group()
jugador = Jugador()
all_sprites.add(jugador)

# --- FUNCIÓN DE REINICIO ---
def reiniciar_nivel():
    balas_jugador.empty()
    balas_enemigas.empty()
    jefe_grupo.empty()
    potenciadores.empty()
    obstaculos.empty()
    
    jugador.rect.center = (100, ALTO // 2)
    jugador.vidas = 5
    jugador.vidas_iniciales = 5
    jugador.invulnerable = False
    jugador.bombas = 0
    jugador.escudo_activo = False
    jugador.muertes = 0
    
    return 0, 1

def continuar_juego():
    balas_enemigas.empty()
    potenciadores.empty()
    
    if len(jefe_grupo) > 0:
        jefe = jefe_grupo.sprite
        jefe.lasers_horizontales = []
        jefe.ondas_sonicas = []
        jefe.tormentas_rayos = []
    
    jugador.resetear_posicion()
    jugador.vidas = 3

# --- LOOP PRINCIPAL NIVEL 1 ---

def juego():
    estado = 0  # 0: Historia, 1: Cuenta, 2: Juego, 3: Winner, 4: Resultados, 5: Game Over
    
    puntaje = 0
    estado_anterior = 2
    
    fondo_x = 0
    tiempo_inicio_conteo = 0
    tiempo_inicio_nivel = 0
    
    tiempo_inicio_winner = 0
    efecto_salto = 0
    direccion_salto = 1
    
    tiempo_total_nivel = 0
    
    tiempo_temblor = 0
    intensidad_temblor = 0
    mensaje_powerup = ""
    tiempo_mensaje = 0
    
    # Variables para efectos de pantalla
    parpadeo_alpha = 0
    direccion_parpadeo = 1
    parpadeo_activo = False
    
    # Variables para música
    musica_activa = False
    musica_pausada = False
    
    # Textos para la historia
    titulo_inicio = "Y CAAS?"
    subtitulo_inicio = "NIVEL1"
    
    historia_inicio = (
     "Memo llega al edificio F20, donde lo espera el temido Profe Casto. "
    "Este es el primer paso hacia su graduación galáctica. Tendrás unos "
    "instantes para prepararte antes de que Casto despliegue toda su "
    "precisión y poder. ¡Esquiva, resiste y vence para aprobar la materia!"
    )
    
    pantalla_historia = PantallaHistoria(titulo_inicio, subtitulo_inicio, historia_inicio)
    
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
                pantalla_historia.manejar_eventos([event])
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b and estado == 2:
                    jugador.lanzar_bomba()
                
                if estado == 5:  # Game Over
                    if event.key == pygame.K_c:
                        if SND_COIN: SND_COIN.play()
                        continuar_juego()
                        estado = estado_anterior
                        if musica_pausada:
                            reanudar_musica()
                            musica_pausada = False

                    elif event.key == pygame.K_r:
                        puntaje, estado = reiniciar_nivel()
                        tiempo_inicio_conteo = pygame.time.get_ticks()
                        tiempo_inicio_nivel = pygame.time.get_ticks()
                        if SND_CONTEO: SND_CONTEO.play()
                        detener_musica()
                        musica_activa = False
                        musica_pausada = False

                    elif event.key == pygame.K_m:
                        ejecutando = False
                
                if estado == 4:  # Resultados
                    if event.key == pygame.K_SPACE:
                        exito, mensaje = cargar_siguiente_nivel()
                        if not exito:
                            # Mostrar error
                            pass
                    
                    elif event.key == pygame.K_r:
                        puntaje, estado = reiniciar_nivel()
                        tiempo_inicio_conteo = pygame.time.get_ticks()
                        tiempo_inicio_nivel = pygame.time.get_ticks()
                        detener_musica()
                        musica_activa = False
                        musica_pausada = False
                    
                    elif event.key == pygame.K_ESCAPE:
                        ejecutando = False

        # --- MÁQUINA DE ESTADOS ---
        if estado == 0:
            pantalla_historia.actualizar(dt)
            pantalla_historia.dibujar(PANTALLA)
            
            if pantalla_historia.terminada:
                estado = 1
                tiempo_inicio_conteo = pygame.time.get_ticks()
                tiempo_inicio_nivel = pygame.time.get_ticks()
                if SND_CONTEO: SND_CONTEO.play()

        elif estado == 1:
            PANTALLA.blit(IMG_FONDO, (0,0))
            ahora = pygame.time.get_ticks()
            delta = ahora - tiempo_inicio_conteo
            
            texto = ""
            color = BLANCO
            if delta < 500: 
                texto = "3"
                color = ROJO_NEON
            elif delta < 800: 
                texto = "2"
                color = NARANJA_NEON
            elif delta < 1000: 
                texto = "1"
                color = AMARILLO_NEON
            elif delta < 4000: 
                texto = "¡COMIENZA!"
                color = VERDE_NEON
                # Iniciar música cuando empieza el juego
                if not musica_activa:
                    reproducir_musica_fondo()
                    musica_activa = True
            else:
                estado = 2
                jefe = JefeNivel1()
                all_sprites.add(jefe)
                jefe_grupo.add(jefe)
            
            if texto:
                surf = FUENTE_GRANDE.render(texto, True, color)
                PANTALLA.blit(surf, surf.get_rect(center=(ANCHO//2, ALTO//2)))

        elif estado == 2:
            # Obtener jefe para efectos
            jefe = None
            if len(jefe_grupo) > 0:
                jefe = jefe_grupo.sprite
            
            # Efecto de temblor base
            offset_x, offset_y = (0, 0)
            
            # Efecto de temblor del jefe
            if jefe:
                jefe_offset_x, jefe_offset_y = jefe.get_temblor_offset()
                offset_x += jefe_offset_x
                offset_y += jefe_offset_y
                
                # Verificar si está en fase agresiva para efectos adicionales
                if jefe.fase_agresiva:
                    # Temblor constante más fuerte
                    offset_x += random.randint(-jefe.intensidad_temblor, jefe.intensidad_temblor)
                    offset_y += random.randint(-jefe.intensidad_temblor, jefe.intensidad_temblor)
                    
                    # Parpadeo de pantalla PERMANENTE después de 24 segundos
                    if jefe.parpadeo_activo:
                        parpadeo_activo = True
                        # Obtener alpha del jefe para el parpadeo
                        parpadeo_alpha = jefe.get_parpadeo_alpha()
            
            # Temblor por golpes
            if tiempo_temblor > 0:
                offset_x += random.randint(-intensidad_temblor, intensidad_temblor)
                offset_y += random.randint(-intensidad_temblor, intensidad_temblor)
                tiempo_temblor -= 1
            
            # Scroll Fondo con offset
            fondo_x -= 2
            if fondo_x <= -ANCHO: fondo_x = 0
            
            # Crear superficie para efectos de parpadeo
            pantalla_base = pygame.Surface((ANCHO, ALTO))
            pantalla_base.blit(IMG_FONDO, (fondo_x + offset_x, offset_y))
            pantalla_base.blit(IMG_FONDO, (fondo_x + ANCHO + offset_x, offset_y))

            # Generar Potenciadores
            if len(potenciadores) == 0 and random.randint(0, 400) < 2:
                tipo = random.randint(1, 3)
                p = Potenciador(tipo)
                all_sprites.add(p)
                potenciadores.add(p)

            # Actualizar y dibujar sprites en pantalla_base
            all_sprites.update()
            all_sprites.draw(pantalla_base)
            
            # Dibujar efectos del jefe
            if jefe:
                jefe.dibujar_efectos(pantalla_base)
            
            # Copiar a pantalla principal
            PANTALLA.blit(pantalla_base, (0, 0))
            
            # Aplicar efecto de parpadeo si está activo (DESPUÉS DE 24 SEGUNDOS)
            if parpadeo_activo and parpadeo_alpha > 0:
                # Crear overlay de parpadeo con color rojo intenso
                overlay = pygame.Surface((ANCHO, ALTO))
                overlay.set_alpha(int(parpadeo_alpha))
                overlay.fill((255, 50, 50))  # Rojo parpadeante
                PANTALLA.blit(overlay, (0, 0))

        elif estado == 3:
            PANTALLA.blit(IMG_FONDO, (0,0))
            efecto_salto += direccion_salto * 3
            if abs(efecto_salto) > 25: direccion_salto *= -1
            
            r = IMG_WINNER.get_rect(center=(ANCHO//2, ALTO//2 + efecto_salto))
            PANTALLA.blit(IMG_WINNER, r)
            
            if pygame.time.get_ticks() - tiempo_inicio_winner > 3000:
                estado = 4
                detener_musica()
                musica_activa = False

        elif estado == 4:
            # Calcular estadísticas
            dano_jefe = 0
            if len(jefe_grupo) > 0:
                jefe = jefe_grupo.sprite
                dano_jefe = jefe.vida_max - jefe.vida
            else:
                dano_jefe = 150  # Vida máxima del jefe
            
            minutos = int(tiempo_total_nivel // 60)
            segundos = int(tiempo_total_nivel % 60)
            tiempo_formateado = f"{minutos:02d}:{segundos:02d}"
            
            estadisticas = {
                'puntaje': puntaje,
                'dano_jefe': dano_jefe,
                'muertes': jugador.muertes,
                'tiempo_formateado': tiempo_formateado,
                'vidas_restantes': jugador.vidas,
                'vidas_iniciales': jugador.vidas_iniciales
            }
            
            dibujar_resultados_finales(PANTALLA, estadisticas)
            
        elif estado == 5:
            if musica_activa and not musica_pausada:
                pausar_musica()
                musica_pausada = True
            
            PANTALLA.blit(IMG_FONDO, (0,0)) 
            dibujar_game_over(PANTALLA, puntaje)

        # --- COLISIONES (Estado 2) ---
        if estado == 2:
            # Colisiones con potenciadores
            hits_powerups = pygame.sprite.spritecollide(jugador, potenciadores, True)
            for powerup in hits_powerups:
                mensaje = powerup.aplicar(jugador)
                mensaje_powerup = mensaje
                tiempo_mensaje = pygame.time.get_ticks()
            
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
                        tiempo_temblor = 5
                        intensidad_temblor = 2
            
            # Daño al Jugador
            if pygame.sprite.spritecollide(jugador, balas_enemigas, True):
                if jugador.recibir_dano():
                    if SND_EXPLOSION: SND_EXPLOSION.play()
                    tiempo_temblor = 10
                    intensidad_temblor = 2

            if len(jefe_grupo) > 0 and pygame.sprite.spritecollide(jugador, jefe_grupo, False):
                if jugador.recibir_dano():
                    if SND_EXPLOSION: SND_EXPLOSION.play()
                    tiempo_temblor = 15
                    intensidad_temblor = 4
            
            # Láseres horizontales
            if len(jefe_grupo) > 0:
                jefe = jefe_grupo.sprite
                for laser in jefe.lasers_horizontales:
                    if laser.activo:
                        laser_rect = pygame.Rect(0, laser.y - 5, ANCHO, 10)
                        if laser_rect.colliderect(jugador.rect):
                            if jugador.recibir_dano():
                                if SND_EXPLOSION: SND_EXPLOSION.play()
                                tiempo_temblor = 8
                                intensidad_temblor = 2
            
            # Ondas sónicas
            for onda in jefe.ondas_sonicas[:]:
                distancia = math.sqrt((onda.x - jugador.rect.centerx)**2 + 
                                    (onda.y - jugador.rect.centery)**2)
                if distancia < onda.radio:
                    if jugador.recibir_dano():
                        if SND_EXPLOSION: SND_EXPLOSION.play()
                        tiempo_temblor = 6
                        intensidad_temblor = 2
            
            # Verificar Muerte
            if jugador.vidas <= 0:
                estado_anterior = estado
                estado = 5
                if SND_GAMEOVER: SND_GAMEOVER.play()

            # HUD
            if len(jefe_grupo) > 0:
                dibujar_hud(PANTALLA, 10, 10, jugador.vidas, puntaje, jugador, tiempo_total_nivel, jefe_grupo.sprite)
            
            # Mostrar mensaje de potenciador
            if mensaje_powerup and pygame.time.get_ticks() - tiempo_mensaje < 2000:
                txt_powerup = FUENTE_MEDIANA.render(mensaje_powerup, True, AMARILLO_NEON)
                PANTALLA.blit(txt_powerup, (ANCHO//2 - txt_powerup.get_width()//2, 100))
            elif pygame.time.get_ticks() - tiempo_mensaje >= 2000:
                mensaje_powerup = ""

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    juego()