import numpy as np

#1. Función para generar la matriz booleana aleatoria 
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
    if R > 100:
        print(f"Límite de filas excedido. Ingresa Nuevamente: ")
        R = int(input("Ingresa número de Filas (máx 100): "))
    if C > 10:
        print(f"Límite de columnas excedido. Ingresa Nuevamente: ")
        C = int(input("Ingresa número de Columnas (máx 10): "))

    print(f"Generando matriz booleana de {R}x{C}...")
    matriz_booleana = np.random.choice([True, False], size=(R, C), p=[0.7, 0.3])
    
    return matriz_booleana


# --- 2. Rutina para convertir y calcular la densidad ---
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
        for j in range(R):
            if i == j:
                continue
            
            condición_1 = np.all(matriz_booleana[j] <= matriz_booleana[i])
            condición_2 = np.any(matriz_booleana[j] < matriz_booleana[i])

            if condición_1 and condición_2: 
                es_basica[i] = False
                break    
    
    matriz_basica = matriz_booleana[es_basica]

    ##=====     Densidad    =====##

    # Número total de unos en la matriz Basica
    num_unos = np.sum(matriz_basica)

    # Número total de elementos
    num_total_elementos = matriz_basica.size

    # Calcular la densidad
    densidad = num_unos / num_total_elementos

    return matriz_basica, densidad




if __name__ == "__main__":
    # Generar matriz
    matriz_bool = generar_matriz_booleana()
    R, C = matriz_bool.shape

    print("Matriz Booleana():\n", matriz_bool)

    # Implementar rutina y calcular densidad
    matriz_basica, densidad = Matriz_basica_densidad(matriz_bool)

    print("\n" + "="*50)
    print("\n Conversión y Cálculo de Densidad\n")

    print("Matriz Básica Convertida:\n", matriz_basica)

    print(f"\nDensidad Calculada: **{densidad:.4f}** (o {densidad*100:.2f}%)")
    print("\n" + "="*50)