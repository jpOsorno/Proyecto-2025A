from models.logic.phi import Phi
from models.logic.q_nodes import QNodes
from src.controllers.manager import Manager

from src.models.logic.force import BruteForce


def start_up():
    """Punto de entrada principal"""
    #                ABCD #
    estado_inicio = "10000"
    config_sistema = Manager(estado_inicial=estado_inicio)

    ## Ejemplo de solución mediante fuerza bruta ##

    analizador_fb = Phi(config_sistema)
    print(analizador_fb.aplicar_estrategia("11111", "01101", "10110"))

    analizador_fb = BruteForce(config_sistema)
    print(analizador_fb.aplicar_estrategia("11111", "01101", "10110"))

    analizador_fb = QNodes(config_sistema)
    print(analizador_fb.aplicar_estrategia("11111", "01101", "10110"))
