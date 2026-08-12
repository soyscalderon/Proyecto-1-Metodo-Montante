import os
import sys
from fractions import Fraction

from modules.montante import (
    MontanteError,
    adjugate,
    determinant,
    format_fraction,
    inverse,
    parse_number,
    solvability,
    solve_system,
)


def read_int(prompt):
    """Read a positive integer, retrying until the input is valid."""
    while True:
        raw = input(prompt).strip()
        try:
            value = int(raw)
            if value <= 0:
                print("Debe ser un número entero positivo. Intenta de nuevo.")
                continue
            return value
        except ValueError:
            print(f'"{raw}" no es un número entero válido. Intenta de nuevo.')


def read_fraction(prompt):
    """Read a numeric value (integer or float), retrying until valid."""
    while True:
        raw = input(prompt).strip()
        try:
            return parse_number(raw)
        except MontanteError as error:
            print(f"Entrada inválida: {error}. Intenta de nuevo.")


def read_row(size):
    """Read one row of `size` numbers separated by whitespace."""
    while True:
        raw = input(f"  Ingresa los {size} coeficientes separados por espacio: ").strip()
        parts = raw.split()
        if len(parts) != size:
            print(
                f"Se esperaban exactamente {size} valores y se recibieron "
                f"{len(parts)}. Intenta de nuevo."
            )
            continue
        try:
            return [parse_number(part) for part in parts]
        except MontanteError as error:
            print(f"Entrada inválida: {error}. Intenta de nuevo.")


def read_choice(prompt, lower, upper):
    """Read an integer option inside [lower, upper]."""
    while True:
        raw = input(prompt).strip()
        try:
            value = int(raw)
            if lower <= value <= upper:
                return value
            print(f"Opción fuera de rango (se esperaba entre {lower} y {upper}).")
        except ValueError:
            print(f'"{raw}" no es un número entero válido.')


def format_decimal(value):
    """Short decimal representation of a Fraction."""
    text = f"{float(value):.6f}".rstrip("0").rstrip(".")
    return text if text not in ("", "-") else "0"


def clear_console():
    """Clear the console after each menu option.

    Detects the operative system to use the right command and only
    clears when running in an interactive terminal.
    """
    if not sys.stdin.isatty():
        return
    os.system("cls" if os.name == "nt" else "clear")


def pause():
    """Pause until the user presses a key, like Windows 'pause'.

    Lets the user read the result of an option before the console is
    cleared. Uses the native 'pause' command on Windows and a plain
    prompt elsewhere.
    """
    if not sys.stdin.isatty():
        return
    if os.name == "nt":
        os.system("pause")
    else:
        input("Presiona Enter para continuar...")


def display_matrix(matrix, title="Matriz"):
    if not matrix:
        print("  (matriz vacía)")
        return
    rows = [[format_fraction(cell) for cell in row] for row in matrix]
    columns = len(rows[0])
    widths = [
        max(len(rows[i][j]) for i in range(len(rows))) for j in range(columns)
    ]
    print(f"--- {title} ---")
    for row in rows:
        print("  " + "  ".join(cell.rjust(widths[j]) for j, cell in enumerate(row)))


class SystemState:
    def __init__(self):
        self.size = 0
        self.coefficients = []
        self.constants = []

    def is_empty(self):
        return self.size == 0


def option_enter_system(state):
    size = read_int("Tamaño de la matriz cuadrada (n): ")
    coefficients = []
    for i in range(size):
        print(f"Ecuación {i + 1}:")
        coefficients.append(read_row(size))
    constants = [
        read_fraction(f"  ¿A qué es igual la ecuación {i + 1}? ")
        for i in range(size)
    ]
    state.size = size
    state.coefficients = coefficients
    state.constants = constants
    print("\nSistema registrado correctamente.\n")
    option_show_system(state)


def option_edit_element(state):
    if state.is_empty():
        print("Primero debes ingresar el sistema (opción 1).\n")
        return
    print("Editar:")
    print("  1) Un coeficiente de la matriz")
    print("  2) Un término independiente")
    choice = read_choice("Selecciona (1-2): ", 1, 2)
    if choice == 1:
        row = read_int(f"Fila (1-{state.size}): ")
        col = read_int(f"Columna (1-{state.size}): ")
        if row > state.size or col > state.size:
            print("La posición está fuera de los límites de la matriz.\n")
            return
        value = read_fraction(f"Nuevo valor para [{row}][{col}]: ")
        state.coefficients[row - 1][col - 1] = value
        print("Coeficiente actualizado.\n")
    else:
        equation = read_int(f"Ecuación (1-{state.size}): ")
        if equation > state.size:
            print("La ecuación está fuera de rango.\n")
            return
        value = read_fraction(f"Nuevo término independiente de la ecuación {equation}: ")
        state.constants[equation - 1] = value
        print("Término independiente actualizado.\n")
    option_show_system(state)


def option_solve(state):
    if state.is_empty():
        print("Primero debes ingresar el sistema (opción 1).\n")
        return
    ok, reason = solvability(state.coefficients, state.constants)
    print(f"\nVerificación de solvencia: {reason}")
    if not ok:
        print("No se aplicará el método de Montante.\n")
        return
    if determinant(state.coefficients) == 0:
        print(
            "El sistema tiene infinitas soluciones; el método de Montante "
            "solo aplica cuando la solución es única.\n"
        )
        return
    try:
        solutions = solve_system(state.coefficients, state.constants)
    except MontanteError as error:
        print(f"No se pudo resolver el sistema: {error}\n")
        return
    print("\nResultados de las ecuaciones:")
    for i, value in enumerate(solutions, start=1):
        print(
            f"  x{i} = {format_fraction(value)}"
            f"  ≈  {format_decimal(value)}"
        )
    print()


def option_adjugate(state):
    if state.is_empty():
        print("Primero debes ingresar el sistema (opción 1).\n")
        return
    try:
        result = adjugate(state.coefficients)
    except MontanteError as error:
        print(f"No se pudo calcular la adjunta: {error}\n")
        return
    print()
    display_matrix(result, "Matriz adjunta")
    print()


def option_inverse(state):
    if state.is_empty():
        print("Primero debes ingresar el sistema (opción 1).\n")
        return
    try:
        result = inverse(state.coefficients)
    except MontanteError as error:
        print(f"No se pudo calcular la inversa: {error}\n")
        return
    print()
    display_matrix(result, "Matriz inversa")
    print()


def option_determinant(state):
    if state.is_empty():
        print("Primero debes ingresar el sistema (opción 1).\n")
        return
    value = determinant(state.coefficients)
    print(
        f"\nDeterminante de la matriz: {format_fraction(value)}"
        f"  ≈  {format_decimal(value)}\n"
    )


def option_show_system(state):
    if state.is_empty():
        print("  (no hay sistema registrado)\n")
        return
    print()
    display_matrix(state.coefficients, "Matriz de coeficientes")
    display_matrix(
        [[value] for value in state.constants], "Términos independientes"
    )
    print()


def run():
    state = SystemState()
    while True:
        clear_console()
        print("=== Método de Montante ===")
        print("Sistema de ecuaciones lineales: Ax = b\n")
        print("Menú:")
        print("  1) Ingresar / reingresar el sistema de ecuaciones")
        print("  2) Editar matriz o términos independientes")
        print("  3) Obtener resultados de las ecuaciones")
        print("  4) Obtener la matriz adjunta")
        print("  5) Obtener la matriz inversa")
        print("  6) Mostrar el determinante de la matriz")
        print("  7) Mostrar el sistema actual")
        print("  8) Salir")
        choice = read_choice("Selecciona una opción (1-8): ", 1, 8)
        try:
            if choice == 1:
                option_enter_system(state)
            elif choice == 2:
                option_edit_element(state)
            elif choice == 3:
                option_solve(state)
            elif choice == 4:
                option_adjugate(state)
            elif choice == 5:
                option_inverse(state)
            elif choice == 6:
                option_determinant(state)
            elif choice == 7:
                option_show_system(state)
            elif choice == 8:
                print("¡Hasta luego!")
                break
        except MontanteError as error:
            print(f"Error: {error}\n")
        except (KeyboardInterrupt, EOFError):
            print("\n¡Hasta luego!")
            break
        pause()
