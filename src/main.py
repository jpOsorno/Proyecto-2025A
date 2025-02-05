from models.strategies.phi import Phi
from models.strategies.q_nodes import QNodes
from src.controllers.manager import Manager

from src.models.strategies.force import BruteForce


def start_up():
    """Punto de entrada principal"""
    #                ABCD #
    estado_inicio = "1000"
    config_sistema = Manager(estado_inicial=estado_inicio)

    ## Ejemplo de solución mediante fuerza bruta ##

    analizador_fb = QNodes(config_sistema)
    resultado = analizador_fb.aplicar_estrategia(
        "1111",
        "0111",
        "1000",
    )

    print(resultado)
