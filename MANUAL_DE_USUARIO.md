# Manual de Usuario - Generador Automático de Casos de Prueba

## 📋 Tabla de Contenidos
1. [Introducción](#introducción)
2. [Requisitos del Sistema](#requisitos-del-sistema)
3. [Instalación](#instalación)
4. [Estructura del Proyecto](#estructura-del-proyecto)
5. [Cómo Usar el Programa](#cómo-usar-el-programa)
6. [Configuración de la Gramática](#configuración-de-la-gramática)
7. [Parámetros de Generación](#parámetros-de-generación)
8. [Salida del Programa](#salida-del-programa)
9. [Ejemplos Prácticos](#ejemplos-prácticos)
10. [Solución de Problemas](#solución-de-problemas)

---

## Introducción

El **Generador Automático de Casos de Prueba** es una herramienta que genera casos de prueba (test cases) de forma automática a partir de una **gramática libre de contexto** (CFG - Context-Free Grammar).

### ¿Qué hace?

El programa:
- ✅ Carga una gramática desde un archivo de texto
- ✅ Genera **casos válidos** mediante derivación según las reglas gramaticales
- ✅ Genera **casos extremos** (muy profundos o muy largos)
- ✅ Genera **casos inválidos** mediante mutación sintáctica
- ✅ Calcula **métricas estadísticas** sobre los casos generados
- ✅ Exporta los resultados a archivos JSON y reporte de texto

### ¿Para qué sirve?

Es útil para:
- Pruebas de software en compiladores o intérpretes
- Validación de procesadores de lenguajes
- Generación de datos de prueba para analizadores sintácticos
- Investigación en Teoría de la Computación

---

## Requisitos del Sistema

- **Python 3.7 o superior**
- Acceso a línea de comandos/terminal
- ~10 MB de espacio libre en disco

### Verificar versión de Python

```bash
python3 --version
```

Deberías ver algo como: `Python 3.9.0` o superior

---

## Instalación

### Paso 1: Descargar el proyecto

El proyecto ya está descargado. Navega a la carpeta del proyecto:

```bash
cd "Downloads/Mini proyecto teoria de la computacion 2/Code"
```

### Paso 2: Verificar archivos

Asegúrate de que tienes los siguientes archivos:

```
Code/
├── main.py                          # Programa principal
├── gramaticas/
│   └── aritmetica.txt               # Gramática de ejemplo
├── salida/                          # Carpeta para resultados (se crea automáticamente)
└── MANUAL_DE_USUARIO.md             # Este archivo
```

### Paso 3: Ejecutar el programa

```bash
python3 main.py
```

---

## Estructura del Proyecto

### Archivos principales

| Archivo | Descripción |
|---------|-------------|
| `main.py` | Programa principal con toda la lógica |
| `gramaticas/aritmetica.txt` | Ejemplo de gramática (expresiones aritméticas) |
| `salida/` | Carpeta donde se guardan los resultados |

### Directorio de salida

Cuando ejecutes el programa, se crearán automáticamente:

```
salida/
├── casos_generados.json             # Lista de casos en formato JSON
└── reporte_metricas.txt             # Estadísticas de los casos
```

---

## Cómo Usar el Programa

### Ejecución básica

1. Abre una terminal
2. Navega al directorio del proyecto
3. Ejecuta:
   ```bash
   python3 main.py
   ```

### Flujo de ejecución

```
┌─────────────────────────────────┐
│  INICIO DEL PROGRAMA            │
└─────────────────────────────────┘
              ↓
┌─────────────────────────────────┐
│ 1. Seleccionar archivo gramática │
└─────────────────────────────────┘
              ↓
┌─────────────────────────────────┐
│ 2. Ingresar parámetros          │
│    (cantidad, profundidad, etc) │
└─────────────────────────────────┘
              ↓
┌─────────────────────────────────┐
│ 3. Generar casos                │
│    (válidos, extremos, inválidos)│
└─────────────────────────────────┘
              ↓
┌─────────────────────────────────┐
│ 4. Calcular métricas            │
└─────────────────────────────────┘
              ↓
┌─────────────────────────────────┐
│ 5. Exportar resultados          │
└─────────────────────────────────┘
              ↓
┌─────────────────────────────────┐
│  FIN DEL PROGRAMA               │
└─────────────────────────────────┘
```

---

## Configuración de la Gramática

### Formato de archivo

Las gramáticas se definen en archivos `.txt` usando el siguiente formato:

```
NoTerminal -> producción1 | producción2 | ...
```

**Reglas:**
- Los **no terminales** son caracteres o palabras (ej: `E`, `T`, `F`, `Expr`)
- Los **terminales** son símbolos reales (números, operadores, etc.)
- Las producciones se separan con `|` (pipe)
- Se pueden agregar comentarios con `#`
- Se pueden dejar líneas vacías

### Ejemplo: Gramática de expresiones aritméticas

```plaintext
# Gramática de expresiones aritméticas simples
E -> E + T | E - T | T          # Una expresión es suma/resta o término
T -> T * F | T / F | F          # Un término es multiplicación/división o factor
F -> ( E ) | num                # Un factor es paréntesis o número
```

**Análisis:**
- **Símbolo inicial:** `E` (primer no terminal del archivo)
- **No terminales:** `E`, `T`, `F`
- **Terminales:** `+`, `-`, `*`, `/`, `(`, `)`, `num`

### Crear tu propia gramática

**Ejemplo 1: Lenguaje palindrómico**

```plaintext
S -> a S a | b S b | a | b | epsilon
```

**Ejemplo 2: Lenguaje de paréntesis balanceados**

```plaintext
S -> ( S ) | S S | epsilon
```

**Ejemplo 3: Lenguaje simple**

```plaintext
S -> a S b | ab
```

---

## Parámetros de Generación

Cuando ejecutes el programa, te pedirá que ingreses varios parámetros:

### 1. Ruta de la gramática
```
Ruta del archivo de gramática [.txt] (por defecto: gramaticas/aritmetica.txt): 
```

**Por defecto:** `gramaticas/aritmetica.txt`

**Qué hacer:**
- Presiona ENTER para usar la gramática por defecto
- O escribe la ruta de tu gramática: `gramaticas/migramatica.txt`

### 2. Cantidad de casos válidos
```
Cantidad de casos VÁLIDOS a generar [10]: 
```

**Explicación:** Número de cadenas que cumplen la gramática

**Sugerencia:** 10-50 según necesites

### 3. Cantidad de casos inválidos
```
Cantidad de casos INVÁLIDOS a generar [10]: 
```

**Explicación:** Número de cadenas mutadas (no cumplen la gramática)

**Sugerencia:** 5-20

### 4. Cantidad de casos extremos
```
Cantidad de casos EXTREMOS a generar [5]: 
```

**Explicación:** Cadenas válidas pero muy profundas o muy largas

**Sugerencia:** 2-10

### 5. Profundidad máxima de derivación
```
Profundidad máxima de derivación [10]: 
```

**Explicación:** Cuántos pasos de derivación se permiten

**Valores:**
- Bajo (5-8): Gramáticas simples, cadenas cortas
- Medio (10-15): Gramáticas normales
- Alto (20+): Gramáticas complejas

### 6. Longitud máxima de símbolos terminales
```
Longitud máxima (en símbolos terminales) [15]: 
```

**Explicación:** Número máximo de terminales en la cadena final

**Valores:**
- Bajo (5-10): Cadenas cortas
- Medio (15-25): Cadenas normales
- Alto (30+): Cadenas largas

### 7. Umbral de profundidad extrema
```
Umbral de profundidad para considerar EXTREMA [8]: 
```

**Explicación:** ¿A partir de qué profundidad una cadena se considera "extrema"?

**Sugerencia:** `max_profundidad - 2`

### 8. Umbral de longitud extrema
```
Umbral de longitud para considerar EXTREMA [12]: 
```

**Explicación:** ¿A partir de qué longitud una cadena se considera "extrema"?

**Sugerencia:** `max_longitud - 3`

### 9. Nivel de mutación
```
Nivel de mutación para casos inválidos (número de cambios) [2]: 
```

**Explicación:** Cuántos cambios sintácticos aplicar a cada caso inválido

**Valores:**
- 1: Un cambio (mutación leve)
- 2-3: Varios cambios (mutación moderada)
- 4+: Muchos cambios (mutación severa)

---

## Salida del Programa

### Consola

El programa muestra información en tiempo real:

```
==========================================
 GENERADOR AUTOMÁTICO DE CASOS DE PRUEBA 
 A PARTIR DE UNA GRAMÁTICA LIBRE DE CONTEXTO 
==========================================

Gramática cargada correctamente.
Símbolo inicial: E
No terminales: E, F, T

Generando casos de prueba...

- Casos válidos generados en 0.1234 segundos.
- Casos extremos generados en 0.0567 segundos.
- Casos inválidos generados en 0.0123 segundos.

=== REPORTE ESTADÍSTICO ===
Total de cadenas generadas: 25
Por tipo:
  - valida: 10 (40.00%)
  - invalida: 10 (40.00%)
  - extrema: 5 (20.00%)
Longitud promedio de las expresiones: 8.52
Profundidad máxima alcanzada: 9
Operadores generados por tipo:
  +: 12
  -: 8
  *: 15
  /: 5
  %: 0
Mutaciones promedio (cadenas inválidas): 2.10
============================

Casos de prueba exportados a: salida/casos_generados.json
Reporte de métricas guardado en: salida/reporte_metricas.txt
```

### Archivo JSON

**Ubicación:** `salida/casos_generados.json`

**Contenido:**
```json
[
  {
    "cadena": "num + num * num",
    "tipo": "valida",
    "profundidad": 3,
    "longitud": 5,
    "num_mutaciones": 0
  },
  {
    "cadena": "num ++ num",
    "tipo": "invalida",
    "profundidad": 2,
    "longitud": 4,
    "num_mutaciones": 1
  },
  {
    "cadena": "( num + num ) * ( num - num )",
    "tipo": "extrema",
    "profundidad": 8,
    "longitud": 11,
    "num_mutaciones": 0
  }
]
```

**Campos:**
- `cadena`: La expresión generada
- `tipo`: "valida", "invalida", o "extrema"
- `profundidad`: Niveles de anidamiento/derivación
- `longitud`: Cantidad de símbolos terminales
- `num_mutaciones`: Cambios aplicados (0 para válidas y extremas)

### Archivo de Reporte

**Ubicación:** `salida/reporte_metricas.txt`

**Contenido:**
```
REPORTE ESTADÍSTICO DEL GENERADOR
=================================

Total de cadenas generadas: 25
Por tipo:
  - valida: 10 (40.00%)
  - invalida: 10 (40.00%)
  - extrema: 5 (20.00%)

Longitud promedio de las expresiones: 8.52
Profundidad máxima alcanzada: 9
Operadores generados por tipo:
  +: 12
  -: 8
  *: 15
  /: 5
  %: 0

Mutaciones promedio (cadenas inválidas): 2.10
```

---

## Ejemplos Prácticos

### Ejemplo 1: Usar la gramática por defecto

```bash
$ python3 main.py

Ruta del archivo de gramática [.txt] (por defecto: gramaticas/aritmetica.txt): 
    # Presionas ENTER para usar la default

Cantidad de casos VÁLIDOS a generar [10]: 20
Cantidad de casos INVÁLIDOS a generar [10]: 15
Cantidad de casos EXTREMOS a generar [5]: 8
Profundidad máxima de derivación [10]: 12
Longitud máxima (en símbolos terminales) [15]: 20
Umbral de profundidad para considerar EXTREMA [8]: 10
Umbral de longitud para considerar EXTREMA [12]: 17
Nivel de mutación para casos inválidos (número de cambios) [2]: 3
```

**Resultado:**
- 20 casos válidos
- 8 casos extremos
- 15 casos inválidos
- Salida en `salida/casos_generados.json` y `salida/reporte_metricas.txt`

### Ejemplo 2: Crear una nueva gramática

**Paso 1:** Crea un archivo `gramaticas/palindromo.txt`:

```plaintext
# Gramática de palindromas
S -> a S a | b S b | a | b
```

**Paso 2:** Ejecuta el programa:

```bash
$ python3 main.py

Ruta del archivo de gramática [.txt]: gramaticas/palindromo.txt
Cantidad de casos VÁLIDOS a generar [10]: 15
Cantidad de casos INVÁLIDOS a generar [10]: 10
Cantidad de casos EXTREMOS a generar [5]: 5
Profundidad máxima de derivación [10]: 8
Longitud máxima (en símbolos terminales) [15]: 12
...
```

### Ejemplo 3: Parámetros de prueba rápida

Para probar rápidamente:

```bash
$ python3 main.py

Ruta del archivo de gramática [.txt]: 
    # Default
Cantidad de casos VÁLIDOS a generar [10]: 5
Cantidad de casos INVÁLIDOS a generar [10]: 5
Cantidad de casos EXTREMOS a generar [5]: 2
...
```

---

## Solución de Problemas

### Error: "No se encontró el archivo de gramática"

**Causa:** La ruta del archivo es incorrecta

**Solución:**
1. Verifica que el archivo existe en la carpeta `gramaticas/`
2. Comprueba el nombre del archivo (sensible a mayúsculas)
3. Usa la ruta relativa correcta desde donde ejecutas el programa

**Ejemplo:**
```bash
# ❌ Incorrecto
gramaticas/Aritmetica.txt

# ✅ Correcto
gramaticas/aritmetica.txt
```

---

### Error: "La gramática está vacía o mal definida"

**Causa:** El archivo de gramática no tiene reglas válidas

**Solución:**
1. Verifica que cada línea tiene el formato: `NoTerminal -> producción`
2. Comprueba que no hay líneas vacías al inicio del archivo
3. Elimina comentarios mal formados

**Ejemplo correcto:**
```plaintext
E -> E + T | T
T -> T * F | F
F -> ( E ) | num
```

**Ejemplo incorrecto:**
```plaintext
# Falta la flecha
E E + T | T

# Sintaxis incorrecta
E =>  E + T | T
```

---

### Error: "No se pudo generar una cadena válida"

**Causa:** Los parámetros son muy restrictivos

**Soluciones:**
1. Aumenta `max_profundidad`
2. Aumenta `max_longitud`
3. Aumenta los `reintentos` en el código (línea ~200)
4. Simplifica la gramática

**Ejemplo:**
```
Profundidad máxima de derivación [10]: 15  # Aumenta
Longitud máxima (en símbolos terminales) [15]: 25  # Aumenta
```

---

### Error: "Permission denied" al ejecutar

**Causa:** No tienes permisos de ejecución

**Solución (en macOS/Linux):**
```bash
chmod +x main.py
python3 main.py
```

---

### El programa tarda mucho

**Causa:** Los parámetros son muy exigentes

**Soluciones:**
1. Reduce `cantidad_validas`, `cantidad_invalidas`, `cantidad_extremas`
2. Reduce `max_profundidad` y `max_longitud`
3. Reduce `nivel_mutacion`

---

### No se crean los archivos de salida

**Causa:** No tienes permisos de escritura en la carpeta

**Solución:**
1. Verifica que la carpeta `salida/` existe
2. O crea la carpeta:
   ```bash
   mkdir -p salida
   ```

---

### Diferentes resultados cada vez

**Esto es normal.** El programa usa algoritmos aleatorios para generar casos. Cada ejecución produce resultados diferentes (pero equivalentes en estadísticas).

Para reproducir resultados, modifica la línea 7 de `main.py`:
```python
# Actual:
random.seed()

# Cambiar a:
random.seed(42)  # Número fijo para reproducibilidad
```

---

## Preguntas Frecuentes (FAQ)

### ¿Puedo usar cadenas con espacios?

Sí. Los espacios sirven para separar símbolos. `a + b` son 3 símbolos: `a`, `+`, `b`

### ¿Qué pasa si mi gramática tiene ciclos?

El programa puede entrar en bucles infinitos. Se controla con `max_profundidad`. Si pasa, aumenta ese parámetro.

### ¿Puedo usar caracteres especiales?

Sí, cualquier carácter es válido como terminal. Ejemplos: `@`, `#`, `@`, `ñ`, etc.

### ¿Cómo cambio el símbolo inicial?

El programa usa automáticamente el **primer no terminal** del archivo como símbolo inicial. Reordena las líneas si es necesario.

### ¿Puedo generar 1000 casos?

Sí, pero tardará más tiempo. Configura:
```
Cantidad de casos VÁLIDOS a generar [10]: 1000
```

### ¿Dónde veo el progreso?

El programa imprime tiempos de ejecución:
```
- Casos válidos generados en 0.1234 segundos.
```

---

## Contacto y Soporte

Para problemas adicionales:
1. Verifica que tienes Python 3.7+
2. Revisa que la gramática cumple el formato
3. Comprueba los parámetros de generación
4. Consulta la sección "Solución de Problemas"

---

**Versión del Manual:** 1.0  
**Fecha:** 28 de noviembre de 2025  
**Desarrollo:** Proyecto Teoría de la Computación
