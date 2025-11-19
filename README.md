ProyectoMD — Matemáticas Discretas

Teoría de Testores: Matrices Básicas, Algoritmos YYC y BT, y Matriz B

Universidad San Francisco de Quito (USFQ)

Profesor: Eduardo Alba
Curso: Matemáticas Discretas

Este repositorio contiene el desarrollo completo del proyecto sobre Teoría de Testores, incluyendo la implementación computacional de los algoritmos YYC y BT, el análisis de matrices básicas y la construcción de la Matriz B. El contenido sigue las instrucciones proporcionadas en el documento oficial del proyecto ProyectoTestMatDIS_202510.pdf.

Estructura del proyecto
La estructura final del repositorio será:

ProyectoMD

- Ejercicio1.py
- Ejercicio2.py
- Ejercicio3.py
- Ejercicio4.py
- Ejercicio5.py
- README.md

Descripción de los ejercicios

Ejercicio 1 — Generación de matrices aleatorias
- Se genera una matriz booleana aleatoria.
- Se obtiene su Matriz Básica (MB).
- Se calcula la densidad.
- Se imprime la matriz booleana, MB y densidad.

Ejercicio 2 — Algoritmo YYC
- Se genera una matriz básica A con al menos 6 columnas y densidad ≥ 0.5.
- Se realiza la ejecución manual del algoritmo YYC sobre A.
- Se implementa YYC en Python mostrando testores típicos y tiempo acumulado por fila.
- Se presenta la tabla final de resultados.

Ejercicio 3 — Algoritmo BT (Backtracking)
- Implementación del algoritmo BT para obtener testores y testores típicos.
- Ejecución manual y computacional.
- Medición de tiempos por fila y tiempo total.
- Comparación con el algoritmo YYC.

Ejercicio 4 — Matriz B
- Construcción de la matriz estándar B a partir de los testores típicos.
- Verificación formal de que B es una matriz básica.
- Se aplica BT sobre B para validar su estructura.

Ejercicio 5 — Conclusiones
- Comparación final entre YYC y BT.
- Relación entre las matrices A, MB y B.
- Discusión del desempeño de ambos algoritmos.

Requisitos para ejecutar los scripts necesarios:
- Python 3.8 o superior
- numpy (solo si se usa en el ejercicio 1)

Instalación de numpy:

pip install numpy

Instrucciones de ejecución

Clonar el repositorio:

git clone https://github.com/JuanDAT-3/ProyectoMD.git

cd ProyectoMD

Ejecutar cada ejercicio:

python Ejercicio1.py

python Ejercicio2.py

python Ejercicio3.py

python Ejercicio4.py

python Ejercicio5.py

Cada script muestra:
- la matriz utilizada
- los testores típicos o testores encontrados
- y los tiempos de ejecución cuando corresponde

Autores: Juan Aguilar, Gabriel Zambrano y José Díaz

Universidad San Francisco de Quito (USFQ)

Curso: Matemáticas Discretas

Profesor: Eduardo Alba