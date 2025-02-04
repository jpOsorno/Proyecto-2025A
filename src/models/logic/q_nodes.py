import numpy as np
from src.funcs.base import emd_efecto, setup_logger, ABECEDARY
from src.funcs.format import fmt_biparte_q, fmt_parte_q
from src.middlewares.slogger import get_logger
from src.models.base.loader import Loader
from src.models.base.sia import SIA

from src.models.core.solution import Solution
from src.constants.base import (
    ACTIVOS,
    EFECTO,
    ACTUAL,
    INT_ONE,
    LAST_IDX,
    NEQ_SYM,
)


class QNodes(SIA):
    """
    Clase QNodes para el análisis de redes mediante el algoritmo Q.

    Esta clase implementa un gestor principal para el análisis de redes que utiliza
    el algoritmo Q para encontrar la partición óptima que minimiza la
    pérdida de información en el sistema. Hereda de la clase base SIA (Sistema de
    Información Activo) y proporciona funcionalidades para analizar la estructura
    y dinámica de la red.

    Args:
    ----
        config (Loader):
            Instancia de la clase Loader que contiene la configuración del sistema
            y los parámetros necesarios para el análisis.

    Attributes:
    ----------
        m (int):
            Número de elementos en el conjunto de purview (vista).

        n (int):
            Número de elementos en el conjunto de mecanismos.

        times (tuple[np.ndarray, np.ndarray]):
            Tupla de dos arrays que representan los tiempos para los estados
            actual y efecto del sistema.

        labels (list[tuple]):
            Lista de tuplas conteniendo las etiquetas para los nodos,
            con versiones en minúsculas y mayúsculas del abecedario.

        vertices (set[tuple]):
            Conjunto de vértices que representan los nodos de la red,
            donde cada vértice es una tupla (tiempo, índice).

        memory (dict):
            Diccionario para almacenar resultados intermedios y finales
            del análisis (memoización).

        logger:
            Instancia del logger configurada para el análisis Q.

    Methods:
    -------
        run(conditions, purview, mechanism):
            Ejecuta el análisis principal de la red con las condiciones,
            purview y mecanismo especificados.

        algorithm(vertices):
            Implementa el algoritmo Q para encontrar la partición
            óptima del sistema.

        funcion_submodular(deltas, omegas):
            Calcula la función submodular para evaluar particiones candidatas.

        view_solution(mip):
            Visualiza la solución encontrada en términos de las particiones
            y sus valores asociados.

        nodes_complement(nodes):
            Obtiene el complemento de un conjunto de nodos respecto a todos
            los vértices del sistema.

    Notes:
    -----
    - La clase implementa una versión secuencial del algoritmo Q
      para encontrar la partición que minimiza la pérdida de información.
    - Utiliza memoización para evitar recálculos innecesarios durante el proceso.
    - El análisis se realiza considerando dos tiempos: actual (presente) y
      efecto (futuro).
    - La implementación soporta paralelización tanto en CPU como en GPU
      a través de las optimizaciones de TensorFlow.
    """

    def __init__(self, config: Loader):
        super().__init__(config)
        self.m: int
        self.n: int
        self.times: tuple[np.ndarray, np.ndarray]
        self.labels = [tuple(s.lower() for s in ABECEDARY), ABECEDARY]
        self.vertices: set[tuple]
        self.memory = dict()

        self.logger = get_logger("q_analysis")

    # @profile(context={"type": "Q_analysis"})
    def run(self, conditions, purview, mechansim):
        self.sia_preparar_subsistema(conditions, purview, mechansim)

        # Pondremos el orden (tiempo, indice) con tiempo=1 el futuro, tiempo=0 el presente.
        purv = tuple((EFECTO, pur) for pur in self.sia_subsistema.indices_ncubos)
        mech = tuple((ACTUAL, mec) for mec in self.sia_subsistema.dims_ncubos)

        self.m = len(self.sia_subsistema.indices_ncubos)
        self.n = len(self.sia_subsistema.dims_ncubos)
        self.times = (np.zeros(self.n, dtype=np.int8), np.zeros(self.m, dtype=np.int8))

        vertices = list(mech + purv)
        self.vertices = set(mech + purv)
        mip = self.algorithm(vertices)

        # self.view_solution(mip)
        return (self.memory[mip],)

        # Solution(
        #     )

    def algorithm(self, vertices: list[tuple[int, int]]):
        # Acá puse como una macrológica antes de empezar a implementar #
        #    vertices, self.m, self.n)
        # tomar el elemento inicial para omegas
        # Paralelizar inicialmente en CPU luego en GPU
        # tensorflow hace uso de paralelizaciones en base a la arquitectura del ordenador
        # memoria + tiempo + htop
        # iterar por cada elemento en deltas
        #   Función que itere sobre los deltas restantes y retorne el mínimo. El detalle sobre este método es que (obviando memoización) omega

        # generar la particion tanto en delta individual como en omegas

        # el valor de los tensor y emd se resta entre estos y se genera una emd_delta

        # tras iterar todos los deltas escogemos el mínimo y lo añadimos a omegas

        # tras que omegas sea del tamaño vertices - 1 paramos y tomamos el último elemento en omegas y deltas para agruparlo en vertices

        # repetimos el mismo algoritmo teniendo este grupo (llamaremos a los pares candidatos grupos candidatos porque en nada dejan de ser pares y tienen más de 2 elementos, je)

        # Acá en adelante sí empecé a implementar la lógica.

        omegas_origen = np.array([vertices[0]])
        deltas_origen = np.array(vertices[1:])

        vertices_fase = vertices

        omegas_ciclo = omegas_origen
        deltas_ciclo = deltas_origen
        self.logger.debug(omegas_ciclo, deltas_ciclo)

        particiones_candidatas = []

        # Se iteran dos veces menos obviando las iteraciones donde no hay particiones y cuando quedarían seleccionados todas las particiones.
        for i in range(len(vertices_fase) - 2):
            self.logger.warn(f"\n{'≡' * 50}{i=}")
            self.logger.debug(
                f"FASE con nuevo grupo formado (si i{NEQ_SYM}0):\n\t{vertices_fase}"
            )

            # asignar de nivel anterior a elementos de omegas
            omegas_ciclo = [vertices_fase[0]]
            deltas_ciclo = vertices_fase[1:]

            self.logger.debug(f"fase inicia con W: {omegas_ciclo}")

            for j in range(len(deltas_ciclo) - 1):
                self.logger.warn(f"\n{'='*45}{j=}")
                self.logger.debug(f"CICLO W crece: {omegas_ciclo}")

                # selección primer elemento de vertices

                minimal_emd = 1e5
                iter_mip: tuple[int, int] | list[tuple[int, int]]
                index_mip: int
                for k in range(len(deltas_ciclo)):
                    self.logger.warn(f"\n{'-'*40}{k=}")
                    self.logger.debug("ITER calculando cada delta")
                    iter_emd = self.funcion_submodular(deltas_ciclo[k], omegas_ciclo)
                    self.logger.debug(f"local: {iter_emd}, global: {minimal_emd}")
                    if iter_emd < minimal_emd:
                        minimal_emd = iter_emd
                        iter_mip = deltas_ciclo[k]
                        index_mip = k
                    ...

                omegas_ciclo.append(deltas_ciclo[index_mip])
                self.logger.debug(
                    f"\nCICLO Minimo delta hallado:\n\t{deltas_ciclo[index_mip]=}"
                )
                self.logger.debug("\tAñadir a ciclo omega. Quitándolo de deltas.")
                deltas_ciclo.pop(index_mip)

                print(f"{iter_mip=}")
                ...

            # El detalle es que estas uniones de la ultima y penultima parte se encuentran de la memoización en la generación de las particiones individuales, puesto en algún punto se va a evaluar un delta que será la unión de estos dos en la siguiente iteración.
            # #    penultimo_mip, penultima_emd)

            self.logger.debug("Añadir nueva partición entre ultimos de omega y delta")
            self.logger.debug(f"{omegas_ciclo, deltas_ciclo}")

            if i == 0:
                # Añadimos la primera partición, un único elemento
                particiones_candidatas.append(deltas_ciclo)

            last_pair = (
                [omegas_ciclo[LAST_IDX]]
                if isinstance(omegas_ciclo[LAST_IDX], tuple)
                else omegas_ciclo[LAST_IDX]
            ) + (
                deltas_ciclo[LAST_IDX]
                if isinstance(deltas_ciclo[LAST_IDX], list)
                else deltas_ciclo  # adición de los dos últimos elementos en uno sólo.
            )
            particiones_candidatas.append(last_pair)

            self.logger.debug(last_pair)

            omegas_ciclo.pop()  # quitar el último elemento pues está en el par
            omegas_ciclo.append(last_pair)

            # vertices_fase # cambiarlos y ponerles con el nuevo grupo formado, así cuando vuelva a la fase se repetirá todo igual pero con el grupo en cuenta
            vertices_fase = omegas_ciclo
            ...

        self.logger.warn(
            f"\nGrupos partición obtenidos durante ejecucion:\n{(particiones_candidatas)=}"
        )
        # Esta parte no debería existir u optimizarse pues ya deben estar guardados en memoria
        for particion in particiones_candidatas:
            times = np.copy(self.times)
            for p in particion:
                p_time, p_index = p
                times[p_time][p_index] = ACTIVOS
            subsys = self.sia_subsistema
            biparticion = subsys.bipartir(times[EFECTO], times[ACTUAL])
            vector = biparticion.distribucion_marginal()
            emd_particion = emd_efecto(vector, self.sia_dists_marginales)

            self.memory[tuple(particion)] = emd_particion

        return min(self.memory, key=lambda k: self.memory[k])
        ...

    def funcion_submodular(
        self, deltas: tuple | list[tuple], omegas: list[tuple | list[tuple]]
    ):
        # Acá lo que se hace es a partir de los elementos que estén en el conjunto omega (W) y delta se creen en esencia, las particiones.
        times = np.copy(self.times)

        self.logger.debug(f"{deltas=}")

        # creamos la partición del individual
        if isinstance(deltas, tuple):
            d_time, d_index = deltas
            times[d_time][d_index] = ACTIVOS
        else:
            for delta in deltas:
                d_time, d_index = delta
                times[d_time][d_index] = ACTIVOS

        individual = self.sia_subsistema

        self.logger.info(f"{times[EFECTO], times[ACTUAL]=}")

        dims_efecto_ind = tuple(
            idx for idx, bit in enumerate(times[EFECTO]) if bit == INT_ONE
        )
        dims_presente_ind = tuple(
            idx for idx, bit in enumerate(times[ACTUAL]) if bit == INT_ONE
        )

        ind_part = individual.bipartir(
            np.array(dims_efecto_ind, dtype=np.int8),
            np.array(dims_presente_ind, dtype=np.int8),
        )
        indivector_marginal = ind_part.distribucion_marginal()
        individual_emd = emd_efecto(indivector_marginal, self.sia_dists_marginales)

        self.logger.debug(f"{self.sia_dists_marginales=}")
        self.logger.debug(f"{indivector_marginal=}")

        # memoizamos el individuo

        self.logger.info("ind_part")
        self.logger.info(f"{ind_part}")

        # Luego lo hacemos para los omegas
        for omega in omegas:
            if isinstance(omega, list):
                for omg in omega:
                    o_time, o_index = omg
                    times[o_time][o_index] = ACTIVOS
            else:
                o_time, o_index = omega
                times[o_time][o_index] = ACTIVOS

        combinacion = self.sia_subsistema

        dims_efecto_comb = tuple(
            idx for idx, bit in enumerate(times[EFECTO]) if bit == INT_ONE
        )
        dims_presente_comb = tuple(
            idx for idx, bit in enumerate(times[ACTUAL]) if bit == INT_ONE
        )

        comb_part = combinacion.bipartir(
            np.array(dims_efecto_comb, dtype=np.int8),
            np.array(dims_presente_comb, dtype=np.int8),
        )
        comvector_marginal = comb_part.distribucion_marginal()
        combinada_emd = emd_efecto(comvector_marginal, self.sia_dists_marginales)

        self.logger.debug(f"{omegas=}")

        self.logger.info(f"{times[EFECTO], times[ACTUAL]=}")
        self.logger.info("comb_part")
        self.logger.info(f"{comb_part}")

        self.logger.debug(f"{self.sia_dists_marginales=}")
        self.logger.debug(f"{comvector_marginal=}")

        self.logger.debug(
            f"{combinada_emd - individual_emd}={combinada_emd}-{individual_emd}"
        )

        return combinada_emd - individual_emd

    def view_solution(self, mip: tuple[tuple[int, int]]):
        times = ([], [])
        complement = self.vertices - set(mip)
        for part_prim in mip:
            time, index = part_prim
            letter = self.labels[time][index]
            # ponemos en la parte primal (1)
            times[0].append(letter)

        for part_dual in complement:
            time, index = part_dual
            letter = self.labels[time][index]
            # ponemos en la parte dual (1)
            times[1].append(letter)

        # self.logger.debug(f"{times, self.memory[mip]=}")
        # self.logger.debug(f"{mip=}")
        biparticion_fmt = fmt_biparte_q(times[0], times[1])
        return biparticion_fmt
        # print(f"{mip=}")

    def nodes_complement(self, nodes: list[tuple[int, int]]):
        return list(set(self.vertices) - set(nodes))


""" 
Planteamiento de formar los pares/grupos-candidatos no con listas sino con matriz de adyacencia?
  0  1  2
0[x][ ][x]
1[x][ ][x]
2[x][ ][x]
"""
