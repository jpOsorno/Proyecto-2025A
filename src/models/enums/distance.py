from enum import Enum, member


class MetricDistance(Enum):
    """La clase notaciones recopila diferentes notaciones binarias. Al definir el tipo se accede por `.value`."""

    EMD_EFECTO: member = "emd-effect"
    EMD_CAUSA: member = "emd-cause"
    MANHATTAN: member = "distancia-manhattan"
    EUCLIDIANA: member = "distancia-euclidiana"
