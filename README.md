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
   - Crea una carpeta `proyecto_2025a.egg-info` con metadatos del proyecto

## Verificación
- La instalación es exitosa si:
  - No hay mensajes de error en la terminal
  - Se crea la carpeta `proyecto_2025a.egg-info`
  - Puedes importar las dependencias instaladas desde Python

## Notas Importantes
- Siempre usar PowerShell como terminal predeterminada para consistencia
- El entorno virtual debe estar activado antes de instalar dependencias
- La carpeta `proyecto_2025a.egg-info` es normal y necesaria - se puede agregar a `.gitignore`

## Ejecución del programa

Abres una terminal, escribes `py e` tabulas y das enter, así de simple! Alternativamente escribiendo en terminal `python .\exec.py` deberás ejecutar una muestra del aplicativo para una Red de 04 nodos, generarando un análisis completo sobre la misma, de tal forma que se obtendrán dos artefactos tras la ejecución

Por otro lado puedes realizar un anális específico sobre una red

Al final podemos realizar ejecución desde `py exec` y pasar a corregir los errores de la librería.

# 