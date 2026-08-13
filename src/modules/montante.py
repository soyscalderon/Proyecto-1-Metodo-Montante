from fractions import Fraction
from modules.utils import formatear_a_fraccion

class Matriz:
    def __init__(self):
        self.n = 0
        self.coeficientes = []
        self.constantes = []

    def is_empty(self):
        return self.n == 0

def mostrar_matriz(matriz, title:str="Matriz"):
    if not matriz:
        print("  (Matriz vacía)")
        return
    filas = [[formatear_a_fraccion(valor) for valor in fila] for fila in matriz]
    columnas = len(filas[0])
    anchos = [
        max(len(filas[i][j]) for i in range(len(filas))) for j in range(columnas)
    ]
    print(f"--- {title} ---")
    for fila in filas:
        print("  " + "  ".join(cell.rjust(anchos[j]) for j, cell in enumerate(fila)))

def _copiar(matriz):
    return [fila[:] for fila in matriz]


def _hallar_pivote(matriz, k:int) -> bool:
    """Busca un pivote valido empezando en fila y columna k.

    Cambia filas si es necesario.
    
    Retorna False si toda la columna es 0 (Matriz singular).
    """
    if matriz[k][k] != 0:
        return True
    for fila in range(k + 1, len(matriz)):
        if matriz[fila][k] != 0:
            matriz[k], matriz[fila] = matriz[fila], matriz[k]
            return True
    return False


def eliminacion_montante(aumentada):
    """Aplica el metodo de eliminacion Montante a la matriz aumentado.

    ValueError si algun pivote es 0 (sistema singular).
    """
    matriz = _copiar(aumentada)
    n = len(matriz)
    columnas = len(matriz[0]) if n else 0
    pivote_anterior = Fraction(1)
    for k in range(n):
        if not _hallar_pivote(matriz, k):
            raise ValueError(
                "El sistema es singular: pivote igual a cero en la etapa " f"{k + 1}"
            )
        pivote = matriz[k][k]
        for i in range(n):
            if i == k:
                continue
            for j in range(columnas):
                if j == k:
                    continue
                matriz[i][j] = (
                    pivote * matriz[i][j] - matriz[i][k] * matriz[k][j]
                ) / pivote_anterior
        pivote_anterior = pivote
    return matriz


def determinante(matriz):
    """Calcular el determinantes usando el metodo Montante."""
    n = len(matriz)
    if n == 0:
        return Fraction(1)
    work = _copiar(matriz)
    sign = 1
    pivote_anterior = Fraction(1)
    for k in range(n - 1):
        if work[k][k] == 0:
            swapped = _hallar_pivote(work, k)
            if not swapped:
                return Fraction(0)
            sign = -sign
        pivote = work[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                work[i][j] = (
                    pivote * work[i][j] - work[i][k] * work[k][j]
                ) / pivote_anterior
        pivote_anterior = pivote
    return sign * work[n - 1][n - 1]


def resolver_sistema(coeficientes, constantes):
    """Solve the linear system using the Montante method.

    Returns a list of Fractions with the value of each unknown.
    Raises ValueError if the system has no unique solution.
    """
    n = len(coeficientes)
    aumentada = [fila + [b] for fila, b in zip(coeficientes, constantes)]
    reduced = eliminacion_montante(aumentada)
    last_pivote = reduced[n - 1][n - 1]
    if last_pivote == 0:
        raise ValueError(
            "El sistema no tiene solución única (determinante igual a cero)"
        )
    return [reduced[i][n] / last_pivote for i in range(n)]


def rango(matriz):
    """Row echelon rank of a matriz using exact arithmetic."""
    work = _copiar(matriz)
    n = len(work)
    columnas = len(work[0]) if n else 0
    current_fila = 0
    for col in range(columnas):
        pivote_fila = None
        for i in range(current_fila, n):
            if work[i][col] != 0:
                pivote_fila = i
                break
        if pivote_fila is None:
            continue
        work[current_fila], work[pivote_fila] = work[pivote_fila], work[current_fila]
        pivote = work[current_fila][col]
        for j in range(col, columnas):
            work[current_fila][j] /= pivote
        for i in range(n):
            if i != current_fila and work[i][col] != 0:
                factor = work[i][col]
                for j in range(col, columnas):
                    work[i][j] -= factor * work[current_fila][j]
        current_fila += 1
        if current_fila == n:
            break
    return current_fila


def resoluble(coeficientes, constantes):
    """Verificar si el sistema es resoluble.

    Retorna una tupla (es_resoluble, descripcion). Usa el teorema de Rouche-Frobenius (rango de los coeficientes vs rango de la matriz aumentada).
    """
    aumentada = [fila + [b] for fila, b in zip(coeficientes, constantes)]
    if determinante(coeficientes) != 0:
        return True, (
            "Sistema compatible determinado: solución única "
            "(determinante distinto de cero)."
        )
    rank_a = rango(coeficientes)
    rank_ab = rango(aumentada)
    if rank_a == rank_ab:
        return True, (
            "Sistema compatible indeterminado: tiene infinitas soluciones "
            "(determinante cero, rangos iguales)."
        )
    return False, (
        "Sistema incompatible: no tiene solución "
        "(determinante cero y rangos distintos)."
    )


def _menor(matriz, fila, col):
    return [
        valores_fila[:col] + valores_fila[col + 1 :]
        for valores_fila in (matriz[:fila] + matriz[fila + 1 :])
    ]


def adjunta(matriz):
    """Obtiene la adjunta de la matriz (traspuesta de la matriz de cofactores)."""
    n = len(matriz)
    if n == 1:
        return [[Fraction(1)]]
    adj = [[Fraction(0)] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            cofactor = determinante(_menor(matriz, i, j))
            if (i + j) % 2 == 1:
                cofactor = -cofactor
            adj[j][i] = cofactor
    return adj


def inversa(matriz):
    """Obtiene la matriz inversa usando adjunta/determinante.

    ValueError si la matriz es singular.
    """
    det = determinante(matriz)
    if det == 0:
        raise ValueError(
            "La matriz no tiene inversa: determinante igual a cero"
        )
    adj = adjunta(matriz)
    n = len(matriz)
    return [[adj[i][j] / det for j in range(n)] for i in range(n)]