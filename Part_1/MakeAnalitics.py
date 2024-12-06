import locale
import re

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Устанавливаем русскую локаль для корректной обработки названий месяцев на русском
try:
    locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')  # Для Linux/macOS
    # locale.setlocale(locale.LC_TIME, 'russian')   # Для Windows
except locale.Error:
    print("Не удалось установить русскую локаль. Убедитесь, что она доступна на вашем компьютере.")

# Чтение данных
data_path = r"marketing.csv"
data = pd.read_csv(data_path)

# Очистка данных
data.columns = data.columns.str.strip()  # Удаляем лишние пробелы в названиях колонок
cleaned_data = data.dropna(
    subset=['Device Category', 'Region', 'Goal Completions']).copy()  # Удаление строк с пропусками

# Преобразование строки с процентами в числовой формат
cleaned_data['Goal Conversion Rate'] = cleaned_data['Goal Conversion Rate'].str.replace('%', '').astype(float)

# Очистим даты от лишних символов, включая "г." и возможные пробелы
cleaned_data['Date'] = cleaned_data['Date'].apply(lambda x: re.sub(r' г\.', '', x).strip())

# Преобразуем строку в формат даты
cleaned_data['Date'] = pd.to_datetime(cleaned_data['Date'], format='%d %B %Y', errors='coerce')

# Удаление строк с некорректными датами
cleaned_data = cleaned_data.dropna(subset=['Date'])

# 1. Из каких регионов больше всего заявок?
region_counts = cleaned_data.groupby('Region')['Goal Completions'].sum().sort_values(ascending=False)
print("Топ-3 регионов с наибольшим количеством заявок:")
print(region_counts.head(3))

plt.figure(figsize=(12, 6))
region_counts.head(3).plot(kind='bar')
plt.title('Топ-3 регионов по количеству заявок')
plt.xlabel('Регион')
plt.ylabel('Количество заявок')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# 2. Какой средний процент отказов (Bounce)?
# average_bounce_rate = cleaned_data['Bounce Rate'].mean()
# print(f"Средний процент отказов: {average_bounce_rate:.2f}%")
average_bounce_rate = data['Bounce Rate'].mean() * 100
print(f"Средний процент отказов: {average_bounce_rate:.4f}")

# 3. С каких устройств чаще заходят на сайты?
device_counts = cleaned_data['Device Category'].value_counts()
print("Количество заходов с разных устройств:")
print(device_counts)

plt.figure(figsize=(12, 6))
device_counts.plot(kind='bar')
plt.title('Заходы по устройствам')
plt.xlabel('Устройства')
plt.ylabel('Количество')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# 4. Какие источники наиболее конвертируемые?
# Рассчитаем сумму конверсий по каждому источнику
source_conversion_sum = cleaned_data.groupby('Source')['Goal Completions'].sum().sort_values(ascending=False)

print("Топ источников по количеству конверсий:")
print(source_conversion_sum.head(5))

# Построим график для топ-5 источников
plt.figure(figsize=(12, 6))
source_conversion_sum.head(5).plot(kind='bar')
plt.title('Топ источников по количеству конверсий')
plt.xlabel('Источник')
plt.ylabel('Количество конверсий')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# 5. Расчет ROMI (Return on Marketing Investment)
average_car_price = 5333674.179  # Средняя стоимость авто (получено из PowerBI)
# Вычисление общей выручки
total_revenue = cleaned_data['Goal Completions'].sum() * average_car_price

def clean_numeric(value):
    if pd.isna(value):
        return np.nan
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        cleaned = ''.join(char for char in value if char.isdigit() or char in '.,')
        cleaned = cleaned.replace(',', '.')
        try:
            return float(cleaned)
        except ValueError:
            return np.nan
    return np.nan

numeric_columns = ['Sessions', 'Goal Completions']
for col in numeric_columns:
    cleaned_data[col] = cleaned_data[col].apply(clean_numeric)

grouped = cleaned_data.groupby('Source').agg({
    'Sessions': 'sum',
    'Goal Completions': 'sum'
    })

# Расчет конверсии
grouped['Conversion Rate'] = grouped['Goal Completions'] / grouped['Sessions']

# Расчет дохода на основе средней стоимости автомобиля
grouped['Revenue'] = grouped['Goal Completions'] * average_car_price

# Предположим, что стоимость привлечения одной сессии составляет 100 руб.
cost_per_session = 100
grouped['Marketing Cost'] = grouped['Sessions'] * cost_per_session

# Расчет ROMI
grouped['ROMI'] = (grouped['Revenue'] - grouped['Marketing Cost']) / grouped['Marketing Cost'] * 100
grouped_sorted = grouped.sort_values('ROMI', ascending=False)

print(f"Средняя стоимость проданного автомобиля: {average_car_price:.2f} руб.")
print("\nТоп-10 источников по ROMI:")
print(grouped_sorted[['Sessions', 'Goal Completions', 'Revenue', 'Conversion Rate', 'Marketing Cost', 'ROMI']].head(10))

# 6. Выручка в рублях только по долларовым позициям -- см. в PowerBI

usd_to_rub = 100  # Курс доллара к рублю

# Фильтруем только те строки, где значение в Goal Value содержит знак доллара '$'
if 'Goal Value' in cleaned_data.columns:
    dollar_sales = cleaned_data[cleaned_data['Goal Value'].str.contains(r'\$', na=False)]

    # Удаляем символ '$' и преобразуем к числовому формату
    dollar_sales['Goal Value'] = dollar_sales['Goal Value'].str.replace('$', '').astype(float)

    # Рассчитываем выручку в рублях
    revenue_in_rub = dollar_sales['Goal Value'].sum() * usd_to_rub
    print(f"Выручка в рублях по долларовым позициям: {revenue_in_rub:.2f} руб.")
else:
    print("Нет данных по долларовым позициям.")

# 7. Прогноз до конца февраля по количеству конверсий на каждый день
if pd.api.types.is_datetime64_any_dtype(cleaned_data['Date']):
    daily_conversions = cleaned_data.groupby(cleaned_data['Date'].dt.date)['Goal Completions'].sum()

    # Проверяем, есть ли данные для прогноза
    if len(daily_conversions) > 0:
        forecast_days = pd.date_range(start='2020-02-01', end='2020-02-29')  # Прогноз на февраль
        average_daily_conversions = daily_conversions.mean()
        forecast_conversions = pd.Series(average_daily_conversions, index=forecast_days)
        print("Прогноз по количеству конверсий на каждый день февраля:")
        print(forecast_conversions)
    else:
        print("Нет данных для прогнозирования конверсий на февраль.")
else:
    print("Колонка 'Date' не содержит данные типа datetime.")

# 8. Прогноз выручки за первый квартал
if len(daily_conversions) > 0:
    q1_forecast_revenue = (total_revenue / len(daily_conversions.index)) * 90  # Прогноз на 90 дней
    print(f"Прогнозируемая выручка за первый квартал: {q1_forecast_revenue:.2f} руб.")
else:
    print("Нет данных для прогнозирования выручки за первый квартал.")
