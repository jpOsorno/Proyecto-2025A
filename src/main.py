from src.controllers.manager  import Manager

from src.models.strategies.force import  BruteForce


def start_up():
    """Punto de entrada principal"""
                   # ABCD #
    estado_inicio = "0000000000"
    condiciones =   "1110111111"
    mechanismo =    "0110111111"
    alcance =       "1010111111"

    config_sistema = Manager(estado_inicial=estado_inicio)

    ### Ejemplo de solución mediante  ###

    analizador_fi = BruteForce(config_sistema)
    sia_dos = analizador_fi.aplicar_estrategia(condiciones, alcance, mechanismo)
    print(sia_dos)
