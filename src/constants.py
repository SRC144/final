"""Constantes del sistema CS-GradeCalculator."""

# Requerimientos No Funcionales
MAX_EVALUATIONS = 10  # RNF01: Cantidad máxima de evaluaciones por estudiante
MAX_CONCURRENT_USERS = 50  # RNF02: Usuarios concurrentes soportados
MAX_CALCULATION_TIME_MS = 300  # RNF04: Tiempo máximo de cálculo por solicitud

# Política de Asistencia
MIN_ATTENDANCE_PERCENTAGE = 0.40  # 40% de tardanzas para aplicar penalización
ATTENDANCE_PENALTY_FRACTION = 0.10  # Fracción de penalización (10% de la nota)

# Escala de Notas
MAX_GRADE = 20.0  # Nota máxima en escala 0-20
MIN_GRADE = 0.0  # Nota mínima

# Validación de Pesos
EXPECTED_WEIGHT_SUM = 100.0  # Suma esperada de pesos (100%)
WEIGHT_TOLERANCE = 0.01  # Tolerancia para validación de pesos

# Porcentajes
MIN_PERCENTAGE = 0.0
MAX_PERCENTAGE = 100.0

