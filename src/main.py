from src.controllers.manager import Manager

from src.controllers.strategies.q_nodes import QNodes


def iniciar():
    """Punto de entrada principal"""
                    # ABCD #
    estado_inicial = "1000"
    condiciones =    "1111"
    alcance =        "1111"
    mecanismo =      "1111"

    gestor_sistema = Manager(estado_inicial)

    ### Ejemplo de solución mediante módulo de fuerza bruta ###
    analizador_fb = QNodes(gestor_sistema)
    sia_uno = analizador_fb.aplicar_estrategia(
        condiciones,
        alcance,
        mecanismo,
    )
    print(sia_uno)
