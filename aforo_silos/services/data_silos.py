import pandas as pd
from django.utils import timezone


# RUTA_ACTUAL = Path(__file__).resolve()
# # print(ruta_actual)
# RUTA_PADRE = RUTA_ACTUAL.parent.parent
# # print(ruta_padre)
# RUTA_ARCHIVO = RUTA_PADRE / "staticfiles" / "docs" / "programa_silos_maestro.xlsx"


# print(RUTA_ARCHIVO)
# if RUTA_ARCHIVO.exists():
#     print("existe")
# else:
#     print("no existe")


class DataSilos:

    # Direccion del archivo de datos maestros del silo

    def recuperar_datos(ruta):
        data = pd.read_excel(ruta, 1)
        # print(data)
        return data

    def consultar_aforo(silo, centimetros, data):
        # print(data.columns)
        df_index = data.set_index("CM")
        litros = df_index.loc[centimetros, silo]
        return litros

    def consultar_capacidad(ruta, silo):
        data = pd.read_excel(ruta, 2)
        print(data)
        df_index = data.set_index("SILO")
        capacidad = df_index.loc[silo, "CAPACIDAD TOTAL"]
        return capacidad

    def calcular_peso(densidad, volumen):
        # print(densidad * volumen)
        return densidad * volumen


# clase = DataSilos
# data = DataSilos.recuperar_datos(RUTA_ARCHIVO)


# cm = int(input("cm: "))  # datos de ingreso
# silo = input("silo: ")
# densidad = float((input("densidad: ")))


# litros = clase.consultar_aforo(silo, cm, data)
# peso = clase.calcular_peso(densidad, litros)

# mensage = f"""
#       Litros {litros}
#       peso {peso}
#       """

# print(mensage)


# i = 0
# for centimetro, litro in zip(data["CM"], data["SILO 1"]):

#     # print(centimetro, litro)
#     i = i + 1
#     if i == 100:
#         break
