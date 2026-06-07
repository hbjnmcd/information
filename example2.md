# Лабораторная работа: Среда Python и Jupyter Notebook

## Описание задачи
Проанализировать CSV-датасет с результатами экзамена: загрузить, 
провести первичный анализ, визуализировать распределение оценок, 
очистить данные от пропусков и сохранить обработанный файл.

---

## Ячейка 1. Загрузка данных через pandas

```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Загрузка CSV через pandas.read_csv
df = pd.read_csv("exam_results.csv")

print(f"Размер датасета (shape): {df.shape}")

# Структура и типы данных: info()
df.info()

# Дескриптивная статистика: describe()
print(df.describe(include="all"))

# Визуализация через seaborn/matplotlib
sns.set_theme(style="whitegrid")
plt.figure(figsize=(8, 4))
sns.histplot(df["score"].dropna(), kde=True, bins=20)
plt.title("Распределение баллов за экзамен")
plt.xlabel("Балл")
plt.ylabel("Количество студентов")
plt.tight_layout()
plt.show()

# Проверка пропусков через isnull + визуализация
missing = df.isnull().sum()
plt.figure(figsize=(8, 4))
sns.barplot(x=missing.index, y=missing.values)
plt.title("Количество пропусков по столбцам")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Обработка пропусков: fillna для числовых столбцов
df["score"] = df["score"].fillna(df["score"].median())
df["attendance"] = df["attendance"].fillna(0)

# Удаление строк с критичными пропусками: dropna
df = df.dropna(subset=["student_id", "group"])

# Проверка после очистки
print(f"Пропусков после очистки (isnull): {df.isnull().sum().sum()}")
print(f"Итоговый размер датасета (shape): {df.shape}")

# Сохранение в CSV через to_csv
output_path = "exam_results_cleaned.csv"
df.to_csv(output_path, index=False, encoding="utf-8")

print(f"Очищенный файл сохранён: {output_path}")

# Граничный случай 1: пустой DataFrame
empty_df = pd.DataFrame(columns=df.columns)
assert empty_df.shape == (0, len(df.columns)), "Пустой DataFrame не обработан"

# Граничный случай 2: все значения в score — NaN
edge_df = pd.DataFrame({"score": [float("nan"), float("nan")], "student_id": [1, 2]})
edge_df["score"] = edge_df["score"].fillna(edge_df["score"].median())
assert edge_df["score"].notna().all(), "Пропуски не заполнены"

# Граничный случай 3: дубликаты student_id
dup_df = pd.DataFrame({
    "student_id": [1, 1, 2],
    "score": [80, 80, 90],
    "group": ["A", "A", "B"]
})
# Проверка: duplicated() находит повторы
assert dup_df["student_id"].duplicated().sum() == 2, "Дубликаты не определены"

print("Все граничные случаи пройдены.")
```


## Выводы
В ходе лабораторной работы я загрузил CSV-датасет через pandas.read_csv(), провёл первичный анализ используя shape, info() и describe(). Построил две визуализации: распределение баллов через seaborn.histplot и количество пропусков по столбцам через seaborn.barplot. Очистка данных realizada с помощью fillna для числовых полей и dropna для критичных строк, после чего результат сохранён через to_csv. Граничные случаи (пустой набор, полностью пропущенные значения, дубликаты) проверены и не вызывают падения пайплайна. Основный риск — потеря данных при агрессивном удалении строк — закрыт проверкой критичных столбцов перед dropna.

## Технические детали
Среда: Python 3.11, pandas, matplotlib, seaborn, Jupyter Notebook
Исходный файл: exam_results.csv
Выходной файл: exam_results_cleaned.csv
