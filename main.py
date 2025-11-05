import pygame
import random
import json
import sys
import io
import cairosvg

# Estado inicial
pygame.init()

ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Banderitas")

# Colores
GRIS = (200, 200, 200)
NEGRO = (0, 0, 0)
AZUL = (30, 144, 255)
BLANCO = (255, 255, 255)
ROJO = (200, 50, 50)
VERDE = (0, 150, 0)

# Fuentes de texto
fuente = pygame.font.SysFont("arial", 32)
fuente_pequena = pygame.font.SysFont("arial", 24)

#Cargar banderas/nombres

with open("data/flags.json", "r", encoding="utf-8") as f:
    paises = json.load(f)

lista_paises = list(paises.keys())
TOTAL_PAISES = len(lista_paises)

#Funciones

def mostrar_texto(texto, x, y, color=NEGRO, fuente_obj=fuente):
    superficie = fuente_obj.render(texto, True, color)
    pantalla.blit(superficie, (x, y))

def cargar_bandera_svg(ruta_svg, ancho=300, alto=200):
    """Convierte SVG a PNG en memoria y lo escala a tamaño uniforme"""
    try:
        png_bytes = cairosvg.svg2png(url=ruta_svg, output_width=ancho, output_height=alto)
        imagen = pygame.image.load(io.BytesIO(png_bytes))
        return imagen
    except Exception as e:
        print(f"Error cargando {ruta_svg}: {e}")
        superficie = pygame.Surface((ancho, alto))
        superficie.fill(pygame.color.azure3)
        return superficie

def nueva_pregunta():
    pais = random.choice(lista_paises)
    ruta = paises[pais]
    bandera = cargar_bandera_svg(ruta)
    return pais, bandera

def acabar_partida(final_time, aciertos):
    done = False
    while not done:
        pantalla.fill(GRIS)

        infoRect = pygame.Rect(0, 0, ANCHO, 50)
        pygame.draw.rect(pantalla, AZUL, infoRect, border_radius=8)

        mostrar_texto(f"Tiempo final: {final_time}", 10, 10, NEGRO)

        mostrar_texto(f"Aciertos: {aciertos}", ANCHO / 2.5, 10, NEGRO)

        mostrar_texto(f"Para jugar otra vez pulsa ENTER", ANCHO / 2.5, 300, NEGRO)
        mostrar_texto(f"Para salir pulsa ESC", ANCHO / 2.5, 400, NEGRO)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                print(event)
                if event.key == pygame.K_RETURN:
                    done = True

                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        
        pygame.display.update()
    juego()

def juego():

    #Variables
    aciertos = 0
    NUM_INTENTOS = 3
    intentos = NUM_INTENTOS
    intento = ""
    mensaje = ""
    color_mensaje = NEGRO
    pais_correcto, bandera = nueva_pregunta()
    timer_text = ""

    done = False
    tiempo_inicio = pygame.time.get_ticks()

    while not done:
        pantalla.fill(GRIS)

        infoRect = pygame.Rect(0, 0, ANCHO, 50)
        pygame.draw.rect(pantalla, AZUL, infoRect, border_radius=8)

        # Mostrar bandera
        pantalla.blit(bandera, (ANCHO//2 - 150, 100))

        # Mostrar contador arriba a la izquierda
        mostrar_texto(f"{aciertos}/{TOTAL_PAISES}", 10, 10, NEGRO)

        # Calcular tiempo transcurrido
        ms_transcurridos = pygame.time.get_ticks() - tiempo_inicio
        segundos = ms_transcurridos // 1000
        minutos = segundos // 60
        seg = segundos % 60
        timer_text = f"{minutos:02d}:{seg:02d}"

        mostrar_texto(timer_text, ANCHO - 100, 10, NEGRO)

        text_intentos = f"Intentos: {intentos}"
        mostrar_texto(text_intentos, ANCHO / 2.5, 10, NEGRO)

        # Dibujar cajón de texto visible
        input_rect = pygame.Rect(190, 390, 420, 50)
        pygame.draw.rect(pantalla, BLANCO, input_rect, border_radius=20)
        pygame.draw.rect(pantalla, AZUL, input_rect, 3, border_radius=20)
        mostrar_texto(intento, 200, 400, NEGRO)

        # Mostrar mensaje de resultado
        mostrar_texto(mensaje, 200, 470, color_mensaje, fuente_pequena)

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if intento.strip().lower() == pais_correcto.lower():
                        aciertos += 1
                        mensaje = "¡Correcto!"
                        color_mensaje = VERDE
                        pais_correcto, bandera = nueva_pregunta()
                        intentos = NUM_INTENTOS
                        if aciertos >= TOTAL_PAISES:
                            done = True
                    else:
                        mensaje = f"Incorrect"
                        color_mensaje = ROJO
                        intentos -= 1

                    intento = ""

                    # Comprobamos si alcanzamos el total
                    if intentos <= 0:
                        mensaje = f"Era {pais_correcto}"
                        pais_correcto, bandera = nueva_pregunta()
                        intentos = NUM_INTENTOS

                elif event.key == pygame.K_BACKSPACE:
                    intento = intento[:-1]
                elif event.unicode.isalpha() or event.unicode in " -'":
                    intento += event.unicode
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
    acabar_partida(timer_text, aciertos)

juego()
