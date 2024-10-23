import pandas as pd
import matplotlib.pyplot as plt
import locale
import re

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
cleaned_data = data.dropna(subset=['Device Category', 'Region', 'Goal Completions']).copy()  # Удаление строк с пропусками

# Преобразование строки с процентами в числовой формат
cleaned_data['Goal Conversion Rate'] = cleaned_data['Goal Conversion Rate'].str.replace('%', '').astype(float)

# Очистим даты от лишних символов, включая "г." и возможные пробелы
cleaned_data['Date'] = cleaned_data['Date'].apply(lambda x: re.sub(r' г\.', '', x).strip())

# Преобразуем строку в формат даты
cleaned_data['Date'] = pd.to_datetime(cleaned_data['Date'], format='%d %B %Y', errors='coerce')

# Проверим тип данных после преобразования
print(f"Тип данных в колонке 'Date' после преобразования: {cleaned_data['Date'].dtype}")

# Проверим первые строки после преобразования
print("Первые строки после преобразования:")
print(cleaned_data['Date'].head(10))

# Убедимся, что все данные теперь типа datetime64[ns]
if pd.api.types.is_datetime64_any_dtype(cleaned_data['Date']):
    # Удаление строк с некорректными датами
    cleaned_data = cleaned_data.dropna(subset=['Date'])

    # Группировка данных по датам
    try:
        daily_conversions = cleaned_data.groupby(cleaned_data['Date'].dt.date)['Goal Completions'].sum()

        # Проверяем, есть ли данные для прогноза
        if len(daily_conversions) > 0:
            forecast_days = pd.date_range(start='2024-02-01', end='2024-02-29')  # Прогноз на февраль
            average_daily_conversions = daily_conversions.mean()
            forecast_conversions = pd.Series(average_daily_conversions, index=forecast_days)
            print("Прогноз по количеству конверсий на каждый день февраля:")
            print(forecast_conversions)
        else:
            print("Нет данных для прогнозирования конверсий на февраль.")
    except Exception as e:
        print(f"Ошибка при работе с датами: {e}")
else:
    print("Колонка 'Date' не содержит данные типа datetime.")
