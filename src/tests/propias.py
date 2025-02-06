import numpy as np
import pandas as pd


def generar_subarreglos(arr):
    return [
        arr,  # 1. Todo el arreglo original
        arr[:-1],  # 2. Excluir el último elemento
        arr[1:],  # 3. Excluir el primer elemento
        arr[1:-1],  # 4. Excluir los extremos
        arr[::2],  # 5. Tomar los elementos en posiciones pares
        arr[1::2],  # 6. Tomar los elementos en posiciones impares
        np.delete(
            arr, np.arange(2, len(arr), 3)
        ),  # 7. Omitir los múltiplos de 3 (índices)
    ]


num_nodos = 20
variables = range(num_nodos)

pruebas = []
pruebas_literales = []


for futuro in generar_subarreglos(variables):
    conjunto = []
    futuro = set(futuro)
    for presente in generar_subarreglos(variables):
        presente = set(presente)
        alcance_bin = "".join(["1" if j in futuro else "0" for j in variables])
        mecanismo_bin = "".join(["1" if i in presente else "0" for i in variables])
        alcance = "".join([chr(j + 65) for j in variables if j in futuro]) + "_{t+1}"
        mecanismo = "".join([chr(i + 65) for i in variables if i in presente]) + "_{t}"
        conjunto.append((alcance_bin, mecanismo_bin))
        pruebas_literales.append(f"{alcance}|{mecanismo}")

    pruebas.append(conjunto)

for conjunto in pruebas:
    print(f"{conjunto=}")


# print(f"{pruebas_literales=}")


# Crear un DataFrame
df = pd.DataFrame({"Pruebas": pruebas_literales})

# Guardar en un archivo Excel
df.to_excel(".tests/pruebas.xlsx", index=False)
