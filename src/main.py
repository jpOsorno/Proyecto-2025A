from src.controllers.manager  import Manager

from src.models.strategies.force import BruteForce


def start_up():
    """Punto de entrada principal"""
    # ABCD #
    estado_inicio = "10001111"
    condiciones =   "11101111"
    alcance =       "11101111"
    mechanismo =    "11101111"

    config_sistema = Manager(estado_inicial=estado_inicio)

    ### Ejemplo de solución mediante módulo de pyphi ###

    analizador_fb = BruteForce(config_sistema)
    sia_uno = analizador_fb.aplicar_estrategia(condiciones, alcance, mechanismo)
    print(sia_uno)