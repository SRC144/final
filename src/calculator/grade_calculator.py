"""Calculadora de Notas Finales."""

from typing import Dict, List

from src.constants import (
    EXPECTED_WEIGHT_SUM,
    MAX_EVALUATIONS,
    WEIGHT_TOLERANCE,
)
from src.exceptions import InvalidWeightError, MaxEvaluationsExceededError
from src.models.evaluation import Evaluation
from src.policies.attendance_policy import AttendancePolicy
from src.policies.extra_points_policy import ExtraPointsPolicy


class GradeCalculator:
    """
    Calculadora de notas finales.

    Clase stateless y thread-safe que calcula la nota final de un estudiante
    considerando evaluaciones, asistencia y puntos extra.
    """

    @staticmethod
    def calculate_final_grade(
        evaluations: List[Evaluation],
        has_reached_minimum: bool,
        tardiness_percentage: float,
        all_years_teachers: List[bool],
        extra_points: float,
    ) -> Dict[str, float]:
        """
        Calcula la nota final de un estudiante.

        Proceso:
        1. Valida el número máximo de evaluaciones
        2. Valida que los pesos sumen 100%
        3. Calcula el promedio ponderado
        4. Aplica penalización por asistencia si corresponde
        5. Aplica puntos extra si los profesores están de acuerdo
        6. Retorna el resultado con el detalle del cálculo

        Args:
            evaluations: Lista de evaluaciones del estudiante
            has_reached_minimum: True si alcanzó la asistencia mínima
            tardiness_percentage: Porcentaje de tardanzas (0-100)
            all_years_teachers: Lista de votos de profesores (True/False)
            extra_points: Puntos extra a aplicar (si aplica)

        Returns:
            Diccionario con:
                - final_grade: Nota final calculada
                - weighted_average: Promedio ponderado
                - penalty_applied: Penalización aplicada
                - extra_points_applied: Puntos extra aplicados

        Raises:
            MaxEvaluationsExceededError: Si se excede el máximo de evaluaciones
            InvalidWeightError: Si los pesos no suman 100%
        """
        GradeCalculator._validate_evaluations_count(evaluations)
        GradeCalculator._validate_weights_sum(evaluations)

        weighted_average = GradeCalculator._calculate_weighted_average(evaluations)

        penalty_fraction = AttendancePolicy.calculate_penalty(
            has_reached_minimum, tardiness_percentage
        )
        penalty_applied = weighted_average * penalty_fraction
        grade_after_penalty = weighted_average - penalty_applied

        extra_points_applied = 0.0
        if ExtraPointsPolicy.can_assign_extra_points(all_years_teachers):
            final_grade = ExtraPointsPolicy.apply_extra_points(
                grade_after_penalty, extra_points
            )
            extra_points_applied = final_grade - grade_after_penalty
        else:
            final_grade = grade_after_penalty

        return {
            "final_grade": round(final_grade, 2),
            "weighted_average": round(weighted_average, 2),
            "penalty_applied": round(penalty_applied, 2),
            "extra_points_applied": round(extra_points_applied, 2),
        }

    @staticmethod
    def _validate_evaluations_count(evaluations: List[Evaluation]) -> None:
        """
        Valida que no se exceda el máximo de evaluaciones.

        Args:
            evaluations: Lista de evaluaciones

        Raises:
            MaxEvaluationsExceededError: Si se excede el máximo permitido
        """
        if len(evaluations) > MAX_EVALUATIONS:
            raise MaxEvaluationsExceededError(
                f"Se excedió el máximo de evaluaciones permitidas ({MAX_EVALUATIONS}). "
                f"Evaluaciones recibidas: {len(evaluations)}"
            )

    @staticmethod
    def _validate_weights_sum(evaluations: List[Evaluation]) -> None:
        """
        Valida que la suma de los pesos sea 100%.

        Args:
            evaluations: Lista de evaluaciones

        Raises:
            InvalidWeightError: Si los pesos no suman 100% (con tolerancia)
        """
        if not evaluations:
            return

        total_weight = sum(evaluation.weight for evaluation in evaluations)
        difference = abs(total_weight - EXPECTED_WEIGHT_SUM)

        if difference > WEIGHT_TOLERANCE:
            raise InvalidWeightError(
                f"La suma de los pesos debe ser {EXPECTED_WEIGHT_SUM}%. "
                f"Suma actual: {total_weight}%"
            )

    @staticmethod
    def _calculate_weighted_average(evaluations: List[Evaluation]) -> float:
        """
        Calcula el promedio ponderado de las evaluaciones.

        Fórmula: Σ(nota × peso) / Σ(pesos)

        Args:
            evaluations: Lista de evaluaciones

        Returns:
            Promedio ponderado
        """
        if not evaluations:
            return 0.0

        weighted_sum = sum(
            evaluation.grade * evaluation.weight for evaluation in evaluations
        )
        total_weight = sum(evaluation.weight for evaluation in evaluations)

        if total_weight == 0:
            return 0.0

        return weighted_sum / total_weight

