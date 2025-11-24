"""Política de Asistencia."""

from src.constants import (
    ATTENDANCE_PENALTY_FRACTION,
    MAX_PERCENTAGE,
    MIN_ATTENDANCE_PERCENTAGE,
    MIN_PERCENTAGE,
)
from src.exceptions import InvalidTardinessPercentageError


class AttendancePolicy:
    """Maneja la lógica de validación y penalización por inasistencia."""

    @staticmethod
    def calculate_penalty(
        has_reached_minimum: bool, tardiness_percentage: float
    ) -> float:
        """
        Calcula la penalización por asistencia.

        Si el estudiante alcanzó la asistencia mínima, no hay penalización.
        Si no alcanzó y tiene >= 40% de tardanzas, se aplica una penalización
        como fracción de la nota.

        Args:
            has_reached_minimum: True si el estudiante alcanzó la asistencia mínima
            tardiness_percentage: Porcentaje de tardanzas (0-100)

        Returns:
            Valor de la penalización a aplicar (0 si no hay penalización)

        Raises:
            InvalidTardinessPercentageError: Si el porcentaje está fuera del rango válido
        """
        if has_reached_minimum:
            return 0.0

        AttendancePolicy._validate_tardiness_percentage(tardiness_percentage)

        if tardiness_percentage >= (MIN_ATTENDANCE_PERCENTAGE * 100):
            return ATTENDANCE_PENALTY_FRACTION

        return 0.0

    @staticmethod
    def _validate_tardiness_percentage(tardiness_percentage: float) -> None:
        """
        Valida que el porcentaje de tardanzas esté en el rango válido.

        Args:
            tardiness_percentage: Porcentaje a validar

        Raises:
            InvalidTardinessPercentageError: Si el porcentaje está fuera del rango
        """
        if tardiness_percentage < MIN_PERCENTAGE or tardiness_percentage > MAX_PERCENTAGE:
            raise InvalidTardinessPercentageError(
                f"El porcentaje de tardanzas debe estar entre {MIN_PERCENTAGE} y "
                f"{MAX_PERCENTAGE}. Valor recibido: {tardiness_percentage}"
            )

