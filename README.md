# Proyecto 1: Método de Montante

Aplicación CLI interactiva que resuelve sistemas de ecuaciones lineales cuadrados
usando el **método de Montante** (algoritmo de Bareiss). Implementa aritmética
exacta con `Fraction`, por lo que los resultados no sufren errores de
redondeo.

## Características

- **Entrada interactiva** del sistema de ecuaciones: matriz cuadrada de
  coeficientes y los términos independientes de cada ecuación.
- **Menu completo** para:
  - Ingresar / reingresar el sistema de ecuaciones.
  - Editar cualquier coeficiente o término independiente.
  - Obtener los resultados (las incógnitas) mediante el método de Montante.
  - Obtener la **matriz adjunta**.
  - Obtener la **matriz inversa**.
  - Mostrar el **determinante** de la matriz.
  - Mostrar el sistema actual.
- **Validación de entrada**: todos los datos se verifican con `try/except`;
  solo se aceptan números enteros o flotantes. Los errores se notifican y se
  vuelve a pedir la entrada.
- **Comprobación de solvencia previa**: se aplica el teorema de Rouché-Frobenius
  (rango de la matriz de coeficientes contra el rango de la matriz aumentada)
  antes de aplicar el método, evitando operar sobre sistemas no resolubles o
  sin solución única.
- **Solo librerías estándar**: no requiere dependencias externas.
- **Consola limpia**: detecta el sistema operativo (`os.name`) y limpia la
  pantalla tras cada opción del menú, con una pausa tipo `pause` de Windows
  para poder leer el resultado antes de limpiar.

## Requisitos

- Python 3.x (sin librerías de terceros).

## Instalación y ejecución

```bash
python3 main.py
```

## Uso

Al iniciar se muestra el menú:

```
 1) Ingresar / reingresar el sistema de ecuaciones
 2) Editar matriz o términos independientes
 3) Obtener resultados de las ecuaciones
 4) Obtener la matriz adjunta
 5) Obtener la matriz inversa
 6) Mostrar el determinante de la matriz
 7) Mostrar el sistema actual
 8) Salir
```

Ejemplo de entrada (sistema 3×3):

```
Tamaño de la matriz cuadrada (n): 3
Ecuación 1:
  Ingresa los 3 coeficientes separados por espacio: 2 1 -1
Ecuación 2:
  Ingresa los 3 coeficientes separados por espacio: -3 -1 2
Ecuación 3:
  Ingresa los 3 coeficientes separados por espacio: -2 1 2
  ¿A qué es igual la ecuación 1? 8
  ¿A qué es igual la ecuación 2? -11
  ¿A qué es igual la ecuación 3? -3
```

Salida esperada:

```
Resultados de las ecuaciones:
  x1 = 2  ≈  2
  x2 = 3  ≈  3
  x3 = -1  ≈  -1
```

## El método de Montante

El método de Montante (o algoritmo de Bareiss) es una variante exacta de la
eliminación gaussiana. Sobre la matriz aumentada `[A | b]` de orden `n × (n+1)`
se ejecutan `n` etapas con la recurrencia:

```
                a_kk · a_ij − a_ik · a_kj
a_ij  =  ─────────────────────────────────
                    a_(k-1)(k-1)
```

con `a_(-1)(-1) = 1`. Cada pivote se busca reordenando filas si es cero, y
todas las operaciones son aritmética exacta de enteros/racionales, lo que
evita la acumulación del error de redondeo. Al finalizar, el último elemento
de la diagonal proporciona el determinante y la columna de términos
independientes las soluciones `x_i`.

- **determinante**: pivote final del proceso de eliminación.
- **Matriz adjunta**: transpuesta de la matriz de cofactores (determinantes de
  menores).
- **Matriz inversa**: `adjunta / determinante`.

## Estructura del proyecto

```
.
├── main.py               # Punto de entrada
├── README.md
└── modules/
    ├── __init__.py
    ├── montante.py       # Método de Montante, determinante, adjunta, inversa, solvencia
    └── menu.py           # CLI interactiva, validación y control de consola
```

## Descripción de módulos

| Módulo | Responsabilidad |
| ------ | --------------- |
| `main.py` | Inicia la aplicación desde `modules.menu.run`. |
| `modules/montante.py` | Núcleo matemático: `montante_eliminate`, `determinante`, `solve_system`, `adjugate`, `inverse`, `solvability`, `parse_number`. Usa `fractions` y `decimal` (estándar). |
| `modules/menu.py` | Menú interactivo, lectura con validación de entrada, pausa y limpieza de consola según el SO. |