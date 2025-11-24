"""Política de Puntos Extra."""

from src.constants import MAX_GRADE
from src.exceptions import InvalidExtraPointsError


class ExtraPointsPolicy:
    """Maneja la lógica para la asignación de puntos extra."""

    @staticmethod
    def can_assign_extra_points(all_years_teachers: list[bool]) -> bool:
        """
        Verifica si se pueden asignar puntos extra.

        Los puntos extra solo se pueden asignar si todos los profesores
        del año están de acuerdo (todos los valores en la lista son True).

        Args:
            all_years_teachers: Lista de votos de los profesores (True/False)

        Returns:
            True si todos los profesores están de acuerdo, False en caso contrario
        """
        if not all_years_teachers:
            return False

        return all(all_years_teachers)

    @staticmethod
    def apply_extra_points(base_grade: float, extra_points: float) -> float:
        """
        Aplica puntos extra a la nota base, respetando el máximo permitido.

        Args:
            base_grade: Nota base a la que se aplicarán los puntos extra
            extra_points: Puntos extra a aplicar

        Returns:
            Nota final con puntos extra aplicados (no excede MAX_GRADE)

        Raises:
            InvalidExtraPointsError: Si los puntos extra son negativos
        """
        if extra_points < 0:
            raise InvalidExtraPointsError(
                f"Los puntos extra no pueden ser negativos. Valor recibido: {extra_points}"
            )

        final_grade = base_grade + extra_points

        # No exceder la nota máxima
        return min(final_grade, MAX_GRADE)

