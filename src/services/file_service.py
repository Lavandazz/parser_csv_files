from collections import defaultdict
from abc import ABC, abstractmethod


class BaseReport(ABC):
    """
    Абстрактный базовый класс для всех типов отчетов.
    """
    @abstractmethod
    def generate(self, products):
        """Реализация в дочерних классах"""
        pass

    @abstractmethod
    def get_name(self):
        """Реализация в дочерних классах"""
        pass

    @abstractmethod
    def get_headers(self):
        pass


class RatingReport(BaseReport):
    """
    Отчет по среднему рейтингу товаров по брендам.
    """

    def generate(self, products):
        """
        Вычисляет средний рейтинг для каждого бренда.
        :param products: List(Product)
        :return: Список пар (бренд, средний_рейтинг), отсортированный по убыванию рейтинга
        """
        # создаем словарь и сохраняем ключ: бренд, значение: рейтинг
        ratings = defaultdict(list)
        # Группируем рейтинги по брендам
        for product in products:
            ratings[product.brand].append(product.rating)

        report_data = []
        for brand, ratings in ratings.items():
            # Считаем средний рейтинг по бренду
            avg_rating = sum(ratings) / len(ratings)
            # Добавляем в список пару бренд, округленный рейтинг
            report_data.append((brand, round(avg_rating, 2)))

        # Сортируем элементы по рейтингу. Сначала высокий, потом низкий
        return sorted(report_data, key=lambda x: x[1], reverse=True)

    def get_name(self):
        """Возвращает название отчета """
        return "Средний рейтинг по брендам"

    def get_headers(self):
        """Возвращает заголовки для таблицы рейтингов."""
        return ['Бренд', 'Средний рейтинг']


class PriceReport(BaseReport):
    """Отчет по средней цене товаров по брендам."""
    def generate(self, products):
        print("products:", products)
        # Создаем словарь и сохраняем ключ: рейтинг товара, значение: цена
        prices = defaultdict(list)
        for product in products:
            prices[product.brand].append(product.price)

        report_data = []

        for brand, prices_list in prices.items():
            avg_price = sum(prices_list) / len(prices_list)
            report_data.append((brand, round(avg_price, 2)))

        return sorted(report_data, key=lambda x: x[1], reverse=True)

    def get_name(self):
        """Возвращает название отчета """
        return "Средняя цена по брендам"

    def get_headers(self):
        """Возвращает заголовки для таблицы рейтингов."""
        return ['Бренд', 'Средняя цена']
