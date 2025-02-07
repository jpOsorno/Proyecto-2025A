import pandas as pd
import os
from funcs.base import setup_logger
from models.strategies.phi import Phi
from src.controllers.manager import Manager
from models.strategies.q_nodes import QNodes
from tests.pruebas import NUM_NODOS, PRUEBAS, RED_10

# Nombre del archivo #
FILE_NAME = "src/tests/resultados.xlsx"


def cargar_resultados_existentes():
    """Carga los resultados ya guardados en el archivo para evitar repetir cálculos."""
    if os.path.exists(FILE_NAME):
        df = pd.read_excel(FILE_NAME)
        return {
            (row["Alcance"], row["Mecanismo"]): row["Solución"]
            for _, row in df.iterrows()
        }
    return {}


def guardar_resultados(soluciones):
    """Guarda los resultados en un archivo Excel sin sobrescribir datos previos."""
    df = pd.DataFrame(
        [
            (alcance, mecanismo, solucion)
            for (alcance, mecanismo), solucion in soluciones.items()
        ],
        columns=["Alcance", "Mecanismo", "Solución"],
    )
    df.to_excel(FILE_NAME, index=False)


def start_up():
    """Punto de entrada principal"""

    red_usada = RED_10
    muestras: list[list[tuple[str, str]]] = red_usada[PRUEBAS]
    num_nodos: int = red_usada[NUM_NODOS]

    estado_inicio = f"1{'0' * (num_nodos - 1)}"
    condiciones = "1" * num_nodos

    config_sistema = Manager(estado_inicial=estado_inicio)
    soluciones = cargar_resultados_existentes()  # Cargar resultados previos

    logger = setup_logger("q_strat")
    for lote in muestras:
        for prueba in lote:
            if prueba in soluciones:
                continue  # Si ya está guardado, lo saltamos

            alcance, mecanismo = prueba
            analizador_q = QNodes(config_sistema)

            solucion = analizador_q.aplicar_estrategia(condiciones, alcance, mecanismo)
            soluciones[prueba] = solucion.perdida  # Guardar en memoria

            # Guardar inmediatamente para minimizar pérdida en caso de crash
            guardar_resultados(soluciones)
        break  # Eliminarlo cuando estés listo para ejecutar todo

    logger.debug(f"{soluciones=}")


# condicion, alcance, mecanismo = ("1111", "1110", "1110")  # index out or range
# condicion, alcance, mecanismo = ("1110", "1110", "1110")  # void|void
# condicion, alcance, mecanismo = ("1111", "1000", "0000")  # index out or range

# analizador_fb = BruteForce(config_sistema)
# sia_dos = analizador_fb.aplicar_estrategia(condicion, alcance, mecanismo)
# print(sia_dos)

# analizador_fi = Phi(config_sistema)
# sia_uno = analizador_fi.aplicar_estrategia(condicion, alcance, mecanismo)
# print(sia_uno)

# analizador_fi = QNodes(config_sistema)
# sia_uno = analizador_fi.aplicar_estrategia(condicion, alcance, mecanismo)
# print(sia_uno)
# raise     SystemExit

# logger = setup_logger("strat_analysis")

# ## Ejemplo de solución mediante fuerza bruta ##
# cond_purv_mech = 3
# # for metaestado in generate_final_combinations((n := len(estado_inicio)), cond_purv_mech):
# for state in estados_binarios(len(estado_inicio)):
#     print(f"{state=}")
#     for metastate in generate_combinations(state):
#         condicion, alcance, mecanismo = metastate

#         logger.debug(f"\t{metastate=}")

#         # try:
#         analizador_fi = Phi(config_sistema)
#         sia_uno = analizador_fi.aplicar_estrategia(condicion, alcance, mecanismo)
#         print(sia_uno)

#         analizador_fb = BruteForce(config_sistema)
#         sia_dos = analizador_fb.aplicar_estrategia(condicion, alcance, mecanismo)
#         print(sia_dos)

#         analizador_q = QNodes(config_sistema)
#         sia_tres = analizador_q.aplicar_estrategia(condicion, alcance, mecanismo)
#         print(sia_tres)
#         # logger.debug(sia_tres)

#         # except ValueError as vex:
#         #     # Silenciosamente ignorar ValueError
#         #     logger.info(f"{vex}")
#         # except Exception as ex:
#         #     # Loggear otros tipos de errores
#         #     logger.debug(f"{ex}")
