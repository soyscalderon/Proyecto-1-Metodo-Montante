import os
import sys
from fractions import Fraction
from decimal import Decimal, InvalidOperation

def formatear_a_fraccion(value) -> str:
    """Toma una String, un par de numerador y denominador, un Rational, o un flotante
    
    Lo convierte a cadena con formato fraccion a/b"""
    value = Fraction(value)
    return str(value)

def obtener_numero(text):
    """Parse an integer or float into an exact Fraction.

    Raises ValueError if the input is not a valid number.
    """
    text = str(text).strip()
    if not text:
        raise ValueError("Entrada vacía: se esperaba un número")
    try:
        return Fraction(int(text))
    except ValueError:
        pass
    try:
        decimal = Decimal(text)
        if not decimal.is_finite():
            raise ValueError(f'"{text}" no es un número finito válido')
        return Fraction(decimal)
    except InvalidOperation:
        raise ValueError(f'"{text}" no es un número entero ni flotante válido')

def leer_int(prompt:str):
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


def leer_fraccion(prompt:str):
    """Read a numeric value (integer or float), retrying until valid."""
    while True:
        raw = input(prompt).strip()
        try:
            return obtener_numero(raw)
        except ValueError as error:
            print(f"Entrada inválida: {error}. Intenta de nuevo.")


def leer_fila_matriz(n):
    """Read one fila of `n` numbers separated by whitespace."""
    while True:
        raw = input(f"  Ingresa los {n} coeficientes separados por espacio: ").strip()
        parts = raw.split()
        if len(parts) != n:
            print(
                f"Se esperaban exactamente {n} valores y se recibieron "
                f"{len(parts)}. Intenta de nuevo."
            )
            continue
        try:
            return [obtener_numero(part) for part in parts]
        except ValueError as error:
            print(f"Entrada inválida: {error}. Intenta de nuevo.")


def leer_opcion(prompt:str, lower:int, upper:int) -> int:
    """Lee un entero dentro del rango cerrado [lower, upper]."""
    while True:
        raw = input(prompt).strip()
        try:
            value = int(raw)
            if lower <= value <= upper:
                return value
            print(f"Opción fuera de rango (se esperaba entre {lower} y {upper}).")
        except ValueError:
            print(f'"{raw}" no es un número entero válido.')


def formatear_a_decimal(value:Fraction | str | Decimal) -> str:
    """Short decimal representation of a Fraction."""
    text = f"{float(value):.6f}".rstrip("0").rstrip(".")
    return text if text not in ("", "-") else "0"

def borrar_consola():
    """
    Detecta el sistema operativo y si esta en TTY.\n
    Luego, borra la consola.
    """
    if not sys.stdin.isatty():
        return
    os.system("cls" if os.name == "nt" else "clear")

def pausar():
    """
    Detecta el sistema operativo y si esta en TTY.\n
    Luego, simula el comportamiento de pause en cmd.
    """
    if not sys.stdin.isatty():
        return
    if os.name == "nt":
        os.system("pause")
    else:
        input("Presiona Enter para continuar...")