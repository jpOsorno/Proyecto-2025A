from funcs.base import setup_logger
from models.strategies.q_nodes import QNodes
from src.controllers.manager import Manager
import time

from testing.data import NUM_NODOS, PRUEBAS, RED_10
from testing.funcs import cargar_resultados_existentes, guardar_resultados


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

            inicio_tiempo = time.time()
            solucion = analizador_q.aplicar_estrategia(condiciones, alcance, mecanismo)
            tiempo_ejecucion = time.time() - inicio_tiempo

            soluciones[prueba] = (
                solucion.perdida,
                tiempo_ejecucion,
            )  # Guardar en memoria

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
