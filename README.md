# Proyecto-2025A

Base del proyecto para dar desarrollo a estrategias más elaboradas.

Para clonar el repositorio con github debemos tener GIT y aplicar el comando sobre un directorio cómodo para guardar el proyecto `git clone https://github.com/Complexum/Proyecto-2025A .` y poder comenzar con nuestra asombrosa aventura!

---

## Instalación

Guía de Configuración del Entorno con VSCode

### ⚙️ Instalación - Configuración

#### 📋 **Requisitos Mínimos**
- ![PowerShell](https://img.shields.io/badge/-PowerShell-blue?style=flat-square) Terminal PowerShell/Bash.
- ![VSCode](https://img.shields.io/badge/-VSCode-007ACC?logo=visualstudiocode&style=flat-square) Visual Studio Code instalado.
- ![Python](https://img.shields.io/badge/-Python%203.10.5-3776AB?logo=python&style=flat-square) Versión python 3.10.5 (o similar).

---

#### 🚀 **Configuración**

1. **🔥 Crear Entorno Virtual**  
   - Abre VSCode y presiona `Ctrl + Shift + P`.
   - Busca y selecciona:  
     `Python: Create Environment` → `Venv` → `Python 3.10.5 64-bit` y si es el de la `(Microsoft Store)` mejor. En este paso, es usualmente recomendable el hacer instalación del Virtual Environment mediante el archivo de requerimientos, no obstante si deseas jugartela a una instalación más eficiente y controlada _(no aplica a todos)_, puedes usar UV. Esto 
   - ![Wait](https://img.shields.io/badge/-ESPERA_5_segundos-important) Hasta que aparezca la carpeta `.venv`

2. **🔄 Reinicio**
   - Cierra y vuelve a abrir VSCode (obligado ✨).
   - Verifica que en la terminal veas `(.venv)` al principio  
     *(Si no: Ejecuta `.\.venv\Scripts\activate` manualmente)*


> **💣 (Opcional) Instalación con UV**
>   En la terminal PowerShell (.venv activado): 
>   Primero instalamos `uv` con 
>   ```powershell
>   pip install uv
>   ```
>   Procedemos a instalar las librerías con
>   ```powershell
>   python -m uv pip install -e .
>   ```

> **Este comando:**
> Instala dependencias de pyproject.toml
> Configura el proyecto en modo desarrollo (-e)
> Genera proyecto_2025a.egg-info con metadatos

1. ✅ Verificación Exitosa
   ✔️ Sin errores en terminal
   ✔️ Carpeta proyecto_2025a.egg-info creada
   ✔️ Posibilidad de importar dependencias desde Python

🔥 Notas Críticas
   - Procura usar la PowerShell como terminal predeterminada (o Bash)
   - Activar entorno virtual antes de cualquier operación
   - La carpeta proyecto_2025a.egg-info es esencial

### Ejecución del programa

Abres una terminal, escribes `py e` tabulas y das enter, _así de simple_! Alternativamente escribiendo en terminal `python .\exec.py` deberás ejecutar una muestra del aplicativo para una Red de 04 nodos, generarando un análisis completo sobre la misma, de tal forma que se obtendrán varios artefactos tras la ejecución.

Por otro lado puedes realizar un anális específico sobre una red usando el método `aplicar_estrategia(...)` con los parámetros respectivos.

Si te sale un error que esté asociado con las herramientas de desarrollo de c++, esto ocurre puesto Pyphi utiliza compiladores en Cython/C/C++ para el cálculo de la EMD Causal. Con esto debes debes instalar [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/es/visual-cpp-build-tools/) o si ya lo tienes dale en "Modificar" para posteriormente seleccionar la `MSVCv142 - VS 2019 C++ x64/86 build tools`, con esto debería de arreglarse para siempre.

Al final podemos realizar ejecución desde `py exec` y pasar a corregir los errores de la librería Pyphi (en el documento `.docs\errors.md` encuentras la guía de bolsillo para arreglar estos problemas).

> Tras ello podrás realizar distintas pruebas en el aplicativo, por ejemplo tenemos:

> Si quisiéramos hacer una prueba con un subsistema **específico** para una red utilizando fuerza bruta, hacemos lo siguiente:

```py
from src.controllers.manager import Manager
from src.models.strategies.force import BruteForce

def start_up():
    """Punto de entrada principal"""
    # ABCD #
    estado_inicio = "1000"
    condiciones =   "1110"
    alcance =       "1110"
    mechanismo =    "1110"

    config_sistema = Manager(estado_inicial=estado_inicio)

    ### Ejemplo de solución mediante módulo de fuerza bruta ###
    analizador_fb = BruteForce(config_sistema)
    sia_uno = analizador_fb.aplicar_estrategia(condiciones, alcance, mechanismo)
    print(sia_uno)
```

Podemos ver cómo al definir el estado inicial `1000` estamos usando implícitamente una red de 04 nodos y sólo asignamos al primer nodo _(el A)_ el valor de 1 _(canal activo)_ y los demás _(BCD=000)_ o inactivos.

Esta estará ubicada en el directorio `.samples\`, si tenemos varias deberemos configurar en el `Manager` cuál querremos utilizar manualmente o cambiando la página desde la configuración del aplicativo.

---

Por ejemplo, una ejecución con **Pyphi** para una red específica se vería así:

```py
from src.controllers.manager import Manager
from src.models.strategies.phi import Phi

def start_up():
    """Punto de entrada principal"""
                   # ABCD #
    estado_inicio = "1000"
    condiciones =   "1110"
    mechanismo =    "0110"
    alcance =       "1010"

    config_sistema = Manager(estado_inicial=estado_inicio)

    ### Ejemplo de solución mediante Pyphi ###
    analizador_fi = Phi(config_sistema)
    sia_dos = analizador_fi.aplicar_estrategia(condiciones, alcance, mechanismo)
    print(sia_dos)
```

Donde sobre un sistema de nodos $V=\{A,B,C,D\}$ tomamos un sistema candidato $V_c=\{A,B,C\}$ subsistema, y en los tiempos $t_0=\{B,C\}$ y $t_1=\{A,C\}$, nótese cómo sólo en el subsistema se presenta temporalidad.

Como se aprecia, cada variable está asociada con una posición, de forma que las variables a **mantener** tienen el bit en uno (1), mientras que las que querremos **descartar** las enviaremos en cero (0).

---

#### Herramientas de diagnóstico

En este caso, lo que hacemos es ejecutar un análisis completo sobre una red, analizando todos sus posibles sistemas candidatos. Para cada uno de ellos, se evalúan sus posibles subsistemas y sobre cada uno se realiza un _Análisis de Irreducibilidad Sistémica_ (SIA), proporcionando tanto la solución de la ejecución como metadatos para un análisis más profundo.

Este resultado se ubicará en el directorio `review\resolver\red_ejecutada\estado_inicial\`, donde:
- Cada sistema candidato será un archivo Excel.
- Cada hoja representará un posible subsistema.
- Cada fila mostrará una partición de las variables en tiempo presente $(t_0)$.
- Las columnas indicarán el estado en un tiempo futuro $(t_1)$.

Además, se cuenta con un decorador `@profile` en `src.middlewares.profile`, aplicable sobre cualquier función. Este decorador permite generar un análisis temporal del llamado de subrutinas, con dos modos de visualización: una vista global _(Call Stack)_ y una vista particular _(Timeline)_. Esto será útil para la detección de **cuellos de botella** y la optimización del programa.

Adicionalmente, en el directorio `logs`, cada vez que se use `self.logger` en la clase de ejecución, se generará un archivo con los datos logeados. Estos se almacenan por carpetas con la estructura `dia_mes_año\hora\metodo_del_log`, lo que permite un seguimiento detallado de la ejecución. Este logger se vuelve especialmente útil cuando los rastros de ejecución son extremadamente extensos.

---

Si deseas realizar un análisis completo de una red mediante fuerza bruta, puedes hacerlo con el siguiente código:

```py
from src.controllers.manager import Manager
from src.models.strategies.force import BruteForce

def start_up():
    """Punto de entrada principal"""
                   # ABCD #
    estado_inicio = "1000"
    config_sistema = Manager(estado_inicial=estado_inicio)

    ## Ejemplo de solución mediante fuerza bruta ##
    analizador_fb = BruteForce(config_sistema)
    analizador_fb.analizar_completamente_una_red()
```

---

### Pruebas 🧪

En el archivo de pruebas en el directorio `.tests` encontrarás el documento excel con las pruebas a resolver mediante uso del aplicativo.

Si deseas realizar pruebas con una matriz superior a las ya diseñadas, puedes hacer uso del `Manager` para generar una nueva, de forma tal que usando su método `generar_red(dimensiones: int)` quedará almacenada en el directorio de samples para su uso posterior.

Para finalizar cabe recordar que el repositorio está atento a cambios o mejoras propuestas por parte de los cursantes, de forma que es oportuno realizar `git pull origin main` para tener siempre la versión más reciente 🫶!
