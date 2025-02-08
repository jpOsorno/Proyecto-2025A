from src.controllers.manager  import Manager

from src.models.strategies.force import BruteForce


def start_up():
    """Punto de entrada principal"""
                   # ABCD #
    estado_inicio = "1000"
    config_sistema = Manager(estado_inicial=estado_inicio)

    ## Ejemplo de solución mediante fuerza bruta ##

    analizador_fb = BruteForce(config_sistema)
    analizador_fb.analizar_completamente_una_red()