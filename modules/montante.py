from decimal import Decimal, InvalidOperation
from fractions import Fraction


class MontanteError(Exception):
    pass


def parse_number(text):
    """Parse an integer or float into an exact Fraction.

    Raises MontanteError if the input is not a valid number.
    """
    text = str(text).strip().replace(",", ".")
    if not text:
        raise MontanteError("Entrada vacía: se esperaba un número")
    try:
        return Fraction(int(text))
    except ValueError:
        pass
    try:
        decimal = Decimal(text)
        if not decimal.is_finite():
            raise MontanteError(f'"{text}" no es un número finito válido')
        return Fraction(decimal)
    except InvalidOperation:
        raise MontanteError(f'"{text}" no es un número entero ni flotante válido')


def _copy(matrix):
    return [row[:] for row in matrix]


def _find_pivot(matrix, k):
    """Look for a non-zero pivot in column k from row k downwards.

    Swaps rows if needed and returns True on success, False if the
    whole column is zero (singular matrix).
    """
    if matrix[k][k] != 0:
        return True
    for row in range(k + 1, len(matrix)):
        if matrix[row][k] != 0:
            matrix[k], matrix[row] = matrix[row], matrix[k]
            return True
    return False


def montante_eliminate(augmented):
    """Apply the Montante (Bareiss) elimination to the augmented matrix.

    The matrix is transformed so that for every row i, the value in the
    last column equals the determinant of the original coefficient matrix
    with column i replaced by the constants vector.

    Raises MontanteError if a pivot is zero (singular system).
    """
    matrix = _copy(augmented)
    n = len(matrix)
    columns = len(matrix[0]) if n else 0
    previous_pivot = Fraction(1)
    for k in range(n):
        if not _find_pivot(matrix, k):
            raise MontanteError(
                "El sistema es singular: pivote igual a cero en la etapa " f"{k + 1}"
            )
        pivot = matrix[k][k]
        for i in range(n):
            if i == k:
                continue
            for j in range(columns):
                if j == k:
                    continue
                matrix[i][j] = (
                    pivot * matrix[i][j] - matrix[i][k] * matrix[k][j]
                ) / previous_pivot
        previous_pivot = pivot
    return matrix


def determinant(matrix):
    """Compute the determinant with the Montante (Bareiss) algorithm."""
    n = len(matrix)
    if n == 0:
        return Fraction(1)
    work = _copy(matrix)
    sign = 1
    previous_pivot = Fraction(1)
    for k in range(n - 1):
        if work[k][k] == 0:
            swapped = _find_pivot(work, k)
            if not swapped:
                return Fraction(0)
            sign = -sign
        pivot = work[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                work[i][j] = (
                    pivot * work[i][j] - work[i][k] * work[k][j]
                ) / previous_pivot
        previous_pivot = pivot
    return sign * work[n - 1][n - 1]


def solve_system(coefficients, constants):
    """Solve the linear system using the Montante method.

    Returns a list of Fractions with the value of each unknown.
    Raises MontanteError if the system has no unique solution.
    """
    size = len(coefficients)
    augmented = [row + [b] for row, b in zip(coefficients, constants)]
    reduced = montante_eliminate(augmented)
    last_pivot = reduced[size - 1][size - 1]
    if last_pivot == 0:
        raise MontanteError(
            "El sistema no tiene solución única (determinante igual a cero)"
        )
    return [reduced[i][size] / last_pivot for i in range(size)]


def rank(matrix):
    """Row echelon rank of a matrix using exact arithmetic."""
    work = _copy(matrix)
    n = len(work)
    columns = len(work[0]) if n else 0
    current_row = 0
    for col in range(columns):
        pivot_row = None
        for i in range(current_row, n):
            if work[i][col] != 0:
                pivot_row = i
                break
        if pivot_row is None:
            continue
        work[current_row], work[pivot_row] = work[pivot_row], work[current_row]
        pivot = work[current_row][col]
        for j in range(col, columns):
            work[current_row][j] /= pivot
        for i in range(n):
            if i != current_row and work[i][col] != 0:
                factor = work[i][col]
                for j in range(col, columns):
                    work[i][j] -= factor * work[current_row][j]
        current_row += 1
        if current_row == n:
            break
    return current_row


def solvability(coefficients, constants):
    """Check whether the equations system is solvable before applying Montante.

    Returns a tuple (is_solvable, description). Uses the Rouche-Frobenius
    theorem (rank of coefficients vs rank of the augmented matrix).
    """
    augmented = [row + [b] for row, b in zip(coefficients, constants)]
    if determinant(coefficients) != 0:
        return True, (
            "Sistema compatible determinado: solución única "
            "(determinante distinto de cero)."
        )
    rank_a = rank(coefficients)
    rank_ab = rank(augmented)
    if rank_a == rank_ab:
        return True, (
            "Sistema compatible indeterminado: tiene infinitas soluciones "
            "(determinante cero, rangos iguales)."
        )
    return False, (
        "Sistema incompatible: no tiene solución "
        "(determinante cero y rangos distintos)."
    )


def _minor(matrix, row, col):
    return [
        row_values[:col] + row_values[col + 1 :]
        for row_values in (matrix[:row] + matrix[row + 1 :])
    ]


def adjugate(matrix):
    """Adjugate matrix (transpose of the cofactor matrix)."""
    n = len(matrix)
    if n == 1:
        return [[Fraction(1)]]
    adj = [[Fraction(0)] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            cofactor = determinant(_minor(matrix, i, j))
            if (i + j) % 2 == 1:
                cofactor = -cofactor
            adj[j][i] = cofactor
    return adj


def inverse(matrix):
    """Inverse matrix using adjugate over determinant.

    Raises MontanteError if the matrix is singular.
    """
    det = determinant(matrix)
    if det == 0:
        raise MontanteError(
            "La matriz no tiene inversa: determinante igual a cero"
        )
    adj = adjugate(matrix)
    n = len(matrix)
    return [[adj[i][j] / det for j in range(n)] for i in range(n)]


def format_fraction(value):
    """Human friendly representation of a Fraction."""
    value = Fraction(value)
    return str(value)
