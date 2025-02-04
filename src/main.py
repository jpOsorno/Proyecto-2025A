from models.base.manager import Manager

from src.models.logic.force import BruteForce


def start_up():
    """Punto de entrada principal"""

    estado_inicio = "1000"
    sys_config = Manager(estado_inicial=estado_inicio)

    ### Ejemplo de solución mediante fuerza bruta ###

    bf_analyzer = BruteForce(sys_config)
    bf_analyzer.analizar_completamente_una_red()
