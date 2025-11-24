"""Tests unitarios para la clase ExtraPointsPolicy."""

import pytest

from src.constants import MAX_GRADE
from src.exceptions import InvalidExtraPointsError
from src.policies.extra_points_policy import ExtraPointsPolicy


class TestExtraPointsPolicy:
    """Tests para la clase ExtraPointsPolicy."""

    def test_shouldReturnTrueWhenAllTeachersAgree(self) -> None:
        """Debe retornar True cuando todos los profesores están de acuerdo."""
        all_teachers_agree = [True, True, True]
        can_assign = ExtraPointsPolicy.can_assign_extra_points(all_teachers_agree)
        assert can_assign is True

    def test_shouldReturnFalseWhenAnyTeacherDisagrees(self) -> None:
        """Debe retornar False cuando algún profesor no está de acuerdo."""
        some_disagree = [True, False, True]
        can_assign = ExtraPointsPolicy.can_assign_extra_points(some_disagree)
        assert can_assign is False

        all_disagree = [False, False, False]
        can_assign = ExtraPointsPolicy.can_assign_extra_points(all_disagree)
        assert can_assign is False

    def test_shouldReturnFalseWhenEmptyList(self) -> None:
        """Debe retornar False cuando la lista está vacía."""
        can_assign = ExtraPointsPolicy.can_assign_extra_points([])
        assert can_assign is False

    def test_shouldReturnCappedGradeWhenExtraPointsExceedMaximum(self) -> None:
        """Debe retornar nota máxima cuando puntos extra exceden el máximo."""
        base_grade = 18.0
        extra_points = 5.0
        final_grade = ExtraPointsPolicy.apply_extra_points(base_grade, extra_points)
        assert final_grade == MAX_GRADE

    def test_shouldApplyExtraPointsWhenWithinLimit(self) -> None:
        """Debe aplicar puntos extra cuando están dentro del límite."""
        base_grade = 15.0
        extra_points = 2.0
        final_grade = ExtraPointsPolicy.apply_extra_points(base_grade, extra_points)
        assert final_grade == 17.0

    def test_shouldRaiseErrorWhenExtraPointsAreNegative(self) -> None:
        """Debe lanzar error cuando los puntos extra son negativos."""
        with pytest.raises(InvalidExtraPointsError):
            ExtraPointsPolicy.apply_extra_points(base_grade=15.0, extra_points=-1.0)

    def test_shouldReturnBaseGradeWhenExtraPointsAreZero(self) -> None:
        """Debe retornar la nota base cuando puntos extra son cero."""
        base_grade = 15.0
        final_grade = ExtraPointsPolicy.apply_extra_points(base_grade, 0.0)
        assert final_grade == base_grade

    def test_shouldHandleSingleTeacherAgreement(self) -> None:
        """Debe manejar correctamente un solo profesor de acuerdo."""
        single_teacher = [True]
        can_assign = ExtraPointsPolicy.can_assign_extra_points(single_teacher)
        assert can_assign is True

