# Proyecto-2025A

Base del proyecto para dar desarrollo a estrategias más elaboradas.

## Instalación

Guía de Configuración del Entorno con UV y VSCode

## Requisitos Previos
- Visual Studio Code instalado
- Python 3.11.9
- Terminal PowerShell

## Pasos de Configuración

### 1. Configuración del Entorno Virtual
1. Abrir el proyecto en Visual Studio Code
2. Presionar `Ctrl + Shift + P` para abrir la paleta de comandos
3. Buscar y seleccionar `Python: Create Environment`
4. Elegir la opción `Venv`
5. Seleccionar `Python 3.11.9 64-bit (Microsoft Store)`
6. Esperar a que se complete la creación del entorno

### 2. Preparación del Entorno
1. Reiniciar Visual Studio Code para asegurar que reconozca el nuevo entorno
2. Abrir una nueva terminal PowerShell desde VSCode
3. Verificar que el entorno virtual esté activado (puede ser con `py --version`) - debería verse el prefijo `(.venv)` en la terminal
4. Si no está activado, ejecutar:
   ```powershell
   .\.venv\Scripts\activate
   ```

### 3. Instalación de Dependencias con UV
1. Con el entorno virtual activado, ejecutar:
   ```powershell
   python -m uv pip install -e .
   ```
2. Este comando:
   - Instala todas las dependencias definidas en `pyproject.toml`
   - Instala el proyecto en modo desarrollo (-e)
   - Crea una carpeta `proyecto_2025a.egg-info` con metadatos del proyecto.

## Verificación
- La instalación es exitosa si:
  - No hay mensajes de error en la terminal.
  - Se crea la carpeta `proyecto_2025a.egg-info`.
  - Puedes importar las dependencias instaladas desde Python.

## Notas Importantes
- Siempre usar PowerShell como terminal predeterminada para consistencia.
- El entorno virtual debe estar activado antes de instalar dependencias.
- La carpeta `proyecto_2025a.egg-info` es normal y necesaria - se puede agregar a `.gitignore`.

## Ejecución del programa

Abres una terminal, escribes `py e` tabulas y das enter, así de simple! Alternativamente escribiendo en terminal `python .\exec.py` deberás ejecutar una muestra del aplicativo para una Red de 04 nodos, generarando un análisis completo sobre la misma, de tal forma que se obtendrán dos artefactos tras la ejecución

Por otro lado puedes realizar un anális específico sobre una red

Al final podemos realizar ejecución desde `py exec` y pasar a corregir los errores de la librería Pyphi (en el documento `.docs\errors.md` encuentras la guía de bolsillo para arreglar estos problemas).

Tras ello podrás realizar distintas pruebas en el aplicativo, por ejemplo, el código por defecto tenemos:
```py

from models.base.manager import Manager

from src.models.logic.phi import Phi
from src.models.logic.force import BruteForce
from src.models.logic.q_nodes import QNodes


def start_up():
    """Punto de entrada principal"""
    #                ABCDEFGHIJ...
    estado_inicio = "1000"
    sys_config = Manager(estado_inicial=estado_inicio)

    ### Ejemplo de solución mediante fuerza bruta ###

    bf_analyzer = BruteForce(sys_config)
    bf_analyzer.analizar_completamente_una_red()

```

En este lo que hacemos es ejecutar un análsis de forma completa sobre una red, analizando lo que son todos sus posibles sistemas candidatos, por cada uno de ellos sus posibles subsistemas y sobre cada uni hacemos un análisis de irreducibilidad sistémica (SIA), de forma que tendremos tanto la solución de la ejecución como una serie metadatos sobre los que podemos dar un análisis.
Este resultado se ubicará en el directorio `review\resolver\red_ejecutada\estado_inicial\`, donde el sistema candidato será un archivo excel, cada hoja un posible subsistema, cada fila una partición de las variables en tiempo presente $(t_0)$ y las columnas para un tiempo futuro $(t_1)$ de forma que las variables que pertenezcan a un mismo dígito pertenecen a la misma partición.

Primeramente se cuenta con un decorador `@profile` encontrado en `src.middlewares.profile` aplicable sobre cualquier función, este nos permite generar un análisis temporal del llamado de subrutinas, teniendo dos modos de visualización podremos apreciar una vista global (Call Stack) y particular (Timeline). Este decorador nos será especialmente útil para la detección de cuellos de botella durante la ejecución del programa para cualquier subrutina usada, además de permitirnos conocer el uso de CPU y dar uso en procesos de optimización.

Secundariamente sobre el directorio `logs`, cada que se use el objeto `self.logger` en la clase de ejecución se generará un archivo indicando los datos logeados/impresos para hacer un seguimiento completo de la ejecución, este se almacena por carpetas de la forma `dia_mes_año\hora\metodo_del_log` manteniendo un historial de las ejecuciones. Este logger se volverá casual/sospechosamente útil cuando el rastro de las ejecuciones sea _extremandamente_ extenso para algún proceso.


## Pruebas

En el archivo de pruebas en el directorio `.tests` encontrarás el documento excel con las pruebas a resolver mediante uso del aplicativo.