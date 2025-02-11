from src.controllers.strategies.phi import Phi
from src.controllers.manager import Manager

from src.controllers.strategies.force import BruteForce


def iniciar():
    """Punto de entrada principal"""
                   # ABCD #
    estado_inicio = "10000000"
    condiciones =   "11111111"
    alcance =       "10101010"
    mecanismo =     "11111111"

    config_sistema = Manager(estado_inicial=estado_inicio)

    ### Ejemplo de solución mediante módulo de fuerza bruta ###
    analizador_fb = Phi(config_sistema)
    sia_uno = analizador_fb.aplicar_estrategia(condiciones, alcance, mecanismo)
    print(sia_uno)
