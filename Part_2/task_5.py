from scipy import stats

# Данные для групп A и B
mean_A = 360
std_A = 40
n_A = 9802

mean_B = 352
std_B = 58
n_B = 9789

# Выполним двухвыборочный t-тест с допущением о неравных дисперсиях (тест Уэлча)
t_stat, p_value = stats.ttest_ind_from_stats(
    mean1=mean_A, std1=std_A, nobs1=n_A,
    mean2=mean_B, std2=std_B, nobs2=n_B,
    equal_var=False  # Используем для неравных дисперсий
)

# Выводим t-статистику и p-значение
print(f'T-статистика: {t_stat:.2f} P-значение: {p_value}')