# Errores de compilación - Pyphi

Pyphi es una librería desarrollada para el cálculo y trabajo en IIT versión 4.0, a pesar del árduo desarrollo realizado es un proyecto open source de forma que reciben cierta colaboración activamente, no obstante no está excento de errores como los siguientes al inicio de su ejecución:

> ImportError: cannot import name 'Iterable' from 'collections'
> AttributeError: module 'collections' has no attribute 'Sequence'
> AttributeError: module 'collections' has no attribute 'Mapping'

Para solucionarlos primero debemos hacer ejecución del aplicativo de forma tal que tengamos el trazo del error.
Posteriormente en terminal vamos a ubicar el enlace donde indica se produjo el error y con `ctrl + clic` nos redireccionará hasta el punto interno de la librería, el enlace tiene una estructura similar a `..ruta_usuario..\.venv\Lib\site-packages\pyphi\clase_del_error.py`

> Ejemplo:
>> ImportError: cannot import name 'Iterable' from 'collections' (C:\\Program Files\\WindowsApps\\PythonSoftwareFoundation.Python.3.11_3.11.2544.0_x64__qbz5n2kfra8p0\\Lib\\collections\\_\_init__.py)
>
> Vamos hasta
> > ..path\\.venv\\Lib\\site-packages\\pyphi\\memory.py

Este proceso de acceder a la clase del error será repetitivo, no obstante la solución será siempre la misma.

En el punto específico del error se nos indicará que se intenta usar una colección, no obstante esta fue movida y por ende el acceso es errado, con esto si tenemos:

> `from collections import Iterable`

Corregiremos por 
> `from collections.abc import Iterable`

Esto se puede hacer a nivel de paquete o de implementación, tal que también podemos autocompletar la librería, por ejemplo cambiamos:

> `import collections`
> `class Account(cmp.Orderable, collections.Sequence):`

Por el acceso a la clase asociada, así podemos importar correctamente la librería con mayor facilidad 

> `import collections`
> `import collections.abc`
> `class Account(cmp.Orderable, collections.abc.Sequence):`

Con esto lograremos resolver estos errores internos a la librería y dar uso libremente.
