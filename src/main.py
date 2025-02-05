from controllers.manager import Manager

from src.models.logic.q_nodes import QNodes


def start_up():
    """Punto de entrada principal"""
    # ABCD #
    estado_inicio = "1000"
    condiciones = "1110"
    alcance = "1110"
    mechanismo = "1110"

    sys_config = Manager(estado_inicial=estado_inicio)

    ### Ejemplo de solución mediante módulo de pyphi ###

    analizador_q = QNodes(sys_config)
    sia_uno = analizador_q.aplicar_estrategia(condiciones, alcance, mechanismo)
    print(sia_uno)
