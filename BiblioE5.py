import numpy as np 
import time 

# ==================        YYC         ====================
# ======      Funciones de formato      ======
def format_tau(tau, rasgos):
    """Convierte un set de índices como {0, 2} a un string como {x1, x3}"""
    if not tau:
        return "∅"
    return "{" + ", ".join(sorted([rasgos[j] for j in tau])) + "}"

def print_psi(psi, rasgos, step_name, elapsed_time):
    """
    Imprime el estado actual de Psi:
    1. Imprime el conjunto de testores
    2. Imprime el tiempo de ejecución acumulado
    """
    print(f"\n--- {step_name} ---")
    
    if not psi:
        print("Psi* = { ∅ }")
    else:
        list_str = [format_tau(tau, rasgos) for tau in psi]
        print(f"Psi* = {{ {', '.join(sorted(list_str))} }}")
    
    # Imprimir tiempo acumulado
    print(f"Tiempo Acumulado: {elapsed_time:.8f} segundos") 

# =====       Funciones YCC     =====
def minimizar_por_inclusion_sets(conjuntos):
    """
    Recibe un iterable de testores (frozenset) y devuelve
    solo los mínimos por inclusión.
    """
    if not conjuntos:
        return set()
    
    # Convertimos a sets mutables para trabajar
    sets_list = [set(t) for t in conjuntos]
    # Ordenamos por tamaño (primero los más pequeños)
    sets_list.sort(key=len)

    keep = [True] * len(sets_list)

    for i in range(len(sets_list)):
        if not keep[i]:
            continue
        # Solo comparamos con los que vienen después (más grandes o igual tamaño)
        for j in range(i + 1, len(sets_list)):
            if keep[j] and sets_list[i].issubset(sets_list[j]):
                # si el pequeño i está contenido en j, el grande j no es mínimo
                keep[j] = False

    resultado = set()
    for i, k in enumerate(keep):
        if k:
            resultado.add(frozenset(sets_list[i]))
    return resultado

def find_compatible_set(MB, tau, xp, current_row_index):
    """
    Verifica si un nuevo testor candidato (tau U {xp}) es TÍPICO (minimal)
    revisando si forma un "conjunto compatible".
    
    Argumentos:
    MB: La Matriz Básica completa 
    tau (set): El testor que falló.
    xp (int): La columna de reparación.
    current_row_index (int): El índice de la fila actual que estamos analizando.
    """
    tau_union_xp = tau | {xp} ## Union de ambos conjuntos

    cols_indices = list(tau_union_xp)
    rows_indices = list(range(current_row_index + 1))

    ## Creación de RefSM
    try:
        RefSM = MB[np.ix_(rows_indices, cols_indices)]
    except IndexError:
        print("Error: Índices fuera de rango al crear RefSM")
        return False
    
    row_sums = np.sum(RefSM, axis=1)
    rows_with_sum_1_indices = np.where(row_sums == 1)[0]
    num_typical_rows = len(rows_with_sum_1_indices)
    num_candidate_cols = len(tau_union_xp)

    ## Condición 1
    condition_1 = (num_typical_rows >= num_candidate_cols)

    # Redifinición de RefSM
    RefSM_redefined = RefSM[rows_with_sum_1_indices, :]
    
    # Condición 2
    col_sums = np.sum(RefSM_redefined, axis=0)
    condition_2 = np.all(col_sums >= 1)

    return condition_1 and condition_2

def YYC(MB):

    if MB.size == 0:
        print("Matriz Básica Vacía")
        return set()

    R,C = MB.shape
    #rasgos = [f'x{j+1}' for j in range(C)] #Para Impresión
    
    #start_time = time.perf_counter() ## Temporizador para rendimiento
    psi = set() # Conjunto de testores ψ* vacío

    #=====      Primera Fila        =====
    r1 = MB[0, :] 

    for i in range(C):
        if r1[i] == 1:
            psi.add(frozenset({i}))
    
    # # Tiempo en Fila 1   
    # time_fila_1 = time.perf_counter() - start_time
    # # Imprimir testores Fila 1
    # print_psi(psi, rasgos, "Fila 1", time_fila_1)

    #=====      Segunda Fila en Adelante        =====

    for i in range(1, R):
        ri = MB[i, :]
        psi_aux = set()
        extend_cols = {j for j, val in enumerate(ri) if val == 1} ## Fila con 1
        
        # Comprobar testores anteriores
        for tau_j in psi:
            survives = any(ri[xp] == 1 for xp in tau_j) # Si nueva fila coontiene almenos un 1 en las columnas elegidas

            if survives:
                psi_aux.add(tau_j) 
            else: 
                for xp in extend_cols:
                    # Llamada al Algoritmo de compatibilidad
                    if find_compatible_set(MB, tau_j, xp, i):
                        psi_aux.add(tau_j | {xp})
        
        # Comprobar Minimalidad (Que no exista un testor subconjunto de otro)
        # Comprobar Minimalidad (Que no exista un testor subconjunto de otro)
        psi = minimizar_por_inclusion_sets(psi_aux)


        # # Calcular tiempo acumulado Fila i
        # cumulative_time = time.perf_counter() - start_time
        # # Imprimir testores Fila i
        # print_psi(psi, rasgos, f"Fila {i+1}", cumulative_time)
    
    return psi

# ==================        BT          ====================

# --- Funciones Auxiliares para BT ---

def cubre_fila(M, cols, i):
    """Verifica si el subconjunto 'cols' cubre la fila 'i' (tiene al menos un 1)."""
    for c in cols:
        if M[i][c] == 1:
            return True
    return False

def minimizar_por_inclusion(lista):
    """
    Versión OPTIMIZADA: Ordena por tamaño para acelerar la poda.
    Si A es subconjunto de B, eliminamos B (porque A es más pequeño y suficiente).
    """
    if not lista: return []
    
    # 1. Convertimos a sets para velocidad
    # Convertimos cada elemento a set para poder usar operaciones de conjuntos
    sets = [set(x) for x in lista]
    
    # 2. ORDENAR por tamaño (Clave para la optimización)
    # Es mucho más probable que un conjunto pequeño elimine a uno grande.
    sets.sort(key=len)
    
    keep = [True] * len(sets)
    
    # 3. Comparación dirigida
    for i in range(len(sets)):
        if not keep[i]: continue
        
        # Solo comparamos contra los que siguen (que son igual o más grandes)
        for j in range(i + 1, len(sets)):
            if keep[j]:
                # Si el pequeño (i) es subconjunto del grande (j), el grande sobra.
                if sets[i].issubset(sets[j]):
                    keep[j] = False

    # 4. Reconstruir resultado
    res = []
    for i, k in enumerate(keep):
        if k:
            res.append(sorted(list(sets[i])))
            
    return res

def tiene_testigos(M, cols):
    """
    Verifica la condición de tipicidad: cada columna del testor debe ser
    la ÚNICA con un '1' en al menos una fila de la submatriz.
    """
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

# --- Algoritmo BT ---

def BT(MB):
    """
    Implementación del algoritmo BT optimizada para benchmark.
    Retorna: Un set de frozensets (los testores típicos).
    """
    R = len(MB)
    if R == 0:
        return set()
    
    C = len(MB[0])
    if C == 0:
        return set()

    # --- Paso 1: Procesar primera fila ---
    # Candidatos iniciales: columnas con '1' en la fila 0
    r = 0
    cand = [[j] for j in range(C) if MB[r][j] == 1]
    cand = minimizar_por_inclusion(cand)

    # --- Paso 2: Procesar filas restantes ---
    for r in range(1, R):
        nuevos = []
        for s in cand:
            # Si el candidato ya cubre la fila 'r', sobrevive
            if cubre_fila(MB, s, r):
                nuevos.append(s[:])
            else:
                # Si no, intentamos extenderlo con columnas que tengan un '1' en 'r'
                for j in range(C):
                    # Solo añadimos columnas que tengan 1 y no estén ya en 's'
                    if MB[r][j] == 1 and j not in s:
                        t = s + [j]
                        t.sort()
                        if t not in nuevos:
                            nuevos.append(t)
        
        # Poda por inclusión al final de cada fila
        cand = minimizar_por_inclusion(nuevos)

    # --- Paso 3: Filtrar Tipicidad Final ---
    # De los testores válidos, nos quedamos solo con los Típicos
    testores_validos = cand
    tipicos_list = minimizar_por_inclusion([s for s in testores_validos if tiene_testigos(MB, s)])
    
    # Convertir a set de frozensets para estandarizar con YYC
    return {frozenset(t) for t in tipicos_list}
