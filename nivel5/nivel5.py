# nivel5/nivel5.py

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
pygame.display.set_caption("Nivel 5 - EL RECTOR")

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
DORADO = (255, 215, 0)
PLATEADO = (192, 192, 192)
ROSA_FUCSIA = (255, 0, 255)
VERDE_LIMA = (50, 205, 50)
NARANJA_FUEGO = (255, 69, 0)

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
        ruta_nivel5 = os.path.join("nivel5", nombre)
        if os.path.exists(ruta_nivel5):
            if alpha:
                img = pygame.image.load(ruta_nivel5).convert_alpha()
            else:
                img = pygame.image.load(ruta_nivel5).convert()
        else:
            ruta_nivel3 = os.path.join("nivel3", nombre)
            if os.path.exists(ruta_nivel3):
                if alpha:
                    img = pygame.image.load(ruta_nivel3).convert_alpha()
                else:
                    img = pygame.image.load(ruta_nivel3).convert()
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
IMG_FONDO = cargar_imagen("fondo_nivel3.png")
IMG_WINNER = cargar_imagen("winner.png", (400, 200))
IMG_VIDA_ICONO = cargar_imagen("vidas.png", (30, 30))

# Imágenes para los jefes
IMG_JEFE1 = cargar_imagen("jefe_nivel5.png", (200, 200))
IMG_JEFE2 = cargar_imagen("jefe_nivel5.png", (220, 220))
IMG_JEFE3 = cargar_imagen("jefe_nivel5.png", (240, 240))
IMG_JEFE4 = cargar_imagen("jefe_nivel5.png", (260, 260))
IMG_JEFE5 = cargar_imagen("jefe_nivel5.png", (300, 300))

# Imágenes para las pantallas de historia
IMG_HISTORIA_INICIO = cargar_imagen("historia_inicio_nivel5.png", (ANCHO, ALTO), alpha=True)
IMG_HISTORIA_FINAL1 = cargar_imagen("historia_inicio_nivel5.png", (ANCHO, ALTO), alpha=True)
IMG_HISTORIA_FINAL2 = cargar_imagen("historia_final_nivel5.png", (ANCHO, ALTO), alpha=True)
IMG_HISTORIA_FINAL3 = cargar_imagen("historia_inicio_nivel5.png", (ANCHO, ALTO), alpha=True)

# Escalar fondo
if IMG_FONDO.get_size() != (ANCHO, ALTO):
    IMG_FONDO = pygame.transform.scale(IMG_FONDO, (ANCHO, ALTO))

# Sonidos
def cargar_sonido(nombre):
    try:
        ruta_nivel5 = os.path.join("nivel5", nombre)
        if os.path.exists(ruta_nivel5):
            return pygame.mixer.Sound(ruta_nivel5)
        else:
            ruta_nivel3 = os.path.join("nivel3", nombre)
            if os.path.exists(ruta_nivel3):
                return pygame.mixer.Sound(ruta_nivel3)
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
SND_BOSS_HURT = cargar_sonido("boss_hurt.mp3")
SND_BOSS_TRANSFORM = cargar_sonido("boss_transform.mp3")
SND_LASER = cargar_sonido("disparo.mp3")
SND_ELECTRICIDAD = cargar_sonido("explosion.mp3")
SND_CAIDA_FUEGO = cargar_sonido("explosion.mp3")

# --- CLASES ---

class PantallaHistoria:
    def __init__(self, imagen_fondo, titulo, subtitulo, texto_historia):
        self.imagen_fondo = imagen_fondo
        self.titulo = titulo
        self.subtitulo = subtitulo
        self.texto_historia = texto_historia
        
        self.palabras = texto_historia.split()
        self.palabras_mostradas = 0
        self.temporizador_palabra = 0
        self.intervalo_palabra = 70
        self.tiempo_inicio = 0
        
        self.efecto_brillo = 0
        self.direccion_brillo = 1
        self.particulas = []
        self.generar_particulas()
        
        self.terminada = False
        self.saltar = False
        
        self.sonido_escritura = cargar_sonido("teclado.mp3")
        
        self.alpha_panel = 0
        self.alpha_texto = 0
        self.fase_transicion = 0
    
    def generar_particulas(self):
        self.particulas = []
        for _ in range(50):
            x = random.randint(0, ANCHO)
            y = random.randint(0, ALTO)
            velocidad_x = random.uniform(-0.5, 0.5)
            velocidad_y = random.uniform(-0.5, 0.5)
            tamaño = random.randint(1, 3)
            vida = random.randint(50, 150)
            color = random.choice([DORADO, PLATEADO, PURPURA_NEON, CIAN_NEON, ROSA_NEON])
            self.particulas.append([x, y, velocidad_x, velocidad_y, tamaño, vida, color])
    
    def actualizar_particulas(self):
        for i, particula in enumerate(self.particulas):
            particula[0] += particula[2]
            particula[1] += particula[3]
            particula[5] -= 1
            
            if particula[5] <= 0:
                x = random.randint(0, ANCHO)
                y = random.randint(0, ALTO)
                velocidad_x = random.uniform(-0.5, 0.5)
                velocidad_y = random.uniform(-0.5, 0.5)
                tamaño = random.randint(1, 3)
                vida = random.randint(50, 150)
                color = random.choice([DORADO, PLATEADO, PURPURA_NEON, CIAN_NEON, ROSA_NEON])
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
                    elif pygame.time.get_ticks() - self.tiempo_inicio > 2000:
                        self.terminada = True
    
    def dibujar(self, pantalla):
        pantalla.blit(self.imagen_fondo, (0, 0))
        
        for particula in self.particulas:
            x, y, _, _, tamaño, vida, color = particula
            alpha = min(255, vida * 2)
            s = pygame.Surface((tamaño*2, tamaño*2), pygame.SRCALPHA)
            pygame.draw.circle(s, (*color[:3], alpha), (tamaño, tamaño), tamaño)
            pantalla.blit(s, (int(x), int(y)))
        
        # Panel central
        panel_ancho = min(1000, ANCHO - 200)
        panel_alto = min(600, ALTO - 100)
        panel_x = (ANCHO - panel_ancho) // 2
        panel_y = (ALTO - panel_alto) // 2
        
        panel_surface = pygame.Surface((panel_ancho, panel_alto), pygame.SRCALPHA)
        panel_color = (10, 10, 30, int(self.alpha_panel * 0.8))
        pygame.draw.rect(panel_surface, panel_color, (0, 0, panel_ancho, panel_alto), border_radius=15)
        
        borde_color = list(DORADO)
        borde_color = [int(c * (0.7 + 0.3 * self.efecto_brillo)) for c in borde_color]
        pygame.draw.rect(panel_surface, (*borde_color, int(self.alpha_panel)), 
                        (0, 0, panel_ancho, panel_alto), 5, border_radius=15)
        
        pantalla.blit(panel_surface, (panel_x, panel_y))
        
        # Título
        titulo_color = list(DORADO)
        titulo_color = [int(c * (0.8 + 0.2 * self.efecto_brillo)) for c in titulo_color]
        titulo_alpha = min(255, int(self.alpha_texto))
        
        titulo_surf = FUENTE_TITULO.render(self.titulo, True, (*titulo_color, titulo_alpha))
        titulo_rect = titulo_surf.get_rect(center=(ANCHO // 2, panel_y + 80))
        
        titulo_sombra = FUENTE_TITULO.render(self.titulo, True, (100, 80, 0, titulo_alpha))
        pantalla.blit(titulo_sombra, (titulo_rect.x + 4, titulo_rect.y + 4))
        pantalla.blit(titulo_surf, titulo_rect)
        
        # Subtítulo
        subtitulo_alpha = min(255, int(self.alpha_texto * 0.9))
        subtitulo_surf = FUENTE_SUBTITULO.render(self.subtitulo, True, (PLATEADO[0], PLATEADO[1], PLATEADO[2], subtitulo_alpha))
        subtitulo_rect = subtitulo_surf.get_rect(center=(ANCHO // 2, panel_y + 150))
        pantalla.blit(subtitulo_surf, subtitulo_rect)
        
        # Línea decorativa
        pygame.draw.line(pantalla, (PURPURA_NEON[0], PURPURA_NEON[1], PURPURA_NEON[2], subtitulo_alpha),
                        (panel_x + 50, panel_y + 190),
                        (panel_x + panel_ancho - 50, panel_y + 190), 3)
        
        # Texto de historia
        texto_actual = " ".join(self.palabras[:self.palabras_mostradas])
        texto_x = panel_x + 60
        texto_y = panel_y + 220
        ancho_texto = panel_ancho - 120
        
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
            if y_pos < panel_y + panel_alto - 100:
                linea_alpha = min(255, int(self.alpha_texto * (1.0 - i * 0.05)))
                if linea_alpha > 0:
                    linea_surf = FUENTE_HISTORIA.render(linea, True, (BLANCO[0], BLANCO[1], BLANCO[2], linea_alpha))
                    pantalla.blit(linea_surf, (texto_x, y_pos))
                    y_pos += 40
        
        # Cursor parpadeante
        if self.palabras_mostradas < len(self.palabras) and self.fase_transicion >= 1:
            if (pygame.time.get_ticks() // 500) % 2 == 0:
                if palabras_linea:
                    ultima_linea = palabras_linea[-1]
                    cursor_x = texto_x + FUENTE_HISTORIA.size(ultima_linea)[0]
                    cursor_y = y_pos - 10
                else:
                    cursor_x = texto_x
                    cursor_y = texto_y
                
                cursor_height = 35
                cursor_alpha = min(255, int(self.alpha_texto))
                pygame.draw.rect(pantalla, (DORADO[0], DORADO[1], DORADO[2], cursor_alpha),
                               (cursor_x, cursor_y, 3, cursor_height))
        
        # Mensaje para continuar
        if self.palabras_mostradas >= len(self.palabras) and self.fase_transicion >= 1:
            if (pygame.time.get_ticks() // 500) % 2 == 0:
                continuar_alpha = min(255, int(self.alpha_texto))
                continuar_surf = FUENTE_ARCADA.render("Presiona ESPACIO para continuar", True, 
                                                    (AMARILLO[0], AMARILLO[1], AMARILLO[2], continuar_alpha))
                continuar_rect = continuar_surf.get_rect(center=(ANCHO // 2, panel_y + panel_alto - 60))
                
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
    
    def reiniciar(self):
        self.palabras_mostradas = 0
        self.temporizador_palabra = 0
        self.tiempo_inicio = 0
        self.terminada = False
        self.saltar = False
        self.alpha_panel = 0
        self.alpha_texto = 0
        self.fase_transicion = 0

# --- CLASE JUGADOR CON DISPARO ORIGINAL ---
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
        self.intervalo_disparo = 200  # Igual que en nivel 3

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
        # DISPARO ORIGINAL DEL NIVEL 3 - Simple y directo
        if self.misiles_temporales_activos:
            return self.disparar_misil_temporal()
        else:
            bala = BalaJugador(self.rect.right, self.rect.centery)
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
            bomba = BombaExplosiva(self.rect.centerx, self.rect.centery)
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

# --- DISPARO ORIGINAL DEL JUGADOR ---
class BalaJugador(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # DISPARO IDÉNTICO AL DEL NIVEL 3
        self.image = pygame.Surface((15, 4), pygame.SRCALPHA)
        pygame.draw.rect(self.image, (0, 255, 255), (0, 0, 15, 4))
        pygame.draw.rect(self.image, (255, 255, 255), (0, 0, 5, 4))
        self.rect = self.image.get_rect(midleft=(x, y))
        self.velocidad_x = 8
        self.velocidad_y = 0
        
    def update(self):
        self.rect.x += self.velocidad_x
        self.rect.y += self.velocidad_y
        
        if (self.rect.right < 0 or self.rect.left > ANCHO or 
            self.rect.bottom < 0 or self.rect.top > ALTO):
            self.kill()

# --- CLASE PARA BALAS DE ENEMIGOS ---
class BalaEnemiga(pygame.sprite.Sprite):
    def __init__(self, x, y, color=None, tamaño=30, velocidad_x=-5):
        super().__init__()
        self.tamaño = tamaño
        self.color = color if color else random.choice([ROSA_NEON, VERDE_NEON, CIAN_NEON, PURPURA_NEON])
        self.velocidad_x = velocidad_x
        self.velocidad_y = 0
        self.tiempo_vida = 0
        
        # Crear bala con efectos espectaculares
        self.image = pygame.Surface((tamaño, tamaño), pygame.SRCALPHA)
        
        # Círculo exterior brillante
        pygame.draw.circle(self.image, (*self.color, 200), (tamaño//2, tamaño//2), tamaño//2)
        
        # Círculo medio con color más brillante
        color_medio = tuple(min(255, c + 50) for c in self.color)
        pygame.draw.circle(self.image, (*color_medio, 220), (tamaño//2, tamaño//2), tamaño//3)
        
        # Núcleo blanco brillante
        pygame.draw.circle(self.image, (*BLANCO, 240), (tamaño//2, tamaño//2), tamaño//6)
        
        # Puntos brillantes
        for _ in range(8):
            px = random.randint(2, tamaño-2)
            py = random.randint(2, tamaño-2)
            radio = random.randint(2, 4)
            pygame.draw.circle(self.image, (*BLANCO, 200), (px, py), radio)
        
        self.rect = self.image.get_rect(center=(x, y))
        
    def update(self):
        self.rect.x += self.velocidad_x
        self.rect.y += self.velocidad_y
        self.tiempo_vida += 1
        
        # Efecto de pulsación más pronunciado
        if self.tiempo_vida % 4 == 0:
            pulsacion = math.sin(self.tiempo_vida * 0.1) * 5
            tamaño_actual = self.tamaño + int(pulsacion)
            self.image = pygame.transform.scale(self.image, (tamaño_actual, tamaño_actual))
            self.rect = self.image.get_rect(center=self.rect.center)
        
        # Cambio de color sutil
        if self.tiempo_vida % 10 == 0:
            factor = math.sin(self.tiempo_vida * 0.05) * 0.3 + 0.7
            color_actual = tuple(int(c * factor) for c in self.color)
            
            # Recrear la bala con nuevo color
            self.image = pygame.Surface((self.tamaño, self.tamaño), pygame.SRCALPHA)
            pygame.draw.circle(self.image, (*color_actual, 200), (self.tamaño//2, self.tamaño//2), self.tamaño//2)
            color_medio = tuple(min(255, c + 50) for c in color_actual)
            pygame.draw.circle(self.image, (*color_medio, 220), (self.tamaño//2, self.tamaño//2), self.tamaño//3)
            pygame.draw.circle(self.image, (*BLANCO, 240), (self.tamaño//2, self.tamaño//2), self.tamaño//6)
        
        if self.rect.right < 0 or self.rect.left > ANCHO or self.rect.top > ALTO or self.rect.bottom < 0:
            self.kill()

# --- CLASES DE ATAQUES ESPECTACULARES PARA LOS JEFES ---

class BalaEnergiaGrande(pygame.sprite.Sprite):
    def __init__(self, x, y, color=None, tamaño=40, velocidad_x=-5):
        super().__init__()
        self.tamaño = tamaño
        self.color = color if color else random.choice([ROSA_NEON, VERDE_NEON, CIAN_NEON, PURPURA_NEON])
        self.velocidad_x = velocidad_x
        self.velocidad_y = 0
        self.tiempo_vida = 0
        
        # Crear bala con efectos espectaculares
        self.image = pygame.Surface((tamaño, tamaño), pygame.SRCALPHA)
        
        # Círculo exterior brillante
        pygame.draw.circle(self.image, (*self.color, 200), (tamaño//2, tamaño//2), tamaño//2)
        
        # Círculo medio con color más brillante
        color_medio = tuple(min(255, c + 50) for c in self.color)
        pygame.draw.circle(self.image, (*color_medio, 220), (tamaño//2, tamaño//2), tamaño//3)
        
        # Núcleo blanco brillante
        pygame.draw.circle(self.image, (*BLANCO, 240), (tamaño//2, tamaño//2), tamaño//6)
        
        # Puntos brillantes
        for _ in range(8):
            px = random.randint(2, tamaño-2)
            py = random.randint(2, tamaño-2)
            radio = random.randint(2, 4)
            pygame.draw.circle(self.image, (*BLANCO, 200), (px, py), radio)
        
        self.rect = self.image.get_rect(center=(x, y))
        
    def update(self):
        self.rect.x += self.velocidad_x
        self.rect.y += self.velocidad_y
        self.tiempo_vida += 1
        
        # Efecto de pulsación más pronunciado
        if self.tiempo_vida % 4 == 0:
            pulsacion = math.sin(self.tiempo_vida * 0.1) * 5
            tamaño_actual = self.tamaño + int(pulsacion)
            self.image = pygame.transform.scale(self.image, (tamaño_actual, tamaño_actual))
            self.rect = self.image.get_rect(center=self.rect.center)
        
        # Cambio de color sutil
        if self.tiempo_vida % 10 == 0:
            factor = math.sin(self.tiempo_vida * 0.05) * 0.3 + 0.7
            color_actual = tuple(int(c * factor) for c in self.color)
            
            # Recrear la bala con nuevo color
            self.image = pygame.Surface((self.tamaño, self.tamaño), pygame.SRCALPHA)
            pygame.draw.circle(self.image, (*color_actual, 200), (self.tamaño//2, self.tamaño//2), self.tamaño//2)
            color_medio = tuple(min(255, c + 50) for c in color_actual)
            pygame.draw.circle(self.image, (*color_medio, 220), (self.tamaño//2, self.tamaño//2), self.tamaño//3)
            pygame.draw.circle(self.image, (*BLANCO, 240), (self.tamaño//2, self.tamaño//2), self.tamaño//6)
        
        if self.rect.right < 0 or self.rect.left > ANCHO or self.rect.top > ALTO or self.rect.bottom < 0:
            self.kill()

class MisilTeledirigido(pygame.sprite.Sprite):
    def __init__(self, x, y, objetivo, color=ROJO):
        super().__init__()
        self.tamaño = 45
        self.objetivo = objetivo
        self.color = color
        
        # Crear misil con diseño detallado
        self.image = pygame.Surface((self.tamaño, self.tamaño), pygame.SRCALPHA)
        
        # Cuerpo del misil
        pygame.draw.ellipse(self.image, self.color, (5, 10, 35, 25))
        
        # Cabezal del misil
        pygame.draw.polygon(self.image, NARANJA, [(40, 17), (self.tamaño, 12), (self.tamaño, 22)])
        
        # Alas
        pygame.draw.polygon(self.image, (200, 100, 0), [(20, 10), (15, 0), (25, 0)])
        pygame.draw.polygon(self.image, (200, 100, 0), [(20, 35), (15, 45), (25, 45)])
        
        # Detalles
        pygame.draw.line(self.image, AMARILLO, (15, 17), (35, 17), 2)
        for i in range(3):
            pygame.draw.circle(self.image, CIAN_NEON, (25 + i*5, 22), 2)
        
        self.rect = self.image.get_rect(center=(x, y))
        self.velocidad = 4
        self.velocidad_x = 0
        self.velocidad_y = 0
        self.angulo = 0
        
        # Guardar una copia original de la imagen para rotar
        self.image_original = self.image.copy()
        
    def update(self):
        if self.objetivo and self.objetivo.alive():
            # Seguimiento al objetivo
            dx = self.objetivo.rect.centerx - self.rect.centerx
            dy = self.objetivo.rect.centery - self.rect.centery
            distancia = max(1, math.sqrt(dx*dx + dy*dy))
            
            self.velocidad_x = (dx / distancia) * self.velocidad
            self.velocidad_y = (dy / distancia) * self.velocidad
            
            # Actualizar ángulo para rotación
            self.angulo = math.atan2(dy, dx)
            
            # Rotar imagen según dirección (usar la imagen original)
            self.image = pygame.transform.rotate(self.image_original, -math.degrees(self.angulo))
            self.rect = self.image.get_rect(center=self.rect.center)
        
        self.rect.x += self.velocidad_x
        self.rect.y += self.velocidad_y
        
        # Efecto de estela
        if random.random() < 0.3:
            estela = Estela(self.rect.centerx + 10, self.rect.centery, self.color)
            all_sprites.add(estela)
        
        if (self.rect.right < 0 or self.rect.left > ANCHO or 
            self.rect.bottom < 0 or self.rect.top > ALTO):
            self.kill()

class Estela(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.radio = 8
        self.color = color
        self.alpha = 150
        self.vida = 20
        
        self.image = pygame.Surface((self.radio*2, self.radio*2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (*self.color, self.alpha), (self.radio, self.radio), self.radio)
        
        self.rect = self.image.get_rect(center=(x, y))
        
    def update(self):
        self.vida -= 1
        self.alpha = max(0, self.alpha - 8)
        
        if self.alpha > 0:
            self.image = pygame.Surface((self.radio*2, self.radio*2), pygame.SRCALPHA)
            pygame.draw.circle(self.image, (*self.color, self.alpha), (self.radio, self.radio), self.radio)
            self.rect = self.image.get_rect(center=self.rect.center)
        
        if self.vida <= 0:
            self.kill()

class BombaExplosiva(pygame.sprite.Sprite):
    def __init__(self, x, y, color=NARANJA_FUEGO):
        super().__init__()
        self.tamaño = 50
        self.color = color
        self.tiempo_explosion = 80
        self.temporizador = 0
        self.exploto = False
        
        # Crear bomba con diseño detallado
        self.image = pygame.Surface((self.tamaño, self.tamaño), pygame.SRCALPHA)
        
        # Cuerpo principal
        pygame.draw.circle(self.image, self.color, (self.tamaño//2, self.tamaño//2), self.tamaño//2)
        
        # Franjas
        for i in range(3):
            y_pos = 5 + i * 15
            pygame.draw.rect(self.image, AMARILLO, (10, y_pos, 30, 8))
        
        # Mechas
        for i in range(3):
            x_pos = 15 + i * 10
            pygame.draw.line(self.image, GRIS_OSCURO, (x_pos, 5), (x_pos, 0), 2)
        
        self.rect = self.image.get_rect(center=(x, y))
        self.velocidad_x = -3
        
        # Guardar una copia original para rotar
        self.image_original = self.image.copy()
        
    def update(self):
        if not self.exploto:
            self.rect.x += self.velocidad_x
            self.temporizador += 1
            
            # Rotación (usar la imagen original)
            angulo = self.temporizador * 3
            self.image = pygame.transform.rotate(self.image_original, angulo)
            self.rect = self.image.get_rect(center=self.rect.center)
            
            # Parpadeo antes de explotar
            if self.temporizador > self.tiempo_explosion - 20:
                if (self.temporizador // 5) % 2 == 0:
                    self.image.set_alpha(100)
                else:
                    self.image.set_alpha(255)
            
            if self.temporizador >= self.tiempo_explosion:
                self.explotar()
                
            if self.rect.right < 0:
                self.kill()
    
    def explotar(self):
        self.exploto = True
        
        if SND_EXPLOSION:
            SND_EXPLOSION.play()
        
        # Crear explosión grande
        explosion = ExplosionGrande(self.rect.centerx, self.rect.centery)
        all_sprites.add(explosion)
        
        # Daño a área
        for sprite in all_sprites:
            if hasattr(sprite, 'rect'):
                distancia = math.sqrt((sprite.rect.centerx - self.rect.centerx)**2 + 
                                    (sprite.rect.centery - self.rect.centery)**2)
                if distancia < 150:
                    if hasattr(sprite, 'recibir_dano'):
                        sprite.recibir_dano()
        
        self.kill()

class ExplosionGrande(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.radio = 10
        self.radio_maximo = 120
        self.velocidad_crecimiento = 8
        self.color_base = NARANJA_FUEGO
        self.anillos = []
        
        # Crear una imagen básica (invisible)
        self.image = pygame.Surface((self.radio_maximo*2, self.radio_maximo*2), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(x, y))
        
        # Crear anillos iniciales
        for i in range(3):
            self.anillos.append({
                'radio': 5,
                'color': random.choice([NARANJA_FUEGO, AMARILLO, ROJO, NARANJA]),
                'grosor': 8 - i*2,
                'alpha': 200 - i*50
            })
        
    def update(self):
        self.radio += self.velocidad_crecimiento
        
        # Actualizar anillos
        for anillo in self.anillos:
            anillo['radio'] += self.velocidad_crecimiento * 0.8
            anillo['alpha'] = max(0, anillo['alpha'] - 10)
        
        # Crear nuevos anillos
        if random.random() < 0.3 and self.radio < self.radio_maximo:
            self.anillos.append({
                'radio': 10,
                'color': random.choice([NARANJA_FUEGO, AMARILLO, ROJO]),
                'grosor': random.randint(4, 7),
                'alpha': 180
            })
        
        if self.radio >= self.radio_maximo:
            self.kill()
            
    def draw(self, surface):
        # Dibujar explosión principal
        for i in range(5, 0, -1):
            radio_actual = self.radio - i * 10
            if radio_actual > 0:
                alpha = 150 - i * 25
                color = (self.color_base[0], min(255, self.color_base[1] + i*20), 0, alpha)
                pygame.draw.circle(surface, color, self.rect.center, radio_actual, 6 - i)
        
        # Dibujar anillos
        for anillo in self.anillos:
            if anillo['alpha'] > 0:
                color = (*anillo['color'][:3], int(anillo['alpha']))
                pygame.draw.circle(surface, color, self.rect.center, int(anillo['radio']), anillo['grosor'])

class LaserHorizontalGrande(pygame.sprite.Sprite):
    def __init__(self, y, color=ROJO):
        super().__init__()
        self.duracion = 100
        self.temporizador = 0
        self.ancho = 15
        self.y = y
        self.color = color
        
        # Crear una imagen básica
        self.image = pygame.Surface((ANCHO, self.ancho), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(ANCHO//2, y))
        
    def update(self):
        self.temporizador += 1
        if self.temporizador >= self.duracion:
            self.kill()
            
    def draw(self, surface):
        if self.temporizador < self.duracion - 20:
            # Efecto de láser pulsante
            brillo = (math.sin(pygame.time.get_ticks() * 0.015) * 0.5 + 0.5) * 200 + 55
            
            # Línea principal con gradiente
            for i in range(self.ancho):
                factor = i / self.ancho
                color = (self.color[0], 
                        int(self.color[1] * (0.5 + factor * 0.5)), 
                        int(brillo * factor))
                pygame.draw.line(surface, color, (0, self.y + i - self.ancho//2), 
                               (ANCHO, self.y + i - self.ancho//2), 1)
            
            # Efecto de brillo interior
            for i in range(3):
                color_brillo = (255, min(255, int(brillo + i*40)), 100, 150)
                pygame.draw.line(surface, color_brillo, (0, self.y), (ANCHO, self.y), 5 - i)

class OndaExpansiva(pygame.sprite.Sprite):
    def __init__(self, x, y, color=AZUL_ELECTRICO):
        super().__init__()
        self.radio = 20
        self.radio_maximo = 400
        self.velocidad_crecimiento = 10
        self.color = color
        self.anillos = []
        
        # Crear una imagen básica
        self.image = pygame.Surface((self.radio_maximo*2, self.radio_maximo*2), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(x, y))
        
    def update(self):
        self.radio += self.velocidad_crecimiento
        
        # Crear nuevo anillo cada cierto tiempo
        if self.radio % 30 == 0 and self.radio < self.radio_maximo - 50:
            self.anillos.append({
                'radio': 20,
                'alpha': 180,
                'color': random.choice([CIAN_NEON, AZUL_ELECTRICO, VERDE_NEON])
            })
        
        # Actualizar anillos
        for anillo in self.anillos[:]:
            anillo['radio'] += self.velocidad_crecimiento * 0.7
            anillo['alpha'] -= 8
            
            if anillo['alpha'] <= 0:
                self.anillos.remove(anillo)
        
        if self.radio >= self.radio_maximo:
            self.kill()
            
    def draw(self, surface):
        # Dibujar onda principal
        for i in range(5, 0, -1):
            radio_actual = self.radio - i * 20
            if radio_actual > 0:
                alpha = 120 - i * 20
                grosor = 6 - i
                pygame.draw.circle(surface, (*self.color[:3], alpha), 
                                 self.rect.center, radio_actual, grosor)
        
        # Dibujar anillos adicionales
        for anillo in self.anillos:
            if anillo['alpha'] > 0:
                pygame.draw.circle(surface, (*anillo['color'][:3], int(anillo['alpha'])), 
                                 self.rect.center, int(anillo['radio']), 3)

class FuegoArtificialEspectacular(pygame.sprite.Sprite):
    def __init__(self, x, y, color=None):
        super().__init__()
        self.x = x
        self.y = y
        self.color = color if color else random.choice([ROJO, VERDE, AZUL, AMARILLO, PURPURA, CIAN_NEON, ROSA_NEON])
        self.altura_maxima = random.randint(100, 300)
        self.velocidad = random.uniform(6, 10)
        self.exploto = False
        self.tiempo_explosion = 0
        
        self.particulas = []
        self.tipo_explosion = random.choice(['circular', 'estrella', 'anillo', 'espiral'])
        
        # Crear una imagen básica (pequeño punto)
        self.image = pygame.Surface((10, 10), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (5, 5), 2)
        self.rect = self.image.get_rect(center=(x, y))
        
    def update(self):
        if not self.exploto:
            self.y -= self.velocidad
            self.rect.center = (self.x, self.y)
            if self.y < self.altura_maxima:
                self.exploto = True
                self.crear_explosion_espectacular()
        else:
            self.tiempo_explosion += 1
            
            # Actualizar partículas
            for particula in self.particulas[:]:
                particula[0] += particula[2]
                particula[1] += particula[3]
                particula[5] -= 1
                particula[3] += 0.1  # Gravedad
                
                if particula[5] <= 0:
                    self.particulas.remove(particula)
            
            if self.tiempo_explosion > 80 and len(self.particulas) == 0:
                self.kill()
    
    def crear_explosion_espectacular(self):
        if SND_FUEGOS_ARTIFICIALES:
            SND_FUEGOS_ARTIFICIALES.play()
        
        if self.tipo_explosion == 'circular':
            self.crear_explosion_circular()
        elif self.tipo_explosion == 'estrella':
            self.crear_explosion_estrella()
        elif self.tipo_explosion == 'anillo':
            self.crear_explosion_anillo()
        else:  # espiral
            self.crear_explosion_espiral()
    
    def crear_explosion_circular(self):
        for _ in range(random.randint(40, 60)):
            angulo = random.uniform(0, 2 * math.pi)
            velocidad = random.uniform(2, 5)
            velocidad_x = math.cos(angulo) * velocidad
            velocidad_y = math.sin(angulo) * velocidad
            tamaño = random.randint(3, 6)
            vida = random.randint(40, 80)
            color_variacion = random.choice([self.color, 
                                           tuple(min(255, c + 50) for c in self.color),
                                           tuple(max(0, c - 50) for c in self.color)])
            self.particulas.append([self.x, self.y, velocidad_x, velocidad_y, tamaño, vida, color_variacion])
    
    def crear_explosion_estrella(self):
        puntas = random.randint(5, 8)
        for i in range(puntas * 10):
            angulo = (i / (puntas * 10)) * 2 * math.pi
            # Patrón de estrella
            velocidad = random.uniform(1, 4) * (1 + 0.5 * math.sin(puntas * angulo))
            velocidad_x = math.cos(angulo) * velocidad
            velocidad_y = math.sin(angulo) * velocidad
            tamaño = random.randint(2, 5)
            vida = random.randint(50, 90)
            self.particulas.append([self.x, self.y, velocidad_x, velocidad_y, tamaño, vida, self.color])
    
    def crear_explosion_anillo(self):
        for i in range(50):
            angulo = (i / 50) * 2 * math.pi
            velocidad = 3.5
            velocidad_x = math.cos(angulo) * velocidad
            velocidad_y = math.sin(angulo) * velocidad
            tamaño = random.randint(3, 5)
            vida = random.randint(60, 100)
            self.particulas.append([self.x, self.y, velocidad_x, velocidad_y, tamaño, vida, self.color])
            
            # Segundo anillo interno
            if i % 2 == 0:
                velocidad_interna = 2
                velocidad_x_interna = math.cos(angulo + 0.2) * velocidad_interna
                velocidad_y_interna = math.sin(angulo + 0.2) * velocidad_interna
                self.particulas.append([self.x, self.y, velocidad_x_interna, velocidad_y_interna, 
                                      tamaño-1, vida-20, CIAN_NEON])
    
    def crear_explosion_espiral(self):
        for i in range(60):
            angulo = (i / 60) * 4 * math.pi  # 2 vueltas completas
            radio = (i / 60) * 100
            velocidad = 0.1
            velocidad_x = math.cos(angulo) * velocidad * radio
            velocidad_y = math.sin(angulo) * velocidad * radio
            tamaño = 2 + int(i / 20)
            vida = 80 - i
            self.particulas.append([self.x, self.y, velocidad_x, velocidad_y, tamaño, vida, self.color])

class BolaFuegoGigante(pygame.sprite.Sprite):
    def __init__(self, x, y, color=NARANJA_FUEGO):
        super().__init__()
        self.tamaño = random.randint(60, 90)
        self.color_base = color
        self.velocidad_y = random.uniform(4, 7)
        self.velocidad_x = random.uniform(-1.5, 1.5)
        self.rotacion = 0
        self.tiempo_vida = 0
        
        # Crear bola de fuego con efectos
        self.image = pygame.Surface((self.tamaño*2, self.tamaño*2), pygame.SRCALPHA)
        
        # Núcleo
        pygame.draw.circle(self.image, self.color_base, (self.tamaño, self.tamaño), self.tamaño)
        
        # Capas internas
        for i in range(3, 0, -1):
            radio = self.tamaño * i // 4
            color_capa = (min(255, self.color_base[0] + i*30), 
                         min(255, self.color_base[1] + i*20), 
                         0)
            pygame.draw.circle(self.image, color_capa, (self.tamaño, self.tamaño), radio)
        
        # Centella
        pygame.draw.circle(self.image, AMARILLO, (self.tamaño, self.tamaño), self.tamaño // 6)
        
        self.rect = self.image.get_rect(center=(x, y))
        
        # Guardar una copia original para rotar
        self.image_original = self.image.copy()
        
    def update(self):
        self.rect.y += self.velocidad_y
        self.rect.x += self.velocidad_x
        self.rotacion += 3
        self.tiempo_vida += 1
        
        # Rotar la imagen (usar la imagen original)
        rotated = pygame.transform.rotate(self.image_original, self.rotacion)
        self.rect = rotated.get_rect(center=self.rect.center)
        self.image = rotated
        
        # Efecto de pulsación
        if self.tiempo_vida % 5 == 0:
            pulsacion = math.sin(self.tiempo_vida * 0.1) * 0.2 + 0.8
            nuevo_tamaño = int(self.tamaño * pulsacion)
            self.image = pygame.transform.scale(self.image, (nuevo_tamaño*2, nuevo_tamaño*2))
            self.rect = self.image.get_rect(center=self.rect.center)
        
        # Crear estela de chispas
        if random.random() < 0.4:
            chispa = ChispaFuego(self.rect.centerx + random.randint(-10, 10),
                                self.rect.centery + random.randint(-10, 10))
            all_sprites.add(chispa)
        
        if self.rect.top > ALTO or self.rect.right < 0 or self.rect.left > ANCHO:
            self.kill()

class ChispaFuego(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.tamaño = random.randint(3, 8)
        self.color = random.choice([AMARILLO, NARANJA, ROJO])
        self.vida = random.randint(20, 40)
        self.velocidad_x = random.uniform(-2, 2)
        self.velocidad_y = random.uniform(-1, 1)
        
        self.image = pygame.Surface((self.tamaño*2, self.tamaño*2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (self.tamaño, self.tamaño), self.tamaño)
        
        self.rect = self.image.get_rect(center=(x, y))
        
    def update(self):
        self.rect.x += self.velocidad_x
        self.rect.y += self.velocidad_y
        self.vida -= 1
        
        # Reducir tamaño con el tiempo
        if self.vida % 2 == 0:
            self.tamaño = max(1, self.tamaño - 1)
            self.image = pygame.Surface((self.tamaño*2, self.tamaño*2), pygame.SRCALPHA)
            alpha = min(255, self.vida * 6)
            pygame.draw.circle(self.image, (*self.color, alpha), (self.tamaño, self.tamaño), self.tamaño)
            self.rect = self.image.get_rect(center=self.rect.center)
        
        if self.vida <= 0:
            self.kill()

# --- CLASES DE JEFES MEJORADAS ---

class JefeBase(pygame.sprite.Sprite):
    def __init__(self, imagen, vida, velocidad_y=1.5, tamaño=(200, 200)):
        super().__init__()
        self.image_original = imagen
        self.image = self.image_original.copy()
        self.rect = self.image.get_rect()
        self.rect.x = ANCHO - tamaño[0] - 50
        self.rect.y = ALTO // 2 - tamaño[1] // 2
        
        self.vida = vida
        self.vida_max = vida
        self.velocidad_y = velocidad_y
        self.direccion_y = 1
        
        self.temporizador_ataque = 0
        self.cooldown_ataque = 0
        
        self.ataques_activos = []
        self.tiempo_temblor = 0
        self.intensidad_temblor = 0
        self.animacion_dano = 0
        
        # Colores por jefe
        self.colores_ataque = []
        
    def update(self):
        # Movimiento vertical
        self.rect.y += self.velocidad_y * self.direccion_y
        
        # Límites
        if self.rect.y <= 50:
            self.rect.y = 50
            self.direccion_y = 1
        elif self.rect.y >= ALTO - self.rect.height - 50:
            self.rect.y = ALTO - self.rect.height - 50
            self.direccion_y = -1
        
        # Temporizador de ataque
        self.temporizador_ataque += 1
        
        # Actualizar ataques activos
        for ataque in self.ataques_activos[:]:
            if hasattr(ataque, 'update'):
                ataque.update()
            if hasattr(ataque, 'temporizador') and ataque.temporizador >= getattr(ataque, 'duracion', 0):
                self.ataques_activos.remove(ataque)
        
        # Animación de daño
        if self.animacion_dano > 0:
            self.animacion_dano -= 1
            self.image.set_alpha(150 + (self.animacion_dano * 10))
        else:
            self.image.set_alpha(255)
        
        if self.tiempo_temblor > 0:
            self.tiempo_temblor -= 1
    
    def recibir_dano(self, cantidad=1):
        self.vida -= cantidad
        self.animacion_dano = 10
        
        if SND_BOSS_HURT:
            SND_BOSS_HURT.play()
        
        self.activar_temblor(4)
        return self.vida <= 0
    
    def activar_temblor(self, intensidad):
        self.tiempo_temblor = 5
        self.intensidad_temblor = intensidad
    
    def get_temblor_offset(self):
        if self.tiempo_temblor > 0:
            return (random.randint(-self.intensidad_temblor, self.intensidad_temblor),
                   random.randint(-self.intensidad_temblor, self.intensidad_temblor))
        return (0, 0)
    
    def draw_efectos(self, surface):
        for ataque in self.ataques_activos:
            if hasattr(ataque, 'draw'):
                ataque.draw(surface)

class Jefe1(JefeBase):
    def __init__(self):
        super().__init__(IMG_JEFE1, 100, 1.0)
        self.cooldown_ataque = 100
        self.colores_ataque = [CIAN_NEON, AZUL_ELECTRICO, VERDE_LIMA]
    
    def update(self):
        super().update()
        
        if self.temporizador_ataque % self.cooldown_ataque == 0:
            self.ataque_pasivo_mejorado()
    
    def ataque_pasivo_mejorado(self):
        # Balas grandes y coloridas
        for i in range(3):
            color = random.choice(self.colores_ataque)
            y_pos = self.rect.centery + (i-1) * 70
            bala = BalaEnemiga(self.rect.left, y_pos, color, tamaño=45, velocidad_x=-4)
            all_sprites.add(bala)
            balas_enemigas.add(bala)

class Jefe2(JefeBase):
    def __init__(self):
        super().__init__(IMG_JEFE2, 150, 1.2)
        self.cooldown_ataque = 80
        self.colores_ataque = [VERDE_NEON, ROSA_FUCSIA, PURPURA_NEON]
        self.contador_misiles = 0
    
    def update(self):
        super().update()
        
        if self.temporizador_ataque % self.cooldown_ataque == 0:
            self.ataque_misiles_teledirigidos()
        
        # Bombas cada 120 frames
        if self.temporizador_ataque % 120 == 0:
            self.ataque_bombas()
    
    def ataque_misiles_teledirigidos(self):
        # Misiles teledirigidos coloridos
        if len(jugador_grupo) > 0:
            jugador = jugador_grupo.sprite
            for _ in range(2):
                color = random.choice(self.colores_ataque)
                misil = MisilTeledirigido(self.rect.left, 
                                         self.rect.centery + random.randint(-50, 50),
                                         jugador, color)
                all_sprites.add(misil)
                balas_enemigas.add(misil)
    
    def ataque_bombas(self):
        # Bombas explosivas
        for i in range(2):
            y_pos = self.rect.centery + (i-0.5) * 80
            color = random.choice([NARANJA_FUEGO, ROJO, AMARILLO])
            bomba = BombaExplosiva(self.rect.left, y_pos, color)
            all_sprites.add(bomba)
            balas_enemigas.add(bomba)

class Jefe3(JefeBase):
    def __init__(self):
        super().__init__(IMG_JEFE3, 200, 1.5)
        self.cooldown_ataque = 60
        self.colores_ataque = [ROSA_NEON, CIAN_NEON, AMARILLO, VERDE_NEON]
        self.modo_fuegos = 0
    
    def update(self):
        super().update()
        
        # Fuegos artificiales sincronizados
        if self.temporizador_ataque % self.cooldown_ataque == 0:
            self.ataque_fuegos_artificiales()
        
        # Bolas de fuego gigantes
        if self.temporizador_ataque % 90 == 0:
            self.ataque_bolas_fuego_gigantes()
        
        # Ondas expansivas
        if self.temporizador_ataque % 150 == 0:
            self.ataque_ondas_expansivas()
    
    def ataque_fuegos_artificiales(self):
        # Fuegos artificiales espectaculares sincronizados
        posiciones = [ANCHO//4, ANCHO//2, ANCHO*3//4]
        for x in posiciones:
            color = random.choice(self.colores_ataque)
            fuego = FuegoArtificialEspectacular(x, ALTO + 30, color)
            self.ataques_activos.append(fuego)
            all_sprites.add(fuego)
    
    def ataque_bolas_fuego_gigantes(self):
        # Bolas de fuego gigantes desde arriba
        for _ in range(3):
            x = random.randint(100, ANCHO - 100)
            color = random.choice([NARANJA_FUEGO, ROJO, (255, 100, 0)])
            bola = BolaFuegoGigante(x, -100, color)
            all_sprites.add(bola)
            balas_enemigas.add(bola)
            if SND_CAIDA_FUEGO:
                SND_CAIDA_FUEGO.play()
    
    def ataque_ondas_expansivas(self):
        # Ondas expansivas desde el jefe
        color = random.choice(self.colores_ataque)
        onda = OndaExpansiva(self.rect.centerx, self.rect.centery, color)
        self.ataques_activos.append(onda)

class Jefe4(JefeBase):
    def __init__(self):
        super().__init__(IMG_JEFE4, 200, 1.8)
        self.cooldown_ataque = 50
        self.colores_ataque = [PURPURA_NEON, ROSA_FUCSIA, AZUL_ELECTRICO]
        self.ultimo_laser = 0
    
    def update(self):
        super().update()
        
        # Ataque de láseres gigantes
        if self.temporizador_ataque % 80 == 0:
            self.ataque_lasers_gigantes()
        
        # Ataque de ráfaga mejorada
        if self.temporizador_ataque % 40 == 0:
            self.ataque_rafaga_mejorada()
        
        # Ataque de energía en espiral
        if self.temporizador_ataque % 120 == 0:
            self.ataque_espiral_energia()
    
    def ataque_lasers_gigantes(self):
        # Láseres horizontales gigantes
        for _ in range(2):
            y = random.randint(100, ALTO - 100)
            color = random.choice(self.colores_ataque)
            laser = LaserHorizontalGrande(y, color)
            self.ataques_activos.append(laser)
            if SND_LASER:
                SND_LASER.play()
    
    def ataque_rafaga_mejorada(self):
        # Ráfaga de balas grandes en patrón complejo
        for i in range(12):
            angulo = (i / 12) * 2 * math.pi
            velocidad = random.uniform(3, 6)
            velocidad_x = math.cos(angulo) * velocidad
            velocidad_y = math.sin(angulo) * velocidad
            
            color = random.choice(self.colores_ataque)
            tamaño = random.randint(35, 50)
            bala = BalaEnemiga(self.rect.centerx, self.rect.centery,
                                   color, tamaño, velocidad_x)
            bala.velocidad_y = velocidad_y
            all_sprites.add(bala)
            balas_enemigas.add(bala)
    
    def ataque_espiral_energia(self):
        # Espiral de energía colorida
        for i in range(24):
            angulo = (i / 24) * 4 * math.pi  # 2 vueltas
            radio = 100 + i * 5
            velocidad = 0.2
            velocidad_x = math.cos(angulo) * velocidad * radio
            velocidad_y = math.sin(angulo) * velocidad * radio
            
            color = self.colores_ataque[i % len(self.colores_ataque)]
            tamaño = 30 - i // 2
            bala = BalaEnemiga(self.rect.centerx, self.rect.centery,
                                   color, tamaño, velocidad_x)
            bala.velocidad_y = velocidad_y
            all_sprites.add(bala)
            balas_enemigas.add(bala)

class Jefe5(JefeBase):
    def __init__(self):
        super().__init__(IMG_JEFE5, 300, 2.0)  # REDUCIDO: 300 de vida (en lugar de 500)
        self.cooldown_ataque = 60  # REDUCIDO: Cooldown más largo (en lugar de 30)
        self.colores_ataque = [DORADO, PLATEADO, ROSA_FUCSIA, CIAN_NEON, VERDE_NEON, NARANJA_FUEGO]
        self.modo_ataque = 0
        self.contador_ataque = 0
        self.ataques_por_modo = 2  # REDUCIDO: Menos ataques por modo
        
    def update(self):
        super().update()
        
        self.contador_ataque += 1
        
        # Cambiar modo de ataque cada 5 segundos (más lento que antes)
        if self.contador_ataque % 300 == 0:  # 5 segundos en lugar de 3
            self.modo_ataque = (self.modo_ataque + 1) % self.ataques_por_modo
        
        # Ejecutar ataque según el modo (con cooldown aumentado)
        if self.temporizador_ataque % self.cooldown_ataque == 0:
            if self.modo_ataque == 0:
                self.ataque_tormenta_simplificada()
            elif self.modo_ataque == 1:
                self.ataque_fuegos_espectaculares()
    
    def ataque_tormenta_simplificada(self):
        # Tormenta de proyectiles (más simple que antes)
        for _ in range(6):  # REDUCIDO: 6 proyectiles en lugar de 10
            x = self.rect.left
            y = random.randint(self.rect.top, self.rect.bottom)
            color = random.choice(self.colores_ataque)
            tamaño = random.randint(40, 55)  # REDUCIDO: Tamaño menor
            bala = BalaEnemiga(x, y, color, tamaño, -6)  # REDUCIDO: Velocidad -6 en lugar de -9
            bala.velocidad_y = random.uniform(-2, 2)  # REDUCIDO: Menos variación vertical
            all_sprites.add(bala)
            balas_enemigas.add(bala)
    
    def ataque_fuegos_espectaculares(self):
        # Fuegos artificiales (similares al jefe 4 pero menos intensos)
        posiciones = [ANCHO//4, ANCHO//2, ANCHO*3//4]
        for x in posiciones:
            color = random.choice(self.colores_ataque)
            fuego = FuegoArtificialEspectacular(x, ALTO + 50, color)
            self.ataques_activos.append(fuego)
            all_sprites.add(fuego)
        
        # Añadir algunos láseres horizontales (menos que el jefe 4)
        for i in range(2):  # REDUCIDO: Solo 2 láseres
            y = 150 + i * 200
            color = random.choice(self.colores_ataque)
            laser = LaserHorizontalGrande(y, color)
            self.ataques_activos.append(laser)
            if SND_LASER:
                SND_LASER.play()

# --- FUNCIONES AUXILIARES ---

def dibujar_barra_vida(surface, x, y, ancho, alto, vida, vida_max, color):
    pygame.draw.rect(surface, (30, 30, 30), (x, y, ancho, alto), border_radius=5)
    
    if vida > 0:
        ancho_vida = int((vida / vida_max) * (ancho - 6))
        # Gradiente de color para la barra de vida
        for i in range(ancho_vida):
            factor = i / ancho_vida
            color_gradiente = (int(color[0] * factor), 
                             int(color[1] * (0.5 + factor * 0.5)), 
                             color[2])
            pygame.draw.line(surface, color_gradiente, (x + 3 + i, y + 3), 
                           (x + 3 + i, y + alto - 3), 1)
    
    pygame.draw.rect(surface, BLANCO, (x, y, ancho, alto), 3, border_radius=5)
    
    # Texto de vida
    texto_vida = f"{vida}/{vida_max}"
    txt_surf = FUENTE_PEQ.render(texto_vida, True, BLANCO)
    surface.blit(txt_surf, (x + ancho // 2 - txt_surf.get_width() // 2, y - 25))

def dibujar_hud(surf, jugador, jefe_actual, jefe_numero, tiempo_transcurrido):
    # Vidas del jugador
    for i in range(jugador.vidas):
        surf.blit(IMG_VIDA_ICONO, (10 + (i * 35), 10))
    
    # Información del jefe actual
    if jefe_actual:
        # Título del jefe con efecto
        tiempo = pygame.time.get_ticks() * 0.001
        brillo = (math.sin(tiempo * 3) * 0.3 + 0.7) * 255
        
        jefe_texto = FUENTE_MEDIANA.render(f"JEFE {jefe_numero}/5", True, 
                                          (int(brillo), int(brillo*0.8), 0))
        sombra_texto = FUENTE_MEDIANA.render(f"JEFE {jefe_numero}/5", True, 
                                           (100, 80, 0))
        
        surf.blit(sombra_texto, (ANCHO // 2 - jefe_texto.get_width() // 2 + 2, 12))
        surf.blit(jefe_texto, (ANCHO // 2 - jefe_texto.get_width() // 2, 10))
        
        # Barra de vida del jefe
        dibujar_barra_vida(surf, ANCHO // 2 - 250, 60, 500, 30, 
                          jefe_actual.vida, jefe_actual.vida_max, 
                          jefe_actual.colores_ataque[0] if jefe_actual.colores_ataque else DORADO)
    
    # Tiempo transcurrido
    minutos = int(tiempo_transcurrido // 60)
    segundos = int(tiempo_transcurrido % 60)
    
    tiempo_texto = FUENTE_PEQ.render(f"TIEMPO: {minutos:02d}:{segundos:02d}", True, CIAN_NEON)
    tiempo_sombra = FUENTE_PEQ.render(f"TIEMPO: {minutos:02d}:{segundos:02d}", True, (0, 100, 150))
    
    surf.blit(tiempo_sombra, (ANCHO - 152, 12))
    surf.blit(tiempo_texto, (ANCHO - 150, 10))
    
    # Indicador de vibración (después de 44 segundos)
    if tiempo_transcurrido > 44:
        if (pygame.time.get_ticks() // 300) % 2 == 0:
            vibracion_texto = FUENTE_PEQ.render("¡VIBRACIÓN ACTIVA!", True, ROJO)
            vibracion_sombra = FUENTE_PEQ.render("¡VIBRACIÓN ACTIVA!", True, (100, 0, 0))
            
            surf.blit(vibracion_sombra, (ANCHO // 2 - vibracion_texto.get_width() // 2 + 2, ALTO - 42))
            surf.blit(vibracion_texto, (ANCHO // 2 - vibracion_texto.get_width() // 2, ALTO - 40))

def dibujar_transicion_jefe(surf, jefe_numero, alpha):
    overlay = pygame.Surface((ANCHO, ALTO))
    overlay.set_alpha(alpha)
    overlay.fill(NEGRO)
    surf.blit(overlay, (0, 0))
    
    if alpha > 100:
        # Texto principal con efecto brillante
        tiempo = pygame.time.get_ticks() * 0.005
        brillo = (math.sin(tiempo * 2) * 0.5 + 0.5) * 255
        
        texto = FUENTE_TITULO.render(f"JEFE {jefe_numero}", True, 
                                    (int(brillo), int(brillo*0.7), 0))
        texto_rect = texto.get_rect(center=(ANCHO // 2, ALTO // 2 - 50))
        
        sombra = FUENTE_TITULO.render(f"JEFE {jefe_numero}", True, (80, 60, 0))
        surf.blit(sombra, (texto_rect.x + 4, texto_rect.y + 4))
        surf.blit(texto, texto_rect)
        
        # Subtítulo
        subtitulo = FUENTE_MEDIANA.render("¡PREPÁRATE PARA LO PEOR!", True, 
                                         (int(brillo*0.8), int(brillo), 0))
        subtitulo_rect = subtitulo.get_rect(center=(ANCHO // 2, ALTO // 2 + 20))
        surf.blit(subtitulo, subtitulo_rect)
        
        # Efecto de partículas durante transición
        if alpha > 150:
            for _ in range(5):
                x = random.randint(0, ANCHO)
                y = random.randint(0, ALTO)
                tamaño = random.randint(2, 5)
                color = random.choice([DORADO, NARANJA_FUEGO, AMARILLO])
                pygame.draw.circle(surf, color, (x, y), tamaño)

def dibujar_game_over(surf, puntaje):
    overlay = pygame.Surface((ANCHO, ALTO))
    overlay.set_alpha(200)
    overlay.fill(NEGRO)
    surf.blit(overlay, (0,0))
    
    txt_go = FUENTE_GRANDE.render("GAME OVER", True, ROJO)
    txt_pts = FUENTE_MEDIANA.render(f"Puntaje: {puntaje}", True, BLANCO)
    
    txt_op1 = FUENTE_PEQ.render("[C]ontinuar (3 vidas)", True, AMARILLO)
    txt_op2 = FUENTE_PEQ.render("[R]eintentar Nivel", True, BLANCO)
    txt_op3 = FUENTE_PEQ.render("[M]enú Principal", True, BLANCO)
    
    cx, cy = ANCHO // 2, ALTO // 2
    surf.blit(txt_go, txt_go.get_rect(center=(cx, cy - 100)))
    surf.blit(txt_pts, txt_pts.get_rect(center=(cx, cy - 40)))
    surf.blit(txt_op1, txt_op1.get_rect(center=(cx, cy + 40)))
    surf.blit(txt_op2, txt_op2.get_rect(center=(cx, cy + 80)))
    surf.blit(txt_op3, txt_op3.get_rect(center=(cx, cy + 120)))

def dibujar_victoria(surf):
    surf.fill(NEGRO)
    
    # Estrellas de fondo animadas
    tiempo = pygame.time.get_ticks() * 0.001
    for i in range(200):
        x = random.randint(0, ANCHO)
        y = random.randint(0, ALTO)
        tamaño = random.randint(1, 4)
        brillo = 100 + int(155 * (math.sin(tiempo + i * 0.1) * 0.5 + 0.5))
        pygame.draw.circle(surf, (brillo, brillo, brillo), (x, y), tamaño)
    
    # Título con efecto brillante
    brillo_titulo = (math.sin(tiempo * 2) * 0.5 + 0.5) * 255
    titulo = FUENTE_TITULO.render("¡VICTORIA TOTAL!", True, 
                                 (int(brillo_titulo), int(brillo_titulo*0.8), 0))
    subtitulo = FUENTE_MEDIANA.render("Has derrotado al rector", True, PLATEADO)
    
    titulo_rect = titulo.get_rect(center=(ANCHO // 2, ALTO // 2 - 50))
    subtitulo_rect = subtitulo.get_rect(center=(ANCHO // 2, ALTO // 2 + 20))
    
    # Sombra del título
    titulo_sombra = FUENTE_TITULO.render("¡VICTORIA TOTAL!", True, (100, 80, 0))
    surf.blit(titulo_sombra, (titulo_rect.x + 3, titulo_rect.y + 3))
    surf.blit(titulo, titulo_rect)
    surf.blit(subtitulo, subtitulo_rect)
    
    # Instrucción parpadeante
    if (pygame.time.get_ticks() // 500) % 2 == 0:
        instruccion = FUENTE_ARCADA.render("Presiona ESPACIO para ver el final", True, VERDE_NEON)
        instruccion_rect = instruccion.get_rect(center=(ANCHO // 2, ALTO - 100))
        
        instruccion_sombra = FUENTE_ARCADA.render("Presiona ESPACIO para ver el final", True, (0, 100, 0))
        surf.blit(instruccion_sombra, (instruccion_rect.x + 2, instruccion_rect.y + 2))
        surf.blit(instruccion, instruccion_rect)

def reproducir_musica(ruta, volumen=0.6):
    try:
        ruta_nivel5 = os.path.join("nivel5", ruta)
        if os.path.exists(ruta_nivel5):
            pygame.mixer.music.load(ruta_nivel5)
        else:
            ruta_nivel3 = os.path.join("nivel3", ruta)
            if os.path.exists(ruta_nivel3):
                pygame.mixer.music.load(ruta_nivel3)
            else:
                pygame.mixer.music.load(ruta)
                
        pygame.mixer.music.stop()
        pygame.mixer.music.set_volume(volumen)
        pygame.mixer.music.play(-1)
        return True
    except:
        print(f"No se pudo cargar la música: {ruta}")
        return False

# --- GRUPOS DE SPRITES GLOBALES ---
all_sprites = pygame.sprite.Group()
balas_jugador = pygame.sprite.Group()
balas_enemigas = pygame.sprite.Group()
jugador_grupo = pygame.sprite.GroupSingle()
jefe_grupo = pygame.sprite.GroupSingle()

# --- FUNCIÓN DE REINICIO ---
def reiniciar_nivel():
    all_sprites.empty()
    balas_jugador.empty()
    balas_enemigas.empty()
    jugador_grupo.empty()
    jefe_grupo.empty()
    
    jugador = Jugador()
    all_sprites.add(jugador)
    jugador_grupo.add(jugador)
    
    return jugador, 0, 1

def continuar_juego(jugador):
    """Función corregida para continuar el juego después de usar coin"""
    # Resetear posición del jugador
    jugador.resetear_posicion()
    
    # Establecer vidas a 3 (como se muestra en la pantalla de Game Over)
    jugador.vidas = 3
    
    # Limpiar todas las balas enemigas para dar al jugador una oportunidad
    for bala in balas_enemigas:
        bala.kill()
    
    # Limpiar ataques activos del jefe si existe
    if jefe_grupo.sprite:
        jefe = jefe_grupo.sprite
        jefe.ataques_activos.clear()
        
    # Reproducir sonido de coin
    if SND_COIN:
        SND_COIN.play()

# --- LOOP PRINCIPAL NIVEL 5 MEJORADO ---

def juego():
    estado = 0
    # 0: Historia Intro, 1: Cuenta, 2: Juego, 3: Transición Jefe, 4: Victoria, 5: Historias Finales, 6: Game Over
    
    jugador, puntaje, jefe_actual_num = reiniciar_nivel()
    
    fondo_x = 0
    tiempo_inicio_nivel = 0
    tiempo_transcurrido = 0
    
    # Control de jefes
    jefes = [Jefe1, Jefe2, Jefe3, Jefe4, Jefe5]
    jefe_actual = None
    transicion_jefe = False
    alpha_transicion = 255
    duracion_transicion = 0
    
    # Efectos especiales
    tiempo_vibracion = 0
    vibrando = False
    tiempo_destello = 0
    destello_alpha = 0
    
    # Estados del juego
    musica_reproduciendose = False
    estado_anterior = 2
    
    # Textos para las historias
    textos_historia = [
        {
            "titulo": "NIVEL 5: LA BATALLA FINAL",
            "subtitulo": "EL DESAFÍO CONTRA EL RECTOR",
            "texto":  "Motocle llega a la batalla final frente al Rector, quien se niega a entregarle su título. "
    "Este es el duelo decisivo: cada ataque pondrá a prueba todo lo aprendido. "
    "Prepárate, solo venciendo al Rector podrás graduarte."
        },
        {
            "titulo": "EL LEGADO PERDURABLE",
            "subtitulo": "YA TE PUEDES GRADUAR",
            "texto": "Motocle derrota al Rector y finalmente obtiene su título. "
    "Su aventura llega a su fin con una victoria merecida."
        },
        {
            "titulo": "MÁS ALLÁ DE LA BATALLA",
            "subtitulo": "AHORA EMPIEZA EL MUNDO LABORAL",
            "texto":  "El Rector cae ante Motocle. Tras superar todos los desafíos, "
    "recibe por fin su título galáctico."
        },
        {
            "titulo": "EL FIN DEL VIAJE",
            "subtitulo": "AVER SI ENCUENTRAS CHAMBA SUERTE!",
            "texto":  "Motocle vence en la batalla final. El Rector, sin más opción, "
    "le entrega el título que tanto había negado."
        }
    ]
    
    # Crear pantallas de historia
    pantallas_historia = []
    for i, texto in enumerate(textos_historia):
        if i == 0:
            imagen = IMG_HISTORIA_INICIO
        elif i == 1:
            imagen = IMG_HISTORIA_FINAL1
        elif i == 2:
            imagen = IMG_HISTORIA_FINAL2
        else:
            imagen = IMG_HISTORIA_FINAL3
            
        pantalla = PantallaHistoria(
            imagen,
            texto["titulo"],
            texto["subtitulo"],
            texto["texto"]
        )
        pantallas_historia.append(pantalla)
    
    pantalla_historia_actual = 0
    
    reloj = pygame.time.Clock()
    ejecutando = True

    while ejecutando:
        dt = reloj.tick(FPS)
        
        eventos = pygame.event.get()
        for event in eventos:
            if event.type == pygame.QUIT:
                ejecutando = False
            
            if estado == 0 or estado == 5:
                if pantalla_historia_actual < len(pantallas_historia):
                    pantallas_historia[pantalla_historia_actual].manejar_eventos([event])
            
            if event.type == pygame.KEYDOWN:
                if estado == 2 and event.key == pygame.K_b:
                    # Podrías añadir bombas si quieres
                    pass
                
                if estado == 6:  # Game Over
                    if event.key == pygame.K_c:
                        # Usar coin para continuar
                        continuar_juego(jugador)
                        estado = estado_anterior  # Volver al estado anterior (normalmente 2)
                        if musica_reproduciendose:
                            pygame.mixer.music.unpause()
                    
                    elif event.key == pygame.K_r:
                        # Reiniciar nivel completamente
                        jugador, puntaje, jefe_actual_num = reiniciar_nivel()
                        tiempo_inicio_nivel = pygame.time.get_ticks()
                        estado = 1
                    
                    elif event.key == pygame.K_m:
                        print("Regresando al menú principal...")
                        ejecutando = False
                
                if estado == 4:  # Victoria
                    if event.key == pygame.K_SPACE:
                        estado = 5
                        pantalla_historia_actual = 1
                        pantallas_historia[pantalla_historia_actual].reiniciar()
                
                if estado == 5:  # Historias finales
                    if event.key == pygame.K_ESCAPE:
                        ejecutando = False
        
        # --- MÁQUINA DE ESTADOS ---
        if estado == 0:
            pantallas_historia[0].actualizar(dt)
            pantallas_historia[0].dibujar(PANTALLA)
            
            if pantallas_historia[0].terminada:
                estado = 1
                tiempo_inicio_nivel = pygame.time.get_ticks()
        
        elif estado == 1:
            # Pantalla de conteo con efectos
            PANTALLA.blit(IMG_FONDO, (0,0))
            
            tiempo_delta = pygame.time.get_ticks() - tiempo_inicio_nivel
            texto = ""
            color = DORADO
            
            if tiempo_delta < 1000:
                texto = "3"
                color = ROJO
            elif tiempo_delta < 2000:
                texto = "2"
                color = NARANJA
            elif tiempo_delta < 3000:
                texto = "1"
                color = AMARILLO
            elif tiempo_delta < 4000:
                texto = "¡EL RECTOR!"
                color = VERDE_NEON
                if not musica_reproduciendose:
                    reproducir_musica("musica_batalla_final.mp3", 0.7)
                    musica_reproduciendose = True
            else:
                estado = 2
                jefe_actual = jefes[0]()
                all_sprites.add(jefe_actual)
                jefe_grupo.add(jefe_actual)
                jefe_actual_num = 1
            
            if texto:
                # Efecto de escala para el texto
                escala = 1.0 + math.sin(tiempo_delta * 0.01) * 0.2
                fuente_temp = pygame.font.SysFont("Arial", int(60 * escala), bold=True)
                surf = fuente_temp.render(texto, True, color)
                PANTALLA.blit(surf, surf.get_rect(center=(ANCHO//2, ALTO//2)))
                
                # Partículas durante el conteo
                for _ in range(3):
                    x = random.randint(ANCHO//2 - 100, ANCHO//2 + 100)
                    y = random.randint(ALTO//2 - 100, ALTO//2 + 100)
                    tamaño = random.randint(2, 5)
                    pygame.draw.circle(PANTALLA, color, (x, y), tamaño)
        
        elif estado == 2:
            # Juego principal
            tiempo_transcurrido = (pygame.time.get_ticks() - tiempo_inicio_nivel) / 1000.0
            
            # Efecto de vibración (comienza a los 44 segundos)
            offset_x, offset_y = 0, 0
            if tiempo_transcurrido > 44:
                vibrando = True
                if tiempo_vibracion <= 0:
                    tiempo_vibracion = random.randint(10, 30)
                else:
                    tiempo_vibracion -= 1
                    offset_x = random.randint(-4, 4)
                    offset_y = random.randint(-4, 4)
            
            # Efecto de destello aleatorio
            if random.randint(0, 200) < 2 and tiempo_transcurrido > 44:
                tiempo_destello = 15
                destello_alpha = 120
            
            if tiempo_destello > 0:
                tiempo_destello -= 1
                destello_alpha = max(0, destello_alpha - 8)
            
            # Scroll del fondo con efectos
            fondo_x -= 5
            if fondo_x <= -ANCHO: fondo_x = 0
            
            # Dibujar fondo con offset de vibración
            PANTALLA.blit(IMG_FONDO, (fondo_x + offset_x, offset_y))
            PANTALLA.blit(IMG_FONDO, (fondo_x + ANCHO + offset_x, offset_y))
            
            # Aplicar destello si está activo
            if destello_alpha > 0:
                destello_surf = pygame.Surface((ANCHO, ALTO))
                destello_surf.fill(BLANCO)
                destello_surf.set_alpha(destello_alpha)
                PANTALLA.blit(destello_surf, (0, 0))
            
            # Actualizar sprites
            all_sprites.update()
            
            # Dibujar sprites normales
            all_sprites.draw(PANTALLA)
            
            # Dibujar efectos especiales de los jefes
            if jefe_actual:
                jefe_actual.draw_efectos(PANTALLA)
            
            # Dibujar partículas de efectos especiales después
            for sprite in all_sprites:
                if isinstance(sprite, FuegoArtificialEspectacular):
                    # Dibujar partículas de fuegos artificiales
                    for particula in sprite.particulas:
                        x, y, _, _, tamaño, vida, color = particula
                        alpha = min(255, vida * 3)
                        pygame.draw.circle(PANTALLA, (*color, alpha), (int(x), int(y)), tamaño)
            
            # HUD
            dibujar_hud(PANTALLA, jugador, jefe_actual, jefe_actual_num, tiempo_transcurrido)
            
            # Verificar si el jefe actual fue derrotado
            if jefe_actual and jefe_actual.vida <= 0:
                jefe_actual.kill()
                jefe_actual_num += 1
                
                if jefe_actual_num <= 5:
                    estado = 3
                    transicion_jefe = True
                    alpha_transicion = 255
                    duracion_transicion = pygame.time.get_ticks()
                else:
                    estado = 4
                    if SND_VICTORY: SND_VICTORY.play()
        
        elif estado == 3:
            # Transición entre jefes
            PANTALLA.blit(IMG_FONDO, (0, 0))
            all_sprites.draw(PANTALLA)
            
            # Dibujar efectos especiales
            if jefe_actual:
                jefe_actual.draw_efectos(PANTALLA)
            
            alpha_transicion = max(0, alpha_transicion - 3)
            dibujar_transicion_jefe(PANTALLA, jefe_actual_num, alpha_transicion)
            
            if alpha_transicion <= 0:
                transicion_jefe = False
                estado = 2
                if jefe_actual_num <= 5:
                    jefe_actual = jefes[jefe_actual_num - 1]()
                    all_sprites.add(jefe_actual)
                    jefe_grupo.add(jefe_actual)
                    
                    # Efecto de transformación
                    if SND_BOSS_TRANSFORM:
                        SND_BOSS_TRANSFORM.play()
                        
                    # Explosión de transformación
                    explosion = ExplosionGrande(jefe_actual.rect.centerx, jefe_actual.rect.centery)
                    all_sprites.add(explosion)
        
        elif estado == 4:
            # Pantalla de victoria
            dibujar_victoria(PANTALLA)
        
        elif estado == 5:
            # Historias finales
            if pantalla_historia_actual < len(pantallas_historia):
                pantallas_historia[pantalla_historia_actual].actualizar(dt)
                pantallas_historia[pantalla_historia_actual].dibujar(PANTALLA)
                
                if pantallas_historia[pantalla_historia_actual].terminada:
                    pantalla_historia_actual += 1
                    if pantalla_historia_actual < len(pantallas_historia):
                        pantallas_historia[pantalla_historia_actual].reiniciar()
                    else:
                        # Fin del juego
                        print("¡Juego completado!")
                        ejecutando = False
        
        elif estado == 6:
            # Game Over
            if musica_reproduciendose:
                pygame.mixer.music.pause()
            
            PANTALLA.blit(IMG_FONDO, (0, 0))
            all_sprites.draw(PANTALLA)
            dibujar_hud(PANTALLA, jugador, jefe_actual, jefe_actual_num, tiempo_transcurrido)
            dibujar_game_over(PANTALLA, puntaje)
        
        # --- COLISIONES (solo en estado 2) ---
        if estado == 2:
            # 1. Balas jugador -> jefe
            if jefe_actual:
                hits = pygame.sprite.groupcollide(jefe_grupo, balas_jugador, False, True)
                for jefe in hits:
                    puntaje += 15  # Más puntos por golpear
                    if jefe.recibir_dano():
                        # El jefe muere, se maneja en la máquina de estados
                        pass
            
            # 2. Balas enemigas -> jugador
            hits_jugador = pygame.sprite.spritecollide(jugador, balas_enemigas, True)
            for _ in hits_jugador:
                if jugador.recibir_dano():
                    if SND_EXPLOSION: SND_EXPLOSION.play()
            
            # 3. Colisión balas jugador vs balas enemigas
            # Hacer que las balas desaparezcan cuando chocan
            colisiones_balas = pygame.sprite.groupcollide(balas_jugador, balas_enemigas, True, True)
            
            # Crear efecto visual cuando las balas chocan
            for bala_jugador, balas_enemigas_list in colisiones_balas.items():
                for bala_enemiga in balas_enemigas_list:
                    # Crear pequeña explosión en el punto de colisión
                    x = (bala_jugador.rect.centerx + bala_enemiga.rect.centerx) // 2
                    y = (bala_jugador.rect.centery + bala_enemiga.rect.centery) // 2
                    
                    # Crear efecto de partículas
                    for _ in range(8):
                        tamaño = random.randint(2, 5)
                        color = random.choice([AMARILLO, CIAN_NEON, BLANCO])
                        velocidad_x = random.uniform(-2, 2)
                        velocidad_y = random.uniform(-2, 2)
                        vida = random.randint(15, 30)
                        
                        # Crear partícula simple
                        particula_surf = pygame.Surface((tamaño*2, tamaño*2), pygame.SRCALPHA)
                        pygame.draw.circle(particula_surf, color, (tamaño, tamaño), tamaño)
                        
                        # Por simplicidad, solo dibujamos directamente
                        pygame.draw.circle(PANTALLA, color, (int(x), int(y)), tamaño)
            
            # 4. Colisión jugador -> jefe
            if jefe_actual and pygame.sprite.collide_rect(jugador, jefe_actual):
                if jugador.recibir_dano():
                    if SND_EXPLOSION: SND_EXPLOSION.play()
            
            # 5. Colisión con ataques especiales del jefe
            if jefe_actual:
                for ataque in jefe_actual.ataques_activos:
                    if isinstance(ataque, LaserHorizontalGrande):
                        # Verificar colisión con láser horizontal
                        laser_rect = pygame.Rect(0, ataque.y - ataque.ancho//2, ANCHO, ataque.ancho)
                        if laser_rect.colliderect(jugador.rect):
                            if jugador.recibir_dano():
                                if SND_EXPLOSION: SND_EXPLOSION.play()
            
            # Verificar muerte del jugador
            if jugador.vidas <= 0:
                estado_anterior = estado
                estado = 6
                if SND_GAMEOVER: SND_GAMEOVER.play()
        
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    juego()