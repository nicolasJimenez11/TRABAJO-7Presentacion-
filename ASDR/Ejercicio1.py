from collections import defaultdict

# Gramatica (Ejercicio 1)

gramatica = {
    "S": [["A", "B", "C", "D"]],
    "A": [["dos"], ["ε"]],
    "B": [["tres"], ["cuatro"], ["cinco"]],
    "C": [["seis"], ["ε"]],
    "D": [["uno"], ["B", "E"]],
    "E": [["tres"]]
}

no_terminales = list(gramatica.keys())

# ---------------- PRIMEROS ----------------
def calcular_primeros():
    primeros = defaultdict(set)

    cambio = True
    while cambio:
        cambio = False
        for nt in gramatica:
            for prod in gramatica[nt]:
                for simbolo in prod:
                    if simbolo not in gramatica:  # terminal
                        if simbolo not in primeros[nt]:
                            primeros[nt].add(simbolo)
                            cambio = True
                        break
                    else:
                        antes = len(primeros[nt])
                        primeros[nt] |= (primeros[simbolo] - {"ε"})
                        if "ε" not in primeros[simbolo]:
                            break
                        if antes != len(primeros[nt]):
                            cambio = True
                else:
                    primeros[nt].add("ε")
    return primeros

# ---------------- SIGUIENTES ----------------
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

# ---------------- PREDICCIÓN ----------------
def calcular_prediccion(primeros, siguientes):
    prediccion = {}

    for nt in gramatica:
        for prod in gramatica[nt]:
            key = (nt, tuple(prod))
            conjunto = set()

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

# ---------------- LL(1) ----------------
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

# ---------------- EJECUCIÓN ----------------
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