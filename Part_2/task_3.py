# Данные конверсий для трех источников
conversions = [25000, 30000, 32000]
visitors = 40000  # Общее количество посетителей для каждого источника

# Рассчитаем конверсию для каждого источника
conversion_rates = [conv / visitors for conv in conversions]

print(conversion_rates)

# Выполним Z-тест для сравнения пропорций между источниками
from statsmodels.stats.proportion import proportions_ztest

# Подготовим данные для теста
conversion_counts = [25000, 30000, 32000]
sample_sizes = [visitors] * 3

# Проведем Z-тест для сравнения каждого источника с предыдущим
z_stat_1_vs_2, p_value_1_vs_2 = proportions_ztest([conversion_counts[0], conversion_counts[1]],
                                                  [sample_sizes[0], sample_sizes[1]])
z_stat_2_vs_3, p_value_2_vs_3 = proportions_ztest([conversion_counts[1], conversion_counts[2]],
                                                  [sample_sizes[1], sample_sizes[2]])

print(f'Z-статистика: {z_stat_1_vs_2:.2f} P-значение: {p_value_1_vs_2:.5f}')
print(f'Z-статистика: {z_stat_2_vs_3:.2f} P-значение: {p_value_2_vs_3:.5f}')
