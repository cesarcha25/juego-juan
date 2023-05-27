import pygame
import random

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
ancho_pantalla = 600
alto_pantalla = 600
pantalla = pygame.display.set_mode((ancho_pantalla, alto_pantalla))
pygame.display.set_caption("Juego de Nave - Niveles de dificultad")

# Colores
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)

# Nave
ancho_nave = 50
alto_nave = 50
posicion_nave_x = ancho_pantalla // 2 - ancho_nave // 2
posicion_nave_y = alto_pantalla - alto_nave - 20
velocidad_nave = 5

# Proyectil
ancho_proyectil = 25
alto_proyectil = 10
posicion_proyectil_x = 0
posicion_proyectil_y = 0
velocidad_proyectil = 15
estado_proyectil = "listo"

# Enemigos
ancho_enemigo = 50
alto_enemigo = 50
posicion_enemigo_x = random.randint(0, ancho_pantalla - ancho_enemigo)
posicion_enemigo_y = 0
velocidad_enemigo = 3

# Puntuación
puntuacion = 0
fuente = pygame.font.Font(None, 36)

# Niveles de dificultad
niveles = [
    {"velocidad_obstaculos": 3, "velocidad_enemigos": 3, "fondo": "nivel1.png"},
    {"velocidad_obstaculos": 5, "velocidad_enemigos": 5, "fondo": "nivel2.png"},
    {"velocidad_obstaculos": 6, "velocidad_enemigos": 6, "fondo": "nivel3.png"}
]
nivel_actual = 0
texto_nivel = fuente.render("Nivel: " + str(nivel_actual + 1), True, ROJO)

# Cargar fondos de juego
fondos = []
for nivel in niveles:
    fondo = pygame.image.load(nivel["fondo"]).convert()
    fondo = pygame.transform.scale(fondo, (ancho_pantalla, alto_pantalla))
    fondos.append(fondo)

# Función para dibujar la nave
def dibujar_nave(x, y):
    pygame.draw.rect(pantalla, AZUL, (x, y, ancho_nave, alto_nave))

# Función para disparar un proyectil
def disparar_proyectil(x, y):
    global estado_proyectil
    estado_proyectil = "disparo"
    pygame.draw.rect(pantalla, ROJO, (x + ancho_nave // 2, y, ancho_proyectil, alto_proyectil))

# Función para verificar colisiones
def verificar_colision(enemigo_x, enemigo_y, proyectil_x, proyectil_y):
    if (
        proyectil_y < enemigo_y + alto_enemigo
        and proyectil_y + alto_proyectil > enemigo_y
        and proyectil_x < enemigo_x + ancho_enemigo
        and proyectil_x + ancho_proyectil > enemigo_x
    ):
        return True
    return False

# Bucle principal del juego
corriendo = True
reloj = pygame.time.Clock()

while corriendo:
    # Manejo de eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE and estado_proyectil == "listo":
                posicion_proyectil_x = posicion_nave_x
                posicion_proyectil_y = posicion_nave_y
                disparar_proyectil(posicion_proyectil_x, posicion_proyectil_y)

    # Movimiento de la nave
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT] and posicion_nave_x > 0:
        posicion_nave_x -= velocidad_nave
    if teclas[pygame.K_RIGHT] and posicion_nave_x < ancho_pantalla - ancho_nave:
        posicion_nave_x += velocidad_nave

    # Movimiento del proyectil
    if estado_proyectil == "disparo":
        posicion_proyectil_y -= velocidad_proyectil
        if posicion_proyectil_y <= 0:
            estado_proyectil = "listo"

    # Movimiento del enemigo
    posicion_enemigo_y += niveles[nivel_actual]["velocidad_enemigos"]
    if posicion_enemigo_y > alto_pantalla:
        posicion_enemigo_x = random.randint(0, ancho_pantalla - ancho_enemigo)
        posicion_enemigo_y = 0
        if estado_proyectil == "listo":
            puntuacion -= 1

    # Verificar colisión con el enemigo
    if verificar_colision(posicion_enemigo_x, posicion_enemigo_y, posicion_proyectil_x, posicion_proyectil_y):
        posicion_enemigo_x = random.randint(0, ancho_pantalla - ancho_enemigo)
        posicion_enemigo_y = 0
        puntuacion += 1
        estado_proyectil = "listo"
        velocidad_enemigo *= 0.7  # Disminuir la velocidad del enemigo en un 30%

    # Verificar si se alcanzó el límite de puntos para pasar al siguiente nivel o finalizar el juego
    if puntuacion >= 60:
        corriendo = False
    elif puntuacion >= 40 and nivel_actual < len(niveles) - 1:
        nivel_actual = 2
        texto_nivel = fuente.render("Nivel: " + str(nivel_actual + 1), True, ROJO)
    elif puntuacion >= 30 and nivel_actual < len(niveles) - 1:
        nivel_actual = 1
        texto_nivel = fuente.render("Nivel: " + str(nivel_actual + 1), True, ROJO)

    # Dibujar en la pantalla
    pantalla.blit(fondos[nivel_actual], (0, 0))
    dibujar_nave(posicion_nave_x, posicion_nave_y)
    if estado_proyectil == "disparo":
        disparar_proyectil(posicion_proyectil_x, posicion_proyectil_y)
    pygame.draw.rect(pantalla, ROJO, (posicion_enemigo_x, posicion_enemigo_y, ancho_enemigo, alto_enemigo))
    pantalla.blit(texto_nivel, (10, 10))

    # Mostrar puntuación en la pantalla
    texto_puntuacion = fuente.render("Puntuación: " + str(puntuacion), True, ROJO)
    pantalla.blit(texto_puntuacion, (10, 50))

    # Actualizar la pantalla
    pygame.display.flip()

    # Controlar la velocidad del juego
    reloj.tick(60)

# Terminar Pygame
pygame.quit()
