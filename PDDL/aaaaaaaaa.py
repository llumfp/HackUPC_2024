import pandas as pd
import numpy as np
import random


def extraer_acciones(file_path):
    acciones = []
    aux = False
    with open(file_path, 'r') as file:
        for line in file:
            if line.strip().startswith("step"):
                aux = True
                # Encuentra el índice del primer dos puntos y toma el contenido después
            if aux:
                if not line.strip():
                    break
                partes = line.split(":", 1)
                if len(partes) > 1:
                    accion = partes[1].strip()
                    acciones.append(accion)
    return acciones

# Ejemplo de uso
acciones_extraidas = extraer_acciones("./output.txt")


def crear_sequencia(acciones_extraidas):
    resultados_step = []
    resultados_shelf = []
    
    for i in acciones_extraidas:
        action = i.split()
        if action[0] == "MOVE":
            if "CASHIER" != action[3]:
                resultados_step.append(int(action[3][4:]))
            
            else:
                resultados_step.append(0)

        if action[0] == "PICK_PRODUCT":
            resultados_shelf.append((int(action[3][5:]), int(action[4][4:])))
    
    return resultados_step, resultados_shelf
step, shelf = crear_sequencia(acciones_extraidas)

import numpy as np
import matplotlib.pyplot as plt
import imageio
import os
import numpy as np
import matplotlib.pyplot as plt
import imageio
import os

def crear_graficas(steps, n=8, m=11):
    preparacio_video = []
    # Matriz inicial
    matriz = np.zeros((n, m))
    matriz[0, 0] = 1
    matriz[0, 4:9] = 2
    matriz[3, 4:9] = 2
    matriz[4, 4:9] = 2
    matriz[7, 4:9] = 2
    matriz[1, 4:9] = 3
    matriz[2, 4:9] = 3
    matriz[5, 4:9] = 3
    matriz[6, 4:9] = 3

    preparacio_video.append(matriz.copy())  # Utilizamos .copy() para evitar modificar la matriz original

    indice_estanteria = 1  # Inicializar el índice de la primera estantería

    # Iterar sobre cada paso
    for paso in steps:
        fila = paso // m  # Calcular la fila usando división entera
        columna = paso % m  # Calcular la columna usando el módulo
        matriz_temporal = matriz.copy()  # Copiar la matriz original para mantenerla inmutable
        if matriz_temporal[fila, columna] == 2:
            matriz_temporal[fila, columna] = indice_estanteria  # Asignar el índice único a la estantería
            indice_estanteria += 1  # Incrementar el índice para la siguiente estantería
        else:
            matriz_temporal[fila, columna] = 4  # Actualizar la celda a 4 si es el camino
        preparacio_video.append(matriz_temporal)

    return preparacio_video

def generar_gif(preparacio_video, nombre_archivo='evolucion_mercado.gif'):
    imagenes = []
    for matriz in preparacio_video:
        # Crear la figura y el gráfico
        fig, ax = plt.subplots()
        ax.imshow(matriz, cmap='viridis')

        # Añadir números a las estanterías
        for i in range(matriz.shape[0]):
            for j in range(matriz.shape[1]):
                if matriz[i, j] != 0:
                    ax.text(j, i, int(matriz[i, j]), ha='center', va='center', color='white')

        ax.set_title('Evolución del mercado')
        ax.set_xticks([])
        ax.set_yticks([])

        # Guardar la figura como una imagen
        imagen_archivo = 'temp.png'
        plt.savefig(imagen_archivo)
        imagenes.append(imageio.imread(imagen_archivo))
        plt.close()
        # Eliminar la imagen temporal
        os.remove(imagen_archivo)

    # Crear el GIF
    imageio.mimsave(nombre_archivo, imagenes, duration=0.5)




preparacion_video = crear_graficas(step)

# Generar el GIF
generar_gif(preparacion_video)

