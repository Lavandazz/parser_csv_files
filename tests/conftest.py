import pytest

from src.models import Product
from src.parser import Parser
from src.reports import ReportRegistry
from src.services.file_service import RatingReport, PriceReport


@pytest.fixture
def sample_report():
    ReportRegistry.register_report("rating", RatingReport)
    ReportRegistry.register_report("price", PriceReport)


@pytest.fixture
def sample_parser():
    return Parser()


@pytest.fixture
def sample_products():
    return [
        Product(name="iphone 13 mini", brand="apple", price=599, rating=4.5),
        Product(name="redmi 10c", brand="xiaomi", price=149, rating=4.2),
        Product(name="iphone se", brand="apple", price=429, rating=4.1)
    ]


@pytest.fixture
def sample_text():
    csv_text = ("name,brand,price,rating\n"
                "iphone 13 mini,apple,599,4.5\n"
                "redmi 10c,xiaomi,149,4.1\n"
                "iphone se,apple,429,4.1")
    return csv_text
