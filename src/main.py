from src.models.base.loader import Loader
from src.middlewares.profile import profiler_manager

from src.models.logic.phi import Phi
from src.models.logic.force import BruteForce
from src.models.logic.q_nodes import QNodes


def start_up():
    """Punto de entrada principal"""
    profiler_manager.enabled = True

    #                ABCDEFGHIJ...
    estado_inicio = "1000"
    condiciones__ = "1110"
    alcance______ = "1110"
    mechanismo___ = "1110"

    sys_config = Loader(
        estado_inicial=estado_inicio,
    )
    ### Ejemplo de solución mediante módulo de pyphi ###

    # pyphi_analyzer = Phi(sys_config)
    # sia_uno = pyphi_analyzer.run(condiciones__, alcance______, mechanismo___)
    # print(sia_uno)

    ### Ejemplo de solución mediante fuerza bruta ###

    # bf_analyzer = BruteForce(sys_config)
    # sia_dos = bf_analyzer.run(condiciones__, alcance______, mechanismo___)
    # print(sia_dos)
    # bf_analyzer.analizar_completamente_una_red()

    q_analyzer = QNodes(sys_config)
    sia_tres = q_analyzer.run(condiciones__, alcance______, mechanismo___)
    print(sia_tres)
