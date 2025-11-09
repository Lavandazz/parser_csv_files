from src.parser import Parser
from src.reports import ReportRegistry
from src.services.file_service import RatingReport, PriceReport

# python main.py --files data/products1.csv data/products2.csv --report rating


def register_reports():
    """
    Регистрация отчетов.
    """
    ReportRegistry.register_report("rating", RatingReport)
    ReportRegistry.register_report("price", PriceReport)


def main():
    register_reports()
    parser = Parser()
    parser.run_parsing()


if __name__ == '__main__':
    main()
