"""Tests unitarios para la clase AttendancePolicy."""

import pytest

from src.constants import MAX_PERCENTAGE, MIN_ATTENDANCE_PERCENTAGE, MIN_PERCENTAGE
from src.exceptions import InvalidTardinessPercentageError
from src.policies.attendance_policy import AttendancePolicy


class TestAttendancePolicy:
    """Tests para la clase AttendancePolicy."""

    def test_shouldReturnZeroWhenMinimumAttendanceReached(self) -> None:
        """Debe retornar 0 cuando se alcanza la asistencia mínima."""
        penalty = AttendancePolicy.calculate_penalty(
            has_reached_minimum=True, tardiness_percentage=50.0
        )
        assert penalty == 0.0

    def test_shouldReturnPenaltyWhenTardinessExceedsThreshold(self) -> None:
        """Debe retornar penalización cuando tardanzas >= 40%."""
        threshold = MIN_ATTENDANCE_PERCENTAGE * 100
        penalty = AttendancePolicy.calculate_penalty(
            has_reached_minimum=False, tardiness_percentage=threshold
        )
        assert penalty > 0.0

        penalty = AttendancePolicy.calculate_penalty(
            has_reached_minimum=False, tardiness_percentage=50.0
        )
        assert penalty > 0.0

    def test_shouldReturnZeroWhenTardinessBelowThreshold(self) -> None:
        """Debe retornar 0 cuando tardanzas < 40%."""
        penalty = AttendancePolicy.calculate_penalty(
            has_reached_minimum=False, tardiness_percentage=39.0
        )
        assert penalty == 0.0

    def test_shouldRaiseErrorWhenTardinessPercentageIsNegative(self) -> None:
        """Debe lanzar error cuando el porcentaje de tardanzas es negativo."""
        with pytest.raises(InvalidTardinessPercentageError):
            AttendancePolicy.calculate_penalty(
                has_reached_minimum=False, tardiness_percentage=-1.0
            )

    def test_shouldRaiseErrorWhenTardinessPercentageExceedsMaximum(self) -> None:
        """Debe lanzar error cuando el porcentaje excede 100%."""
        with pytest.raises(InvalidTardinessPercentageError):
            AttendancePolicy.calculate_penalty(
                has_reached_minimum=False, tardiness_percentage=MAX_PERCENTAGE + 1
            )

    def test_shouldAcceptTardinessAtBoundaries(self) -> None:
        """Debe aceptar porcentajes en los límites válidos."""
        penalty_min = AttendancePolicy.calculate_penalty(
            has_reached_minimum=False, tardiness_percentage=MIN_PERCENTAGE
        )
        assert penalty_min >= 0.0

        penalty_max = AttendancePolicy.calculate_penalty(
            has_reached_minimum=False, tardiness_percentage=MAX_PERCENTAGE
        )
        assert penalty_max >= 0.0

