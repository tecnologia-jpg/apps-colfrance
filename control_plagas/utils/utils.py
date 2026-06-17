# Prototipo de busqueda de plaga


TIPO_PLAGA = {
    "rastreras": [
        "Cucarachas",
        "Hormigas",
        "Escarabajos",
        "Arañas",
        "Lepismas (pececillos de plata)",
    ],
    "voladoras": [
        "Moscas",
        "Mosquitos",
        "Polillas",
        "Avispas",
        "Abejas",
    ],
    "roedoras": [
        "Ratón doméstico",
        "Rata gris",
        "Rata negra",
    ],
}

tipos = list(TIPO_PLAGA.keys())

for i, tipo in enumerate(tipos):
    print(i, tipo)

tipo_index = int(input("Seleccione el tipo de plaga: "))
tipo = tipos[tipo_index]

for i, plaga in enumerate(TIPO_PLAGA[tipo]):
    print(i, plaga)

plaga_index = int(input("Seleccione la plaga: "))

print("Plaga seleccionada:", TIPO_PLAGA[tipo][plaga_index])
