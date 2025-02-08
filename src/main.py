from src.controllers.manager import Manager

from src.models.strategies.force import BruteForce


def start_up():
    """Punto de entrada principal"""
    # ABCD #
    estado_inicio = "100011"
    condiciones = "111011"
    alcance = "111011"
    mechanismo = "111011"

    config_sistema = Manager(estado_inicial=estado_inicio)

    ### Ejemplo de solución mediante módulo de pyphi ###

    analizador_fb = BruteForce(config_sistema)
    sia_uno = analizador_fb.aplicar_estrategia(condiciones, alcance, mechanismo)
    print(sia_uno)
