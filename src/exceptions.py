"""Excepciones personalizadas del sistema."""


class GradeCalculatorError(Exception):
    """Excepción base para errores del calculador de notas."""

    pass


class InvalidEvaluationError(GradeCalculatorError):
    """Error cuando una evaluación es inválida."""

    pass


class InvalidWeightError(GradeCalculatorError):
    """Error cuando los pesos de las evaluaciones son inválidos."""

    pass


class MaxEvaluationsExceededError(GradeCalculatorError):
    """Error cuando se excede el máximo de evaluaciones permitidas."""

    pass


class InvalidTardinessPercentageError(GradeCalculatorError):
    """Error cuando el porcentaje de tardanzas es inválido."""

    pass


class InvalidExtraPointsError(GradeCalculatorError):
    """Error cuando los puntos extra son inválidos."""

    pass

