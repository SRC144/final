"""Tests unitarios para la clase Evaluation."""

import pytest

from src.constants import MAX_GRADE, MIN_GRADE
from src.exceptions import InvalidEvaluationError
from src.models.evaluation import Evaluation


class TestEvaluation:
    """Tests para la clase Evaluation."""

    def test_shouldReturnTrueWhenGradeIsValid(self) -> None:
        """Debe crear una evaluación cuando la nota es válida."""
        evaluation = Evaluation(grade=15.5, weight=30.0)
        assert evaluation.grade == 15.5
        assert evaluation.weight == 30.0

    def test_shouldReturnFalseWhenGradeIsNegative(self) -> None:
        """Debe lanzar error cuando la nota es negativa."""
        with pytest.raises(InvalidEvaluationError):
            Evaluation(grade=-1.0, weight=30.0)

    def test_shouldReturnFalseWhenGradeExceedsMaximum(self) -> None:
        """Debe lanzar error cuando la nota excede el máximo."""
        with pytest.raises(InvalidEvaluationError):
            Evaluation(grade=MAX_GRADE + 1, weight=30.0)

    def test_shouldReturnFalseWhenWeightIsInvalid(self) -> None:
        """Debe lanzar error cuando el peso es inválido."""
        with pytest.raises(InvalidEvaluationError):
            Evaluation(grade=15.0, weight=-5.0)

        with pytest.raises(InvalidEvaluationError):
            Evaluation(grade=15.0, weight=0.0)

    def test_shouldAcceptGradeAtMinimumBoundary(self) -> None:
        """Debe aceptar nota en el límite mínimo."""
        evaluation = Evaluation(grade=MIN_GRADE, weight=30.0)
        assert evaluation.grade == MIN_GRADE

    def test_shouldAcceptGradeAtMaximumBoundary(self) -> None:
        """Debe aceptar nota en el límite máximo."""
        evaluation = Evaluation(grade=MAX_GRADE, weight=30.0)
        assert evaluation.grade == MAX_GRADE

    def test_shouldReturnCorrectStringRepresentation(self) -> None:
        """Debe retornar representación string correcta."""
        evaluation = Evaluation(grade=15.5, weight=30.0)
        repr_str = repr(evaluation)
        assert "Evaluation" in repr_str
        assert "15.5" in repr_str
        assert "30.0" in repr_str

