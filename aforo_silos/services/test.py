import pandas as pd
from pathlib import Path


RUTA_ACTUAL = Path(__file__).resolve()
# print(ruta_actual)
RUTA_PADRE = RUTA_ACTUAL.parent.parent
# print(ruta_padre)
RUTA_ARCHIVO = RUTA_PADRE / "staticfiles" / "docs" / "programa_silos_maestro.xlsx"


print(RUTA_ARCHIVO)
if RUTA_ARCHIVO.exists():
    print("existe")
else:
    print("no existe")
silo = "SILO 3"
data = pd.read_excel(RUTA_ARCHIVO, 2)

df_index = data.set_index("SILO ")
capacidad = df_index.loc[silo]
print(capacidad)
