import os
import sys
from fractions import Fraction
from decimal import Decimal, InvalidOperation

def formatear_a_fraccion(valor) -> str:
    """Toma una String, un par de numerador y denominador, un Rational, o un flotante
    
    Lo convierte a cadena con formato fraccion a/b"""
    valor = Fraction(valor)
    return str(valor)

def _obtener_numero(texto):
    """Retorna Fraction en base a numero ingresado.

    ValueError si el el valor no es valido.
    """
    texto = str(texto).strip()
    if not texto:
        raise ValueError("Entrada vacía: se esperaba un número")
    try:
        return Fraction(int(texto))
    except ValueError:
        pass
    try:
        decimal = Decimal(texto)
        if not decimal.is_finite():
            raise ValueError(f'"{texto}" no es un número finito válido')
        return Fraction(decimal)
    except InvalidOperation:
        raise ValueError(f'"{texto}" no es un número entero ni flotante válido')

def leer_int(prompt:str):
    """Leer entero positivo."""
    while True:
        entrada = input(prompt).strip()
        try:
            value = int(entrada)
            if value <= 0:
                print("Debe ser un número entero positivo. Intenta de nuevo.")
                continue
            return value
        except ValueError:
            print(f'"{entrada}" no es un número entero válido. Intenta de nuevo.')

def leer_fraccion(prompt:str):
    """Leer int o float, regresar como Fraction usando obtener_numero."""
    while True:
        entrada = input(prompt).strip()
        try:
            return _obtener_numero(entrada)
        except ValueError as error:
            print(f"Entrada inválida: {error}. Intenta de nuevo.")

def leer_fila_matriz(n):
    """Leer una fila de n elementos separados por espacio."""
    while True:
        entrada = input(f"  Ingresa los {n} coeficientes separados por espacio: ").strip()
        coeficientes = entrada.split()
        if len(coeficientes) != n:
            print(
                f"Se esperaban exactamente {n} valores y se recibieron "
                f"{len(coeficientes)}. Intenta de nuevo."
            )
            continue
        try:
            return [_obtener_numero(parte) for parte in coeficientes]
        except ValueError as error:
            print(f"Entrada inválida: {error}. Intenta de nuevo.")

def leer_opcion(prompt:str, lower:int, upper:int) -> int:
    """Lee un entero dentro del rango cerrado [lower, upper]."""
    while True:
        entrada = input(prompt).strip()
        try:
            valor = int(entrada)
            if lower <= valor <= upper:
                return valor
            print(f"Opción fuera de rango (se esperaba entre {lower} y {upper}).")
        except ValueError:
            print(f'"{entrada}" no es un número entero válido.')

def formatear_a_decimal(valor:Fraction | str | Decimal) -> str:
    """Fraccion, string u objeto Decimal a decimal(string)."""
    texto = f"{float(valor):.6f}".rstrip("0").rstrip(".")
    return texto if texto not in ("", "-") else "0"

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