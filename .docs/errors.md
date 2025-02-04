Error:

ImportError: cannot import name 'Iterable' from 'collections' (C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.11_3.11.2544.0_x64__qbz5n2kfra8p0\Lib\collections\__init__.py)

Ir a:
.venv\Lib\site-packages\pyphi\memory.py

Corregir por:
from collections.abc import Iterable

---

Error:

ImportError: cannot import name 'Iterable' from 'collections' (C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.11_3.11.2544.0_x64__qbz5n2kfra8p0\Lib\collections\__init__.py)

Ir a:
.venv\Lib\site-packages\pyphi\models\cmp.py

Poner
from collections.abc import Iterable



---

Error:
  File "...\.venv\Lib\site-packages\pyphi\models\actual_causation.py", line 219, in <module>
    class Account(cmp.Orderable, collections.Sequence):
                                 ^^^^^^^^^^^^^^^^^^^^
AttributeError: module 'collections' has no attribute 'Sequence'

Ir al sitio y poner:

from collections.abc import Sequence

...

class Account(cmp.Orderable, Sequence):

---

Eror
  File "C:\Users\overd\Saved Games\Computacion\Algorithms\project\Zero-Back\.venv\Lib\site-packages\pyphi\models\subsystem.py", line 20, in <module>    
    class CauseEffectStructure(cmp.Orderable, collections.Sequence):

Cambiar
```
from collections.abc import Sequence

class CauseEffectStructure(cmp.Orderable, Sequence):
```

---

Error:
>  File "C:\Users\overd\Saved Games\Computacion\Algorithms\project\Zero-Back\.venv\Lib\site-packages\pyphi\models\cuts.py", line 269, in <module>        
>>    class KPartition(collections.Sequence):

Solución:

```
import collections
from collections.abc import Sequence

class KPartition(Sequence):
```

---
  File "C:\Users\overd\Saved Games\Computacion\Algorithms\project\Zero-Back\.venv\Lib\site-packages\pyphi\registry.py", line 12, in <module>
    class Registry(collections.Mapping):
AttributeError: module 'collections' has no attribute 'Mapping'

Solución

```
from collections.abc import Mapping

...

class Registry(Mapping):
```

---
```
from collections.abc import Sequence
...
class NodeLabels(Sequence):
```