"""Modelo de Evaluación."""

from typing import Optional

from src.constants import MAX_GRADE, MIN_GRADE
from src.exceptions import InvalidEvaluationError


class Evaluation:
    """Representa una evaluación con su nota y peso."""

    def __init__(self, grade: float, weight: float) -> None:
        """
        Inicializa una evaluación.

        Args:
            grade: Nota obtenida (0-20)
            weight: Peso de la evaluación como porcentaje

        Raises:
            InvalidEvaluationError: Si la nota o el peso son inválidos
        """
        self._validate_grade(grade)
        self._validate_weight(weight)

        self._grade = grade
        self._weight = weight

    @property
    def grade(self) -> float:
        """Retorna la nota de la evaluación."""
        return self._grade

    @property
    def weight(self) -> float:
        """Retorna el peso de la evaluación como porcentaje."""
        return self._weight

    def _validate_grade(self, grade: float) -> None:
        """
        Valida que la nota esté en el rango válido.

        Args:
            grade: Nota a validar

        Raises:
            InvalidEvaluationError: Si la nota está fuera del rango válido
        """
        if grade < MIN_GRADE or grade > MAX_GRADE:
            raise InvalidEvaluationError(
                f"La nota debe estar entre {MIN_GRADE} y {MAX_GRADE}. "
                f"Valor recibido: {grade}"
            )

    def _validate_weight(self, weight: float) -> None:
        """
        Valida que el peso sea positivo.

        Args:
            weight: Peso a validar

        Raises:
            InvalidEvaluationError: Si el peso es negativo o cero
        """
        if weight <= 0:
            raise InvalidEvaluationError(
                f"El peso debe ser positivo. Valor recibido: {weight}"
            )

    def __repr__(self) -> str:
        """Representación string de la evaluación."""
        return f"Evaluation(grade={self._grade}, weight={self._weight}%)"

