from models.base.manager import Manager

from src.models.logic.force import BruteForce


def start_up():
    """Punto de entrada principal"""

    estado_inicio = "1000"
    condiciones__ = "1000"
    alcance______ = "1110"
    mechanismo___ = "1110"

    sys_config = Manager(estado_inicial=estado_inicio)

    ### Ejemplo de solución mediante fuerza bruta ###

    analizador_fb = BruteForce(sys_config)
    sia_uno = analizador_fb.aplicar_estrategia(condiciones__, alcance______, mechanismo___)
    print(sia_uno)
    
