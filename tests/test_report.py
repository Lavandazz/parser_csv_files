from src.models import Product
from src.services.file_service import RatingReport


rating_report = RatingReport()


def test_rating_rating_report():
    """
    Проверяем, что отчет имеет правильное название
    """
    assert rating_report.get_name() == "Средний рейтинг по брендам"


def test_headers_rating_report():
    """
    Проверяем заголовки таблицы рейтингов
    """
    assert rating_report.get_headers() == ["Бренд", "Средний рейтинг"]


def test_generate_rating_report():
    products = [
        Product(name="iphone 15 pro", brand="apple", price=999, rating=4.9),
        Product(name="galaxy s23 ultra", brand="samsung", price=1199, rating=4.8)
    ]
    result = rating_report.generate(products)
    assert len(result) == 2
    assert result[0][0] == "apple"
    assert result[1][1] == 4.8


def test_rating_report():
    products = [
        Product(name="iphone se", brand="apple", price=429, rating=4.1),
        Product(name="iphone 13 mini", brand="apple", price=599, rating=4.5)
    ]
    result = rating_report.generate(products)
    avg_rating = sum([4.1, 4.5]) / 2
    assert len(result) == 1
    assert result[0][0] == "apple"
    assert result[0][1] == avg_rating
