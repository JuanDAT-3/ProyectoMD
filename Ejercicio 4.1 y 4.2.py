import numpy as np
from time import perf_counter


# ==========================================================
#      FUNCIONES AUXILIARES DEL ALGORITMO BT COMPLETO
# ==========================================================

def minimizar_por_inclusion(lista):
    mins = []
    for s in lista:
        if not any(set(t).issubset(s) for t in lista if t != s):
            mins.append(s)
    return mins


def cubre_fila(MB, s, r):
    return any(MB[r][j] == 1 for j in s)


def tiene_testigos(MB, s):
    for j in s:
        ok = False
        for r in range(len(MB)):
            if MB[r][j] == 1 and all(MB[r][k] == 0 for k in s if k != j):
                ok = True
                break
        if not ok:
            return False
    return True


def densidad(M):
    if len(M)==0: 
        return 0
    total = len(M)*len(M[0])
    unos = sum(sum(fila) for fila in M)
    return unos/total


# ==========================================================
#                ALGORITMO BT COMPLETO
# ==========================================================

def bt(MB, devolver_traza=True):

    R = len(MB)
    C = len(MB[0]) if R>0 else 0

    if R==0 or C==0:
        return {
            "testores":[],
            "tipicos":[],
            "tiempos_ms":[],
            "tiempo_total_ms":0.0,
            "traza":[],
            "densidad":0.0
        }

    traza = []
    tiempos = []
    t_total0 = perf_counter()

    # ==========================
    #      Fila r1
    # ==========================
    t0 = perf_counter()
    r = 0
    cand = [[j] for j in range(C) if MB[r][j]==1]
    cand = minimizar_por_inclusion(cand)
    t1 = perf_counter()

    if devolver_traza:
        traza.append([s[:] for s in cand])
    tiempos.append((t1 - t0)*1000)

    # ==========================
    #     Filas r2..rR
    # ==========================
    for r in range(1, R):
        t0 = perf_counter()
        nuevos = []

        for s in cand:
            if cubre_fila(MB, s, r):
                nuevos.append(s[:])
            else:
                for j in range(C):
                    if MB[r][j] == 1 and j not in s:
                        t = s + [j]
                        t.sort()
                        if t not in nuevos:
                            nuevos.append(t)

        cand = minimizar_por_inclusion(nuevos)
        t1 = perf_counter()

        if devolver_traza:
            traza.append([s[:] for s in cand])
        tiempos.append((t1 - t0)*1000)

    # ==========================
    #    Resultados finales
    # ==========================
    testores = cand[:]
    tipicos = minimizar_por_inclusion([s for s in testores if tiene_testigos(MB, s)])
    t_total1 = perf_counter()

    return {
        "testores": testores,
        "tipicos": tipicos,
        "tiempos_ms": tiempos,
        "tiempo_total_ms": (t_total1 - t_total0)*1000,
        "traza": traza if devolver_traza else None,
        "densidad": densidad(MB),
    }


# ==========================================================
#         IMPRESIÓN DE RESULTADOS BT COMPLETO
# ==========================================================

def imprimir_resultados(res):
    def ver(conj):
        return [[x+1 for x in s] for s in conj]

    print("Densidad(MB):", round(res.get("densidad",0.0), 3))

    if res.get("traza") is not None:
        print("\nCandidatos por fila (Ψ*):")
        for i, nivel in enumerate(res["traza"], 1):
            print(f" r{i}:", ver(nivel))

    print("\nTestores mínimos por cobertura:")
    print(" ", ver(res["testores"]))

    print("Testores típicos:")
    print(" ", ver(res["tipicos"]))

    print("\nTiempos por fila (ms):", ["{:.3f}".format(x) for x in res["tiempos_ms"]])
    print("Tiempo total (ms): {:.3f}".format(res["tiempo_total_ms"]))


# ==========================================================
#     CONSTRUIR MATRIZ B A PARTIR DE LOS TESTORES ψ*
# ==========================================================

def construir_matriz_B(A, num_cols):
    B = np.zeros((len(A), num_cols), dtype=int)
    for i, testor in enumerate(A):
        for col in testor:
            B[i, col] = 1
    return B


# ==========================================================
#                PROGRAMA PRINCIPAL
# ==========================================================

if __name__ == "__main__":

    # Cantidad de columnas del problema
    num_cols = 6

    # Testores típicos dados A (ψ*)
    A = [
        {0, 1},        # {x1, x2}
        {0, 3},        # {x1, x4}
        {0, 4},        # {x1, x5}
        {0, 5},        # {x1, x6}
        {1, 2},        # {x2, x3}
        {2, 3, 5},     # {x3, x4, x6}
        {2, 4}         # {x3, x5}
    ]

    print("===================================")
    print("     Testores típicos A (ψ*)")
    print("===================================")
    for t in A:
        print(sorted(list(t)))


    # Construcción de la matriz B
    B = construir_matriz_B(A, num_cols)

    print("\n===================================")
    print("        MATRIZ B (Notación estándar)")
    print("===================================")
    print(B)
    print(f"\nDimensiones: {B.shape[0]} filas × {B.shape[1]} columnas")


    # Ejecutar EL BT COMPLETO sobre B
    MB = B.tolist()
    
    print("\n===================================")
    print("     RESULTADOS BT COMPLETO SOBRE B")
    print("===================================")

    res = bt(MB, devolver_traza=True)
    imprimir_resultados(res)
