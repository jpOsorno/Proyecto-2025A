from dataclasses import dataclass
from pathlib import Path

from src.constants.base import (
    ABC_START,
    CSV_EXTENSION,
    SAMPLES_PATH,
    RESOLVER_PATH,
)


@dataclass
class Manager:
    """El manejador es el encargado de en funcioón al tamaño del estado inicial y la página asociada, el traer el fichero de formato CSV con las TPM's almacenadas en `samples/` para hacer una rápida depuración de los datos para la creación de sistemas.

    Args:
    ----
        - `estado_inicial` (str): Dado se manejan sistemas binarios es un número base dos de tamaño asociado a la red que se quiera cargar.
        - `pagina` (str): En la ruta de samples se tiene un literal asociado al tamaño de las redes por si se necesita añadir varias de un mismo tamaño.
        ruta_base (Path): Ruta donde se encuentran las muestras de TPMs en representación estado-nodo-on.

    Returns:
    -------
        None: Así mismo se encarga de asociar el directorio donde se mostrarán análisis sobre las ejecuciones, donde el programador haga uso del módulo de logging y profilling.
    """

    estado_inicial: str
    pagina: str = ABC_START
    ruta_base: Path = Path(SAMPLES_PATH)

    @property
    def tpm_filename(self) -> Path:
        return (
            self.ruta_base / f"N{len(self.estado_inicial)}{self.pagina}.{CSV_EXTENSION}"
        )

    @property
    def output_dir(self) -> Path:
        return Path(
            f"{RESOLVER_PATH}/N{len(self.estado_inicial)}{self.pagina}/{''.join(self.estado_inicial)}"
        )
