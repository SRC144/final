"""Interfaz de línea de comandos para CS-GradeCalculator."""

from typing import List

from src.calculator.grade_calculator import GradeCalculator
from src.constants import MAX_EVALUATIONS
from src.exceptions import GradeCalculatorError
from src.models.evaluation import Evaluation


def main() -> None:
    """Función principal del CLI."""
    print("=" * 60)
    print("CS-GradeCalculator - Sistema de Cálculo de Notas Finales")
    print("=" * 60)
    print()

    # Paso 1: Solicitar datos del estudiante
    student_id = input("Ingrese el código o identificador del estudiante: ").strip()
    print(f"\nEstudiante: {student_id}")
    print()

    # Paso 2: Registrar evaluaciones
    evaluations = _register_evaluations()

    # Paso 3: Registrar asistencia mínima
    has_reached_minimum = _register_attendance()

    # Paso 4: Si no alcanzó, solicitar porcentaje de tardanzas
    tardiness_percentage = 0.0
    if not has_reached_minimum:
        tardiness_percentage = _register_tardiness_percentage()

    # Paso 5: Registrar votos de profesores
    all_years_teachers = _register_teachers_votes()

    # Paso 6: Solicitar puntos extra (si aplica)
    extra_points = _register_extra_points(all_years_teachers)

    # Paso 7: Calcular y mostrar resultado
    _calculate_and_display_result(
        evaluations,
        has_reached_minimum,
        tardiness_percentage,
        all_years_teachers,
        extra_points,
        student_id,
    )


def _register_evaluations() -> List[Evaluation]:
    """
    Registra las evaluaciones del estudiante.

    Returns:
        Lista de evaluaciones registradas
    """
    evaluations: List[Evaluation] = []
    print("--- Registro de Evaluaciones ---")
    print(f"Máximo de evaluaciones permitidas: {MAX_EVALUATIONS}")
    print()

    while len(evaluations) < MAX_EVALUATIONS:
        try:
            print(f"Evaluación {len(evaluations) + 1}:")
            grade_str = input("  Nota obtenida (0-20): ").strip()
            weight_str = input("  Peso (%): ").strip()

            grade = float(grade_str)
            weight = float(weight_str)

            evaluation = Evaluation(grade, weight)
            evaluations.append(evaluation)

            print(f"  ✓ Evaluación registrada: Nota={grade}, Peso={weight}%")
            print()

            if len(evaluations) < MAX_EVALUATIONS:
                continue_registering = (
                    input("¿Desea registrar otra evaluación? (s/n): ").strip().lower()
                )
                if continue_registering != "s":
                    break
        except ValueError:
            print("  ✗ Error: Debe ingresar valores numéricos válidos.")
            print()
        except GradeCalculatorError as e:
            print(f"  ✗ Error: {e}")
            print()

    if not evaluations:
        print("⚠ Advertencia: No se registraron evaluaciones.")
        print()

    return evaluations


def _register_attendance() -> bool:
    """
    Registra si el estudiante alcanzó la asistencia mínima.

    Returns:
        True si alcanzó la asistencia mínima, False en caso contrario
    """
    print("--- Asistencia Mínima ---")
    while True:
        response = (
            input("¿El estudiante alcanzó la asistencia mínima? (s/n): ")
            .strip()
            .lower()
        )
        if response == "s":
            print()
            return True
        elif response == "n":
            print()
            return False
        else:
            print("Por favor, ingrese 's' para sí o 'n' para no.")


def _register_tardiness_percentage() -> float:
    """
    Registra el porcentaje de tardanzas.

    Returns:
        Porcentaje de tardanzas (0-100)
    """
    print("--- Porcentaje de Tardanzas ---")
    while True:
        try:
            percentage_str = input("Ingrese el porcentaje de tardanzas (0-100): ").strip()
            percentage = float(percentage_str)

            if 0 <= percentage <= 100:
                print()
                return percentage
            else:
                print("El porcentaje debe estar entre 0 y 100.")
        except ValueError:
            print("Por favor, ingrese un valor numérico válido.")


def _register_teachers_votes() -> List[bool]:
    """
    Registra los votos de los profesores del año.

    Returns:
        Lista de votos (True/False) de los profesores
    """
    print("--- Votos de Profesores del Año ---")
    print("Ingrese los votos de los profesores (s/n para cada uno):")
    print("(s = de acuerdo con puntos extra, n = en desacuerdo)")
    print()

    votes: List[bool] = []
    teacher_num = 1

    while True:
        try:
            vote_str = (
                input(f"Profesor {teacher_num} (s/n, o 'fin' para terminar): ")
                .strip()
                .lower()
            )

            if vote_str == "fin":
                break

            if vote_str == "s":
                votes.append(True)
                teacher_num += 1
            elif vote_str == "n":
                votes.append(False)
                teacher_num += 1
            else:
                print("Por favor, ingrese 's', 'n' o 'fin'.")
        except KeyboardInterrupt:
            break

    if not votes:
        print("⚠ Advertencia: No se registraron votos de profesores.")
        print()

    return votes


def _register_extra_points(all_years_teachers: List[bool]) -> float:
    """
    Registra los puntos extra a aplicar.

    Args:
        all_years_teachers: Lista de votos de profesores

    Returns:
        Puntos extra a aplicar
    """
    print("--- Puntos Extra ---")

    from src.policies.extra_points_policy import ExtraPointsPolicy

    can_assign = ExtraPointsPolicy.can_assign_extra_points(all_years_teachers)

    if not can_assign:
        print(
            "⚠ No se pueden asignar puntos extra: no todos los profesores están de acuerdo."
        )
        print()
        return 0.0

    print("✓ Todos los profesores están de acuerdo. Puede asignar puntos extra.")
    print()

    while True:
        try:
            points_str = input("Ingrese los puntos extra a aplicar (0 o más): ").strip()
            points = float(points_str)

            if points >= 0:
                print()
                return points
            else:
                print("Los puntos extra no pueden ser negativos.")
        except ValueError:
            print("Por favor, ingrese un valor numérico válido.")


def _calculate_and_display_result(
    evaluations: List[Evaluation],
    has_reached_minimum: bool,
    tardiness_percentage: float,
    all_years_teachers: List[bool],
    extra_points: float,
    student_id: str,
) -> None:
    """
    Calcula y muestra el resultado del cálculo de la nota final.

    Args:
        evaluations: Lista de evaluaciones
        has_reached_minimum: Si alcanzó la asistencia mínima
        tardiness_percentage: Porcentaje de tardanzas
        all_years_teachers: Votos de profesores
        extra_points: Puntos extra
        student_id: Identificador del estudiante
    """
    print("=" * 60)
    print("CALCULANDO NOTA FINAL...")
    print("=" * 60)
    print()

    try:
        result = GradeCalculator.calculate_final_grade(
            evaluations,
            has_reached_minimum,
            tardiness_percentage,
            all_years_teachers,
            extra_points,
        )

        print(f"Estudiante: {student_id}")
        print()
        print("--- Detalle del Cálculo ---")
        print(f"Promedio Ponderado: {result['weighted_average']}")
        print(f"Penalización Aplicada: {result['penalty_applied']}")
        print(f"Puntos Extra Aplicados: {result['extra_points_applied']}")
        print()
        print("=" * 60)
        print(f"NOTA FINAL: {result['final_grade']}")
        print("=" * 60)

    except GradeCalculatorError as e:
        print(f"✗ Error al calcular la nota final: {e}")
        print()


if __name__ == "__main__":
    main()

