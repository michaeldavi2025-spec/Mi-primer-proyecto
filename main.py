import csv
import os
import random
import time
from dataclasses import dataclass
from typing import List, Optional

LETRAS = ["A", "B", "C", "D"]

@dataclass
class Pregunta:
    enunciado: str
    opciones: List[str]
    correcta: int          # índice 0..3
    elegida: Optional[int] = None

def cargar_preguntas_desde_csv(ruta="preguntas.csv") -> List[Pregunta]:
    """
    Formato CSV esperado (con encabezado):
    enunciado,opcion_a,opcion_b,opcion_c,opcion_d,correcta
    La columna 'correcta' debe ser A/B/C/D
    """
    preguntas: List[Pregunta] = []
    if not os.path.exists(ruta):
        return preguntas

    with open(ruta, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, 1):
            try:
                enunciado = row["enunciado"].strip()
                opciones = [
                    row["opcion_a"].strip(),
                    row["opcion_b"].strip(),
                    row["opcion_c"].strip(),
                    row["opcion_d"].strip(),
                ]
                letra = row["correcta"].strip().upper()
                idx = LETRAS.index(letra)
                preguntas.append(Pregunta(enunciado, opciones, idx))
            except Exception as e:
                print(f"[Aviso] Fila {i} del CSV inválida: {e}")
    return preguntas

def preguntas_de_demo() -> List[Pregunta]:
    return [
        Pregunta(
            "¿Cuál es la capital de Francia?",
            ["Madrid", "París", "Roma", "Berlín"],
            correcta=1,
        ),
        Pregunta(
            "¿Cuánto es 7 × 8?",
            ["52", "54", "56", "48"],
            correcta=2,
        ),
        Pregunta(
            "¿Quién escribió 'Don Quijote de la Mancha'?",
            ["Gabriel García Márquez", "Mario Vargas Llosa", "Miguel de Cervantes", "Pablo Neruda"],
            correcta=2,
        ),
        Pregunta(
            "¿Cuál es el símbolo químico del oro?",
            ["Ag", "Au", "Gd", "Go"],
            correcta=1,
        ),
        Pregunta(
            "En informática, ¿qué significa CPU?",
            ["Central Processing Unit", "Computer Personal Unit", "Control Program Unit", "Core Processing Utility"],
            correcta=0,
        ),
    ]

def leer_opcion_usuario(prompt: str) -> int:
    while True:
        r = input(prompt).strip().upper()
        if r in LETRAS:
            return LETRAS.index(r)
        print("Ingresa una opción válida (A, B, C o D).")

def ejecutar_quiz(preguntas: List[Pregunta]) -> None:
    random.shuffle(preguntas)
    print("\n=== QUIZ DE OPCIÓN MÚLTIPLE ===")
    print(f"Total de preguntas: {len(preguntas)}")
    print("Responde con A, B, C o D.\n")

    inicio = time.time()
    for i, p in enumerate(preguntas, 1):
        print(f"Pregunta {i}: {p.enunciado}")
        for j, opcion in enumerate(p.opciones):
            print(f"  {LETRAS[j]}) {opcion}")
        p.elegida = leer_opcion_usuario("Tu respuesta: ")
        print()

    fin = time.time()
    duracion = fin - inicio

    # Calcular puntaje
    correctas = sum(1 for p in preguntas if p.elegida == p.correcta)
    total = len(preguntas)
    porcentaje = (correctas / total) * 100 if total else 0.0

    print("=== RESULTADOS ===")
    print(f"Puntaje: {correctas}/{total}  ({porcentaje:.1f}%)")
    print(f"Tiempo: {duracion:.1f} s\n")

    # Resumen por pregunta
    print("Detalle por pregunta:")
    for i, p in enumerate(preguntas, 1):
        letra_correcta = LETRAS[p.correcta]
        letra_elegida = LETRAS[p.elegida] if p.elegida is not None else "-"
        estado = "✅ Correcto" if p.elegida == p.correcta else "❌ Incorrecto"
        print(f"- {i}. {estado} | Elegiste {letra_elegida} | Correcta {letra_correcta} | {p.enunciado}")

def main():
    preguntas = cargar_preguntas_desde_csv("preguntas.csv")
    if not preguntas:
        print("[Info] No se encontró 'preguntas.csv'. Usando preguntas de demo.")
        preguntas = preguntas_de_demo()
    ejecutar_quiz(preguntas)

if __name__ == "__main__":
    main()
