"""Tests unitarios para la clase GradeCalculator."""

import pytest

from src.calculator.grade_calculator import GradeCalculator
from src.constants import MAX_EVALUATIONS
from src.exceptions import InvalidWeightError, MaxEvaluationsExceededError
from src.models.evaluation import Evaluation


class TestGradeCalculator:
    """Tests para la clase GradeCalculator."""

    def test_shouldReturnCorrectWeightedAverageWhenEvaluationsProvided(self) -> None:
        """Debe retornar promedio ponderado correcto cuando hay evaluaciones."""
        evaluations = [
            Evaluation(grade=15.0, weight=30.0),
            Evaluation(grade=18.0, weight=40.0),
            Evaluation(grade=12.0, weight=30.0),
        ]
        result = GradeCalculator.calculate_final_grade(
            evaluations=evaluations,
            has_reached_minimum=True,
            tardiness_percentage=0.0,
            all_years_teachers=[True, True],
            extra_points=0.0,
        )
        # (15*30 + 18*40 + 12*30) / 100 = (450 + 720 + 360) / 100 = 15.3
        assert result["weighted_average"] == 15.3
        assert result["final_grade"] == 15.3

    def test_shouldReturnZeroWhenNoEvaluations(self) -> None:
        """Debe retornar 0 cuando no hay evaluaciones."""
        result = GradeCalculator.calculate_final_grade(
            evaluations=[],
            has_reached_minimum=True,
            tardiness_percentage=0.0,
            all_years_teachers=[True],
            extra_points=0.0,
        )
        assert result["weighted_average"] == 0.0
        assert result["final_grade"] == 0.0

    def test_shouldRaiseErrorWhenMoreThanMaxEvaluations(self) -> None:
        """Debe lanzar error cuando se excede el máximo de evaluaciones."""
        evaluations = [
            Evaluation(grade=15.0, weight=10.0) for _ in range(MAX_EVALUATIONS + 1)
        ]
        with pytest.raises(MaxEvaluationsExceededError):
            GradeCalculator.calculate_final_grade(
                evaluations=evaluations,
                has_reached_minimum=True,
                tardiness_percentage=0.0,
                all_years_teachers=[True],
                extra_points=0.0,
            )

    def test_shouldRaiseErrorWhenWeightsDoNotSumToHundred(self) -> None:
        """Debe lanzar error cuando los pesos no suman 100%."""
        evaluations = [
            Evaluation(grade=15.0, weight=30.0),
            Evaluation(grade=18.0, weight=40.0),
            # Suma: 70%, debería ser 100%
        ]
        with pytest.raises(InvalidWeightError):
            GradeCalculator.calculate_final_grade(
                evaluations=evaluations,
                has_reached_minimum=True,
                tardiness_percentage=0.0,
                all_years_teachers=[True],
                extra_points=0.0,
            )

    def test_shouldApplyPenaltyWhenNoMinimumAttendance(self) -> None:
        """Debe aplicar penalización cuando no hay asistencia mínima."""
        evaluations = [
            Evaluation(grade=15.0, weight=50.0),
            Evaluation(grade=18.0, weight=50.0),
        ]
        result = GradeCalculator.calculate_final_grade(
            evaluations=evaluations,
            has_reached_minimum=False,
            tardiness_percentage=45.0,  # >= 40%
            all_years_teachers=[True],
            extra_points=0.0,
        )
        # Promedio: (15*50 + 18*50) / 100 = 16.5
        # Penalización: 16.5 * 0.10 = 1.65
        # Nota final: 16.5 - 1.65 = 14.85
        assert result["penalty_applied"] > 0.0
        assert result["final_grade"] < result["weighted_average"]

    def test_shouldApplyExtraPointsWhenTeachersAgree(self) -> None:
        """Debe aplicar puntos extra cuando los profesores están de acuerdo."""
        evaluations = [
            Evaluation(grade=15.0, weight=50.0),
            Evaluation(grade=18.0, weight=50.0),
        ]
        result = GradeCalculator.calculate_final_grade(
            evaluations=evaluations,
            has_reached_minimum=True,
            tardiness_percentage=0.0,
            all_years_teachers=[True, True, True],
            extra_points=2.0,
        )
        # Promedio: 16.5
        # Puntos extra: 2.0
        # Nota final: 18.5
        assert result["extra_points_applied"] == 2.0
        assert result["final_grade"] == 18.5

    def test_shouldNotApplyExtraPointsWhenTeachersDisagree(self) -> None:
        """No debe aplicar puntos extra cuando los profesores no están de acuerdo."""
        evaluations = [
            Evaluation(grade=15.0, weight=50.0),
            Evaluation(grade=18.0, weight=50.0),
        ]
        result = GradeCalculator.calculate_final_grade(
            evaluations=evaluations,
            has_reached_minimum=True,
            tardiness_percentage=0.0,
            all_years_teachers=[True, False, True],
            extra_points=2.0,
        )
        # Promedio: 16.5
        # No se aplican puntos extra
        assert result["extra_points_applied"] == 0.0
        assert result["final_grade"] == 16.5

    def test_shouldReturnSameResultForSameInputs(self) -> None:
        """Debe retornar el mismo resultado para los mismos inputs (determinismo)."""
        evaluations = [
            Evaluation(grade=15.0, weight=30.0),
            Evaluation(grade=18.0, weight=40.0),
            Evaluation(grade=12.0, weight=30.0),
        ]
        result1 = GradeCalculator.calculate_final_grade(
            evaluations=evaluations,
            has_reached_minimum=True,
            tardiness_percentage=0.0,
            all_years_teachers=[True, True],
            extra_points=1.0,
        )
        result2 = GradeCalculator.calculate_final_grade(
            evaluations=evaluations,
            has_reached_minimum=True,
            tardiness_percentage=0.0,
            all_years_teachers=[True, True],
            extra_points=1.0,
        )
        assert result1 == result2

    def test_shouldHandleSingleEvaluation(self) -> None:
        """Debe manejar correctamente una sola evaluación."""
        evaluations = [Evaluation(grade=15.0, weight=100.0)]
        result = GradeCalculator.calculate_final_grade(
            evaluations=evaluations,
            has_reached_minimum=True,
            tardiness_percentage=0.0,
            all_years_teachers=[True],
            extra_points=0.0,
        )
        assert result["weighted_average"] == 15.0
        assert result["final_grade"] == 15.0

    def test_shouldCapExtraPointsAtMaximumGrade(self) -> None:
        """Debe limitar la nota final al máximo cuando puntos extra exceden."""
        evaluations = [
            Evaluation(grade=19.0, weight=50.0),
            Evaluation(grade=19.0, weight=50.0),
        ]
        result = GradeCalculator.calculate_final_grade(
            evaluations=evaluations,
            has_reached_minimum=True,
            tardiness_percentage=0.0,
            all_years_teachers=[True, True],
            extra_points=5.0,  # Excedería el máximo
        )
        # Promedio: 19.0
        # Puntos extra aplicados: solo 1.0 (para llegar a 20)
        assert result["final_grade"] == 20.0

    def test_shouldNotApplyPenaltyWhenTardinessBelowThreshold(self) -> None:
        """No debe aplicar penalización cuando tardanzas < 40%."""
        evaluations = [
            Evaluation(grade=15.0, weight=50.0),
            Evaluation(grade=18.0, weight=50.0),
        ]
        result = GradeCalculator.calculate_final_grade(
            evaluations=evaluations,
            has_reached_minimum=False,
            tardiness_percentage=35.0,  # < 40%
            all_years_teachers=[True],
            extra_points=0.0,
        )
        assert result["penalty_applied"] == 0.0
        assert result["final_grade"] == result["weighted_average"]

    def test_shouldHandleMaxEvaluations(self) -> None:
        """Debe manejar correctamente el máximo de evaluaciones permitidas."""
        evaluations = [
            Evaluation(grade=15.0, weight=10.0) for _ in range(MAX_EVALUATIONS)
        ]
        result = GradeCalculator.calculate_final_grade(
            evaluations=evaluations,
            has_reached_minimum=True,
            tardiness_percentage=0.0,
            all_years_teachers=[True],
            extra_points=0.0,
        )
        assert result["weighted_average"] == 15.0

    def test_shouldHandleComplexCalculationWithAllFactors(self) -> None:
        """Debe manejar cálculo complejo con penalización y puntos extra."""
        evaluations = [
            Evaluation(grade=14.0, weight=25.0),
            Evaluation(grade=16.0, weight=35.0),
            Evaluation(grade=18.0, weight=40.0),
        ]
        result = GradeCalculator.calculate_final_grade(
            evaluations=evaluations,
            has_reached_minimum=False,
            tardiness_percentage=45.0,
            all_years_teachers=[True, True],
            extra_points=1.5,
        )
        # Promedio: (14*25 + 16*35 + 18*40) / 100 = (350 + 560 + 720) / 100 = 16.3
        # Penalización: 16.3 * 0.10 = 1.63
        # Nota después de penalización: 16.3 - 1.63 = 14.67
        # Puntos extra: 1.5
        # Nota final: 14.67 + 1.5 = 16.17
        assert result["penalty_applied"] > 0.0
        assert result["extra_points_applied"] > 0.0
        assert result["final_grade"] > 0.0
