from collections import defaultdict

# GRAMATICA 
gramatica = {
    "S": [["B", "uno"], ["dos", "C"], ["ε"]],
    "A": [["S", "tres", "B", "C"], ["cuatro"], ["ε"]],
    "B": [["A", "cinco", "C", "seis"], ["ε"]],
    "C": [["siete", "B"], ["ε"]]
}

# PRIMEROS 
def calcular_primeros():
    primeros = defaultdict(set)

    cambio = True
    while cambio:
        cambio = False
        for nt in gramatica:
            for prod in gramatica[nt]:

                agregar_epsilon = True

                for simbolo in prod:

                    # terminal
                    if simbolo not in gramatica:
                        if simbolo not in primeros[nt]:
                            primeros[nt].add(simbolo)
                            cambio = True
                        agregar_epsilon = False
                        break

                    # no terminal
                    antes = len(primeros[nt])
                    primeros[nt] |= (primeros[simbolo] - {"ε"})

                    if len(primeros[nt]) != antes:
                        cambio = True

                    if "ε" not in primeros[simbolo]:
                        agregar_epsilon = False
                        break

                if agregar_epsilon:
                    if "ε" not in primeros[nt]:
                        primeros[nt].add("ε")
                        cambio = True

    return primeros

# SIGUIENTES 
def calcular_siguientes(primeros):
    siguientes = defaultdict(set)
    siguientes["S"].add("$")

    cambio = True
    while cambio:
        cambio = False
        for nt in gramatica:
            for prod in gramatica[nt]:
                follow_temp = siguientes[nt].copy()

                for simbolo in reversed(prod):
                    if simbolo in gramatica:
                        antes = len(siguientes[simbolo])
                        siguientes[simbolo] |= follow_temp

                        if "ε" in primeros[simbolo]:
                            follow_temp |= (primeros[simbolo] - {"ε"})
                        else:
                            follow_temp = primeros[simbolo]

                        if len(siguientes[simbolo]) != antes:
                            cambio = True
                    else:
                        follow_temp = {simbolo}

    return siguientes

# PREDICCION
def calcular_prediccion(primeros, siguientes):
    prediccion = {}

    for nt in gramatica:
        for prod in gramatica[nt]:
            key = (nt, tuple(prod))
            conjunto = set()

            if prod == ["ε"]:
                conjunto |= siguientes[nt]
            else:
                for simbolo in prod:
                    if simbolo not in gramatica:
                        conjunto.add(simbolo)
                        break
                    else:
                        conjunto |= (primeros[simbolo] - {"ε"})
                        if "ε" not in primeros[simbolo]:
                            break
                else:
                    conjunto |= siguientes[nt]

            prediccion[key] = conjunto

    return prediccion

# LL(1) 
def es_LL1(prediccion):
    reglas = defaultdict(list)

    for (nt, prod), conj in prediccion.items():
        reglas[nt].append(conj)

    for nt in reglas:
        conjuntos = reglas[nt]
        for i in range(len(conjuntos)):
            for j in range(i+1, len(conjuntos)):
                if conjuntos[i] & conjuntos[j]:
                    return False
    return True

# EJECUCIÓN
primeros = calcular_primeros()
siguientes = calcular_siguientes(primeros)
prediccion = calcular_prediccion(primeros, siguientes)

print("Primeros:")
for k, v in primeros.items():
    print(k, ":", v)

print("Siguientes:")
for k, v in siguientes.items():
    print(k, ":", v)

print("Prediccion:")
for (nt, prod), conj in prediccion.items():
    produccion = " ".join(prod)
    print(f"{nt} -> {produccion} : {conj}")

print("¿Es LL(1)?", es_LL1(prediccion))