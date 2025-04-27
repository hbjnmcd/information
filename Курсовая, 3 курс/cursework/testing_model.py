import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima.model import ARIMA

# Функция для проверки стационарности
def test_stationarity(timeseries):
    result = adfuller(timeseries)
    print('Статистика теста:', result[0])
    print('p-значение:', result[1])
    print('Критические значения:')
    for key, value in result[4].items():
        print(f'  {key}: {value}')

    return result[1] < 0.05  # Возвращаем True, если ряд стационарен

# Загрузка данных
file_path = 'C:/Users/mi/Desktop/ИВТ/Курсовая 3 курс/data.xlsx'  # Укажите путь к вашему файлу
df = pd.read_excel(file_path)

'''# Создание временного индекса на основе столбца 'Year'
df['Date'] = pd.to_datetime(df['Year'].astype(str) + '-01-01')
df.set_index('Date', inplace=True)  # Устанавливаем 'Date' как индекс'''

# Проверка стационарности временного ряда 'Births_per_1000'
print("Проверка стационарности временного ряда 'Births_per_1000':")
is_stationary = test_stationarity(df['Births_per_1000'])

diff_count = 0  # Счетчик разностей
print('Ищем количество разностей:')
while not is_stationary:
    # Применяем разности
    df['Births_per_1000'] = df['Births_per_1000'].diff().dropna()
    df = df.dropna()  # Удаляем строки с NaN
    diff_count += 1  # Увеличиваем счетчик разностей

    # Проверяем стационарность разностей
    print(f"Применены {diff_count} разности к временном ряду 'Births_per_1000':")
    print("Проверка стационарности разностей 'Births_per_1000':")
    is_stationary = test_stationarity(df['Births_per_1000'])

# После завершения цикла
print(f"Общее количество примененных разностей: {diff_count}")

# Определяем количество наблюдений
n = len(df['Births_per_1000'])

# Пример оценки модели ARIMA с различными p и q
best_aic = np.inf
best_order = None
best_model = None

# Пробуем разные значения p и q
for p in range(10):  # Измените диапазон по необходимости
    for q in range(10):  # Измените диапазон по необходимости
        try:
            model = ARIMA(df['Births_per_1000'], order=(p, diff_count, q))
            model_fit = model.fit()
            print(f'ARIMA({p}, {diff_count}, {q}) - AIC: {model_fit.aic}')
            if model_fit.aic < best_aic:
                best_aic = model_fit.aic
                best_order = (p, diff_count, q)
                best_model = model_fit
        except Exception as e:
            print(f'Ошибка при оценке модели ARIMA({p}, {diff_count}, {q}): {e}')
            continue

print(f'Лучшие параметры: {best_order} с AIC: {best_aic}')
