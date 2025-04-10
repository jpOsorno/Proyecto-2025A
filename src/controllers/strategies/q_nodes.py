import time
from typing import Union
import numpy as np
from numba import njit
from multiprocessing import Pool, cpu_count
from src.middlewares.slogger import SafeLogger
from src.funcs.base import emd_efecto, ABECEDARY
from src.middlewares.profile import profiler_manager, profile
from src.funcs.format import fmt_biparte_q
from src.controllers.manager import Manager
from src.models.base.sia import SIA
from src.models.core.solution import Solution
from src.constants.models import (
    QNODES_ANALYSIS_TAG,
    QNODES_LABEL,
    QNODES_STRAREGY_TAG,
)
from src.constants.base import (
    TYPE_TAG,
    NET_LABEL,
    INFTY_NEG,
    INFTY_POS,
    LAST_IDX,
    EFECTO,
    ACTUAL,
)

def flatten(arr):
    if isinstance(arr, list):
        return [item for sublist in arr for item in flatten(sublist)] if any(isinstance(i, list) for i in arr) else arr
    return [arr]

def funcion_submodular_pura(sia_subsistema, deltas, omegas, dists_marginales):
    temporal = [[], []]
    key = (tuple(sorted(flatten(deltas))), tuple(sorted(flatten(omegas))))

    if isinstance(deltas, tuple):
        d_tiempo, d_indice = deltas
        temporal[d_tiempo].append(d_indice)
    else:
        for delta in deltas:
            d_tiempo, d_indice = delta
            temporal[d_tiempo].append(d_indice)

    dims_alcance_delta = temporal[EFECTO]
    dims_mecanismo_delta = temporal[ACTUAL]
    particion_delta = sia_subsistema.bipartir(
        np.array(dims_alcance_delta, dtype=np.int8),
        np.array(dims_mecanismo_delta, dtype=np.int8),
    )
    vector_delta_marginal = particion_delta.distribucion_marginal()
    emd_delta = emd_efecto(vector_delta_marginal, dists_marginales)

    for omega in omegas:
        if isinstance(omega, list):
            for omg in omega:
                o_tiempo, o_indice = omg
                temporal[o_tiempo].append(o_indice)
        else:
            o_tiempo, o_indice = omega
            temporal[o_tiempo].append(o_indice)

    dims_alcance_union = temporal[EFECTO]
    dims_mecanismo_union = temporal[ACTUAL]
    particion_union = sia_subsistema.bipartir(
        np.array(dims_alcance_union, dtype=np.int8),
        np.array(dims_mecanismo_union, dtype=np.int8),
    )
    vector_union_marginal = particion_union.distribucion_marginal()
    emd_union = emd_efecto(vector_union_marginal, dists_marginales)

    return key, (emd_union, emd_delta, vector_delta_marginal)

class QNodes(SIA):
    def __init__(self, gestor: Manager):
        super().__init__(gestor)
        profiler_manager.start_session(f"{NET_LABEL}{len(gestor.estado_inicial)}{gestor.pagina}")
        self.m: int
        self.n: int
        self.tiempos: tuple[np.ndarray, np.ndarray]
        self.etiquetas = [tuple(s.lower() for s in ABECEDARY), ABECEDARY]
        self.vertices: set[tuple]
        self.memoria_omega = dict()
        self.memoria_particiones = dict()
        self.indices_alcance: np.ndarray
        self.indices_mecanismo: np.ndarray
        self.logger = SafeLogger(QNODES_STRAREGY_TAG)

    #@profile(context={TYPE_TAG: QNODES_ANALYSIS_TAG})
    def aplicar_estrategia(self, condicion: str, alcance: str, mecanismo: str):
        self.sia_preparar_subsistema(condicion, alcance, mecanismo)

        futuro = tuple((EFECTO, efecto) for efecto in self.sia_subsistema.indices_ncubos)
        presente = tuple((ACTUAL, actual) for actual in self.sia_subsistema.dims_ncubos)

        self.m = self.sia_subsistema.indices_ncubos.size
        self.n = self.sia_subsistema.dims_ncubos.size

        self.indices_alcance = self.sia_subsistema.indices_ncubos
        self.indices_mecanismo = self.sia_subsistema.dims_ncubos

        self.tiempos = (
            np.zeros(self.n, dtype=np.int8),
            np.zeros(self.m, dtype=np.int8),
        )

        vertices = list(presente + futuro)
        self.vertices = set(vertices)
        mip = self.algorithm(vertices)

        fmt_mip = fmt_biparte_q(list(mip), self.nodes_complement(mip))

        return Solution(
            estrategia=QNODES_LABEL,
            perdida=self.memoria_particiones[mip][0],
            distribucion_subsistema=self.sia_dists_marginales,
            distribucion_particion=self.memoria_particiones[mip][1],
            tiempo_total=time.time() - self.sia_tiempo_inicio,
            particion=fmt_mip,
        )

    def algorithm(self, vertices: list[tuple[int, int]]):
        mejores_resultados = []
        max_inicios = min(3, len(vertices) - 1)

        for start_idx in range(max_inicios):
            omegas_origen = [vertices[start_idx]]
            deltas_origen = vertices[:start_idx] + vertices[start_idx + 1:]
            vertices_fase = vertices
            omegas_ciclo = omegas_origen[:]
            deltas_ciclo = deltas_origen[:]

            memoria_local = dict()

            total = len(vertices_fase) - 2
            for i in range(total):
                self.logger.debug(f"total: {total-i}")
                emd_particion_candidata = INFTY_POS

                best_k = -1
                best_result = (INFTY_POS, INFTY_POS, None)

                use_parallel = len(deltas_ciclo) > 50

                if use_parallel:
                    with Pool(cpu_count()) as pool:
                        results = pool.starmap(
                            funcion_submodular_pura,
                            [(self.sia_subsistema, deltas_ciclo[k], list(omegas_ciclo), self.sia_dists_marginales)
                            for k in range(len(deltas_ciclo))]
                        )
                else:
                    results = [
                        funcion_submodular_pura(self.sia_subsistema, deltas_ciclo[k], list(omegas_ciclo), self.sia_dists_marginales)
                        for k in range(len(deltas_ciclo))
                    ]

                for k, (key, (emd_union, emd_delta, dist_marginal_delta)) in enumerate(results):
                    emd_iteracion = emd_union - emd_delta
                    if emd_iteracion < best_result[0]:
                        best_result = (emd_iteracion, emd_delta, dist_marginal_delta)
                        best_k = k
                        if not use_parallel:
                            memoria_local[key] = (emd_union, emd_delta, dist_marginal_delta)
                        if emd_delta == 0:
                            mip_cero = tuple(flatten([*omegas_ciclo, deltas_ciclo[k]]))
                            self.memoria_particiones[mip_cero] = 0, dist_marginal_delta
                            return mip_cero

                omegas_ciclo.append(deltas_ciclo[best_k])
                deltas_ciclo.pop(best_k)

                if deltas_ciclo:
                    last_element = deltas_ciclo[LAST_IDX]
                    clave = tuple(flatten([last_element]))
                    self.memoria_particiones[clave] = best_result[1], best_result[2]

                    ultimo = omegas_ciclo[LAST_IDX]
                    par_candidato = [
                        ultimo if isinstance(ultimo, tuple) else tuple(ultimo),
                        last_element if isinstance(last_element, tuple) else tuple(last_element),
                    ]
                    omegas_ciclo.pop()
                    omegas_ciclo.append(par_candidato)
                    vertices_fase = omegas_ciclo[:]

            mejores_resultados.append(
                min(self.memoria_particiones.items(), key=lambda x: x[1][0])
            )

        mejor = min(mejores_resultados, key=lambda x: x[1][0])[0]
        return mejor

    def nodes_complement(self, nodes: list[tuple[int, int]]):
        return list(self.vertices - set(nodes))
