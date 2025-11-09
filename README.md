# Product Reports Analyzer

Скрипт для анализа товаров из CSV файлов. Генерирует отчеты по рейтингам и ценам брендов.

## Быстрый старт

### 1. Установка зависимостей

pip install -r requirements.txt

### 2. добавьте CSV файлы в папку data.
Файлы должны содержать столбцы: name, brand, price, rating

Пример data/products.csv:

name,brand,price,rating
poco x5 pro,xiaomi,299,4.4
iphone se,apple,429,4.1
galaxy z flip 5,samsung,999,4.6
redmi 10c,xiaomi,149,4.1
iphone 13 mini,apple,599,4.5

### 3. Запуск анализа
bash
# Анализ одного файла
python main.py --files data/products.csv --report rating

# Анализ нескольких файлов
python main.py --files data/products1.csv data/products2.csv --report rating

# Отчет по ценам
python main.py --files data/products.csv --report price

#### Доступные отчеты
rating - средний рейтинг по брендам (сортировка по убыванию)

price - средняя цена по брендам (сортировка по убыванию)

# Запустить все тесты
pytest tests/

# Запустить с подробным выводом
pytest tests/ -v


### Пример отчета

Средний рейтинг по брендам:
+-----------+-------------------+
| Бренд     |   Средний рейтинг |
|-----------+-------------------|
| apple     |              4.85 |
| samsung   |              4.65 |
| xiaomi    |              4.5  |
+-----------+-------------------+

Всего обработано товаров: 10

### Для добавления нового отчета:

Создайте класс в src/services/file_service.py

Унаследуйте от BaseReport

Реализуйте методы generate(), get_name() и get_headers()
