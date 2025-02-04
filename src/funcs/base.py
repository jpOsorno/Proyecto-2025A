import logging
from datetime import datetime
from pathlib import Path

import numpy as np
from numpy.typing import NDArray
from pyemd import emd

from src.constants.base import INT_ZERO
from src.models.enums.distance import MetricDistance
from src.models.enums.notation import Notation

from src.models.base.aplication import aplicacion


# @cache
def get_labels(n: int) -> tuple[str, ...]:
    def get_excel_column(n: int) -> str:
        if n <= 0:
            return ""
        return get_excel_column((n - 1) // 26) + chr((n - 1) % 26 + ord("A"))

    return tuple([get_excel_column(i) for i in range(1, n + 1)])


ABECEDARY = get_labels(40)
LOWER_ABECEDARY = [letter.lower() for letter in ABECEDARY]


def literales(remaining_vars: NDArray[np.int8], lower: bool = False):
    return (
        "".join(ABECEDARY[i].lower() if lower else ABECEDARY[i] for i in remaining_vars)
        if remaining_vars.size
        else "∅"
    )


def seleccionar_metrica(distancia_usada: str):
    distancias_metricas = {
        MetricDistance.EMD_EFECTO.value: emd_efecto,
        MetricDistance.EMD_CAUSA.value: emd_causal,
        # ...otras
    }
    return distancias_metricas[distancia_usada]


def emd_efecto(u: NDArray[np.float32], v: NDArray[np.float32]) -> float:
    """
    Solución analítica de la Earth Mover's Distance basada en variables independientes condicionalmente.
    Sean X_1, X_2 dos variables aleatorias con su correspondiente espacio de estados. Si X_1 y X_2 son independientes y u_1, v_1 dos distribuciones de probabilidad en X_1 y u_2, v_2 dos distribuciones de probabilidad en X_2.

    Args:
        u (NDArray[np.float32]): Histograma/distribución/vector/serie donde cada indice asocia un valor de pobabilidad de tener el nodo en estado OFF.
        v (NDArray[np.float32]): Histograma/distribución/vector/serie donde cada indice asocia un valor de pobabilidad de tener el nodo en estado OFF.

    Returns:
        float: La EMD entre los repertorios efecto es igual a la suma entre las EMD de las distribuciones marginales de cada nodo, de forma que la EMD entre las distribuciones marginales para un nodo es la diferencia absoluta entre las probabilidades con el nodo OFF.
    """
    return np.sum(np.abs(u - v))


def emd_causal(u: NDArray[np.float64], v: NDArray[np.float64]) -> float:
    """
    Calculate the Earth Mover's Distance (EMD) between two probability distributions u and v.
    The Hamming distance was used as the ground metric.
    """
    if not all(isinstance(arr, np.ndarray) for arr in [u, v]):
        raise TypeError("u and v must be numpy arrays.")

    n: int = len(u)
    costs: NDArray[np.float64] = np.empty((n, n))

    for i in range(n):
        # Utiliza comprensión de listas para calcular los costos
        costs[i, :i] = [hamming_distance(i, j) for j in range(i)]
        costs[:i, i] = costs[i, :i]  # Reflejar los valores
    np.fill_diagonal(costs, INT_ZERO)

    cost_mat: NDArray[np.float64] = np.array(costs, dtype=np.float64)
    return emd(u, v, cost_mat)


def hamming_distance(a: int, b: int) -> int:
    return (a ^ b).bit_count()


def reindexar(N: int):
    notaciones = {
        Notation.BIG_ENDIAN.value: range(N),
        Notation.LIL_ENDIAN.value: lil_endian(N),
        # ...otras
    }
    return notaciones[aplicacion.notacion]


def seleccionar_subestado(subestado):
    notaciones = {
        Notation.BIG_ENDIAN.value: subestado,
        Notation.LIL_ENDIAN.value: subestado[::-1],
        # ...otras
    }
    return notaciones[aplicacion.notacion]


def lil_endian(n: int) -> np.ndarray:
    """
    Implementación final optimizada para generación de little endian.
    Combina las mejores prácticas encontradas en nuestras pruebas.
    """
    if n <= 0:
        return np.array([0], dtype=np.uint32)  # Caso especial para n=0

    size = 1 << n
    result = np.zeros(size, dtype=np.uint32)

    # Optimización de parámetros basada en n
    block_bits = max(12, min(16, 28 - int(np.log2(n))))
    block_size = 1 << block_bits

    # Precomputar shifts de una vez
    shifts = np.array([n - i - 1 for i in range(n)], dtype=np.uint32)

    # Pre-alocar buffer para procesamientos por bloque
    block_result = np.zeros(block_size, dtype=np.uint32)

    # Determinar tamaño óptimo de grupo de bits
    bit_group_size = 6 if n > 24 else 4  # Ajuste basado en pruebas empíricas

    for start in range(0, size, block_size):
        end = min(start + block_size, size)
        current_size = end - start

        # Reset eficiente del buffer
        block_result[:current_size] = 0
        block_indices = np.arange(start, end, dtype=np.uint32)

        # Procesar bits en grupos optimizados
        for base_bit in range(0, n, bit_group_size):
            bits_remaining = min(bit_group_size, n - base_bit)
            if bits_remaining <= 0:
                break

            # Optimización: procesamiento de múltiples bits de una vez
            group_mask = np.uint32((1 << bits_remaining) - 1)
            group_values = (block_indices >> base_bit) & group_mask

            for j in range(bits_remaining):
                shift = shifts[base_bit + j]
                bit_value = (group_values >> j) & np.uint32(1)
                block_result[:current_size] |= bit_value << shift

        result[start:end] = block_result[:current_size]

    return result


def dec2bin(decimal: int, width: int) -> str:
    return format(decimal, f"0{width}b")


def setup_logger(name: str) -> logging.Logger:
    """
    Configura un logger con formato detallado y salida a archivo.

    Args:
        name: Nombre base para el archivo de log

    Returns:
        Logger configurado
    """
    # Crear directorio base logs si no existe
    base_log_dir = Path("logs")
    base_log_dir.mkdir(exist_ok=True)

    # Obtener fecha y hora actual
    current_time = datetime.now()

    # Crear subdirectorio con la fecha
    date_dir = base_log_dir / current_time.strftime("%d_%m_%Y")
    date_dir.mkdir(exist_ok=True)

    # Crear subdirectorio con la hora
    hour_dir = date_dir / f"{current_time.strftime('%H')}hrs"
    hour_dir.mkdir(exist_ok=True)

    # Crear archivo de log
    log_file = hour_dir / f"{name}.log"

    # Configurar logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Handler para archivo
    file_handler = logging.FileHandler(log_file, mode="w")
    file_handler.setLevel(logging.DEBUG)

    # Formato detallado
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s\n%(message)s\n"
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger
