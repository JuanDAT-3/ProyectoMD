import numpy as np
import time

# =====     Matriz Booleana (Diferencia)    ======= 
def generar_matriz_booleana():
    """
    Solicita al usuario las dimensiones (filas y columnas)
    y genera una matriz booleana (True/False) aleatoria.
    Limitacion de dimensiones a 100 filas y 10 columnas.
    """
    ## Ingreso de dimensiones de matriz.
    R = int(input("Ingresa número de Filas (máx 100): "))
    C = int(input("Ingresa número de Columnas (máx 10): "))

    # límites definidos
    while((R < 0 or R > 100) or (C < 0 or C > 10)):
        if (R < 0 or R > 100):
            print(f"Límite de filas excedido. Ingresa Nuevamente: ")
            R = int(input("Ingresa número de Filas (máx 100): "))
        if (C < 0 or C > 10):
            print(f"Límite de columnas excedido. Ingresa Nuevamente: ")
            C = int(input("Ingresa número de Columnas (máx 10): "))

    print(f"Generando matriz booleana de {R}x{C}...")
    matriz_booleana = np.random.choice([True, False], size=(R, C), p=[0.7, 0.3])
    
    return matriz_booleana
# Transformación a M Basica y calcular densidad
def Matriz_basica_densidad(matriz_booleana):
    """
    Convierte la matriz booleana a una matriz básica y calcula su densidad.
    """
    ##=====     Matriz Basica    =====##
    # Num Filas y Columna
    R,C = matriz_booleana.shape
    matriz_booleana = matriz_booleana.astype(int) #Transformación a matriz de 1 y 0

    # Asumir que todas las filas son básicas
    es_basica = np.ones(R, dtype=bool)

    # Bucle de Comprobación de filas
    for i in range(R):
        if not es_basica[i]:
            continue
        for j in range(R):
            if i == j or not es_basica[j]:
                continue
            
            condición_1 = np.all(matriz_booleana[j] <= matriz_booleana[i])
            condición_2 = np.any(matriz_booleana[j] < matriz_booleana[i])

            if condición_1 and condición_2: 
                es_basica[i] = False
                break    
    
    matriz_basica = matriz_booleana[es_basica]

    # Eliminación de Duplicados 
    matriz_basica = np.unique(matriz_basica, axis = 0)

    ##=====     Densidad    =====##

    # Número total de unos en la matriz Basica
    num_unos = np.sum(matriz_basica)
    # Número total de elementos
    num_total_elementos = matriz_basica.size

    # Calcular la densidad
    if num_total_elementos == 0:
        densidad = 0.0
    else:
        densidad = num_unos / num_total_elementos

    return matriz_basica, densidad
# Contruir Matriz A;
def Matriz_A():
    ## Ingreso de dimensiones de matriz A.
    R = int(input("Ingresa número de Filas (máx 100): "))
    C = int(input("Ingresa número de Columnas (min 6 , máx 10): "))

    # límites definidos
    while((R < 0 or R > 100) or (C < 6 or C > 10)):
        if (R < 0 or R > 100):
            print(f"Límite de filas excedido. Ingresa Nuevamente: ")
            R = int(input("Ingresa número de Filas (máx 100): "))
        if (C < 6 or C > 10):
            print(f"Límite de columnas excedido. Ingresa Nuevamente: ")
            C = int(input("Ingresa número de Columnas (min 6, máx 10): "))
    
    # Desarrollo MD Y MB
    print(f"Generando matriz booleana de {R}x{C}...")
    matriz_booleana = np.random.choice([True, False], size=(R, C), p=[0.7, 0.3])    
    matriz_A, densidad_A = Matriz_basica_densidad(matriz_booleana)
    counter = 0

    while(densidad_A < 0.5 and counter < 100):
        counter += 1 
        print("Buscando Matriz Basica de densidad mayor o igual a 0.5: \n")
        matriz_booleana = np.random.choice([True, False], size=(R, C), p=[0.7, 0.3])
        matriz_A, densidad_A = Matriz_basica_densidad(matriz_booleana)


    if (densidad_A >= 0.5):
        print("Matriz Basica A encontrada: ")
        print("Número de intentos: ", counter)
        return matriz_A, densidad_A, matriz_booleana
    else:
        print(f"Matriz de densidad 0.5 no encontrada despues de {counter} intentos, Intente nuevamente.")
        return None, 0.0
       

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

    """
    Implementa el algoritmo incremental YYC para encontrar
    el conjunto de todos los Testores Típicos (Psi*).

    Argumentos:
    MB : La Matriz Básica de entrada.

    Retorna:
    set: Un set de 'frozensets'(Tuplas), donde cada frozenset es un Testor Típico.
    """

    if MB.size == 0:
        print("Matriz Básica Vacía")
        return set()

    R,C = MB.shape
    rasgos = [f'x{j+1}' for j in range(C)] #Para Impresión
    start_time = time.perf_counter() ## Temporizador para rendimiento
    psi = set() # Conjunto de testores ψ* vacío

    #=====      Primera Fila        =====
    r1 = MB[0, :] 

    for i in range(C):
        if r1[i] == 1:
            psi.add(frozenset({i}))
    
    # Tiempo en Fila 1   
    time_fila_1 = time.perf_counter() - start_time
    # Imprimir testores Fila 1
    print_psi(psi, rasgos, "Fila 1", time_fila_1)

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
        psi_ref = set() # Set temporal para añadir testores minimos

        for tau_a in psi_aux: #Para cada testor en psi auxiliar (con testores tipicos)
            minimal = True
            for tau_b in psi_aux: # Comprobación con testor del mismo grupo.
                if tau_a !=tau_b and tau_b.issubset(tau_a):
                    minimal = False
                    break
            if minimal:
                psi_ref.add(tau_a) # Si el testor es minimo (sin subconjuntos)

        psi = psi_ref #Asigmaos el nuevo psi con solo testores minimos.

        # Calcular tiempo acumulado Fila i
        cumulative_time = time.perf_counter() - start_time
        # Imprimir testores Fila i
        print_psi(psi, rasgos, f"Fila {i+1}", cumulative_time)
    
    return psi, (time.perf_counter() - start_time), rasgos


# =====  Main   ======
if __name__ == "__main__":  
    """
    Interfaz de usuario amigable para ejecutar el algoritmo YYC.
    """
    print("="*50)
    print("  Implementación Computacional del Algoritmo YYC")
    print("="*50)
    
    while True:
        print("\nSeleccione una opción:")
        print("  1. Generar Matriz Aleatoria")
        print("  2. Generar Matriz A (0.5 de densidad)")
        print("  3. Salir")

        opc = input("Opción: ")
        
        if opc == '1':
            # 1. Generar la matriz aleatoria
            print("Generación de matriz booleana: ")
            matriz_generada = generar_matriz_booleana()
            matriz_basica , densidad = Matriz_basica_densidad(matriz_generada)
            if matriz_generada is not None:
                print("Matriz Básica de Entrada (MB):\n", matriz_basica)
                print("\n" + "="*50)
                print(f"Densidad: {densidad}.")
                print("Iniciando Algoritmo YYC...")
                
                # 2. Ejecutar el algoritmo YYC
                psi_final, tiempo_total, rasgos = YYC(matriz_basica)
                
                print("\n" + "="*50)
                print("EJECUCIÓN FINALIZADA")
               
                print("--- Testores Típicos ---")
                for i in psi_final:
                    print(format_tau(i,rasgos))
                print(f"Tiempo Total de Ejecución: {tiempo_total:.8f} segundos")
                print("--- ---------------- ---")
                print("="*50)
    
        elif opc == '2':
            matriz_A, densidad_A, matriz_bool = Matriz_A()
            
            print("Matriz Booleana para matriz A:\n", matriz_bool.astype(int))
            print("Matriz Básica de Entrada A:\n", matriz_A)
            print(f"Densidad: {densidad_A}.") 
            print("\n" + "="*50)
            
            print("¿Quieres Ejecutar algoritmo YCC en Matriz A?")
            bin = int(input("0. NO | 1. Si: "))

            while (bin < 0 or bin > 1):
                print("Ingreso no valido, intenta de nuevo")
                bin = int(input("0. NO | 1. Si: "))
            
            if(bin == 1):
                psi_final, tiempo_total, rasgos= YYC(matriz_A)
                
                print("\n" + "="*50)
                print("EJECUCIÓN FINALIZADA")
                
                print(f"Tiempo Total de Ejecución: {tiempo_total:.8f} segundos")
                print("="*50)
                break
            else:
                break
        
        elif opc == '3':
            print("Saliendo del programa.")
            break

        else:
            print("Opción no válida. intente de nuevo.")    
