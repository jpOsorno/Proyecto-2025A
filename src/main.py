from funcs.base import generate_combinations, setup_logger, estados_binarios
from src.controllers.manager import Manager

from models.strategies.phi import Phi
from src.models.strategies.force import BruteForce
from models.strategies.q_nodes import QNodes


def start_up():
    """Punto de entrada principal"""
    #                ABCD #
    estado_inicio = "1000"
    config_sistema = Manager(estado_inicial=estado_inicio)

    # condicion, alcance, mecanismo = ("1111", "1110", "1110")  # index out or range
    condicion, alcance, mecanismo = ("1110", "1110", "1110")  # void|void
    # condicion, alcance, mecanismo = ("1111", "1000", "0000")  # index out or range

    analizador_fb = BruteForce(config_sistema)
    sia_dos = analizador_fb.aplicar_estrategia(condicion, alcance, mecanismo)
    print(sia_dos)

    analizador_fi = Phi(config_sistema)
    sia_uno = analizador_fi.aplicar_estrategia(condicion, alcance, mecanismo)
    print(sia_uno)

    analizador_fi = QNodes(config_sistema)
    sia_uno = analizador_fi.aplicar_estrategia(condicion, alcance, mecanismo)
    print(sia_uno)
    raise SystemExit

    logger = setup_logger("strat_analysis")

    ## Ejemplo de solución mediante fuerza bruta ##
    cond_purv_mech = 3
    # for metaestado in generate_final_combinations((n := len(estado_inicio)), cond_purv_mech):
    for state in estados_binarios(len(estado_inicio)):
        print(f"{state=}")
        for metastate in generate_combinations(state):
            condicion, alcance, mecanismo = metastate

            logger.debug(f"\t{metastate=}")

            try:
                # analizador_fi = Phi(config_sistema)
                # sia_uno = analizador_fi.aplicar_estrategia(
                #     condicion, alcance, mecanismo
                # )
                # print(sia_uno)

                # analizador_fb = BruteForce(config_sistema)
                # sia_dos = analizador_fb.aplicar_estrategia(
                #     condicion, alcance, mecanismo
                # )
                # print(sia_dos)

                analizador_q = QNodes(config_sistema)
                sia_tres = analizador_q.aplicar_estrategia(
                    condicion, alcance, mecanismo
                )
                print(sia_tres)
                # logger.debug(sia_tres)

            except ValueError as vex:
                # Silenciosamente ignorar ValueError
                logger.info(f"{vex}")
            except Exception as ex:
                # Loggear otros tipos de errores
                logger.debug(f"{ex}")
