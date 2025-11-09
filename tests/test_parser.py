import os
import tempfile

from src.models import Product
from src.reports import ReportRegistry
from src.utils.logging_config import test_logger


def test_reports(sample_report):
    """
    Регистрация отчетов.
    """

    reports = {
        name: class_report() for name, class_report in ReportRegistry.get_reports().items()
    }
    assert list(reports) == ["rating", "price"]


def test_parser_read_csv(sample_text, sample_parser):
    """
    Проверка чтения csv.
    Создается файл с тестовыми данными.
    :return:
    """
    try:
        with tempfile.NamedTemporaryFile(
                mode="w", dir="tests/files", suffix=".csv", delete=False
        ) as fp:
            fp.write(sample_text)
            test_file = fp.name

        products = sample_parser.read_files([test_file])
        test_logger.debug("Loaded %d products", len(products))
        # Проверяем что вернулся список объектов Product
        assert isinstance(products, list)
        assert len(products) == 3

        assert isinstance(products[0], Product)
        assert isinstance(products[1], Product)

        assert products[0].name == 'iphone 13 mini'
        assert products[0].brand == 'apple'
        assert products[0].price == 599
        assert products[0].rating == 4.5

    finally:
        # Удаляем файл в любом случае (даже если тест упал)
        if os.path.exists(test_file):
            os.unlink(test_file)


def test_read_empty_csv(sample_parser):
    """
    Тест пустого CSV файла (только заголовки).
    Создаем файл, после чтения, удаляем.
    """
    csv_content = "name,brand,price,rating\n"

    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write(csv_content)
        test_file = f.name

    try:
        products = sample_parser.read_files([test_file])
        assert products == []  # должен вернуть пустой список
    finally:
        os.unlink(test_file)


def test_multiple_files(sample_parser):
    """Тест чтения нескольких файлов"""
    csv1 = "name,brand,price,rating\niphone se,apple,429,4.1"
    csv2 = "name,brand,price,rating\ngalaxy z flip 5,samsung,999,4.6"

    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write(csv1)
        file1 = f.name

    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write(csv2)
        file2 = f.name

    try:
        products = sample_parser.read_files([file1, file2])
        assert len(products) == 2
        assert products[0].name == "iphone se"
        assert products[1].name == "galaxy z flip 5"
    finally:
        os.unlink(file1)
        os.unlink(file2)


def test_calculation_price(sample_parser, sample_products):

    # Берем отчет по ценам
    report = sample_parser.reports["price"]
    result = report.generate(sample_products)

    # Проверяем расчет
    apple_price = None
    for brand, price in result:
        if brand == 'apple':
            apple_price = price
            break

    avg_price = sum([599, 429]) / 2
    assert apple_price == 514, f"Ожидалось 514, получилось {avg_price}"


def test_parser_has_correct_reports(sample_parser):
    """Загрузка отчетов"""
    # Проверяем что есть нужные отчеты
    assert 'rating' in sample_parser.reports
    assert 'price' in sample_parser.reports

    # Проверяем что у отчетов есть нужные методы
    assert hasattr(sample_parser.reports['rating'], 'generate')
    assert hasattr(sample_parser.reports['rating'], 'get_name')
    assert hasattr(sample_parser.reports['price'], 'generate')
    assert hasattr(sample_parser.reports['price'], 'get_name')
