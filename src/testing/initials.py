from redes import RED_10A, RED_15A, RED_15B

ordinal_base = 65
red_usada = RED_15B
pruebas = set(red_usada["pruebas"])


pruebas_literales = []
for caso in pruebas:
    futuro, presente = caso.split("|")
    futuro, _ = futuro.split("t")
    presente, _ = presente.split("t")
    print(f"{futuro, presente=}")

    ordinales_f = {ord(f) - ordinal_base for f in futuro}
    ordinales_p = {ord(p) - ordinal_base for p in presente}

    mecanismo = "".join(
        ["1" if i in ordinales_f else "0" for i in range(red_usada["num_nodos"])]
    )
    alcance = "".join(
        ["1" if j in ordinales_p else "0" for j in range(red_usada["num_nodos"])]
    )

    pruebas_literales.append((alcance, mecanismo))

    # print(f"{ordinales_f}")
    # print(f"{ordinales_p}")
    # print(f"{mecanismo}")
    # print(f"{alcance}\n")

print(f"{(pruebas_literales)=}")
print(f"{len(pruebas_literales)=}")
