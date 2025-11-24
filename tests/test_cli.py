"""Tests unitarios para funciones auxiliares del CLI."""

from unittest.mock import patch

import pytest

from src.exceptions import GradeCalculatorError
from src.models.evaluation import Evaluation
from src.policies.extra_points_policy import ExtraPointsPolicy


class TestCLIHelpers:
    """Tests para funciones auxiliares del CLI."""

    def test_shouldImportCLIModule(self) -> None:
        """Debe poder importar el módulo CLI."""
        import src.cli

        assert src.cli is not None

    def test_shouldHaveMainFunction(self) -> None:
        """Debe tener una función main."""
        from src.cli import main

        assert callable(main)

    def test_shouldHaveRegisterFunctions(self) -> None:
        """Debe tener funciones de registro."""
        from src.cli import (
            _register_attendance,
            _register_evaluations,
            _register_extra_points,
            _register_tardiness_percentage,
            _register_teachers_votes,
        )

        assert callable(_register_evaluations)
        assert callable(_register_attendance)
        assert callable(_register_tardiness_percentage)
        assert callable(_register_teachers_votes)
        assert callable(_register_extra_points)

    def test_shouldCalculateAndDisplayResult(self) -> None:
        """Debe calcular y mostrar resultado correctamente."""
        from src.cli import _calculate_and_display_result

        evaluations = [
            Evaluation(grade=15.0, weight=50.0),
            Evaluation(grade=18.0, weight=50.0),
        ]

        with patch("builtins.print"):
            _calculate_and_display_result(
                evaluations=evaluations,
                has_reached_minimum=True,
                tardiness_percentage=0.0,
                all_years_teachers=[True, True],
                extra_points=1.0,
                student_id="TEST001",
            )

    def test_shouldHandleCalculationError(self) -> None:
        """Debe manejar errores en el cálculo."""
        from src.cli import _calculate_and_display_result

        # Evaluaciones con pesos inválidos para provocar error
        evaluations = [
            Evaluation(grade=15.0, weight=30.0),
            Evaluation(grade=18.0, weight=40.0),
        ]

        with patch("builtins.print"):
            _calculate_and_display_result(
                evaluations=evaluations,
                has_reached_minimum=True,
                tardiness_percentage=0.0,
                all_years_teachers=[True],
                extra_points=0.0,
                student_id="TEST001",
            )

    def test_shouldRegisterEvaluationsWithValidInput(self) -> None:
        """Debe registrar evaluaciones con entrada válida."""
        from src.cli import _register_evaluations

        with patch("builtins.input", side_effect=["15.0", "50.0", "n"]):
            with patch("builtins.print"):
                evaluations = _register_evaluations()
                assert len(evaluations) == 1
                assert evaluations[0].grade == 15.0
                assert evaluations[0].weight == 50.0

    def test_shouldRegisterEvaluationsWithMultipleInputs(self) -> None:
        """Debe registrar múltiples evaluaciones."""
        from src.cli import _register_evaluations

        with patch(
            "builtins.input",
            side_effect=["15.0", "50.0", "s", "18.0", "50.0", "n"],
        ):
            with patch("builtins.print"):
                evaluations = _register_evaluations()
                assert len(evaluations) == 2

    def test_shouldHandleInvalidEvaluationInput(self) -> None:
        """Debe manejar entrada inválida en evaluaciones."""
        from src.cli import _register_evaluations

        # Simula entrada inválida (ValueError al convertir) seguida de entrada válida
        # Flujo: invalid_grade -> invalid_weight -> 15.0 -> 50.0 -> n
        with patch(
            "builtins.input",
            side_effect=["invalid_grade", "invalid_weight", "15.0", "50.0", "n"],
        ):
            with patch("builtins.print"):
                evaluations = _register_evaluations()
                # Debe continuar después del error y registrar la evaluación válida
                assert len(evaluations) == 1

    def test_shouldRegisterAttendanceAsYes(self) -> None:
        """Debe registrar asistencia como sí."""
        from src.cli import _register_attendance

        with patch("builtins.input", return_value="s"):
            with patch("builtins.print"):
                result = _register_attendance()
                assert result is True

    def test_shouldRegisterAttendanceAsNo(self) -> None:
        """Debe registrar asistencia como no."""
        from src.cli import _register_attendance

        with patch("builtins.input", return_value="n"):
            with patch("builtins.print"):
                result = _register_attendance()
                assert result is False

    def test_shouldRegisterTardinessPercentage(self) -> None:
        """Debe registrar porcentaje de tardanzas."""
        from src.cli import _register_tardiness_percentage

        with patch("builtins.input", return_value="45.0"):
            with patch("builtins.print"):
                percentage = _register_tardiness_percentage()
                assert percentage == 45.0

    def test_shouldRegisterTeachersVotes(self) -> None:
        """Debe registrar votos de profesores."""
        from src.cli import _register_teachers_votes

        with patch("builtins.input", side_effect=["s", "s", "fin"]):
            with patch("builtins.print"):
                votes = _register_teachers_votes()
                assert len(votes) == 2
                assert all(votes)

    def test_shouldRegisterExtraPointsWhenTeachersAgree(self) -> None:
        """Debe registrar puntos extra cuando profesores están de acuerdo."""
        from src.cli import _register_extra_points

        with patch("builtins.input", return_value="2.0"):
            with patch("builtins.print"):
                points = _register_extra_points([True, True])
                assert points == 2.0

    def test_shouldReturnZeroExtraPointsWhenTeachersDisagree(self) -> None:
        """Debe retornar 0 puntos extra cuando profesores no están de acuerdo."""
        from src.cli import _register_extra_points

        with patch("builtins.print"):
            points = _register_extra_points([True, False])
            assert points == 0.0

