from models.strategies.force import BruteForce
from src.controllers.manager import Manager

from src.models.strategies.phi import Phi


def start_up():
    """Punto de entrada principal"""
    # ABCD #
    estado_inicio = "1000"
    condiciones = "1110"
    mechanismo = "0110"
    alcance = "1010"

    config_sistema = Manager(estado_inicial=estado_inicio)

    ### Ejemplo de solución mediante Pyphi ###

    analizador_fb = BruteForce(config_sistema)
    sia_uno = analizador_fb.aplicar_estrategia(condiciones, alcance, mechanismo)
    print(sia_uno)
