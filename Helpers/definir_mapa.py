import pandas as pd
import numpy as np


# Lee el archivo CSV
df = pd.read_csv('products.csv', sep=';')

# Añade una columna llamada "cantidad" con valores aleatorios entre 0 y 10
df['cantidad'] = np.random.randint(0, 11, size=len(df))


# Ordena el DataFrame por la columna "name"
df = df.sort_values(by='name')

# Define el número de divisiones
n = 20

# Calcula el número de elementos por división
division_size = len(df) // n

# Crea una lista con el número de estanterías para cada fila
estanteria = [i // division_size for i in range(len(df))]

# Añade la columna "estanteria" al DataFrame
df['estanteria'] = estanteria

pd.set_option('display.max_rows', None)


df.to_csv("data_final.csv")