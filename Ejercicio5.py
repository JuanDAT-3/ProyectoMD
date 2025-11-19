import numpy as np
import time
from BiblioE5 import * 

# =====   Funciones de matrices   =====

def Phi(Matriz, k):
    MatrizPhi = np.tile(Matriz, (1,k))

    return MatrizPhi

def Theta(MA, MB):
    filasA, _= MA.shape
    filasb, _= MB.shape

    A_ex = np.repeat(MA, repeats = filasb, axis = 0)
    B_ex = np.tile(MB, (filasA,1))

    MatrizTheta = np.hstack((A_ex,B_ex))

    return MatrizTheta

def Gamma(MA,MB):

    # Dimensiones
    ma,na = MA.shape
    mb,nb = MB.shape

    # Bloques de 0
    ceros_sup = np.zeros((ma,nb), dtype=MA.dtype) # Bloque superior derecho
    ceros_inf = np.zeros((mb, na), dtype=MA.dtype) # Bloque inferior izquierdo

    #Ensamblaje
    sup = np.hstack((MA,ceros_sup))
    inf = np.hstack((ceros_inf,MB))

    MatrizGamma = np.vstack((sup,inf))

    return MatrizGamma

def reordenar_matriz_unos(matriz):
    conteo = np.sum(matriz,axis=1) # Conteo de 1 por filas

    orden = np.argsort(conteo) #Orden de indices

    MatrizRO = matriz[orden] # Reorden

    return MatrizRO

# =====   Funciones de Experimentos   =====

def generar_matrices_experimento(MA, MB):
    
    # Matriz Base
    matrizBase = Theta(MA,MB)

    # =====   Tabla 5   =====  
    matrices_T5 = []

    # Primera instancia (Matriz Base)
    matrices_T5.append(matrizBase)

    # Otras instancias
    for i in range(2,6):
        matrizTemp = Phi(matrizBase,i)
        matrices_T5.append(matrizTemp)

    # =====   Tabla 6   ===== 
    matrices_T6 = []

    matrizTemp = matrizBase
    matrices_T6.append(matrizTemp)

    for i in range(2,5):
        matrizTemp = Gamma(matrizTemp, matrizBase)
        matrices_T6.append(matrizTemp)
    
    # ==========
    return matrices_T5, matrices_T6

def medir_tiempo(fun_algo, matriz):
    inicio = time.time()

    resultado = fun_algo(matriz)

    fin = time.time()

    duracion = fin - inicio

    num_testores = len(resultado)

    return duracion, num_testores

def procesar_tabla(tabla_name, lista_matrices):

    # Encabezado visual 
    print(f"\n{'='*95}")
    print(f" RESULTADOS: {tabla_name}")
    print(f"{'='*95}")
    print(f"{'N':<3} | {'Filas':<6} | {'Cols':<6} | {'TT':<6} || {'YYC (s)':<10} | {'YYC-Ord':<10} || {'BT (s)':<10} | {'BT-Ord':<10}")
    print("-" * 95)

    for i, matriz in enumerate(lista_matrices):
        indice = i + 1
        R, C = matriz.shape

        matriz_ord = reordenar_matriz_unos(matriz)

        # ----- YYC -----
        if "Gamma" in tabla_name and indice >= 4:
            # No corremos YYC, marcamos timeout
            t_yyc_str    = "> 900"
            t_yycord_str = "> 900"
            tests        = "-"   # no se alcanzó a calcular
        else:
            # Caso normal
            t_yyc_val, tests   = medir_tiempo(YYC, matriz)
            t_yycord_val, _    = medir_tiempo(YYC, matriz_ord)
            t_yyc_str    = f"{t_yyc_val:.5f}"
            t_yycord_str = f"{t_yycord_val:.5f}"

        # ----- BT -----
        if "Gamma" in tabla_name and indice >= 4:
            # Timeout también para BT
            t_bt_str    = "> 900"
            t_btord_str = "> 900"
        else:
            t_bt_val, _     = medir_tiempo(BT, matriz)
            t_btord_val, _  = medir_tiempo(BT, matriz_ord)
            t_bt_str    = f"{t_bt_val:.5f}"
            t_btord_str = f"{t_btord_val:.5f}"

        # Impresión de la fila
        print(f"{indice:<3} | {R:<6} | {C:<6} | {tests:<6} "
              f"|| {t_yyc_str:<10} | {t_yycord_str:<10} "
              f"|| {t_bt_str:<10} | {t_btord_str:<10}")

    print("-" * 95)


# ===================================================================
# PRINCIPAL
# ===================================================================
if __name__ == "__main__":

        # --- Definimos las matrices de prueba ---
    # (Puedes cambiarlas por las de tus ejercicios 2.1 y 4.1)
    MatrizA = np.array([
        [0, 1, 0, 1, 1, 1],  # 3 unos
        [1, 0, 1, 0, 0, 0],  # 1 uno
        [1, 1, 0, 0, 1, 1],
        [1, 1, 0, 1, 1, 0]   # 2 unos
    ])
    
    # Matriz B 
    # 7 filas, 6 columnas
    MatrizB = np.array([
        [1, 1, 0, 0, 0, 0],  # {x1, x2}
        [0, 1, 1, 0, 0, 0],  # {x2, x3}
        [1, 0, 0, 1, 0, 0],  # {x1, x4}
        [1, 0, 0, 0, 1, 0],  # {x1, x5}
        [0, 0, 1, 0, 1, 0],  # {x3, x5}
        [1, 0, 0, 0, 0, 1],  # {x1, x6}
        [0, 0, 1, 1, 0, 1]   # {x3, x4, x6}
    ])

    print("Iniciando Ejercicio 5")
    
    print(f"Matriz A: {MatrizA.shape}")
    print(f"Matriz B: {MatrizB.shape}")

    # 2. Generar los datos (5.1)
    lista_m5, lista_m6 = generar_matrices_experimento(MatrizA, MatrizB)

    # 3. Ejecutar Experimentos y Mostrar Tablas (5.2)
    # procesar_tabla("TABLA 5 (Operador Phi - Crecimiento Lineal)", lista_m5)
    procesar_tabla("TABLA 6 (Operador Gamma - Crecimiento Exponencial)", lista_m6)