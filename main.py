import json
import os
import random
import time
from dataclasses import dataclass, asdict
from typing import Dict, List, Tuple, Set, Optional

# ------------------------------------------------------
# MODELOS DE DATOS
# ------------------------------------------------------

Symbol = str
Production = List[Symbol]
Grammar = Dict[str, List[Production]]


@dataclass
class CasoPrueba:
    cadena: str
    tipo: str  # "valida", "invalida", "extrema"
    profundidad: int
    longitud: int
    num_mutaciones: int


# ------------------------------------------------------
# UTILIDADES BÁSICAS
# ------------------------------------------------------


def limpiar_linea(linea: str) -> str:
    """Elimina comentarios y espacios innecesarios de una línea de gramática."""
    linea = linea.strip()
    if "#" in linea:
        linea = linea.split("#", 1)[0]
    return linea.strip()


# ------------------------------------------------------
# CARGA Y REPRESENTACIÓN DE LA GRAMÁTICA
# ------------------------------------------------------


def cargar_gramatica(path: str) -> Tuple[Grammar, str, Set[str]]:
    """
    Carga una gramática desde un archivo .txt.
    Formato esperado:
        E -> E + T | T
        T -> T * F | F
        F -> ( E ) | num
    Retorna:
        - diccionario {NoTerminal: [ [simbolos], ... ]}
        - símbolo inicial
        - conjunto de no terminales
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"No se encontró el archivo de gramática: {path}")

    producciones: Grammar = {}
    no_terminales: Set[str] = set()
    orden_no_terminales: List[str] = []

    with open(path, "r", encoding="utf-8") as f:
        for linea in f:
            linea = limpiar_linea(linea)
            if not linea:
                continue

            if "->" not in linea:
                raise ValueError(f"Línea de gramática inválida (falta '->'): {linea}")

            lhs, rhs = linea.split("->", 1)
            lhs = lhs.strip()
            rhs = rhs.strip()

            if lhs not in no_terminales:
                no_terminales.add(lhs)
                orden_no_terminales.append(lhs)

            alternativas = [alt.strip() for alt in rhs.split("|")]
            for alt in alternativas:
                if not alt:
                    continue
                simbolos = [s for s in alt.split(" ") if s]
                producciones.setdefault(lhs, []).append(simbolos)

    if not orden_no_terminales:
        raise ValueError("La gramática está vacía o mal definida.")

    simbolo_inicial = orden_no_terminales[0]
    return producciones, simbolo_inicial, no_terminales


def es_terminal(simbolo: Symbol, no_terminales: Set[str]) -> bool:
    """Determina si un símbolo es terminal (no aparece en el conjunto de no terminales)."""
    return simbolo not in no_terminales


# ------------------------------------------------------
# DERIVACIÓN: GENERACIÓN DE CADENAS VÁLIDAS
# ------------------------------------------------------


def derivar_recursivo(
    gramatica: Grammar,
    no_terminales: Set[str],
    cadena_actual: List[Symbol],
    profundidad_actual: int,
    max_profundidad: int,
    max_longitud: int,
) -> Optional[Tuple[List[Symbol], int]]:
    """
    Intenta derivar una cadena de terminales a partir de cadena_actual.
    Retorna:
        (lista_de_simbolos_terminales, profundidad_alcanzada) o None si falla.
    """

    # Si superamos la profundidad, cortamos
    if profundidad_actual > max_profundidad:
        return None

    # Si todos son terminales, verificamos longitud
    if all(es_terminal(s, no_terminales) for s in cadena_actual):
        longitud_terminas = len([s for s in cadena_actual if es_terminal(s, no_terminales)])
        if longitud_terminas <= max_longitud:
            return cadena_actual, profundidad_actual
        return None

    # Elegimos un no terminal a expandir
    indices_no_terminales = [
        i for i, s in enumerate(cadena_actual) if not es_terminal(s, no_terminales)
    ]
    if not indices_no_terminales:
        return None

    idx = random.choice(indices_no_terminales)
    nt = cadena_actual[idx]
    producciones = gramatica.get(nt, [])

    if not producciones:
        return None

    # Probamos producciones en orden aleatorio para mayor variedad
    for prod in random.sample(producciones, len(producciones)):
        nueva_cadena = cadena_actual[:idx] + prod + cadena_actual[idx + 1 :]

        # Chequeo simple de longitud aproximada
        term_count = len([s for s in nueva_cadena if es_terminal(s, no_terminales)])
        if term_count > max_longitud * 2:
            continue

        resultado = derivar_recursivo(
            gramatica,
            no_terminales,
            nueva_cadena,
            profundidad_actual + 1,
            max_profundidad,
            max_longitud,
        )
        if resultado is not None:
            return resultado

    return None


def generar_cadena_valida(
    gramatica: Grammar,
    simbolo_inicial: str,
    no_terminales: Set[str],
    max_profundidad: int,
    max_longitud: int,
    reintentos: int = 50,
) -> Tuple[str, int, int]:
    """
    Genera una cadena válida (solo terminales) mediante derivación.
    Retorna: (cadena, profundidad, longitud).
    """
    for _ in range(reintentos):
        resultado = derivar_recursivo(
            gramatica,
            no_terminales,
            [simbolo_inicial],
            profundidad_actual=0,
            max_profundidad=max_profundidad,
            max_longitud=max_longitud,
        )
        if resultado is not None:
            simbolos, profundidad = resultado
            terminales = [s for s in simbolos if es_terminal(s, no_terminales)]
            cadena = " ".join(terminales)
            longitud = len(terminales)
            return cadena, profundidad, longitud

    raise RuntimeError(
        "No se pudo generar una cadena válida con los parámetros dados "
        f"(profundidad={max_profundidad}, longitud={max_longitud})."
    )


# ------------------------------------------------------
# GENERACIÓN DE CASOS EXTREMOS
# ------------------------------------------------------


def generar_cadena_extrema(
    gramatica: Grammar,
    simbolo_inicial: str,
    no_terminales: Set[str],
    max_profundidad: int,
    max_longitud: int,
    umbral_profundidad_extrema: int,
    umbral_longitud_extrema: int,
    reintentos: int = 100,
) -> Tuple[str, int, int]:
    """
    Genera una cadena válida pero 'extrema' (muy profunda o muy larga).
    Retorna: (cadena, profundidad, longitud).
    """
    for _ in range(reintentos):
        cadena, profundidad, longitud = generar_cadena_valida(
            gramatica,
            simbolo_inicial,
            no_terminales,
            max_profundidad=max_profundidad,
            max_longitud=max_longitud,
        )
        if profundidad >= umbral_profundidad_extrema or longitud >= umbral_longitud_extrema:
            return cadena, profundidad, longitud

    # Si no se consigue algo realmente extremo, devolvemos la última válida
    return cadena, profundidad, longitud


# ------------------------------------------------------
# GENERACIÓN DE CASOS INVÁLIDOS (MUTACIÓN)
# ------------------------------------------------------


def mutar_cadena(cadena: str, nivel: int = 1) -> Tuple[str, int]:
    """
    Aplica mutaciones sintácticas simples sobre una cadena.
    nivel = cuántas mutaciones se aplican.
    Retorna: (cadena_mutada, num_mutaciones).
    """
    if not cadena:
        return cadena, 0

    caracteres = list(cadena)
    operadores = "+-*/%"
    num_mutaciones = 0

    for _ in range(nivel):
        if not caracteres:
            break

        tipo = random.choice(["borrar", "insertar_op", "reemplazar", "parentesis"])
        i = random.randrange(len(caracteres))

        if tipo == "borrar":
            caracteres.pop(i)
            num_mutaciones += 1

        elif tipo == "insertar_op":
            op = random.choice(operadores)
            caracteres.insert(i, op)
            num_mutaciones += 1

        elif tipo == "reemplazar":
            nuevo = random.choice(list(operadores) + ["(", ")", "x", "?", "@" ""])
            caracteres[i] = nuevo
            num_mutaciones += 1

        elif tipo == "parentesis":
            # Remover un paréntesis si existe
            indices_par = [idx for idx, c in enumerate(caracteres) if c in "()"]
            if indices_par:
                j = random.choice(indices_par)
                caracteres.pop(j)
                num_mutaciones += 1

    return "".join(caracteres), num_mutaciones


# ------------------------------------------------------
# CÁLCULO DE MÉTRICAS / REPORTE
# ------------------------------------------------------


def calcular_metricas(casos: List[CasoPrueba]) -> Dict[str, object]:
    """Calcula las métricas pedidas en el enunciado del proyecto."""
    total = len(casos)
    if total == 0:
        return {}

    por_tipo = {"valida": 0, "invalida": 0, "extrema": 0}
    longitudes = []
    profundidades = []
    mutaciones = []
    operadores_conteo = {op: 0 for op in ["+", "-", "*", "/", "%"]}

    for c in casos:
        por_tipo[c.tipo] = por_tipo.get(c.tipo, 0) + 1
        longitudes.append(c.longitud)
        profundidades.append(c.profundidad)
        mutaciones.append(c.num_mutaciones)

        for ch in c.cadena:
            if ch in operadores_conteo:
                operadores_conteo[ch] += 1

    distribucion = {
        tipo: (por_tipo[tipo] / total) * 100 for tipo in por_tipo
    }

    metricas = {
        "total_cadenas": total,
        "por_tipo": por_tipo,
        "distribucion_porcentual": distribucion,
        "longitud_promedio": sum(longitudes) / len(longitudes),
        "profundidad_maxima": max(profundidades),
        "operadores_por_tipo": operadores_conteo,
        "mutaciones_promedio": sum(mutaciones) / len(mutaciones),
    }

    return metricas


def imprimir_metricas(metricas: Dict[str, object]) -> None:
    """Muestra las métricas en consola de forma legible."""
    if not metricas:
        print("No hay métricas para mostrar.")
        return

    print("\n=== REPORTE ESTADÍSTICO ===")
    print(f"Total de cadenas generadas: {metricas['total_cadenas']}")
    print("Por tipo:")
    for tipo, cant in metricas["por_tipo"].items():
        porc = metricas["distribucion_porcentual"][tipo]
        print(f"  - {tipo}: {cant} ({porc:.2f}%)")

    print(f"Longitud promedio de las expresiones: {metricas['longitud_promedio']:.2f}")
    print(f"Profundidad máxima alcanzada: {metricas['profundidad_maxima']}")
    print("Operadores generados por tipo:")
    for op, cant in metricas["operadores_por_tipo"].items():
        print(f"  {op}: {cant}")
    print(f"Mutaciones promedio (cadenas inválidas): {metricas['mutaciones_promedio']:.2f}")
    print("============================\n")


# ------------------------------------------------------
# EXPORTACIÓN A JSON / ARCHIVOS
# ------------------------------------------------------


def exportar_casos_json(casos: List[CasoPrueba], path_salida: str) -> None:
    """Exporta la lista de casos de prueba a un archivo JSON."""
    datos = [asdict(c) for c in casos]
    os.makedirs(os.path.dirname(path_salida), exist_ok=True)
    with open(path_salida, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)


def guardar_reporte_metricas(metricas: Dict[str, object], path_salida: str) -> None:
    """Guarda un reporte de métricas en un archivo de texto."""
    os.makedirs(os.path.dirname(path_salida), exist_ok=True)
    with open(path_salida, "w", encoding="utf-8") as f:
        if not metricas:
            f.write("No hay métricas disponibles.\n")
            return

        f.write("REPORTE ESTADÍSTICO DEL GENERADOR\n")
        f.write("=================================\n\n")
        f.write(f"Total de cadenas generadas: {metricas['total_cadenas']}\n")
        f.write("Por tipo:\n")
        for tipo, cant in metricas["por_tipo"].items():
            porc = metricas["distribucion_porcentual"][tipo]
            f.write(f"  - {tipo}: {cant} ({porc:.2f}%)\n")
        f.write(
            f"\nLongitud promedio de las expresiones: "
            f"{metricas['longitud_promedio']:.2f}\n"
        )
        f.write(
            f"Profundidad máxima alcanzada: {metricas['profundidad_maxima']}\n"
        )
        f.write("Operadores generados por tipo:\n")
        for op, cant in metricas["operadores_por_tipo"].items():
            f.write(f"  {op}: {cant}\n")
        f.write(
            f"\nMutaciones promedio (cadenas inválidas): "
            f"{metricas['mutaciones_promedio']:.2f}\n"
        )


# ------------------------------------------------------
# INTERFAZ DE CONSOLA
# ------------------------------------------------------


def pedir_int(mensaje: str, por_defecto: int) -> int:
    """Lee un entero desde consola con valor por defecto."""
    txt = input(f"{mensaje} [{por_defecto}]: ").strip()
    if not txt:
        return por_defecto
    try:
        return int(txt)
    except ValueError:
        print("Valor inválido, usando valor por defecto.")
        return por_defecto


def menu_principal():
    print("==========================================")
    print(" GENERADOR AUTOMÁTICO DE CASOS DE PRUEBA ")
    print(" A PARTIR DE UNA GRAMÁTICA LIBRE DE CONTEXTO ")
    print("==========================================\n")


def main():
    random.seed()

    menu_principal()

    # 1. Cargar gramática
    ruta_gramatica = input(
        "Ruta del archivo de gramática [.txt] "
        "(por defecto: gramaticas/aritmetica.txt): "
    ).strip()
    if not ruta_gramatica:
        ruta_gramatica = "gramaticas/aritmetica.txt"

    try:
        gramatica, simbolo_inicial, no_terminales = cargar_gramatica(ruta_gramatica)
    except Exception as e:
        print(f"Error al cargar la gramática: {e}")
        return

    print(f"\nGramática cargada correctamente.")
    print(f"Símbolo inicial: {simbolo_inicial}")
    print(f"No terminales: {', '.join(sorted(no_terminales))}\n")

    # 2. Configuración del usuario
    cantidad_validas = pedir_int("Cantidad de casos VÁLIDOS a generar", 10)
    cantidad_invalidas = pedir_int("Cantidad de casos INVÁLIDOS a generar", 10)
    cantidad_extremas = pedir_int("Cantidad de casos EXTREMOS a generar", 5)

    max_profundidad = pedir_int("Profundidad máxima de derivación", 10)
    max_longitud = pedir_int("Longitud máxima (en símbolos terminales)", 15)

    umbral_profundidad_extrema = pedir_int(
        "Umbral de profundidad para considerar EXTREMA", max_profundidad - 2
    )
    umbral_longitud_extrema = pedir_int(
        "Umbral de longitud para considerar EXTREMA", max_longitud - 3
    )

    nivel_mutacion = pedir_int(
        "Nivel de mutación para casos inválidos (número de cambios)", 2
    )

    casos: List[CasoPrueba] = []

    print("\nGenerando casos de prueba...\n")

    # 3. Generación de casos válidos
    t0 = time.perf_counter()
    for _ in range(cantidad_validas):
        cadena, profundidad, longitud = generar_cadena_valida(
            gramatica,
            simbolo_inicial,
            no_terminales,
            max_profundidad=max_profundidad,
            max_longitud=max_longitud,
        )
        casos.append(
            CasoPrueba(
                cadena=cadena,
                tipo="valida",
                profundidad=profundidad,
                longitud=longitud,
                num_mutaciones=0,
            )
        )
    t1 = time.perf_counter()
    print(f"- Casos válidos generados en {t1 - t0:.4f} segundos.")

    # 4. Generación de casos extremos
    t0 = time.perf_counter()
    for _ in range(cantidad_extremas):
        cadena, profundidad, longitud = generar_cadena_extrema(
            gramatica,
            simbolo_inicial,
            no_terminales,
            max_profundidad=max_profundidad,
            max_longitud=max_longitud,
            umbral_profundidad_extrema=umbral_profundidad_extrema,
            umbral_longitud_extrema=umbral_longitud_extrema,
        )
        casos.append(
            CasoPrueba(
                cadena=cadena,
                tipo="extrema",
                profundidad=profundidad,
                longitud=longitud,
                num_mutaciones=0,
            )
        )
    t1 = time.perf_counter()
    print(f"- Casos extremos generados en {t1 - t0:.4f} segundos.")

    # 5. Generación de casos inválidos por mutación
    t0 = time.perf_counter()

    # Usaremos cadenas válidas como base
    if not casos:
        print("No hay casos base para generar inválidos.")
    else:
        validas_para_mutar = [c for c in casos if c.tipo == "valida"]
        if not validas_para_mutar:
            validas_para_mutar = casos[:]  # fallback

        for _ in range(cantidad_invalidas):
            base = random.choice(validas_para_mutar)
            cadena_mutada, num_mut = mutar_cadena(base.cadena, nivel=nivel_mutacion)
            casos.append(
                CasoPrueba(
                    cadena=cadena_mutada,
                    tipo="invalida",
                    profundidad=base.profundidad,
                    longitud=len(cadena_mutada.split()),
                    num_mutaciones=num_mut,
                )
            )

    t1 = time.perf_counter()
    print(f"- Casos inválidos generados en {t1 - t0:.4f} segundos.\n")

    # 6. Cálculo de métricas
    metricas = calcular_metricas(casos)
    imprimir_metricas(metricas)

    # 7. Exportar resultados
    ruta_json = os.path.join("salida", "casos_generados.json")
    ruta_reporte = os.path.join("salida", "reporte_metricas.txt")
    exportar_casos_json(casos, ruta_json)
    guardar_reporte_metricas(metricas, ruta_reporte)

    print(f"Casos de prueba exportados a: {ruta_json}")
    print(f"Reporte de métricas guardado en: {ruta_reporte}")
    print("\nProyecto completado. Puedes usar estos archivos como evidencia en el informe.")


if __name__ == "__main__":
    main()