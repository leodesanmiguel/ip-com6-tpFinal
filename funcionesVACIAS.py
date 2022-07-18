from principal import *
from configuracion import *
from silabeo import *
import random
import math



def lectura(archivo, salida):
    ## recorrer el archivo y cargar las palabras en salida
    ## ---- lee el archivo y lo carga en la lista salida, no hace falta que
    ## ---- devuelva una lista sino que lo carga en la lista que recibe como
    ## ---- segundo parÆmetro

    if archivo.readable():  # validar que sea solo de lectura
        for linea in archivo:

            salida.append(linea.rstrip('\n'))

    # Cierra el archivo
    archivo.close()

    #Retornar con el archivo de salida



def nuevaPalabra(lista):
    ## se obtiene un valor random del tamaño de la lista
    ## se elije la palabra y retorna la misma
    ##    aqui se puede validar y hacer que nunca mas se repita
    ##    por ejemplo asinandole un "" a la lista en la posición elegida.
    ##    luego cuando se elige una nueva palabra, verificar que no sea "".
    ##          En ese caso se vuelva a elegir
    ## ---- debe recibir una lista de palabras y devuelve una de ellas elegida
    ## ---- al azar.

    if len(lista)>1:
        return lista[random.randint(1,len(lista))]
    else:
        print("***** >>>> La lista está vacía.")
        sys.exit()


def silabasTOpalabra(silaba):
    ## Hay que recorrer el string y sacarle los caracteres de separación
    ## Retorna una cadena con la palabra completa.
    ## ---- recibe una palabra separada en silabas y devuelve la
    ## ---- palabra sin "
    nvaPalabra = ""
    for c in silaba:
        if c != " " or c != "  " or c != "-":
            nvaPalabra += c

    return nvaPalabra



def palabraTOsilaba(palabra):
    ## recibe la plabra y separa la misma en silabas
    ## Debe retornar la palabra en silabas
    ## ---- Es una función que separa en silabas, hasta ahora usa unas
    ## ---- funciones realizadas por los docentes.

    palabraSilabada=""
    silabas = syllabize(palabra)
    # utiliza la función syllabize ......
    for sil in silabas:
        palabraSilabada += sil + '-'
    
    return palabraSilabada[0:-1]



def esCorrecta(palabraEnSilabasEnPantalla, palabra):
    ## recibe las palabras 1) La elegida por azar
    ##                     2) la escrita por el usuario
    ## Si son iguales para eso usa la conversión de silabas To palabra
    ##               dira TRUE
    ## ---- debe recibir la palabra de la pantalla ya separa en sílabas y
    ## ---- controlar que sea la misma que escribió el usuarix.
    ## ---- Cuidado que el usuarix puede usar espacios
    ## ---- o "-" para separar en sílabas.

    return silabasTOpalabra(palabraEnSilabasEnPantalla) == palabra



def puntaje(palabra):
    ## ----  debe recibir una palabra y devolver el puntaje que corresponde.
    return 5

