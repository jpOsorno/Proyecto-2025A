from src.controllers.manager import Manager

from src.models.logic.force import BruteForce
from models.logic.q_nodes import QNodes
from models.logic.phi import Phi


def start_up():
    """Punto de entrada principal"""
    #                ABCD #
    estado_inicio = "10000"
    config_sistema = Manager(estado_inicial=estado_inicio)

    ## Ejemplo de solución mediante fuerza bruta ##

    condiciones = "10000"
    alcances = "10000"
    mecanismos = "10000"

    # analizador_fb = Phi(config_sistema)
    # print(analizador_fb.aplicar_estrategia(condiciones, alcances, mecanismos))

    analizador_fb = BruteForce(config_sistema)
    print(analizador_fb.aplicar_estrategia(condiciones, alcances, mecanismos))

    # analizador_fb = QNodes(config_sistema)
    # print(analizador_fb.aplicar_estrategia(condiciones, alcances, mecanismos))
