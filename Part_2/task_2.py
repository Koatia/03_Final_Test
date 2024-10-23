from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import proportion_effectsize

# Заданные параметры
current_conversion = 0.05  # Текущая конверсия
expected_increase = 0.002  # Ожидаемое улучшение конверсии
expected_conversion = current_conversion + expected_increase  # Ожидаемая конверсия
alpha = 0.03  # Уровень доверия (1 - 0.97)
power = 0.87  # Мощность теста
visitors_per_month = 40000  # Посетители в месяц

# Рассчитываем эффект на основе разницы конверсий
effect_size = proportion_effectsize(expected_conversion, current_conversion)

# Используем модель для расчета размера выборки
power_analysis = NormalIndPower()

# Размер выборки для каждой группы
sample_size_per_group = power_analysis.solve_power(
    effect_size=effect_size,
    alpha=alpha,
    power=power,
    alternative='two-sided'
    )

# Общее количество пользователей для обеих групп
total_sample_size = sample_size_per_group * 2

# Количество посетителей в день
visitors_per_day = visitors_per_month / 30

# Рассчитаем количество дней, необходимых для тестирования
days_needed = total_sample_size / visitors_per_day

# Вывод результатов
print(f"Необходимое количество пользователей для каждой группы: {sample_size_per_group:.2f}")
print(f"Общее количество пользователей: {total_sample_size:.2f}")
print(f"Необходимое количество дней для тестирования: {days_needed:.2f}")
