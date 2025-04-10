from src.controllers.manager import Manager

from src.controllers.strategies.force import BruteForce
from src.controllers.strategies.q_nodes import QNodes


def iniciar():
    """Punto de entrada principal"""
                    # ABCDEFGHIJ #
    # estado_inicial = "1000000000"
    # condiciones =    "1111111111"
    # alcance =        "1111111111"
    # mecanismo =      "1111111111"

    estado_inicial = "100000000000000"
    condiciones =    "111111111111111"
    alcance =        "111111111111111"
    mecanismo =      "111111111111111"

    # estado_inicial = "10000000000000000000"
    # condiciones =    "11111111111111111111"
    # alcance =        "11111111111111111111"
    # mecanismo =      "11111111111111111110"

    gestor_sistema = Manager(estado_inicial)

    ### Ejemplo de solución mediante módulo de fuerza bruta ###
    analizador_fb = QNodes(gestor_sistema)
    sia_uno = analizador_fb.aplicar_estrategia(
        condiciones,
        alcance,
        mecanismo,
    )
    print(sia_uno)
