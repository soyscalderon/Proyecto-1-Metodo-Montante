
from modules.montante import (
    adjunta,
    determinante,
    formatear_a_fraccion,
    inversa,
    resoluble,
    resolver_sistema,
    mostrar_matriz,
    Matriz
)

from modules.utils import (
    leer_int,
    leer_opcion,
    leer_fraccion,
    leer_fila_matriz,
    formatear_a_decimal,
    borrar_consola,
    pausar
)

def opcion_ingresar_matriz(matriz:Matriz):
    n = leer_int("Tamaño de la matriz cuadrada (n): ")
    coeficientes = []
    for i in range(n):
        print(f"Ecuación {i + 1}:")
        coeficientes.append(leer_fila_matriz(n))
    constantes = [
        leer_fraccion(f"  ¿A qué es igual la ecuación {i + 1}? ")
        for i in range(n)
    ]
    matriz.n = n
    matriz.coeficientes = coeficientes
    matriz.constantes = constantes
    print("\nSistema registrado correctamente.\n")
    opcion_mostrar_matriz(matriz)


def opcion_editar_elemento_de_matriz(matriz:Matriz):
    if matriz.is_empty():
        print("Primero debes ingresar el sistema (opción 1).\n")
        return
    print("Editar:")
    print("  1) Un coeficiente de la matriz")
    print("  2) Un término independiente")
    opcion = leer_opcion("Selecciona (1-2): ", 1, 2)
    if opcion == 1:
        fila = leer_int(f"Fila (1-{matriz.n}): ")
        col = leer_int(f"Columna (1-{matriz.n}): ")
        if fila > matriz.n or col > matriz.n:
            print("La posición está fuera de los límites de la matriz.\n")
            return
        valor = leer_fraccion(f"Nuevo valor para [{fila}][{col}]: ")
        matriz.coeficientes[fila - 1][col - 1] = valor
        print("Coeficiente actualizado.\n")
    else:
        ecuacion = leer_int(f"Ecuación (1-{matriz.n}): ")
        if ecuacion > matriz.n:
            print("La ecuación está fuera de rango.\n")
            return
        valor = leer_fraccion(f"Nuevo término independiente de la ecuación {ecuacion}: ")
        matriz.constantes[ecuacion - 1] = valor
        print("Término independiente actualizado.\n")
    opcion_mostrar_matriz(matriz)


def opcion_resolver(matriz:Matriz):
    if matriz.is_empty():
        print("Primero debes ingresar el sistema (opción 1).\n")
        return
    ok, reason = resoluble(matriz.coeficientes, matriz.constantes)
    print(f"\nVerificación de solvencia: {reason}")
    if not ok:
        print("No se aplicará el método de Montante.\n")
        return
    if determinante(matriz.coeficientes) == 0:
        print(
            "El sistema tiene infinitas soluciones; el método de Montante "
            "solo aplica cuando la solución es única.\n"
        )
        return
    try:
        soluciones = resolver_sistema(matriz.coeficientes, matriz.constantes)
    except ValueError as error:
        print(f"No se pudo resolver el sistema: {error}\n")
        return
    print("\nResultados de las ecuaciones:")
    for i, valor in enumerate(soluciones, start=1):
        print(
            f"  x{i} = {formatear_a_fraccion(valor)}"
            f"  ≈  {formatear_a_decimal(valor)}"
        )
    print()


def opcion_adjunta(matriz:Matriz):
    if matriz.is_empty():
        print("Primero debes ingresar el sistema (opción 1).\n")
        return
    try:
        resultado = adjunta(matriz.coeficientes)
    except ValueError as error:
        print(f"No se pudo calcular la adjunta: {error}\n")
        return
    print()
    mostrar_matriz(resultado, "Matriz adjunta")
    print()


def opcion_inversa(matriz:Matriz):
    if matriz.is_empty():
        print("Primero debes ingresar el sistema (opción 1).\n")
        return
    try:
        resultado = inversa(matriz.coeficientes)
    except ValueError as error:
        print(f"No se pudo calcular la inversa: {error}\n")
        return
    print()
    mostrar_matriz(resultado, "Matriz inversa")
    print()


def opcion_determinante(matriz:Matriz):
    if matriz.is_empty():
        print("Primero debes ingresar el sistema (opción 1).\n")
        return
    valor = determinante(matriz.coeficientes)
    print(
        f"\nDeterminante de la matriz: {formatear_a_fraccion(valor)}"
        f" ≈ {formatear_a_decimal(valor)}\n"
    )


def opcion_mostrar_matriz(matriz:Matriz):
    if matriz.is_empty():
        print("  (No hay sistema registrado)\n")
        return
    print()
    mostrar_matriz(matriz.coeficientes, "Matriz de coeficientes")
    mostrar_matriz(
        [[value] for value in matriz.constantes], "Términos independientes"
    )
    print()


def run():
    matriz = Matriz()
    while True:
        borrar_consola()
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
        choice = leer_opcion("Selecciona una opción (1-8): ", 1, 8)
        try:
            if choice == 1:
                opcion_ingresar_matriz(matriz)
            elif choice == 2:
                opcion_editar_elemento_de_matriz(matriz)
            elif choice == 3:
                opcion_resolver(matriz)
            elif choice == 4:
                opcion_adjunta(matriz)
            elif choice == 5:
                opcion_inversa(matriz)
            elif choice == 6:
                opcion_determinante(matriz)
            elif choice == 7:
                opcion_mostrar_matriz(matriz)
            elif choice == 8:
                print("¡Hasta luego!")
                break
        except ValueError as error:
            print(f"Error: {error}\n")
        except (KeyboardInterrupt, EOFError):
            print("\n¡Hasta luego!")
            break
        pausar()