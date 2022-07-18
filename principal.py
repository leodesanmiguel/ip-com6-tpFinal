#! /usr/bin/env python
import os, random, sys, math
import pygame

from pygame.locals import *
from configuracion import *
from extras import *
from funcionesSeparador import *

from funcionesVACIAS import *

# *********************
# Funcion principal
def main():
        #--> Centrar la ventana y despues inicializar pygame
        os.environ["SDL_VIDEO_CENTERED"] = "1"
        pygame.init()
        #pygame.mixer.init()

        #--> Preparar la ventana
        pygame.display.set_caption("El juego del Mago Goma...")
        screen = pygame.display.set_mode((ANCHO, ALTO))

        #--> tiempo total del juego
        gameClock = pygame.time.Clock()
        totaltime = 0
        segundos = TIEMPO_MAX
        fps = FPS_inicial

        puntos = 0
        palabra = ""
        lemarioEnSilabas=[]
        listaPalabrasDiccionario=[]

        archivo= open("lemario.txt","r", encoding="latin-1")

        ## ------------------------
        ## lectura del diccionario
        ##
        lectura(archivo, listaPalabrasDiccionario)

        ## ------------------------
        ## elige una al azar
        ##       Esta es la primera vez que lo hace
        ##       luego volvera a llamar a nuevaPalabra dentro del ciclo.
        palabraEnPantalla=nuevaPalabra(listaPalabrasDiccionario)

        ## ------------------------
        palabraEnPantallaAnterior=""
        dibujar(screen, palabra, palabraEnPantalla, puntos,segundos)

        while segundos > fps/1000:
        # 1 frame cada 1/fps segundos
            gameClock.tick(fps)
            totaltime += gameClock.get_time()

            if True:
            	fps = 2

            #Buscar la tecla apretada del modulo de eventos de pygame
            for e in pygame.event.get():

                #QUIT es apretar la X en la ventana
                if e.type == QUIT:
                    pygame.quit()
                    return()

                #Ver si fue apretada alguna tecla
                if e.type == KEYDOWN:
                    letra = dameLetraApretada(e.key)
                    palabra += letra #es la palabra que escribe el usuario
                    if e.key == K_BACKSPACE:
                        ## borrar una letra escrita
                        palabra = palabra[0:len(palabra)-1]
                        ##
                        ##  Solo cuando presiona ENTER
                        ##       avanza con la verificaciÃ³n de la palabra
                    if e.key == K_RETURN:
                        ## -------------------------------------
                        ##      entonces pasa la palabra a silabas
                        ##      convierte la palabra en silabas

                        palabraEnPantallaEnSilabas=palabraTOsilaba(palabraEnPantalla)

                        ##
                        ## -------------------------------------
                        ## Verifica que sea correcta la separaciÃ³n.
                        if esCorrecta(palabraEnPantallaEnSilabas, palabra):
                            ##  Si es correcta entonces suma 5 puntos
                            puntos += 5
                        else:
                            ##  Si NO es correcta entonces RESTA 1 puntos
                            puntos -= 1


                        ## ------------------------
                        ## vuelve a eligir una palabra al azar
                        palabraEnPantalla=nuevaPalabra(listaPalabrasDiccionario)

                        ##  Esta palabra es la que almacena lo cargado por teclado
                        ##  queda limpia para la nueva carga
                        palabra = ""

            segundos = TIEMPO_MAX - pygame.time.get_ticks()/1000

            #Limpiar pantalla anterior
            screen.fill(COLOR_FONDO)

            #Dibujar de nuevo todo
            dibujar(screen, palabra, palabraEnPantalla, puntos , segundos)

            pygame.display.flip()

        while 1:
            #Esperar el QUIT del usuario
            for e in pygame.event.get():
                if e.type == QUIT:
                    pygame.quit()
                    return

        archivo.close()

# _______________________________
# *******************************
# Programa Principal ejecuta Main
if __name__ == "__main__":
    main()
