
import json
import requests
import pandas as pd
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_community.chat_models import ChatOpenAI
import json
import os

import subprocess
import re
import pandas as pd
import numpy as np
import random

from dotenv import load_dotenv

load_dotenv()
openai_api_key  = os.getenv('OPENAI_API_KEY')

df = pd.read_csv('../data_final.csv')

def ejecutar_programa(nombre_archivo):
    comando = f".\PDDL\metricff.exe -o PDDL\domain_basic.pddl -f PDDL\problem.pddl -O > PDDL\output.txt"

    # Ejecutar el comando y capturar la salida
    proceso = subprocess.Popen(comando, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, shell=True, universal_newlines=True)
    salida, error = proceso.communicate()

    if error:
        print("Error al ejecutar el comando:", error)
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

    file_name = f"./PDDL/problem.pddl"

    with open(file_name, 'w') as file:
        file.write(content)

    return file_name, content

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

def guidance(lst:list):
        
    prompt_template = """Hey Chat! Given the list of tuples I'll provide, give me a step-by-step explanation in natural language of which section I should go to (first element of the tuple) and which product I need to pick up (second element of the tuple).

    The list is as follows:

    {lst}

    Finally, add a message indicating the user to go to the cashier.

    ANSWER:"""
    prompt = PromptTemplate(template=prompt_template, input_variables=["lst"])

    try:
        llm = ChatOpenAI(temperature=0,openai_api_key=openai_api_key,model_name="gpt-3.5-turbo-0613")
        initial_chain = LLMChain(llm=llm, prompt=prompt, output_key="output",verbose=True)
        result = (initial_chain.run({
                    'lst': lst,
                    }))
        return result
    except Exception as e:
        print(f"Error while calling OpenAI API {e}")

def read_json(file='./Files/product_list.json'):
    with open(file,'r') as f:
        data = json.load(f)
    return data


def planning_function(optimize = True):
    ids = list(dict(read_json()).keys())
    print(ids)

    lista_tuplas = [(fila["id"], fila["estanteria"])
                    for indice, fila in df.iterrows()]

    lista_estanterias = df["estanteria"].unique().tolist()
    lista_productes = df["id"].unique().tolist()
    full_range = list(range(1, 81))
    exclude_ranges = [range(4, 9), range(34, 39), range(44, 49), range(74, 79)]
    cells = [x for x in full_range if all(x not in exclude_range for exclude_range in exclude_ranges)]

    # Usamos un tablero de 8x10
    filtered_adjacencies_list = generate_adjacencies(8, 10)
    filtered_adjacencies_list = generate_adjacency_strings(filtered_adjacencies_list)

    file_name, content = generar_caso(lista_tuplas, lista_estanterias, cells, filtered_adjacencies_list, acces, ids)
    print(f"NOMBRE DEL ARCHIVO: '{file_name}'\nCONTENIDO: \n {content}")

    ejecutar_programa(file_name)

    acciones_extraidas = extraer_acciones("./output.txt")
    print(acciones_extraidas)
    step, shelf = crear_sequencia(acciones_extraidas)
    return guidance(shelf)


planning_function()


 
