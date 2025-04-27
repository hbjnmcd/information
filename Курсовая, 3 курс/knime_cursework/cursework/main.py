import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
from statsmodels.tsa.arima.model import ARIMA



# Шаг 1: Чтение данных из файла Excel
file_path = ('C:/Users/mi/Desktop/ИВТ/Курсовая 3 курс/data.xlsx')  # Укажите путь к вашему файлу
print(file_path)
df = pd.read_excel(file_path)

print(df.head())


# 2. Построение графиков

plt.figure(figsize=(12, 6))

# График количества браков
plt.plot(df['Year'], df['Marriages_per_1000'], marker='o', label='Браки на 1000', color='blue')

# График рождаемости
plt.plot(df['Year'], df['Births_per_1000'], marker='o', label='Рождаемость на 1000', color='orange')

# Настройка меток и заголовка
plt.title('Сравнение количества браков и рождаемости по годам')
plt.xlabel('Год')
plt.ylabel('Показатели на 1000')
plt.legend()  # Добавление легенды
plt.tight_layout()
# Отображение графика
plt.show()

plt.subplot(1,1,1)
plt.plot(df['Year'], df['Social_benefit'], marker='o', color='green')
plt.title('Социальная выплата по рождению ребенка по годам')
plt.xlabel('Год')
plt.ylabel('Выплата (рубли)')

plt.tight_layout()
plt.show()

# 3. Нахождение корреляции
correlation_marriages, p_value_marriages = pearsonr(df['Marriages_per_1000'], df['Births_per_1000'])
correlation_benefit, p_value_benefit = pearsonr(df['Social_benefit'], df['Births_per_1000'])

print(f'Корреляция рождаемости от браков: {correlation_marriages}, p-значение: {p_value_marriages}')
print(f'Корреляция рождаемости от соц выплат: {correlation_benefit}, p-значение: {p_value_benefit}')

# Интерпретация p-значений
alpha = 0.05  # уровень значимости
if p_value_marriages < alpha:
    print("Корреляция между рождаемостью и количеством браков статистически значима.")
else:
    print("Корреляция между рождаемостью и количеством браков не статистически значима.")

if p_value_benefit < alpha:
    print("Корреляция между рождаемостью и социальными выплатами статистически значима.")
else:
    print("Корреляция между рождаемостью и социальными выплатами не значима статистически.")


# 4. Прогнозирование

births_model = ARIMA(df['Births_per_1000'], order=(0, 2, 2)).fit()

# Прогнозируем на 2024-2030 годы (7 лет)
future_births = births_model.forecast(steps=7)

# Выводим результаты
years_forecast = list(range(2024, 2031))  # Годы с 2024 по 2030
forecast_results = pd.DataFrame({'Year': years_forecast, 'Births': future_births})

print("Прогноз рождаемости на 2024-2030 годы:")
print(forecast_results)

# Объединяем исторические данные и прогнозы для графика
new_df = pd.DataFrame({'Year': df['Year'], 'Births': df['Births_per_1000']})
#print(new_df)
full_df = pd.concat([new_df, forecast_results])
#print(full_df)

# Дополнение графика
plt.figure(figsize=(12, 6))
plt.plot(full_df['Year'], full_df['Births'], marker='o', label='Рождаемость на 1000')
plt.title('Прогноз рождаемости на 2024-2030 годы')
plt.xlabel('Год')
plt.ylabel('Рождаемость на 1000')
plt.axvline(x=2023, color='grey', linestyle='--', label='Начало прогноза')
plt.legend()
plt.show()
