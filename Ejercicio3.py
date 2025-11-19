from time import perf_counter
import random

# Utilidades simples
def densidad(M):
    # proporción de 1s en la matriz
    if not M: return 0.0
    R, C = len(M), len(M[0])
    unos = sum(sum(f) for f in M)
    return unos/(R*C) if R*C>0 else 0.0

def cubre_fila(M, cols, i):
    # cols cubre la fila i si alguna columna tiene 1
    for c in cols:
        if M[i][c] == 1:
            return True
    return False

def minimizar_por_inclusion(lista):
    # elimina supersets si ya existe un subset
    sets = [set(s) for s in lista]
    keep = [True]*len(sets)
    for i in range(len(sets)):
        if not keep[i]: continue
        for j in range(len(sets)):
            if i==j or not keep[j]: continue
            if sets[i].issuperset(sets[j]) and sets[i]!=sets[j]:
                keep[i] = False
                break
    res = []
    for i,k in enumerate(keep):
        if k:
            res.append(sorted(list(sets[i])))
    # sin duplicados
    out = []
    for s in res:
        if s not in out:
            out.append(s)
    return out

def tiene_testigos(M, cols):
    # típico: cada columna debe tener una fila donde es la ÚNICA en 1
    R = len(M)
    for c in cols:
        ok = False
        for i in range(R):
            if M[i][c] == 1:
                solo = True
                for k in cols:
                    if k != c and M[i][k] == 1:
                        solo = False
                        break
                if solo:
                    ok = True
                    break
        if not ok:
            return False
    return True

def ver_conj(conj, titulo):
    print(titulo)
    if not conj:
        print("  (vacío)")
        return
    for s in conj:
        print(" ", [x+1 for x in s])  # 1-based

# helpers para MB desde matriz cualquiera
def es_superfila(a, b):
    # a es super-fila de b si a[k] >= b[k] para todo k y en algún k a[k] > b[k]
    mayor = False
    for x, y in zip(a, b):
        if x < y:
            return False
        if x > y:
            mayor = True
    return mayor

def matriz_basica(M):
    # quitar duplicados y super-filas (versión simple)
    sin_dup = []
    for f in M:
        if f not in sin_dup:
            sin_dup.append(f[:])
    keep = [True]*len(sin_dup)
    for i in range(len(sin_dup)):
        if not keep[i]: continue
        for j in range(len(sin_dup)):
            if i==j or not keep[j]: continue
            if es_superfila(sin_dup[i], sin_dup[j]):
                keep[i] = False
                break
    MB = [sin_dup[i][:] for i,k in enumerate(keep) if k]
    return MB

def leer_matriz_manual():
    print("Pega filas 0/1 separadas por espacio. Línea vacía para terminar:")
    M = []
    cols = None
    while True:
        try:
            linea = input().strip()
        except EOFError:
            break
        if not linea:
            break
        fila = [int(x) for x in linea.split()]
        if cols is None:
            cols = len(fila)
        elif len(fila) != cols:
            print("  -> Todas las filas deben tener", cols, "columnas.")
            return []
        if any(x not in (0,1) for x in fila):
            print("  -> Solo 0/1 permitidos.")
            return []
        M.append(fila)
    return M

def generar_aleatoria():
    try:
        R = int(input("Filas (1..100): ").strip() or "0")
        C = int(input("Columnas (1..10): ").strip() or "0")
    except:
        R, C = 0, 0
    R = 1 if R < 1 else (100 if R > 100 else R)
    C = 1 if C < 1 else (10 if C > 10 else C)
    M = [[1 if random.random() < 0.5 else 0 for _ in range(C)] for __ in range(R)]
    return M

# Algoritmo BT como función
def bt(MB, devolver_traza=True):
    """
    MB: matriz booleana básica (0/1). Devuelve dict con:
      - testores (mínimos por cobertura)
      - tipicos (con testigo exclusivo)
      - tiempos_ms (por fila) y tiempo_total_ms
      - traza (candidatos Ψ* por fila)
      - densidad
    """
    R = len(MB)
    C = len(MB[0]) if R>0 else 0
    if R==0 or C==0:
        return {"testores":[], "tipicos":[], "tiempos_ms":[], "tiempo_total_ms":0.0, "traza":[], "densidad":0.0}

    traza = []
    tiempos = []

    t_total0 = perf_counter()

    # r1: singletons que cubren la primera fila
    t0 = perf_counter()
    r = 0
    cand = [[j] for j in range(C) if MB[r][j]==1]
    cand = minimizar_por_inclusion(cand)
    t1 = perf_counter()
    if devolver_traza: traza.append([s[:] for s in cand])
    tiempos.append((t1-t0)*1000)

    # r2..rR
    for r in range(1, R):
        t0 = perf_counter()
        nuevos = []
        for s in cand:
            if cubre_fila(MB, s, r):
                nuevos.append(s[:])
            else:
                for j in range(C):
                    if MB[r][j]==1 and j not in s:
                        t = s + [j]
                        t.sort()
                        if t not in nuevos:
                            nuevos.append(t)
        cand = minimizar_por_inclusion(nuevos)
        t1 = perf_counter()
        if devolver_traza: traza.append([s[:] for s in cand])
        tiempos.append((t1-t0)*1000)

    # resultados
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

def imprimir_resultados(res):
    def ver(conj):
        return [[x+1 for x in s] for s in conj]
    print("Densidad(MB):", round(res.get("densidad",0.0),3))
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

def ver_matriz(M, nombre):
    print(f"{nombre} ({len(M)}x{len(M[0]) if M else 0}), densidad={densidad(M):.3f}")
    for f in M: print(" ", f)

# MAIN (A por defecto; modos opcionales)
if __name__ == "__main__":
    # Modo por defecto: A del Ej.3
    A = [
        [0,1,0,1,1,1],
        [1,0,1,0,0,0],
        [1,1,0,0,1,1],
        [1,1,0,1,1,0],
    ]

    print("Ejercicio 3 - BT (A por defecto)")
    print("Elige modo:  1) A  2) Pegar matriz  3) Aleatoria")
    try:
        modo = int(input("> ").strip() or "1")
    except:
        modo = 1

    if modo == 1:
        M0 = A[:]            # original
        MB = A[:]            # ya es MB
        print("\nModo 1: usando A (por defecto).")
    elif modo == 2:
        M0 = leer_matriz_manual()
        if not M0:
            print("No se ingresó una matriz válida. Saliendo.")
            raise SystemExit
        MB = matriz_basica(M0)
        print("\nModo 2: matriz pegada → MB construida.")
    else:
        M0 = generar_aleatoria()
        MB = matriz_basica(M0)
        print("\nModo 3: matriz aleatoria (Ej.1) → MB construida.")

    print("\nMatriz original:")
    ver_matriz(M0, "M0")
    print("\nMatriz Básica (MB):")
    ver_matriz(MB, "MB")

    res = bt(MB, devolver_traza=True)
    imprimir_resultados(res)