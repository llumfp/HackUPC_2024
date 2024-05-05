import subprocess
import re
import pandas as pd
import numpy as np
import random

df = pd.read_csv('../data_final.csv')

def ejecutar_programa(nombre_archivo):
    comando = f".\metricff -o domain_basic.pddl -f problem-extensio-final.pddl -O > output.txt"

    # Ejecutar el comando y capturar la salida
    proceso = subprocess.Popen(comando, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, shell=True, universal_newlines=True)
    salida, error = proceso.communicate()

    if error:
        print("Error al ejecutar el comando:", error)
        return None

    # Imprimir toda la salida para depuración
    print("Salida del comando:\n", salida)

    # Usar expresiones regulares para encontrar el tiempo total
    match = re.search(r'(\d+\.\d+) seconds total time', salida)
    if match:
        tiempo_total = match.group(1)
        print(f"Tiempo total: {tiempo_total} segundos")
        return tiempo_total
    else:
        print("No se encontró el tiempo total")
        return None

def generate_adjacencies(rows, cols):

    ncells = rows*cols
    adjacencies = []
    for i in range(1, ncells+1):
        if i % cols != 0:
            adjacencies.append((i, i+1))
        if i <= ncells-cols:
            adjacencies.append((i, i+cols))
    
    more_adj = adjacencies.copy()
    for i, j in adjacencies:
        more_adj.append((j, i))

    special_numbers = [
        4, 5, 6, 7, 8,
        34, 35, 36, 37, 38,
        44, 45, 46, 47, 48,
        74, 75, 76, 77, 78
    ]

    filtered_adj = []

    for i, j in more_adj:
        if i not in special_numbers and j not in special_numbers:
            filtered_adj.append((i, j))

    return filtered_adj

def generate_adjacency_strings(adjacencies):
    adjacency_strings = ""
    for adj in adjacencies:
        # Crea un string para cada tupla con el formato especificado
        description = f"        (adjacent cell{adj[0]} cell{adj[1]}) \n"
        adjacency_strings += description

    return adjacency_strings

acces = """        (acces_to cell14 shelf1)
        (acces_to cell15 shelf2)
        (acces_to cell16 shelf3)
        (acces_to cell17 shelf4)
        (acces_to cell18 shelf5)
        (acces_to cell24 shelf6)
        (acces_to cell25 shelf7)
        (acces_to cell26 shelf8)
        (acces_to cell27 shelf9)
        (acces_to cell28 shelf10)
        (acces_to cell54 shelf11)
        (acces_to cell55 shelf12)
        (acces_to cell56 shelf13)
        (acces_to cell57 shelf14)
        (acces_to cell58 shelf15)
        (acces_to cell64 shelf16)
        (acces_to cell65 shelf17)
        (acces_to cell66 shelf18)
        (acces_to cell67 shelf19)
        (acces_to cell68 shelf20)
"""

def generar_caso(lista_tuplas: list, lista_estanterias: list, celads: str, adjacencia: str, acces: str, hold: list, cela_inici: str = "cashier"):  # hold valors que entren
    # Contenido específico del archivo Python
    content = "(define (problem store_problem) ; Nombre del problema.\n"

    # domain
    content += "    (:domain seidor) ; Nombre del dominio al que se asocia este problema.\n"

    # objects
    content += "    (:objects\n"

    content += "        person1 - person\n"
    content += "        cashier - cash\n"

    content += "        "
    for i in lista_estanterias:
        content += f"shelf{i} "
    content += "- shelving"

    content += "\n        "
    for i in lista_tuplas:
        content += f"prod{i[0]} "
    content += "- product"

    content += "\n        "
    for i in celads:
        content += f"cell{i} "

    content += "- aisle"

    content += "    )\n"

    # init
    content += "    (:init\n"
    content += f"        (in person1 {cela_inici})\n"
    content += "        (= (total_meters) 0)\n"

    # content += cela_inici
    content += "        (adjacent cashier cell1)\n"
    content += "        (adjacent cell1 cashier)\n"
    content += adjacencia

    content += acces

    for tupla in lista_tuplas:
        # Concatenar al string content el formato especificado
        content += f"        (inside prod{tupla[0]} shelf{tupla[1]})\n"

    content += "        )\n"

    # goal:
    content += "    (:goal\n"
    content += "        (and\n"
    content += "            (in person1 cashier)\n"

    for i in hold:
        content += f"            (holding prod{i})\n"

    content += ")))"

    file_name = f"problem-extensio-final.pddl"

    with open(file_name, 'w') as file:
        file.write(content)

    return file_name, content


if __name__ == '__main__':

    lista_tuplas = [(fila["id"], fila["estanteria"])
                    for indice, fila in df.iterrows()]

    lista_estanterias = df["estanteria"].unique().tolist()
    lista_productes = df["id"].unique().tolist()

    # Define el rango completo de valores
    full_range = list(range(1, 81))

    # Define los rangos a excluir
    exclude_ranges = [range(4, 9), range(34, 39), range(44, 49), range(74, 79)]

    # Crea una lista que excluya los rangos especificados
    cells = [x for x in full_range if all(x not in exclude_range for exclude_range in exclude_ranges)]


    # Calculando el 5% de los elementos de la lista
    num_elementos = round(len(lista_productes) * 0.05)

    # Seleccionando aleatoriamente el 5% de los elementos
    elementos_seleccionados = random.sample(lista_productes, num_elementos)

    # Usamos un tablero de 8x10
    filtered_adjacencies_list = generate_adjacencies(8, 10)
    filtered_adjacencies_list = generate_adjacency_strings(filtered_adjacencies_list)

    file_name, content = generar_caso(lista_tuplas, lista_estanterias, cells, filtered_adjacencies_list, acces, elementos_seleccionados)
    print(f"NOMBRE DEL ARCHIVO: '{file_name}'\nCONTENIDO: \n {content}")

    ejecutar_programa(file_name)
