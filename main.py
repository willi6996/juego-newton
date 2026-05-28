import pygame
import sys
import math

pygame.init()

ANCHO, ALTO = 1000, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego de las Leyes de Newton - Datos Reales")

reloj = pygame.time.Clock()

BLANCO = (255, 255, 255)
NEGRO = (15, 15, 20)
AZUL = (50, 150, 255)
ROJO = (255, 80, 80)
VERDE = (80, 220, 120)
AMARILLO = (255, 220, 80)
GRIS = (90, 90, 90)
NARANJA = (255, 150, 40)
MORADO = (160, 80, 255)

fuente = pygame.font.SysFont("arial", 22)
fuente_grande = pygame.font.SysFont("arial", 34)
fuente_titulo = pygame.font.SysFont("arial", 44)

estado = "menu"

# Escala real
ESCALA = 50          # 50 pixeles = 1 metro
GRAVEDAD = 9.8      # m/s²
SUELO_Y = 390

# Segunda ley
masa = 5
fuerza = 20
velocidad = 0
pos_x = 100
pos_y = 390
tiempo = 0
distancia = 0

# Primera ley
carro_x = 430
altura_metros = 3
carro_y = SUELO_Y - altura_metros * ESCALA
plataforma_x = 360
plataforma_golpeada = False
carro_cayendo = False
velocidad_caida = 0
velocidad_impacto = 0
tiempo_caida = 0

# Tercera ley
pausado = False
fuerza_accion = 30
masa_cohete = 5
velocidad_cohete = 0
cohete_x = 100
cohete_y = 380

def escribir(texto, x, y, color=BLANCO, grande=False, titulo=False):
    if titulo:
        render = fuente_titulo.render(texto, True, color)
    elif grande:
        render = fuente_grande.render(texto, True, color)
    else:
        render = fuente.render(texto, True, color)
    pantalla.blit(render, (x, y))

def boton(texto, x, y, w, h, color):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    rect = pygame.Rect(x, y, w, h)

    pygame.draw.rect(pantalla, color, rect, border_radius=12)

    if rect.collidepoint(mouse):
        pygame.draw.rect(pantalla, BLANCO, rect, 3, border_radius=12)
        if click[0]:
            return True

    texto_render = fuente.render(texto, True, NEGRO)
    pantalla.blit(texto_render, (x + 20, y + 15))
    return False

def dibujar_carrito(x, y):
    pygame.draw.rect(pantalla, AZUL, (x, y, 120, 50), border_radius=8)
    pygame.draw.circle(pantalla, NEGRO, (int(x + 25), int(y + 55)), 16)
    pygame.draw.circle(pantalla, NEGRO, (int(x + 95), int(y + 55)), 16)
    pygame.draw.circle(pantalla, BLANCO, (int(x + 25), int(y + 55)), 7)
    pygame.draw.circle(pantalla, BLANCO, (int(x + 95), int(y + 55)), 7)

def dibujar_suelo():
    pygame.draw.rect(pantalla, GRIS, (0, 460, ANCHO, 25))

def reiniciar():
    global velocidad, pos_x, tiempo, distancia
    global carro_y, plataforma_x, plataforma_golpeada
    global carro_cayendo, velocidad_caida, velocidad_impacto, tiempo_caida
    global pausado, velocidad_cohete, cohete_x

    velocidad = 0
    pos_x = 100
    tiempo = 0
    distancia = 0

    carro_y = SUELO_Y - altura_metros * ESCALA
    plataforma_x = 360
    plataforma_golpeada = False
    carro_cayendo = False
    velocidad_caida = 0
    velocidad_impacto = 0
    tiempo_caida = 0

    pausado = False
    velocidad_cohete = 0
    cohete_x = 100

def cambiar_estado(nuevo_estado):
    global estado
    estado = nuevo_estado
    reiniciar()

def menu():
    pantalla.fill(NEGRO)

    escribir("JUEGO DE LAS LEYES DE NEWTON", 170, 60, AMARILLO, titulo=True)
    escribir("Selecciona una ley para simularla", 335, 130)

    if boton("1. Primera Ley: Inercia + gravedad real", 310, 200, 420, 60, VERDE):
        cambiar_estado("ley1")

    if boton("2. Segunda Ley: F = m x a", 310, 290, 420, 60, AZUL):
        cambiar_estado("ley2")

    if boton("3. Tercera Ley: Acción y reacción", 310, 380, 420, 60, ROJO):
        cambiar_estado("ley3")

    escribir("Teclas: 1, 2, 3", 420, 500)

def ley1(dt):
    global plataforma_x, plataforma_golpeada, carro_cayendo
    global carro_y, velocidad_caida, velocidad_impacto
    global masa, altura_metros, tiempo_caida

    pantalla.fill(NEGRO)
    dibujar_suelo()

    escribir("PRIMERA LEY: INERCIA CON GRAVEDAD REAL", 160, 35, AMARILLO, grande=True)
    escribir("ESPACIO = golpear | ↑/↓ = altura en metros | ←/→ = cambiar masa", 100, 85)

    peso = masa * GRAVEDAD

    pygame.draw.rect(pantalla, MORADO, (plataforma_x, carro_y + 70, 280, 25), border_radius=8)
    dibujar_carrito(carro_x, carro_y)

    if plataforma_golpeada and plataforma_x < ANCHO:
        plataforma_x += 14

    if plataforma_golpeada:
        carro_cayendo = True

    if carro_cayendo and carro_y < SUELO_Y:
        velocidad_caida += GRAVEDAD * dt
        carro_y += velocidad_caida * ESCALA * dt
        tiempo_caida += dt

    if carro_y >= SUELO_Y:
        carro_y = SUELO_Y
        if velocidad_impacto == 0:
            velocidad_impacto = velocidad_caida
        velocidad_caida = 0

    velocidad_teorica = math.sqrt(2 * GRAVEDAD * altura_metros)

    pygame.draw.rect(pantalla, (30, 30, 40), (600, 125, 380, 335), border_radius=12)
    escribir("Resultados reales", 625, 145, AMARILLO, grande=True)
    escribir(f"Masa del vehículo: {masa} kg", 625, 195)
    escribir(f"Peso: {peso:.2f} N", 625, 225)
    escribir(f"Altura: {altura_metros:.2f} m", 625, 255)
    escribir(f"Gravedad: {GRAVEDAD} m/s²", 625, 285)
    escribir(f"Velocidad de caída: {velocidad_caida:.2f} m/s", 625, 315)
    escribir(f"Tiempo de caída: {tiempo_caida:.2f} s", 625, 345)
    escribir(f"Velocidad teórica: {velocidad_teorica:.2f} m/s", 625, 375)

    if carro_y >= SUELO_Y and plataforma_golpeada:
        escribir(f"Impactó el suelo a: {velocidad_impacto:.2f} m/s", 625, 410, VERDE)
    else:
        escribir("Aún no toca el suelo.", 625, 410)

    escribir("Nota: la masa cambia el peso, pero no cambia la aceleración de caída.", 60, 505)
    escribir("En caída libre, todos los objetos caen con 9.8 m/s² si no hay resistencia del aire.", 60, 535)

def ley2(dt):
    global velocidad, pos_x, tiempo, distancia, fuerza, masa

    pantalla.fill(NEGRO)
    dibujar_suelo()

    escribir("SEGUNDA LEY: FUERZA = MASA x ACELERACIÓN", 150, 35, AMARILLO, grande=True)
    escribir("Cambia fuerza y masa para observar los resultados.", 260, 85)

    aceleracion = fuerza / masa

    velocidad += aceleracion * dt
    pos_x += velocidad * ESCALA * dt
    tiempo += dt
    distancia = (pos_x - 100) / ESCALA

    if pos_x > ANCHO:
        pos_x = -120

    dibujar_carrito(pos_x, pos_y)

    pygame.draw.rect(pantalla, (30, 30, 40), (630, 145, 330, 270), border_radius=12)
    escribir("Resultados", 650, 165, AMARILLO, grande=True)
    escribir(f"Masa: {masa} kg", 650, 215)
    escribir(f"Fuerza: {fuerza} N", 650, 245)
    escribir("Aceleración = F / m", 650, 275)
    escribir(f"Aceleración = {aceleracion:.2f} m/s²", 650, 305, VERDE)
    escribir(f"Velocidad: {velocidad:.2f} m/s", 650, 335)
    escribir(f"Distancia: {distancia:.2f} m", 650, 365)

    escribir("Flecha arriba/abajo: cambiar fuerza", 40, 510)
    escribir("Flecha derecha/izquierda: cambiar masa", 40, 540)

def ley3(dt):
    global velocidad_cohete, cohete_x, fuerza_accion, masa_cohete

    pantalla.fill(NEGRO)
    dibujar_suelo()

    escribir("TERCERA LEY: ACCIÓN Y REACCIÓN", 230, 35, AMARILLO, grande=True)
    escribir("P = pausar | Arriba/abajo = acción | Derecha/izquierda = masa", 160, 85)

    aceleracion = fuerza_accion / masa_cohete
    fuerza_reaccion = -fuerza_accion
    peso = masa_cohete * GRAVEDAD

    if not pausado:
        velocidad_cohete += aceleracion * dt
        cohete_x += velocidad_cohete * ESCALA * dt

    if cohete_x > ANCHO:
        cohete_x = -150

    pygame.draw.polygon(pantalla, NARANJA, [
        (cohete_x, cohete_y + 25),
        (cohete_x - 90, cohete_y),
        (cohete_x - 90, cohete_y + 50)
    ])

    pygame.draw.rect(pantalla, ROJO, (cohete_x, cohete_y, 150, 50), border_radius=20)
    pygame.draw.circle(pantalla, AZUL, (int(cohete_x + 110), cohete_y + 25), 15)

    pygame.draw.rect(pantalla, (30, 30, 40), (610, 140, 360, 300), border_radius=12)
    escribir("Resultados", 635, 160, AMARILLO, grande=True)
    escribir(f"Fuerza de acción: {fuerza_accion} N", 635, 210)
    escribir(f"Fuerza de reacción: {fuerza_reaccion} N", 635, 240)
    escribir(f"Masa del vehículo: {masa_cohete} kg", 635, 270)
    escribir(f"Peso: {peso:.2f} N", 635, 300)
    escribir(f"Aceleración: {aceleracion:.2f} m/s²", 635, 330, VERDE)
    escribir(f"Velocidad: {velocidad_cohete:.2f} m/s", 635, 360)

    if pausado:
        escribir("PAUSADO", 430, 170, ROJO, grande=True)

    escribir("Si aumenta la masa, acelera menos. Si aumenta la acción, acelera más.", 70, 535)

while True:
    dt = reloj.tick(60) / 1000

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_1:
                cambiar_estado("ley1")
            if evento.key == pygame.K_2:
                cambiar_estado("ley2")
            if evento.key == pygame.K_3:
                cambiar_estado("ley3")
            if evento.key == pygame.K_m:
                cambiar_estado("menu")
            if evento.key == pygame.K_r:
                reiniciar()

            if estado == "ley1":
                if evento.key == pygame.K_SPACE:
                    plataforma_golpeada = True

                if not plataforma_golpeada:
                    if evento.key == pygame.K_RIGHT:
                        masa += 1

                    if evento.key == pygame.K_LEFT:
                        masa -= 1
                        if masa < 1:
                            masa = 1

                    if evento.key == pygame.K_UP:
                        altura_metros += 0.5
                        if altura_metros > 5:
                            altura_metros = 5
                        carro_y = SUELO_Y - altura_metros * ESCALA

                    if evento.key == pygame.K_DOWN:
                        altura_metros -= 0.5
                        if altura_metros < 0.5:
                            altura_metros = 0.5
                        carro_y = SUELO_Y - altura_metros * ESCALA

            if estado == "ley2":
                if evento.key == pygame.K_UP:
                    fuerza += 5

                if evento.key == pygame.K_DOWN:
                    fuerza -= 5
                    if fuerza < 0:
                        fuerza = 0

                if evento.key == pygame.K_RIGHT:
                    masa += 1

                if evento.key == pygame.K_LEFT:
                    masa -= 1
                    if masa < 1:
                        masa = 1

            if estado == "ley3":
                if evento.key == pygame.K_p:
                    pausado = not pausado

                if evento.key == pygame.K_UP:
                    fuerza_accion += 5

                if evento.key == pygame.K_DOWN:
                    fuerza_accion -= 5
                    if fuerza_accion < 0:
                        fuerza_accion = 0

                if evento.key == pygame.K_RIGHT:
                    masa_cohete += 1

                if evento.key == pygame.K_LEFT:
                    masa_cohete -= 1
                    if masa_cohete < 1:
                        masa_cohete = 1

    if estado == "menu":
        menu()
    elif estado == "ley1":
        ley1(dt)
    elif estado == "ley2":
        ley2(dt)
    elif estado == "ley3":
        ley3(dt)

    pygame.display.update()