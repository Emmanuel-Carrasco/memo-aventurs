import pygame
import sys
import random
import cv2  # Para video (aún disponible si se necesita en el futuro)
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
pygame.display.set_caption("Nivel 2 - Estilo Cuphead")

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

# FUENTES
FUENTE_GRANDE = pygame.font.SysFont("Arial", 60, bold=True)
FUENTE_MEDIANA = pygame.font.SysFont("Arial", 40, bold=True)
FUENTE_PEQ = pygame.font.SysFont("Arial", 20)
FUENTE_TITULO = pygame.font.SysFont("Arial", 80, bold=True)
FUENTE_ARCADA = pygame.font.SysFont("Courier New", 24, bold=True)
FUENTE_HISTORIA = pygame.font.SysFont("Courier New", 30, bold=True)
FUENTE_SUBTITULO = pygame.font.SysFont("Courier New", 36, bold=True)

# --- CARGA DE RECURSOS DESDE CARPETA NIVEL2 ---
def cargar_imagen(nombre, escala=None, alpha=True):
    try:
        # Buscar en carpeta nivel2 primero
        ruta_nivel2 = os.path.join("nivel2", nombre)
        if os.path.exists(ruta_nivel2):
            if alpha:
                img = pygame.image.load(ruta_nivel2).convert_alpha()
            else:
                img = pygame.image.load(ruta_nivel2).convert()
        else:
            # Si no existe en nivel2, buscar en carpeta actual
            if alpha:
                img = pygame.image.load(nombre).convert_alpha()
            else:
                img = pygame.image.load(nombre).convert()
        
        if escala:
            img = pygame.transform.scale(img, escala)
        return img
    except Exception as e:
        print(f"Error al cargar imagen {nombre}: {e}")
        # Placeholder si falta imagen
        if escala:
            surf = pygame.Surface(escala)
        else:
            surf = pygame.Surface((100, 100))
        surf.fill(ROJO)
        return surf

# Imágenes - Cargar desde carpeta nivel2
IMG_NAVE = cargar_imagen("nave.png", (60, 40))
IMG_ENEMIGO1 = cargar_imagen("enemigo1.png", (50, 50))
IMG_ENEMIGO2 = cargar_imagen("enemigo2.png", (50, 50))
IMG_ENEMIGO3 = cargar_imagen("enemigo3.png", (50, 50))
IMG_JEFE = cargar_imagen("jefe.png", (180, 180))
IMG_FONDO = cargar_imagen("fondo.png")
IMG_WINNER = cargar_imagen("winner.png", (400, 200))
IMG_VIDA_ICONO = cargar_imagen("vidas.png", (30, 30)) # Icono de vida

# Imágenes para obstáculos - desde carpeta nivel2
IMG_OBSTACULO1 = cargar_imagen("ladrillo.png", (60, 40))  # Ladrillo
IMG_OBSTACULO2 = cargar_imagen("linterna.png", (50, 70))  # Linterna
IMG_OBSTACULO3 = cargar_imagen("murcielago.png", (70, 50))  # Murciélago

# Imágenes para potenciadores (más grandes)
IMG_MISIL = cargar_imagen("misil.png", (50, 25))  # Más grande
IMG_BOMBA = cargar_imagen("bomba.png", (50, 50))  # Más grande
IMG_ESCUDO = cargar_imagen("escudo.png", (60, 60))  # Más grande

# Imágenes para las pantallas de historia (debes colocar tus imágenes PNG aquí)
IMG_HISTORIA_INICIO = cargar_imagen("historia_inicio_nivel2.png", (ANCHO, ALTO), alpha=True)
IMG_HISTORIA_FINAL = cargar_imagen("historia_final_nivel2.png", (ANCHO, ALTO), alpha=True)

IMG_FONDO = pygame.transform.scale(IMG_FONDO, (ANCHO, ALTO))

# Sonidos - Cargar desde carpeta nivel2
def cargar_sonido(nombre):
    try:
        # Buscar en carpeta nivel2 primero
        ruta_nivel2 = os.path.join("nivel2", nombre)
        if os.path.exists(ruta_nivel2):
            return pygame.mixer.Sound(ruta_nivel2)
        else:
            # Si no existe en nivel2, buscar en carpeta actual
            return pygame.mixer.Sound(nombre)
    except:
        return None

SND_DISPARO = cargar_sonido("disparo.mp3")
SND_CONTEO = cargar_sonido("conteo.mp3")
SND_COIN = cargar_sonido("coin.mp3")
SND_GAMEOVER = cargar_sonido("gameover.mp3")
SND_EXPLOSION = cargar_sonido("explosion.mp3")
SND_POWERUP = cargar_sonido("powerup.mp3")  # Sonido para potenciadores
SND_VICTORY = cargar_sonido("victory.mp3")  # Sonido de victoria

# --- FUNCIÓN PARA CARGAR SIGUIENTE NIVEL ---
def cargar_siguiente_nivel():
    """Intenta cargar el siguiente nivel (nivel3.py) desde la carpeta nivel3"""
    try:
        # Verificar si existe la carpeta nivel3
        if os.path.exists("nivel3"):
            print("Cargando nivel 3...")
            
            # Buscar el archivo nivel3.py
            archivo_nivel3 = os.path.join("nivel3", "nivel3.py")
            if os.path.exists(archivo_nivel3):
                print(f"Encontrado: {archivo_nivel3}")
                
                # Cerrar Pygame completamente antes de abrir el nuevo nivel
                pygame.quit()
                
                # Usar subprocess para ejecutar el nuevo nivel como un proceso separado
                # Esto asegura que Pygame se reinicie correctamente
                subprocess.Popen([sys.executable, archivo_nivel3])
                
                # Salir del juego actual
                sys.exit(0)
                
            else:
                print(f"Archivo nivel3.py no encontrado en la carpeta 'nivel3'")
                print(f"Buscando en: {os.path.abspath('nivel3')}")
                
                # Mostrar mensaje de error en pantalla
                mensaje_error = "Nivel 3 no disponible aún"
                return False, mensaje_error
        else:
            print("Carpeta 'nivel3' no encontrada")
            mensaje_error = "Carpeta 'nivel3' no encontrada"
            return False, mensaje_error
            
    except Exception as e:
        print(f"Error al cargar nivel 3: {e}")
        mensaje_error = f"Error: {str(e)[:50]}..."
        return False, mensaje_error
    
    return True, ""

# --- NUEVO: Clase para pantalla de historia estilo arcade con texto a la derecha ---
class PantallaHistoriaDerecha:
    def __init__(self, imagen_fondo, titulo, subtitulo, texto_historia):
        self.imagen_fondo = imagen_fondo
        self.titulo = titulo
        self.subtitulo = subtitulo
        self.texto_historia = texto_historia
        
        # Animación de texto palabra por palabra
        self.palabras = texto_historia.split()
        self.palabras_mostradas = 0
        self.temporizador_palabra = 0
        self.intervalo_palabra = 80  # ms entre palabras
        self.tiempo_inicio = 0
        
        # Efectos visuales
        self.efecto_brillo = 0
        self.direccion_brillo = 1
        self.particulas = []
        self.generar_particulas()
        
        # Panel de texto (lado derecho)
        self.ancho_panel = 550  # Ancho del panel de texto
        self.margen_panel = 40  # Margen interno del panel
        
        # Control de estado
        self.terminada = False
        self.saltar = False
        
        # Sonido de escritura (opcional)
        self.sonido_escritura = cargar_sonido("teclado.mp3")
        
        # Efecto de transición
        self.alpha_panel = 0
        self.alpha_texto = 0
        self.fase_transicion = 0  # 0: entrada panel, 1: entrada texto, 2: completa
        
    def generar_particulas(self):
        """Genera partículas para el efecto arcade"""
        self.particulas = []
        for _ in range(30):  # Menos partículas para no tapar el texto
            x = random.randint(0, ANCHO)
            y = random.randint(0, ALTO)
            velocidad_x = random.uniform(-0.3, 0.3)
            velocidad_y = random.uniform(-0.3, 0.3)
            tamaño = random.randint(1, 2)
            vida = random.randint(50, 150)
            color = random.choice([AZUL_ELECTRICO, VERDE_NEON, ROSA_NEON, AMARILLO])
            self.particulas.append([x, y, velocidad_x, velocidad_y, tamaño, vida, color])
    
    def actualizar_particulas(self):
        """Actualiza las partículas del fondo"""
        for i, particula in enumerate(self.particulas):
            # Mover partícula
            particula[0] += particula[2]
            particula[1] += particula[3]
            
            # Reducir vida
            particula[5] -= 1
            
            # Si la partícula muere, crear una nueva
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
        """Actualiza la animación de la pantalla de historia"""
        if self.saltar:
            self.terminada = True
            return
        
        # Actualizar efecto de brillo
        self.efecto_brillo += 0.05 * self.direccion_brillo
        if self.efecto_brillo > 1.0 or self.efecto_brillo < 0.0:
            self.direccion_brillo *= -1
        
        # Actualizar partículas
        self.actualizar_particulas()
        
        # Actualizar transición
        if self.fase_transicion == 0:
            self.alpha_panel = min(255, self.alpha_panel + 5)
            if self.alpha_panel >= 255:
                self.fase_transicion = 1
        elif self.fase_transicion == 1:
            self.alpha_texto = min(255, self.alpha_texto + 3)
            if self.alpha_texto >= 255:
                self.fase_transicion = 2
        
        # Controlar animación de texto palabra por palabra
        if self.fase_transicion >= 1:
            self.temporizador_palabra += dt
            
            if self.temporizador_palabra >= self.intervalo_palabra:
                if self.palabras_mostradas < len(self.palabras):
                    # Reproducir sonido de escritura si está disponible
                    if self.sonido_escritura and random.random() < 0.3:
                        self.sonido_escritura.play()
                    
                    self.palabras_mostradas += 1
                    self.temporizador_palabra = 0
                else:
                    # Todas las palabras mostradas, esperar para continuar
                    if self.tiempo_inicio == 0:
                        self.tiempo_inicio = pygame.time.get_ticks()
                    elif pygame.time.get_ticks() - self.tiempo_inicio > 3000:  # Esperar 3 segundos
                        self.terminada = True
    
    def dibujar(self, pantalla):
        """Dibuja la pantalla de historia con texto a la derecha"""
        # Dibujar fondo con imagen
        pantalla.blit(self.imagen_fondo, (0, 0))
        
        # Dibujar partículas
        for particula in self.particulas:
            x, y, _, _, tamaño, vida, color = particula
            alpha = min(255, vida * 2)
            s = pygame.Surface((tamaño*2, tamaño*2), pygame.SRCALPHA)
            pygame.draw.circle(s, (*color[:3], alpha), (tamaño, tamaño), tamaño)
            pantalla.blit(s, (int(x), int(y)))
        
        # Dibujar panel negro semitransparente en el lado derecho
        panel_surface = pygame.Surface((self.ancho_panel, ALTO), pygame.SRCALPHA)
        panel_color = (10, 10, 20, int(self.alpha_panel * 0.9))  # Negro azulado
        pygame.draw.rect(panel_surface, panel_color, (0, 0, self.ancho_panel, ALTO))
        
        # Borde neón para el panel
        borde_color = list(AZUL_ELECTRICO)
        borde_color = [int(c * (0.7 + 0.3 * self.efecto_brillo)) for c in borde_color]
        pygame.draw.rect(panel_surface, (*borde_color, int(self.alpha_panel)), 
                        (0, 0, self.ancho_panel, ALTO), 4)
        
        # Dibujar líneas de escaneo estilo arcade
        tiempo = pygame.time.get_ticks() * 0.002
        scan_y = int((math.sin(tiempo) * 0.5 + 0.5) * ALTO)
        pygame.draw.line(panel_surface, (0, 255, 255, 100), 
                        (10, scan_y), (self.ancho_panel - 10, scan_y), 2)
        
        pantalla.blit(panel_surface, (ANCHO - self.ancho_panel, 0))
        
        # Dibujar título con efecto de brillo (dentro del panel)
        titulo_color = list(CIAN_NEON)
        titulo_color = [int(c * (0.8 + 0.2 * self.efecto_brillo)) for c in titulo_color]
        titulo_alpha = min(255, int(self.alpha_texto))
        
        titulo_surf = FUENTE_TITULO.render(self.titulo, True, (*titulo_color, titulo_alpha))
        titulo_rect = titulo_surf.get_rect(center=(ANCHO - self.ancho_panel//2, 100))
        
        # Sombra del título
        titulo_sombra = FUENTE_TITULO.render(self.titulo, True, (0, 100, 150, titulo_alpha))
        pantalla.blit(titulo_sombra, (titulo_rect.x + 4, titulo_rect.y + 4))
        pantalla.blit(titulo_surf, titulo_rect)
        
        # Dibujar subtítulo
        subtitulo_alpha = min(255, int(self.alpha_texto * 0.9))
        subtitulo_surf = FUENTE_SUBTITULO.render(self.subtitulo, True, (VERDE_NEON[0], VERDE_NEON[1], VERDE_NEON[2], subtitulo_alpha))
        subtitulo_rect = subtitulo_surf.get_rect(center=(ANCHO - self.ancho_panel//2, 170))
        pantalla.blit(subtitulo_surf, subtitulo_rect)
        
        # Dibujar separador decorativo
        separador_y = 210
        pygame.draw.line(pantalla, (PURPURA_NEON[0], PURPURA_NEON[1], PURPURA_NEON[2], subtitulo_alpha),
                        (ANCHO - self.ancho_panel + 50, separador_y),
                        (ANCHO - 50, separador_y), 3)
        
        # Dibujar texto de la historia con animación palabra por palabra
        texto_actual = " ".join(self.palabras[:self.palabras_mostradas])
        
        # Configurar área de texto
        texto_x = ANCHO - self.ancho_panel + self.margen_panel
        texto_y = 250
        ancho_texto = self.ancho_panel - 2 * self.margen_panel
        
        # Dividir el texto en líneas para que quepa en el área
        palabras_linea = []
        linea_actual = []
        
        for palabra in texto_actual.split():
            linea_actual.append(palabra)
            linea_texto = " ".join(linea_actual)
            ancho_linea = FUENTE_HISTORIA.size(linea_texto)[0]
            
            if ancho_linea > ancho_texto:
                # Quitar la última palabra y guardar la línea
                ultima_palabra = linea_actual.pop()
                palabras_linea.append(" ".join(linea_actual))
                linea_actual = [ultima_palabra]
        
        # Añadir la última línea
        if linea_actual:
            palabras_linea.append(" ".join(linea_actual))
        
        # Dibujar cada línea con efecto de aparición
        y_pos = texto_y
        for i, linea in enumerate(palabras_linea):
            if y_pos < ALTO - 100:  # No dibujar fuera de pantalla
                # Calcular alpha para efecto de aparición progresivo
                linea_alpha = min(255, int(self.alpha_texto * (1.0 - i * 0.1)))
                if linea_alpha > 0:
                    linea_surf = FUENTE_HISTORIA.render(linea, True, (BLANCO[0], BLANCO[1], BLANCO[2], linea_alpha))
                    pantalla.blit(linea_surf, (texto_x, y_pos))
                    y_pos += 40
        
        # Dibujar cursor parpadeante al final del texto
        if self.palabras_mostradas < len(self.palabras) and self.fase_transicion >= 1:
            if (pygame.time.get_ticks() // 500) % 2 == 0:
                # Calcular posición del cursor
                texto_hasta_ahora = " ".join(self.palabras[:self.palabras_mostradas])
                if palabras_linea:
                    # Encontrar posición del cursor
                    ultima_linea = palabras_linea[-1]
                    cursor_x = texto_x + FUENTE_HISTORIA.size(ultima_linea)[0]
                    cursor_y = y_pos - 10  # Ajustar para última línea
                else:
                    cursor_x = texto_x
                    cursor_y = texto_y
                
                # Dibujar cursor
                cursor_height = 35
                cursor_alpha = min(255, int(self.alpha_texto))
                pygame.draw.rect(pantalla, (VERDE_NEON[0], VERDE_NEON[1], VERDE_NEON[2], cursor_alpha),
                               (cursor_x, cursor_y, 3, cursor_height))
        
        # Si el texto está completo, mostrar instrucción para continuar
        if self.palabras_mostradas >= len(self.palabras) and self.fase_transicion >= 1:
            if (pygame.time.get_ticks() // 500) % 2 == 0:  # Parpadeo cada 500ms
                continuar_alpha = min(255, int(self.alpha_texto))
                continuar_surf = FUENTE_ARCADA.render("Presiona ESPACIO para continuar", True, 
                                                    (AMARILLO[0], AMARILLO[1], AMARILLO[2], continuar_alpha))
                continuar_rect = continuar_surf.get_rect(center=(ANCHO - self.ancho_panel//2, ALTO - 60))
                
                # Sombra del texto
                continuar_sombra = FUENTE_ARCADA.render("Presiona ESPACIO para continuar", True, 
                                                       (NARANJA[0], NARANJA[1], NARANJA[2], continuar_alpha))
                pantalla.blit(continuar_sombra, (continuar_rect.x + 2, continuar_rect.y + 2))
                pantalla.blit(continuar_surf, continuar_rect)
    
    def manejar_eventos(self, eventos):
        """Maneja eventos de entrada"""
        for evento in eventos:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    if self.palabras_mostradas < len(self.palabras):
                        # Mostrar todo el texto inmediatamente
                        self.palabras_mostradas = len(self.palabras)
                        self.tiempo_inicio = pygame.time.get_ticks()
                    else:
                        # Continuar al siguiente estado
                        self.terminada = True
                elif evento.key == pygame.K_ESCAPE:
                    # Saltar completamente la pantalla
                    self.saltar = True
                    self.terminada = True
    
    def reiniciar(self):
        """Reinicia la animación"""
        self.palabras_mostradas = 0
        self.temporizador_palabra = 0
        self.tiempo_inicio = 0
        self.terminada = False
        self.saltar = False
        self.alpha_panel = 0
        self.alpha_texto = 0
        self.fase_transicion = 0

# --- CLASES DEL JUEGO ---

class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image_original = IMG_NAVE
        self.image = self.image_original.copy()
        self.rect = self.image.get_rect()
        self.rect.center = (100, ALTO // 2)
        self.velocidad = 5
        
        # Sistema de vidas
        self.vidas = 3
        self.vidas_iniciales = 3
        
        # Sistema de invulnerabilidad (para no morir instantáneamente)
        self.invulnerable = False
        self.tiempo_golpe = 0
        self.duracion_invulnerabilidad = 2000 # 2 segundos
        
        # Animación de la nave
        self.animacion_tiempo = 0
        self.offset_y = 0
        
        # Potenciadores
        self.misiles = 0
        self.bombas = 0
        self.escudo_activo = False
        self.tiempo_escudo = 0
        self.duracion_escudo = 5000  # 5 segundos
        
        # Nuevo: Misiles temporales
        self.misiles_temporales_activos = False
        self.tiempo_misiles_temporales = 0
        self.duracion_misiles_temporales = 5000  # 5 segundos
        
        # Estadísticas
        self.muertes = 0
        self.monedas_gastadas = 0
        
        # Control de disparo automático
        self.ultimo_disparo = 0
        self.intervalo_disparo = 200  # milisegundos entre disparos

    def update(self):
        # Movimiento
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.velocidad
        if teclas[pygame.K_DOWN] and self.rect.bottom < ALTO:
            self.rect.y += self.velocidad
        if teclas[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.velocidad
        if teclas[pygame.K_RIGHT] and self.rect.right < ANCHO:
            self.rect.x += self.velocidad

        # Animación de flotación
        self.animacion_tiempo += 0.1
        self.offset_y = math.sin(self.animacion_tiempo) * 2
        self.rect.y += int(self.offset_y)
        
        # Rotación sutil basada en movimiento
        if teclas[pygame.K_UP]:
            self.image = pygame.transform.rotate(self.image_original, 5)
        elif teclas[pygame.K_DOWN]:
            self.image = pygame.transform.rotate(self.image_original, -5)
        else:
            self.image = self.image_original.copy()
        
        # Actualizar rect después de rotación
        nuevo_rect = self.image.get_rect(center=self.rect.center)
        self.rect = nuevo_rect

        # Manejo de invulnerabilidad (parpadeo)
        if self.invulnerable:
            ahora = pygame.time.get_ticks()
            if ahora - self.tiempo_golpe > self.duracion_invulnerabilidad:
                self.invulnerable = False
                self.image.set_alpha(255) # Restaurar visibilidad completa
            else:
                # Efecto de parpadeo
                if (ahora // 200) % 2 == 0:
                    self.image.set_alpha(100)
                else:
                    self.image.set_alpha(255)
        else:
            self.image.set_alpha(255)
            
        # Manejo del escudo
        if self.escudo_activo:
            ahora = pygame.time.get_ticks()
            if ahora - self.tiempo_escudo > self.duracion_escudo:
                self.escudo_activo = False
        
        # Manejo de misiles temporales
        if self.misiles_temporales_activos:
            ahora = pygame.time.get_ticks()
            if ahora - self.tiempo_misiles_temporales > self.duracion_misiles_temporales:
                self.misiles_temporales_activos = False

        # Disparo automático al mantener ESPACIO presionado
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
            return True # Recibió daño real
        return False

    def disparar(self):
        if self.misiles_temporales_activos:
            # Disparar misil teledirigido
            return self.disparar_misil_temporal()
        else:
            # Disparo normal
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
        # Encontrar el objetivo más cercano (enemigo o jefe)
        objetivo = None
        distancia_minima = float('inf')
        
        # Buscar en enemigos
        for enemigo in enemigos:
            distancia = math.sqrt((enemigo.rect.centerx - self.rect.centerx)**2 + 
                                (enemigo.rect.centery - self.rect.centery)**2)
            if distancia < distancia_minima:
                distancia_minima = distancia
                objetivo = enemigo
        
        # Buscar en jefe
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

class Enemigo(pygame.sprite.Sprite):
    def __init__(self, tipo):
        super().__init__()
        self.tipo = tipo
        if tipo == 1:
            self.image = IMG_ENEMIGO1
            self.velocidad_x = -4
            self.vida = 1
            self.velocidad_persecucion = 2
        elif tipo == 2:
            self.image = IMG_ENEMIGO2
            self.velocidad_x = -6
            self.vida = 1
            self.velocidad_persecucion = 3
        elif tipo == 3:
            self.image = IMG_ENEMIGO3
            self.velocidad_x = -3
            self.vida = 2
            self.velocidad_persecucion = 1.5
        
        self.rect = self.image.get_rect()
        self.rect.x = ANCHO + random.randint(10, 100)
        self.rect.y = random.randint(50, ALTO - 50)
        self.temporizador_disparo = 0
        self.persiguiendo = False
        self.distancia_persecucion = 300
        self.velocidad_original_x = self.velocidad_x
        
        # En nivel 2, no todos los enemigos atacan
        self.puede_atacar = random.choice([True, False])

    def update(self):
        # Comportamiento según tipo
        if self.tipo == 1:  # Enemigo básico que persigue
            self.perseguir_jugador()
        elif self.tipo == 2:  # Enemigo rápido con movimiento sinusoidal
            self.movimiento_sinusoidal()
        elif self.tipo == 3:  # Enemigo tanque que dispara
            if self.puede_atacar:  # Solo dispara si puede atacar
                self.disparar_al_jugador()
            else:
                self.rect.x += self.velocidad_x
            
        # Eliminar si sale de pantalla
        if self.rect.right < 0:
            self.kill()

    def perseguir_jugador(self):
        """Enemigo tipo 1: Persigue al jugador cuando está cerca"""
        distancia = math.sqrt((jugador.rect.centerx - self.rect.centerx)**2 + 
                            (jugador.rect.centery - self.rect.centery)**2)
        
        if distancia < self.distancia_persecucion:
            self.persiguiendo = True
            # Moverse hacia el jugador
            dx = jugador.rect.centerx - self.rect.centerx
            dy = jugador.rect.centery - self.rect.centery
            distancia = max(1, math.sqrt(dx*dx + dy*dy))
            
            # Normalizar y aplicar velocidad
            dx = dx / distancia * self.velocidad_persecucion
            dy = dy / distancia * self.velocidad_persecucion
            
            self.rect.x += dx
            self.rect.y += dy
        else:
            self.persiguiendo = False
            # Movimiento normal
            self.rect.x += self.velocidad_x

    def movimiento_sinusoidal(self):
        """Enemigo tipo 2: Movimiento sinusoidal + evasión"""
        # Movimiento base sinusoidal
        self.rect.x += self.velocidad_x
        self.rect.y += int(np.sin(pygame.time.get_ticks() * 0.01) * 3)
        
        # Evitar al jugador si está muy cerca
        distancia = math.sqrt((jugador.rect.centerx - self.rect.centerx)**2 + 
                            (jugador.rect.centery - self.rect.centery)**2)
        
        if distancia < 150:
            dx = self.rect.centerx - jugador.rect.centerx
            dy = self.rect.centery - jugador.rect.centery
            distancia = max(1, math.sqrt(dx*dx + dy*dy))
            
            # Moverse en dirección opuesta al jugador
            dx = dx / distancia * 2
            dy = dy / distancia * 2
            
            self.rect.x += dx
            self.rect.y += dy

    def disparar_al_jugador(self):
        """Enemigo tipo 3: Dispara hacia el jugador"""
        self.rect.x += self.velocidad_x
        
        # Disparar hacia el jugador
        self.temporizador_disparo += 1
        if self.temporizador_disparo >= 80:  # Disparo cada ~1.3 segundos
            # Calcular dirección al jugador
            dx = jugador.rect.centerx - self.rect.centerx
            dy = jugador.rect.centery - self.rect.centery
            distancia = max(1, math.sqrt(dx*dx + dy*dy))
            
            # Normalizar y crear bala con dirección
            velocidad_bala = 7
            bala = Bala(self.rect.left, self.rect.centery, 
                       es_jugador=False, 
                       velocidad_x=(dx/distancia)*velocidad_bala,
                       velocidad_y=(dy/distancia)*velocidad_bala)
            all_sprites.add(bala)
            balas_enemigas.add(bala)
            self.temporizador_disparo = 0

class Obstaculo(pygame.sprite.Sprite):
    def __init__(self, tipo):
        super().__init__()
        self.tipo = tipo
        if tipo == 1:
            self.image = IMG_OBSTACULO1  # Ladrillo
            self.velocidad = random.randint(4, 7)
        elif tipo == 2:
            self.image = IMG_OBSTACULO2  # Linterna
            self.velocidad = random.randint(5, 8)
        elif tipo == 3:
            self.image = IMG_OBSTACULO3  # Murciélago
            self.velocidad = random.randint(6, 9)
            
        self.rect = self.image.get_rect()
        self.rect.x = ANCHO + random.randint(10, 100)
        self.rect.y = random.randint(50, ALTO - 50)
        
        # Movimiento especial para murciélago
        if tipo == 3:
            self.velocidad_y = random.uniform(-1, 1)
            self.tiempo_animacion = 0

    def update(self):
        self.rect.x -= self.velocidad
        
        # Movimiento especial para murciélago (vuelo ondulado)
        if self.tipo == 3:
            self.tiempo_animacion += 0.1
            self.rect.y += math.sin(self.tiempo_animacion) * 2
            
        # Eliminar si sale de pantalla
        if self.rect.right < 0:
            self.kill()

class Bala(pygame.sprite.Sprite):
    def __init__(self, x, y, es_jugador, velocidad_x=None, velocidad_y=0):
        super().__init__()
        self.es_jugador = es_jugador
        color = AMARILLO if es_jugador else ROJO
        self.image = pygame.Surface((10, 5) if velocidad_y == 0 else (8, 8))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.velocidad_x = velocidad_x if velocidad_x else (10 if es_jugador else -7)
        self.velocidad_y = velocidad_y

    def update(self):
        self.rect.x += self.velocidad_x
        self.rect.y += self.velocidad_y
        if (self.rect.right < 0 or self.rect.left > ANCHO or 
            self.rect.bottom < 0 or self.rect.top > ALTO):
            self.kill()

class BolaFuego(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.circle(self.image, NARANJA, (15, 15), 15)
        pygame.draw.circle(self.image, AMARILLO, (15, 15), 10)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.velocidad_y = random.randint(3, 7)
        self.velocidad_x = random.uniform(-1, 1)

    def update(self):
        self.rect.y += self.velocidad_y
        self.rect.x += self.velocidad_x
        if self.rect.top > ALTO or self.rect.right < 0 or self.rect.left > ANCHO:
            self.kill()

class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y, objetivo_x, objetivo_y):
        super().__init__()
        self.duracion = 60  # frames que dura el láser
        self.temporizador = 0
        self.rect = pygame.Rect(x, y, 10, 10)
        self.objetivo_x = objetivo_x
        self.objetivo_y = objetivo_y
        self.creciendo = True
        
        # Calcular dirección
        dx = objetivo_x - x
        dy = objetivo_y - y
        distancia = max(1, math.sqrt(dx*dx + dy*dy))
        self.dx = dx / distancia
        self.dy = dy / distancia
        
        self.longitud = 0
        self.longitud_maxima = distancia
        
    def update(self):
        self.temporizador += 1
        
        if self.creciendo:
            self.longitud += 15
            if self.longitud >= self.longitud_maxima:
                self.longitud = self.longitud_maxima
                self.creciendo = False
                
        if self.temporizador >= self.duracion:
            self.kill()
            
    def draw(self, surface):
        if self.creciendo or self.temporizador < self.duracion - 10:
            end_x = self.rect.x + self.dx * self.longitud
            end_y = self.rect.y + self.dy * self.longitud
            
            # Dibujar línea del láser con efecto
            for i in range(3):
                offset = random.randint(-1, 1)
                color = (255, 100 + offset*50, 0)
                pygame.draw.line(surface, color, 
                               (self.rect.x, self.rect.y), 
                               (end_x, end_y), 3 - i)

class Anillo(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.radio = 5
        self.radio_maximo = 100
        self.velocidad_crecimiento = 2
        self.image = pygame.Surface((self.radio_maximo*2, self.radio_maximo*2), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(x, y))
        self.activo = True
        
    def update(self):
        self.radio += self.velocidad_crecimiento
        if self.radio >= self.radio_maximo:
            self.kill()
            
    def draw(self, surface):
        if self.activo:
            # Dibujar anillo expansivo
            pygame.draw.circle(surface, (0, 200, 255), 
                             self.rect.center, self.radio, 3)
            pygame.draw.circle(surface, (100, 255, 255), 
                             self.rect.center, self.radio-2, 1)

class MisilTeledirigido(pygame.sprite.Sprite):
    def __init__(self, x, y, objetivo):
        super().__init__()
        self.image_original = IMG_MISIL
        self.image = self.image_original.copy()
        self.rect = self.image.get_rect(center=(x, y))
        self.objetivo = objetivo
        self.velocidad = 6
        self.giro_maximo = 0.1  # Velocidad máxima de giro
        self.velocidad_x = 0
        self.velocidad_y = 0
        
    def update(self):
        if self.objetivo and self.objetivo.alive():
            # Seguir al objetivo suavemente
            dx = self.objetivo.rect.centerx - self.rect.centerx
            dy = self.objetivo.rect.centery - self.rect.centery
            distancia = max(1, math.sqrt(dx*dx + dy*dy))
            
            # Normalizar dirección deseada
            dx_normal = dx / distancia
            dy_normal = dy / distancia
            
            # Calcular dirección actual
            angulo_actual = math.atan2(self.velocidad_y, self.velocidad_x) if self.velocidad_x != 0 or self.velocidad_y != 0 else 0
            
            # Calcular dirección deseada
            angulo_deseado = math.atan2(dy_normal, dx_normal)
            
            # Suavizar el giro
            diferencia_angulo = angulo_deseado - angulo_actual
            while diferencia_angulo > math.pi:
                diferencia_angulo -= 2 * math.pi
            while diferencia_angulo < -math.pi:
                diferencia_angulo += 2 * math.pi
                
            angulo_actual += max(-self.giro_maximo, min(self.giro_maximo, diferencia_angulo))
            
            # Actualizar velocidades
            self.velocidad_x = math.cos(angulo_actual) * self.velocidad
            self.velocidad_y = math.sin(angulo_actual) * self.velocidad
            
            # Actualizar posición
            self.rect.x += self.velocidad_x
            self.rect.y += self.velocidad_y
            
            # Rotar imagen según dirección
            angulo_grados = math.degrees(angulo_actual)
            self.image = pygame.transform.rotate(self.image_original, -angulo_grados)
            self.rect = self.image.get_rect(center=self.rect.center)
            
            # Verificar colisión con objetivo
            if pygame.sprite.collide_rect(self, self.objetivo):
                if SND_EXPLOSION: SND_EXPLOSION.play()
                self.objetivo.vida -= 1
                if self.objetivo.vida <= 0:
                    self.objetivo.kill()
                self.kill()
        else:
            # Si el objetivo ya no existe, volar en línea recta
            self.rect.x += self.velocidad_x
            self.rect.y += self.velocidad_y
            
        # Eliminar si sale de pantalla
        if (self.rect.right < 0 or self.rect.left > ANCHO or 
            self.rect.bottom < 0 or self.rect.top > ALTO):
            self.kill()

class Bomba(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image_original = IMG_BOMBA
        self.image = self.image_original.copy()
        self.rect = self.image.get_rect(center=(x, y))
        self.velocidad = 5
        self.tiempo_explosion = 60  # Frames hasta explotar
        self.temporizador = 0
        self.exploto = False
        
    def update(self):
        if not self.exploto:
            # Movimiento hacia adelante
            self.rect.x += self.velocidad
            
            # Animación de rotación
            self.temporizador += 1
            angulo = self.temporizador * 5
            self.image = pygame.transform.rotate(self.image_original, angulo)
            self.rect = self.image.get_rect(center=self.rect.center)
            
            # Verificar si es tiempo de explotar
            if self.temporizador >= self.tiempo_explosion:
                self.explotar()
                
            # Eliminar si sale de pantalla
            if self.rect.left > ANCHO:
                self.kill()
    
    def explotar(self):
        self.exploto = True
        if SND_EXPLOSION: SND_EXPLOSION.play()
        
        # Encontrar los 5 enemigos más cercanos
        enemigos_cercanos = []
        for enemigo in enemigos:
            distancia = math.sqrt((enemigo.rect.centerx - self.rect.centerx)**2 + 
                                (enemigo.rect.centery - self.rect.centery)**2)
            enemigos_cercanos.append((distancia, enemigo))
        
        # Ordenar por distancia y tomar los 5 más cercanos
        enemigos_cercanos.sort(key=lambda x: x[0])
        for i in range(min(5, len(enemigos_cercanos))):
            enemigos_cercanos[i][1].kill()
            
        # Destruir también los 5 obstáculos más cercanos
        obstaculos_cercanos = []
        for obstaculo in obstaculos:
            distancia = math.sqrt((obstaculo.rect.centerx - self.rect.centerx)**2 + 
                                (obstaculo.rect.centery - self.rect.centery)**2)
            obstaculos_cercanos.append((distancia, obstaculo))
        
        # Ordenar por distancia y tomar los 5 más cercanos
        obstaculos_cercanos.sort(key=lambda x: x[0])
        for i in range(min(5, len(obstaculos_cercanos))):
            obstaculos_cercanos[i][1].kill()
            
        # Efecto visual de explosión
        explosion = Explosion(self.rect.centerx, self.rect.centery)
        all_sprites.add(explosion)
        
        self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.radio = 5
        self.radio_maximo = 100
        self.velocidad_crecimiento = 5
        self.image = pygame.Surface((self.radio_maximo*2, self.radio_maximo*2), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(x, y))
        
    def update(self):
        self.radio += self.velocidad_crecimiento
        if self.radio >= self.radio_maximo:
            self.kill()
            
    def draw(self, surface):
        # Dibujar explosión
        pygame.draw.circle(surface, (255, 200, 0), 
                         self.rect.center, self.radio, 3)
        pygame.draw.circle(surface, (255, 100, 0), 
                         self.rect.center, self.radio-10, 2)

class CampoFuerza(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.radio = 50
        self.duracion = 300  # 5 segundos
        self.temporizador = 0
        self.image = pygame.Surface((self.radio*2, self.radio*2), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(x, y))
        
    def update(self):
        self.temporizador += 1
        if self.temporizador >= self.duracion:
            self.kill()
            
    def draw(self, surface):
        # Dibujar campo de fuerza con efecto pulsante
        pulsacion = math.sin(self.temporizador * 0.1) * 5
        radio_actual = self.radio + pulsacion
        
        for i in range(3):
            alpha = 100 - i * 30
            pygame.draw.circle(surface, (100, 200, 255, alpha), 
                             self.rect.center, radio_actual - i*5, 3)

class Escudo(pygame.sprite.Sprite):
    def __init__(self, jugador):
        super().__init__()
        self.jugador = jugador
        self.radio = 40
        self.image = pygame.Surface((self.radio*2, self.radio*2), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=self.jugador.rect.center)
        
    def update(self):
        # Seguir al jugador
        if self.jugador.alive():
            self.rect.center = self.jugador.rect.center
        else:
            self.kill()
        
    def draw(self, surface):
        # Dibujar escudo con efecto pulsante
        tiempo = pygame.time.get_ticks() * 0.01
        pulsacion = math.sin(tiempo) * 3
        radio_actual = self.radio + pulsacion
        
        # Escudo azul transparente con múltiples capas
        for i in range(3):
            alpha = 150 - i * 50
            grosor = 4 - i
            pygame.draw.circle(surface, (100, 200, 255, alpha), 
                             self.rect.center, radio_actual - i*5, grosor)

class Potenciador(pygame.sprite.Sprite):
    def __init__(self, tipo):
        super().__init__()
        self.tipo = tipo  # 1: Misil, 2: Bomba, 3: Escudo
        
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
        self.velocidad_x = -3
        
        # Animación
        self.tiempo_animacion = 0
        self.radio_aura = 40  # Aura más grande
        
    def update(self):
        self.rect.x += self.velocidad_x
        
        # Animación de flotación
        self.tiempo_animacion += 0.1
        self.rect.y += math.sin(self.tiempo_animacion) * 2
        
        # Eliminar si sale de pantalla
        if self.rect.right < 0:
            self.kill()
            
    def draw_aura(self, surface):
        # Dibujar aura alrededor del potenciador
        tiempo = pygame.time.get_ticks() * 0.01
        pulsacion = math.sin(tiempo) * 8  # Pulsación más pronunciada
        radio_actual = self.radio_aura + pulsacion
        
        # Aura pulsante más visible
        for i in range(3):
            alpha = 150 - i * 50  # Más visible
            pygame.draw.circle(surface, (*self.aura_color, alpha), 
                             self.rect.center, radio_actual - i*5, 4)  # Línea más gruesa
            
    def aplicar(self, jugador):
        if SND_POWERUP: SND_POWERUP.play()
        
        if self.tipo == 1:
            jugador.activar_misiles_temporales()
            return "¡MISILES TELEDIRIGIDOS TEMPORALES!"
        elif self.tipo == 2:
            jugador.bombas += 1
            return "¡BOMBA MULTI-OBJETIVO!"
        elif self.tipo == 3:
            jugador.activar_escudo()
            return "¡ESCUDO ACTIVADO!"

class Jefe(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = IMG_JEFE
        self.rect = self.image.get_rect()
        self.rect.x = ANCHO + 50
        self.rect.y = ALTO // 2 - 75
        self.vida = 50
        self.vida_max = 50
        self.velocidad_y = 3
        self.entrando = True
        
        # Sistema de ataques mejorado
        self.temporizador_ataque = 0
        self.ataque_actual = 0
        self.duracion_ataque = 180  # 3 segundos por ataque
        self.cooldown_ataque = 60   # 1 segundo entre ataques
        
        # Ataque 1: Disparos triples (original)
        self.temporizador_disparo = 0
        
        # Ataque 2: Bolas de fuego
        self.temporizador_bolas_fuego = 0
        
        # Ataque 3: Láser
        self.lasers = pygame.sprite.Group()
        self.temporizador_laser = 0
        
        # Ataque 4: Anillos expansivos
        self.anillos = pygame.sprite.Group()
        self.temporizador_anillos = 0
        
        # Nuevos ataques para nivel 2
        # Ataque 5: Rayos eléctricos
        self.rayos = pygame.sprite.Group()
        self.temporizador_rayos = 0
        
        # Ataque 6: Olas de choque
        self.olas = pygame.sprite.Group()
        self.temporizador_olas = 0
        
        # Ataque 7: Campos magnéticos
        self.campos_magneticos = pygame.sprite.Group()
        self.temporizador_campos = 0
        
        # Efectos de cámara
        self.tiempo_temblor = 0
        self.intensidad_temblor = 0

    def update(self):
        # Movimiento básico
        if self.entrando:
            self.rect.x -= 2
            if self.rect.right <= ANCHO - 20:
                self.entrando = False
        else:
            # Movimiento vertical suave
            self.rect.y += self.velocidad_y
            if self.rect.top <= 50 or self.rect.bottom >= ALTO - 50:
                self.velocidad_y *= -1
            
            # Sistema de ciclo de ataques
            self.temporizador_ataque += 1
            
            if self.temporizador_ataque > self.duracion_ataque + self.cooldown_ataque:
                self.temporizador_ataque = 0
                self.ataque_actual = (self.ataque_actual + 1) % 7  # Ahora 7 ataques
                # Activar efecto de cámara al cambiar ataque
                self.activar_temblor(10)
            
            # Ejecutar ataque actual
            if self.temporizador_ataque < self.duracion_ataque:
                if self.ataque_actual == 0:
                    self.ataque_disparos_triples()
                elif self.ataque_actual == 1:
                    self.ataque_bolas_fuego()
                elif self.ataque_actual == 2:
                    self.ataque_laser()
                elif self.ataque_actual == 3:
                    self.ataque_anillos()
                elif self.ataque_actual == 4:
                    self.ataque_rayos_electricos()
                elif self.ataque_actual == 5:
                    self.ataque_olas_choque()
                elif self.ataque_actual == 6:
                    self.ataque_campos_magneticos()
            
            # Actualizar efectos
            self.lasers.update()
            self.anillos.update()
            self.rayos.update()
            self.olas.update()
            self.campos_magneticos.update()
            
            # Actualizar temblor de cámara
            if self.tiempo_temblor > 0:
                self.tiempo_temblor -= 1

    def ataque_disparos_triples(self):
        # Ataque original: disparos en triple línea
        self.temporizador_disparo += 1
        if self.temporizador_disparo >= 30:  # Disparo cada 0.5 segundos
            for i in range(-1, 2):
                bala = Bala(self.rect.left, self.rect.centery + (i*30), es_jugador=False, velocidad_x=-8)
                all_sprites.add(bala)
                balas_enemigas.add(bala)
            self.temporizador_disparo = 0
            # Temblor leve para disparos
            self.activar_temblor(3)

    def ataque_bolas_fuego(self):
        # Lluvia de bolas de fuego desde arriba
        self.temporizador_bolas_fuego += 1
        if self.temporizador_bolas_fuego >= 20:  # Cada 0.33 segundos
            for _ in range(2):  # 2 bolas a la vez
                x = random.randint(100, ANCHO - 100)
                bola = BolaFuego(x, -20)
                all_sprites.add(bola)
                balas_enemigas.add(bola)
            self.temporizador_bolas_fuego = 0

    def ataque_laser(self):
        # Láser que apunta al jugador
        self.temporizador_laser += 1
        if self.temporizador_laser >= 90:  # Cada 1.5 segundos
            laser = Laser(self.rect.centerx, self.rect.centery, 
                         jugador.rect.centerx, jugador.rect.centery)
            self.lasers.add(laser)
            self.temporizador_laser = 0
            # Temblor fuerte para láser
            self.activar_temblor(8)

    def ataque_anillos(self):
        # Anillos expansivos desde el jefe
        self.temporizador_anillos += 1
        if self.temporizador_anillos >= 45:  # Cada 0.75 segundos
            anillo = Anillo(self.rect.centerx, self.rect.centery)
            self.anillos.add(anillo)
            self.temporizador_anillos = 0
            # Temblor medio para anillos
            self.activar_temblor(5)

    def ataque_rayos_electricos(self):
        # Rayos eléctricos que se extienden desde el jefe
        self.temporizador_rayos += 1
        if self.temporizador_rayos >= 60:  # Cada 1 segundo
            for i in range(3):  # 3 rayos a la vez
                rayo = RayoElectrico(self.rect.centerx, self.rect.centery, 
                                    random.randint(0, ANCHO), random.randint(0, ALTO))
                self.rayos.add(rayo)
            self.temporizador_rayos = 0
            # Temblor medio para rayos
            self.activar_temblor(4)

    def ataque_olas_choque(self):
        # Olas de choque que se expanden desde el jefe
        self.temporizador_olas += 1
        if self.temporizador_olas >= 75:  # Cada 1.25 segundos
            ola = OlaChoque(self.rect.centerx, self.rect.centery)
            self.olas.add(ola)
            self.temporizador_olas = 0
            # Temblor fuerte para olas
            self.activar_temblor(6)

    def ataque_campos_magneticos(self):
        # Campos magnéticos que atraen al jugador
        self.temporizador_campos += 1
        if self.temporizador_campos >= 100:  # Cada 1.66 segundos
            x = random.randint(200, ANCHO - 200)
            y = random.randint(100, ALTO - 100)
            campo = CampoMagnetico(x, y)
            self.campos_magneticos.add(campo)
            self.temporizador_campos = 0
            # Temblor leve para campos
            self.activar_temblor(2)

    def activar_temblor(self, intensidad):
        self.tiempo_temblor = 10  # Duración del temblor en frames
        self.intensidad_temblor = intensidad

    def draw_efectos(self, surface):
        # Dibujar lasers, anillos, rayos, olas y campos magnéticos
        for laser in self.lasers:
            laser.draw(surface)
        for anillo in self.anillos:
            anillo.draw(surface)
        for rayo in self.rayos:
            rayo.draw(surface)
        for ola in self.olas:
            ola.draw(surface)
        for campo in self.campos_magneticos:
            campo.draw(surface)

    def get_temblor_offset(self):
        if self.tiempo_temblor > 0:
            return (random.randint(-self.intensidad_temblor, self.intensidad_temblor),
                   random.randint(-self.intensidad_temblor, self.intensidad_temblor))
        return (0, 0)

class RayoElectrico(pygame.sprite.Sprite):
    def __init__(self, x, y, objetivo_x, objetivo_y):
        super().__init__()
        self.duracion = 45  # frames que dura el rayo
        self.temporizador = 0
        self.rect = pygame.Rect(x, y, 10, 10)
        self.objetivo_x = objetivo_x
        self.objetivo_y = objetivo_y
        self.activo = True
        
        # Calcular dirección
        dx = objetivo_x - x
        dy = objetivo_y - y
        distancia = max(1, math.sqrt(dx*dx + dy*dy))
        self.dx = dx / distancia
        self.dy = dy / distancia
        
        self.longitud = 0
        self.longitud_maxima = distancia
        
    def update(self):
        self.temporizador += 1
        if self.temporizador >= self.duracion:
            self.kill()
            
    def draw(self, surface):
        if self.activo:
            end_x = self.rect.x + self.dx * self.longitud_maxima
            end_y = self.rect.y + self.dy * self.longitud_maxima
            
            # Dibujar rayo eléctrico con efecto de chispas
            for i in range(5):
                offset_x = random.randint(-3, 3)
                offset_y = random.randint(-3, 3)
                color = (100, 200, 255) if i % 2 == 0 else (200, 230, 255)
                pygame.draw.line(surface, color, 
                               (self.rect.x + offset_x, self.rect.y + offset_y), 
                               (end_x + offset_x, end_y + offset_y), 2)

class OlaChoque(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.radio = 10
        self.radio_maximo = 300
        self.velocidad_crecimiento = 8
        self.image = pygame.Surface((self.radio_maximo*2, self.radio_maximo*2), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(x, y))
        self.activo = True
        
    def update(self):
        self.radio += self.velocidad_crecimiento
        if self.radio >= self.radio_maximo:
            self.kill()
            
    def draw(self, surface):
        if self.activo:
            # Dibujar ola de choque con efecto de onda
            for i in range(3):
                alpha = 150 - i * 50
                grosor = 5 - i
                pygame.draw.circle(surface, (0, 150, 255, alpha), 
                                 self.rect.center, self.radio - i*20, grosor)

class CampoMagnetico(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.radio = 60
        self.duracion = 200  # 3.33 segundos
        self.temporizador = 0
        self.image = pygame.Surface((self.radio*2, self.radio*2), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(x, y))
        self.fuerza_atraccion = 0.5
        
    def update(self):
        self.temporizador += 1
        
        # Atraer al jugador si está dentro del radio
        if jugador.alive():
            distancia = math.sqrt((jugador.rect.centerx - self.rect.centerx)**2 + 
                                (jugador.rect.centery - self.rect.centery)**2)
            if distancia < self.radio * 2:  # Radio de influencia más grande
                dx = self.rect.centerx - jugador.rect.centerx
                dy = self.rect.centery - jugador.rect.centery
                distancia = max(1, math.sqrt(dx*dx + dy*dy))
                
                # Aplicar fuerza de atracción
                jugador.rect.x += (dx / distancia) * self.fuerza_atraccion
                jugador.rect.y += (dy / distancia) * self.fuerza_atraccion
        
        if self.temporizador >= self.duracion:
            self.kill()
            
    def draw(self, surface):
        # Dibujar campo magnético con efecto pulsante
        tiempo = pygame.time.get_ticks() * 0.01
        pulsacion = math.sin(tiempo) * 10
        radio_actual = self.radio + pulsacion
        
        # Campo magnético con efecto de líneas de fuerza
        for i in range(5):
            alpha = 100 - i * 20
            pygame.draw.circle(surface, (150, 150, 255, alpha), 
                             self.rect.center, radio_actual - i*10, 2)

# --- FUNCIONES AUXILIARES ---

def reproducir_video_con_sonido(ruta, sonido_personalizado=None):
    """Reproduce video en formato horizontal respetando su duración original con sonido personalizado"""
    # Buscar en carpeta nivel2 primero
    ruta_nivel2 = os.path.join("nivel2", ruta)
    if os.path.exists(ruta_nivel2):
        cap = cv2.VideoCapture(ruta_nivel2)
    else:
        # Si no existe en nivel2, buscar en carpeta actual
        cap = cv2.VideoCapture(ruta)
        
    if not cap.isOpened():
        print(f"Error al cargar video: {ruta}")
        return False
    
    # Obtener información del video
    fps_original = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duracion_total = total_frames / fps_original if fps_original > 0 else 0
    
    print(f"Reproduciendo: {ruta} - Duración: {duracion_total:.2f} segundos")
    
    # Reproducir sonido personalizado si se proporciona
    if sonido_personalizado:
        sonido_personalizado.play()
    
    reloj_video = pygame.time.Clock()
    tiempo_inicio = pygame.time.get_ticks()
    reproduciendo = True
    
    while reproduciendo and cap.isOpened():
        tiempo_actual = pygame.time.get_ticks()
        tiempo_transcurrido = (tiempo_actual - tiempo_inicio) / 1000.0
        
        # Salir si se acabó el tiempo del video
        if tiempo_transcurrido >= duracion_total:
            break
            
        # Leer frame actual basado en el tiempo transcurrido
        frame_pos = int(tiempo_transcurrido * fps_original)
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_pos)
        ret, frame = cap.read()
        
        if not ret:
            break
            
        # Convertir de BGR a RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Redimensionar para que ocupe toda la pantalla horizontalmente
        frame = cv2.resize(frame, (ANCHO, ALTO))
        
        # CORREGIDO: Voltear horizontalmente para corregir efecto espejo
        frame = cv2.flip(frame, 1)
        
        # Rotar para orientación correcta
        frame = np.rot90(frame)
        frame = pygame.surfarray.make_surface(frame)
        
        # Manejar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cap.release()
                if sonido_personalizado:
                    sonido_personalizado.stop()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE:
                    reproduciendo = False

        PANTALLA.blit(frame, (0, 0))
        pygame.display.flip()
        reloj_video.tick(FPS)
    
    cap.release()
    if sonido_personalizado:
        sonido_personalizado.stop()
    return True

def reproducir_musica(ruta, volumen=0.5):
    """Reproduce música respetando su duración"""
    try:
        # Buscar en carpeta nivel2 primero
        ruta_nivel2 = os.path.join("nivel2", ruta)
        if os.path.exists(ruta_nivel2):
            pygame.mixer.music.load(ruta_nivel2)
        else:
            # Si no existe en nivel2, buscar en carpeta actual
            pygame.mixer.music.load(ruta)
            
        # Detener cualquier música que esté sonando antes de reproducir una nueva
        pygame.mixer.music.stop()
        pygame.mixer.music.set_volume(volumen)
        pygame.mixer.music.play(-1)  # -1 para loop infinito
        return True
    except:
        print(f"No se pudo cargar la música: {ruta}")
        return False

def detener_musica():
    """Detiene la música de fondo"""
    pygame.mixer.music.stop()

def pausar_musica():
    """Pausa la música de fondo"""
    pygame.mixer.music.pause()

def reanudar_musica():
    """Reanuda la música de fondo desde donde se pausó"""
    pygame.mixer.music.unpause()

def dibujar_barra_arcade(surface, x, y, ancho, alto, progreso, color_fondo, color_relleno, texto=""):
    """Dibuja una barra de progreso estilo arcade"""
    # Fondo de la barra
    pygame.draw.rect(surface, color_fondo, (x, y, ancho, alto), border_radius=5)
    
    # Relleno
    if progreso > 0:
        ancho_relleno = int((ancho - 4) * progreso)
        pygame.draw.rect(surface, color_relleno, (x + 2, y + 2, ancho_relleno, alto - 4), border_radius=3)
    
    # Borde
    pygame.draw.rect(surface, BLANCO, (x, y, ancho, alto), 2, border_radius=5)
    
    # Texto
    if texto:
        txt = FUENTE_PEQ.render(texto, True, BLANCO)
        surface.blit(txt, (x + ancho + 10, y))

def dibujar_hud(surf, x, y, vidas, puntaje, meta_puntaje, jugador, tiempo_transcurrido, enemigos_eliminados):
    # 1. Dibujar iconos de vidas
    for i in range(vidas):
        surf.blit(IMG_VIDA_ICONO, (x + (i * 35), y))
    
    # 2. Barra de progreso para el Jefe (estilo arcade)
    progreso_jefe = min(puntaje / meta_puntaje, 1.0)
    dibujar_barra_arcade(surf, ANCHO // 2 - 100, 10, 200, 20, progreso_jefe, 
                        (50, 50, 50), AZUL, f"JEFE: {int(progreso_jefe*100)}%")
    
    # 3. Barra de puntaje (estilo arcade)
    max_puntaje = 1000
    progreso_puntaje = min(puntaje / max_puntaje, 1.0)
    dibujar_barra_arcade(surf, 10, 50, 200, 20, progreso_puntaje,
                        (50, 50, 50), VERDE_NEON, f"PTS: {puntaje}")
    
    # 4. Barra de tiempo (estilo arcade)
    max_tiempo = 300  # 5 minutos máximo
    progreso_tiempo = min(tiempo_transcurrido / max_tiempo, 1.0)
    tiempo_restante = max(0, max_tiempo - tiempo_transcurrido)
    minutos = int(tiempo_restante // 60)
    segundos = int(tiempo_restante % 60)
    dibujar_barra_arcade(surf, ANCHO - 210, 50, 200, 20, progreso_tiempo,
                        (50, 50, 50), NARANJA, f"TIME: {minutos:02d}:{segundos:02d}")
    
    # 5. Mostrar potenciadores activos
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
    
    # 6. Estadísticas rápidas
    txt_eliminados = FUENTE_PEQ.render(f"Eliminados: {enemigos_eliminados}", True, AMARILLO)
    surf.blit(txt_eliminados, (ANCHO - 150, 80))

def dibujar_game_over(surf, puntaje):
    # Fondo semitransparente
    overlay = pygame.Surface((ANCHO, ALTO))
    overlay.set_alpha(200)
    overlay.fill(NEGRO)
    surf.blit(overlay, (0,0))
    
    # Textos
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
    """Dibuja la pantalla de resultados finales estilo arcade"""
    # Fondo con efecto de partículas
    surf.fill(NEGRO)
    
    # Efecto de estrellas en el fondo
    for i in range(100):
        x = random.randint(0, ANCHO)
        y = random.randint(0, ALTO)
        tamaño = random.randint(1, 3)
        brillo = random.randint(100, 255)
        pygame.draw.circle(surf, (brillo, brillo, brillo), (x, y), tamaño)
    
    # Título
    titulo = FUENTE_TITULO.render("¡NIVEL 2 COMPLETADO!", True, VERDE_NEON)
    titulo_shadow = FUENTE_TITULO.render("¡NIVEL 2 COMPLETADO!", True, VERDE)
    
    surf.blit(titulo_shadow, (ANCHO//2 - titulo.get_width()//2 + 3, 53))
    surf.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 50))
    
    # Estadísticas
    y_pos = 150
    estadisticas_lista = [
        (f"PUNTAJE TOTAL: {estadisticas['puntaje']}", VERDE_NEON),
        (f"NAVES ELIMINADAS: {estadisticas['enemigos_eliminados']}", AMARILLO),
        (f"MUERTES: {estadisticas['muertes']}", ROJO),
        (f"MONEDAS GASTADAS: {estadisticas['monedas_gastadas']}", NARANJA),
        (f"TIEMPO TOTAL: {estadisticas['tiempo_formateado']}", CYAN),
        (f"VIDAS RESTANTES: {estadisticas['vidas_restantes']}/{estadisticas['vidas_iniciales']}", AZUL)
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
        alt_txt = FUENTE_ARCADA.render("Presiona R para reiniciar nivel 2", True, AMARILLO)
        surf.blit(alt_txt, (ANCHO//2 - alt_txt.get_width()//2, y_pos + 20))
        y_pos += 40
    
    # Mensaje parpadeante estilo arcade
    tiempo_actual = pygame.time.get_ticks()
    if (tiempo_actual // 500) % 2 == 0:  # Parpadeo cada 500ms
        if not mensaje_error:
            mensaje = FUENTE_ARCADA.render("PRESIONA ESPACIO para avanzar al NIVEL 3 o ESC para salir", True, BLANCO)
        else:
            mensaje = FUENTE_ARCADA.render("PRESIONA R para reiniciar nivel 2 o ESC para salir", True, BLANCO)
        surf.blit(mensaje, (ANCHO//2 - mensaje.get_width()//2, ALTO - 80))

# --- GRUPOS DE SPRITES GLOBALES ---
all_sprites = pygame.sprite.Group()
enemigos = pygame.sprite.Group()
balas_jugador = pygame.sprite.Group()
balas_enemigas = pygame.sprite.Group()
jefe_grupo = pygame.sprite.GroupSingle()
potenciadores = pygame.sprite.Group()
escudo_grupo = pygame.sprite.GroupSingle()
obstaculos = pygame.sprite.Group()  # Nuevo grupo para obstáculos
jugador = Jugador()
all_sprites.add(jugador)

# --- FUNCIÓN DE REINICIO ---
def reiniciar_nivel(completo=True):
    # Limpiar todos los grupos
    enemigos.empty()
    balas_jugador.empty()
    balas_enemigas.empty()
    jefe_grupo.empty()
    potenciadores.empty()
    escudo_grupo.empty()
    obstaculos.empty()  # Limpiar obstáculos
    
    # Reiniciar jugador
    jugador.rect.center = (100, ALTO // 2)
    jugador.vidas = 3
    jugador.vidas_iniciales = 3
    jugador.invulnerable = False
    jugador.misiles = 0
    jugador.bombas = 0
    jugador.escudo_activo = False
    jugador.misiles_temporales_activos = False
    jugador.muertes = 0
    jugador.monedas_gastadas = 0
    
    if completo:
        return 0, 1 # Retorna puntaje 0 y estado 1 (Cuenta regresiva)
    else:
        return None # Solo reinicia posiciones/vidas

# --- LOOP PRINCIPAL ---

def juego():
    estado = 0 
    # 0: Historia Intro, 1: Cuenta, 2: Juego, 3: Jefe, 4: Winner, 5: Historia Final, 6: Game Over, 7: Resultados Finales
    
    puntaje = 0
    META_PUNTAJE = 20 # Puntos necesarios para el jefe
    estado_anterior = 2 # Para saber donde regresar al continuar
    
    fondo_x = 0
    tiempo_inicio_conteo = 0
    tiempo_inicio_nivel = 0
    
    tiempo_inicio_winner = 0
    efecto_salto = 0
    direccion_salto = 1
    
    # Estadísticas
    enemigos_eliminados = 0
    tiempo_total_nivel = 0
    
    # Efectos de pantalla
    tiempo_temblor = 0
    intensidad_temblor = 0
    mensaje_powerup = ""
    tiempo_mensaje = 0
    
    # Control para temblor a los 30 segundos
    temblor_30s_activado = False
    tiempo_inicio_temblor_30s = 0
    duracion_temblor_30s = 10000  # 10 segundos en milisegundos

    # Control de música mejorado
    musica_reproduciendose = False
    musica_pausada = False
    musica_posicion = 0  # Variable para guardar la posición de la música

    # Textos para la historia INICIO (puedes modificar estos textos según tu historia)
    titulo_inicio = "VICTOR?"
    subtitulo_inicio = "NIVEL2"
    
    historia_inicio = (
        "Motocle llega al edificio K1, donde enfrenta al Profe Víctor. "
    "Este reto no será sencillo: Víctor ataca rápido y cambia de ritmo. "
    "Mantén el enfoque y demuestra que puedes superar esta materia."
    )
    
    # Textos para la historia FINAL (puedes modificar estos textos según tu historia)
    titulo_final = "SI SE PUDO"
    subtitulo_final = "LE GANAMOS"
    
    historia_final = (
         "Motocle derrota al Profe Víctor y supera el desafío del K1. "
    "Su esfuerzo rinde frutos: obtiene una excelente calificación y avanza "
    "con firmeza hacia su graduación galáctica."
    )
    
    # Crear pantallas de historia
    pantalla_historia_inicio = PantallaHistoriaDerecha(IMG_HISTORIA_INICIO, titulo_inicio, subtitulo_inicio, historia_inicio)
    pantalla_historia_final = PantallaHistoriaDerecha(IMG_HISTORIA_FINAL, titulo_final, subtitulo_final, historia_final)
    
    # Variable para mensaje de error al cargar nivel 3
    mensaje_error_nivel3 = ""
    
    reloj = pygame.time.Clock()
    ejecutando = True

    while ejecutando:
        dt = reloj.tick(FPS)
        
        # Calcular tiempo transcurrido
        if estado in [2, 3]:  # Solo contar tiempo durante el juego
            tiempo_total_nivel = (pygame.time.get_ticks() - tiempo_inicio_nivel) / 1000.0
            
            # Activar temblor a los 30 segundos
            if estado == 2 and not temblor_30s_activado and tiempo_total_nivel >= 30:
                print("¡Temblor de 30 segundos activado!")
                temblor_30s_activado = True
                tiempo_inicio_temblor_30s = pygame.time.get_ticks()
                tiempo_temblor = 1000  # Valor alto para que dure
                intensidad_temblor = 8  # Intensidad moderada
        
        # Controlar duración del temblor de 30 segundos
        if temblor_30s_activado:
            tiempo_transcurrido_temblor = pygame.time.get_ticks() - tiempo_inicio_temblor_30s
            if tiempo_transcurrido_temblor >= duracion_temblor_30s:
                print("Temblor de 30 segundos terminado")
                temblor_30s_activado = False
                tiempo_temblor = 0
                intensidad_temblor = 0
        
        eventos = pygame.event.get()
        for event in eventos:
            if event.type == pygame.QUIT:
                ejecutando = False
            
            # Estados de historia manejan sus propios eventos
            if estado == 0:  # Historia inicio
                pantalla_historia_inicio.manejar_eventos([event])
            elif estado == 5:  # Historia final
                pantalla_historia_final.manejar_eventos([event])
            
            if event.type == pygame.KEYDOWN:
                # Bomba (solo con tecla B)
                if event.key == pygame.K_b and (estado == 2 or estado == 3):  # Bomba
                    if jugador.lanzar_bomba():
                        # Efecto visual/sonoro
                        pass
                
                # Opciones Game Over
                if estado == 6:
                    if event.key == pygame.K_c: # Continuar
                        if SND_COIN: SND_COIN.play()
                        # Regresar al estado donde murió
                        estado = estado_anterior
                        # Reiniciar vidas y limpiar balas peligrosas cercanas
                        jugador.vidas = 3
                        jugador.invulnerable = True
                        jugador.tiempo_golpe = pygame.time.get_ticks()
                        balas_enemigas.empty()
                        # Reanudar música SOLO si estaba pausada
                        if musica_pausada:
                            reanudar_musica()
                            musica_reproduciendose = True
                            musica_pausada = False

                    elif event.key == pygame.K_r: # Reiniciar Nivel
                        puntaje, estado = reiniciar_nivel(completo=True)
                        tiempo_inicio_conteo = pygame.time.get_ticks()
                        tiempo_inicio_nivel = pygame.time.get_ticks()
                        enemigos_eliminados = 0
                        # Reiniciar también el temblor de 30 segundos
                        temblor_30s_activado = False
                        tiempo_temblor = 0
                        intensidad_temblor = 0
                        if SND_CONTEO: SND_CONTEO.play()
                        detener_musica()
                        musica_reproduciendose = False
                        musica_pausada = False

                    elif event.key == pygame.K_m: # Menú Principal
                        print("Regresando al menú principal... (Pendiente)")
                        ejecutando = False
                
                # Resultados finales
                if estado == 7:
                    if event.key == pygame.K_SPACE and not mensaje_error_nivel3:
                        # Intentar cargar nivel 3
                        exito, mensaje = cargar_siguiente_nivel()
                        if not exito:
                            mensaje_error_nivel3 = mensaje
                    
                    elif event.key == pygame.K_r:  # Reiniciar nivel 2
                        puntaje, estado = reiniciar_nivel(completo=True)
                        tiempo_inicio_conteo = pygame.time.get_ticks()
                        tiempo_inicio_nivel = pygame.time.get_ticks()
                        enemigos_eliminados = 0
                        mensaje_error_nivel3 = ""  # Limpiar mensaje de error
                        # Reiniciar también el temblor de 30 segundos
                        temblor_30s_activado = False
                        tiempo_temblor = 0
                        intensidad_temblor = 0
                        detener_musica()
                        musica_reproduciendose = False
                        musica_pausada = False
                    
                    elif event.key == pygame.K_ESCAPE:
                        print("Saliendo del juego...")
                        ejecutando = False

        # --- MÁQUINA DE ESTADOS ---

        if estado == 0: # Historia Inicio
            pantalla_historia_inicio.actualizar(dt)
            pantalla_historia_inicio.dibujar(PANTALLA)
            
            if pantalla_historia_inicio.terminada:
                estado = 1
                tiempo_inicio_conteo = pygame.time.get_ticks()
                tiempo_inicio_nivel = pygame.time.get_ticks()
                if SND_CONTEO: SND_CONTEO.play()

        elif estado == 1: # Cuenta Regresiva
            PANTALLA.blit(IMG_FONDO, (0,0))
            ahora = pygame.time.get_ticks()
            delta = ahora - tiempo_inicio_conteo
            
            texto = ""
            if delta < 500: texto = "3"
            elif delta < 800: texto = "2"
            elif delta < 1000: texto = "1"
            elif delta < 4000: 
                texto = "¡VAMOS!"
                if not musica_reproduciendose and not musica_pausada:
                    reproducir_musica("fondo_musica_nivel2.mp3", 0.5)
                    musica_reproduciendose = True
            else:
                estado = 2 
            
            if texto:
                surf = FUENTE_GRANDE.render(texto, True, AMARILLO)
                PANTALLA.blit(surf, surf.get_rect(center=(ANCHO//2, ALTO//2)))

        elif estado == 2: # Juego Normal
            # Aplicar efecto de temblor si está activo (temblor de 30 segundos u otros)
            offset_x, offset_y = (0, 0)
            if tiempo_temblor > 0:
                offset_x += random.randint(-intensidad_temblor, intensidad_temblor)
                offset_y += random.randint(-intensidad_temblor, intensidad_temblor)
                tiempo_temblor -= 1
            
            # Scroll Fondo con posible temblor
            fondo_x -= 2
            if fondo_x <= -ANCHO: fondo_x = 0
            PANTALLA.blit(IMG_FONDO, (fondo_x + offset_x, offset_y))
            PANTALLA.blit(IMG_FONDO, (fondo_x + ANCHO + offset_x, offset_y))

            # Generar Enemigos
            if len(enemigos) < 4 and random.randint(0, 100) < 2:
                tipo = random.randint(1, 3)
                e = Enemigo(tipo)
                all_sprites.add(e)
                enemigos.add(e)
            
            # Generar obstáculos
            if random.randint(0, 100) < 3:  # Probabilidad incrementada de generar obstáculos
                tipo_obstaculo = random.randint(1, 3)
                obstaculo = Obstaculo(tipo_obstaculo)
                all_sprites.add(obstaculo)
                obstaculos.add(obstaculo)
            
            # Generar Potenciadores
            if len(potenciadores) == 0 and random.randint(0, 500) < 2:
                tipo = random.randint(1, 3)
                p = Potenciador(tipo)
                all_sprites.add(p)
                potenciadores.add(p)
            
            # Checar invocación jefe
            if puntaje >= META_PUNTAJE and len(enemigos) == 0:
                estado = 3
                # Limpiar balas viejas
                balas_enemigas.empty()
                balas_jugador.empty()
                # Crear jefe
                jefe = Jefe()
                all_sprites.add(jefe)
                jefe_grupo.add(jefe)

            all_sprites.update()
            all_sprites.draw(PANTALLA)
            
            # Dibujar auras de potenciadores
            for potenciador in potenciadores:
                potenciador.draw_aura(PANTALLA)

        elif estado == 3: # Jefe
            # Aplicar efecto de temblor si está activo
            offset_x, offset_y = (0, 0)
            if len(jefe_grupo) > 0:
                jefe = jefe_grupo.sprite
                jefe_offset_x, jefe_offset_y = jefe.get_temblor_offset()
                offset_x += jefe_offset_x
                offset_y += jefe_offset_y
            
            # Aplicar efecto de temblor por daño o temblor de 30 segundos
            if tiempo_temblor > 0:
                offset_x += random.randint(-intensidad_temblor, intensidad_temblor)
                offset_y += random.randint(-intensidad_temblor, intensidad_temblor)
                tiempo_temblor -= 1
            
            # Scroll Fondo con temblor
            fondo_x -= 5
            if fondo_x <= -ANCHO: fondo_x = 0
            PANTALLA.blit(IMG_FONDO, (fondo_x + offset_x, offset_y))
            PANTALLA.blit(IMG_FONDO, (fondo_x + ANCHO + offset_x, offset_y))

            # Generar obstáculos durante la pelea con el jefe
            if random.randint(0, 100) < 3:  # Probabilidad incrementada durante jefe
                tipo_obstaculo = random.randint(1, 3)
                obstaculo = Obstaculo(tipo_obstaculo)
                all_sprites.add(obstaculo)
                obstaculos.add(obstaculo)

            all_sprites.update()
            all_sprites.draw(PANTALLA)
            
            # Dibujar auras de potenciadores
            for potenciador in potenciadores:
                potenciador.draw_aura(PANTALLA)
            
            # Dibujar escudo si está activo - SIEMPRE VISIBLE
            if jugador.escudo_activo:
                if len(escudo_grupo) == 0:
                    escudo = Escudo(jugador)
                    escudo_grupo.add(escudo)
                for escudo in escudo_grupo:
                    escudo.update()
                    escudo.draw(PANTALLA)
            else:
                escudo_grupo.empty()
            
            # Dibujar efectos especiales del jefe
            if len(jefe_grupo) > 0:
                jefe_grupo.sprite.draw_efectos(PANTALLA)
            
            # Barra vida Jefe
            if len(jefe_grupo) > 0:
                j = jefe_grupo.sprite
                porc = max(0, (j.vida / j.vida_max))
                # Dibujar barra jefe estilo arcade
                dibujar_barra_arcade(PANTALLA, ANCHO-220, 20, 200, 20, porc,
                                   (50, 50, 50), ROJO, f"BOSS: {int(porc*100)}%")

        elif estado == 4: # Winner
            PANTALLA.blit(IMG_FONDO, (0,0))
            efecto_salto += direccion_salto * 2
            if abs(efecto_salto) > 20: direccion_salto *= -1
            
            r = IMG_WINNER.get_rect(center=(ANCHO//2, ALTO//2 + efecto_salto))
            PANTALLA.blit(IMG_WINNER, r)
            
            if pygame.time.get_ticks() - tiempo_inicio_winner > 3000:  # Mostrar winner por 3 segundos
                estado = 5  # Ir a historia final
                pantalla_historia_final.reiniciar()

        elif estado == 5: # Historia Final
            detener_musica()
            musica_reproduciendose = False
            musica_pausada = False
            
            pantalla_historia_final.actualizar(dt)
            pantalla_historia_final.dibujar(PANTALLA)
            
            if pantalla_historia_final.terminada:
                # Después de la historia, mostrar resultados finales
                estado = 7

        elif estado == 6: # Game Over
            # Pausar música solo la primera vez que entramos al Game Over
            if musica_reproduciendose and not musica_pausada:
                pausar_musica()
                musica_pausada = True
            
            PANTALLA.blit(IMG_FONDO, (0,0)) 
            dibujar_game_over(PANTALLA, puntaje)
            
        elif estado == 7: # Resultados Finales
            # Preparar estadísticas
            minutos = int(tiempo_total_nivel // 60)
            segundos = int(tiempo_total_nivel % 60)
            tiempo_formateado = f"{minutos:02d}:{segundos:02d}"
            
            estadisticas = {
                'puntaje': puntaje,
                'enemigos_eliminados': enemigos_eliminados,
                'muertes': jugador.muertes,
                'monedas_gastadas': jugador.monedas_gastadas,
                'tiempo_formateado': tiempo_formateado,
                'vidas_restantes': jugador.vidas,
                'vidas_iniciales': jugador.vidas_iniciales
            }
            
            dibujar_resultados_finales(PANTALLA, estadisticas, mensaje_error_nivel3)

        # --- COLISIONES COMUNES (Estados 2 y 3) ---
        if estado in [2, 3]:
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
                    # Activar temblor de pantalla
                    tiempo_temblor = 15
                    intensidad_temblor = 4
            
            # Balas Jugador destruyen Balas Enemigas
            balas_destruidas = pygame.sprite.groupcollide(balas_jugador, balas_enemigas, True, True)
            for bala_jugador, balas_enemigas_list in balas_destruidas.items():
                # Efecto visual/sonoro opcional cuando las balas chocan
                if SND_EXPLOSION: 
                    SND_EXPLOSION.play()
                # Podrías agregar aquí un efecto de explosión pequeño
                
            # Balas Jugador -> Enemigos
            hits = pygame.sprite.groupcollide(enemigos, balas_jugador, True, True)
            for hit in hits: 
                puntaje += 1
                enemigos_eliminados += 1
                if SND_EXPLOSION: SND_EXPLOSION.play()
            
            # Balas Jugador -> Jefe
            if estado == 3 and len(jefe_grupo) > 0:
                hits_j = pygame.sprite.groupcollide(jefe_grupo, balas_jugador, False, True)
                for j in hits_j:
                    j.vida -= 1
                    if j.vida <= 0:
                        j.kill()
                        estado = 4
                        tiempo_inicio_winner = pygame.time.get_ticks()
                        balas_enemigas.empty()
                        if SND_EXPLOSION: SND_EXPLOSION.play()
                        if SND_VICTORY: SND_VICTORY.play()

            # Daño al Jugador
            # 1. Chocar con enemigo
            if pygame.sprite.spritecollide(jugador, enemigos, True):
                if jugador.recibir_dano(): 
                    if SND_EXPLOSION: SND_EXPLOSION.play()
                    # Activar temblor de pantalla
                    tiempo_temblor = 20
                    intensidad_temblor = 5
            
            # 2. Chocar con bala enemiga
            if pygame.sprite.spritecollide(jugador, balas_enemigas, True):
                if jugador.recibir_dano():
                    if SND_EXPLOSION: SND_EXPLOSION.play()
                    # Activar temblor de pantalla
                    tiempo_temblor = 15
                    intensidad_temblor = 3

            # 3. Chocar con Jefe
            if pygame.sprite.spritecollide(jugador, jefe_grupo, False):
                if jugador.recibir_dano():
                    if SND_EXPLOSION: SND_EXPLOSION.play()
                    # Activar temblor de pantalla
                    tiempo_temblor = 25
                    intensidad_temblor = 7
            
            # 4. Chocar con láser
            if estado == 3 and len(jefe_grupo) > 0:
                jefe = jefe_grupo.sprite
                for laser in jefe.lasers:
                    if not laser.creciendo and laser.temporizador < laser.duracion - 10:
                        # Crear rectángulo temporal para la colisión del láser
                        laser_rect = pygame.Rect(laser.rect.x, laser.rect.y, 
                                               laser.longitud * abs(laser.dx), 
                                               laser.longitud * abs(laser.dy))
                        if laser_rect.colliderect(jugador.rect):
                            if jugador.recibir_dano():
                                if SND_EXPLOSION: SND_EXPLOSION.play()
                                # Activar temblor de pantalla
                                tiempo_temblor = 20
                                intensidad_temblor = 6
            
            # 5. Chocar con anillos
            if estado == 3 and len(jefe_grupo) > 0:
                jefe = jefe_grupo.sprite
                for anillo in jefe.anillos:
                    distancia = math.sqrt((jugador.rect.centerx - anillo.rect.centerx)**2 + 
                                        (jugador.rect.centery - anillo.rect.centery)**2)
                    if anillo.radio - 10 < distancia < anillo.radio + 10:
                        if jugador.recibir_dano():
                            if SND_EXPLOSION: SND_EXPLOSION.play()
                            # Activar temblor de pantalla
                            tiempo_temblor = 15
                            intensidad_temblor = 4
            
            # 6. Chocar con rayos eléctricos
            if estado == 3 and len(jefe_grupo) > 0:
                jefe = jefe_grupo.sprite
                for rayo in jefe.rayos:
                    # Crear rectángulo temporal para la colisión del rayo
                    rayo_rect = pygame.Rect(rayo.rect.x, rayo.rect.y, 
                                          rayo.longitud_maxima * abs(rayo.dx), 
                                          rayo.longitud_maxima * abs(rayo.dy))
                    if rayo_rect.colliderect(jugador.rect):
                        if jugador.recibir_dano():
                            if SND_EXPLOSION: SND_EXPLOSION.play()
                            # Activar temblor de pantalla
                            tiempo_temblor = 18
                            intensidad_temblor = 5
            
            # 7. Chocar con olas de choque
            if estado == 3 and len(jefe_grupo) > 0:
                jefe = jefe_grupo.sprite
                for ola in jefe.olas:
                    distancia = math.sqrt((jugador.rect.centerx - ola.rect.centerx)**2 + 
                                        (jugador.rect.centery - ola.rect.centery)**2)
                    if distancia < ola.radio:
                        if jugador.recibir_dano():
                            if SND_EXPLOSION: SND_EXPLOSION.play()
                            # Activar temblor de pantalla
                            tiempo_temblor = 22
                            intensidad_temblor = 7
            
            # 8. Chocar con campos magnéticos
            if estado == 3 and len(jefe_grupo) > 0:
                jefe = jefe_grupo.sprite
                for campo in jefe.campos_magneticos:
                    distancia = math.sqrt((jugador.rect.centerx - campo.rect.centerx)**2 + 
                                        (jugador.rect.centery - campo.rect.centery)**2)
                    if distancia < campo.radio:
                        if jugador.recibir_dano():
                            if SND_EXPLOSION: SND_EXPLOSION.play()
                            # Activar temblor de pantalla
                            tiempo_temblor = 10
                            intensidad_temblor = 3
            
            # Verificar Muerte
            if jugador.vidas <= 0:
                estado_anterior = estado # Guardamos si estábamos en juego o jefe
                estado = 6 # Game Over
                if musica_reproduciendose and not musica_pausada:
                    pausar_musica()
                    musica_pausada = True
                if SND_GAMEOVER: SND_GAMEOVER.play()

            # HUD (Vidas y Progreso Jefe)
            dibujar_hud(PANTALLA, 10, 10, jugador.vidas, puntaje, META_PUNTAJE, jugador, tiempo_total_nivel, enemigos_eliminados)
            
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