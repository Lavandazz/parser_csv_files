import argparse
import csv

from dataclasses import dataclass
from tabulate import tabulate

from src.models import Product
from src.reports import ReportRegistry
from src.utils.logging_config import parser_logger


@dataclass()
class Parser:
    """
    Класс для обработки аргументов командной строки и генерации отчетов.
    """
    def __init__(self):
        """
        Инициализирует парсер и загружает все доступные отчеты из реестра.
        Имеет вид: {'rating': RatingReport(), 'price': PriceReport()}
        """
        self.reports = {
            name: class_report() for name, class_report in ReportRegistry.get_reports().items()
        }
        parser_logger.info(f"Загружены отчеты: {list(self.reports.keys())}")

    def parser_arguments(self):
        """
        Парсит аргументы командной строки.
        - files: список путей к CSV файлам
        - report: тип запрашиваемого отчета
        :return:
        """
        parser = argparse.ArgumentParser(
            description="Отчеты по товарам"
        )

        parser.add_argument(
            "--files",
            nargs="+",
            help="Список CSV файлов необходимо указывать через пробел",
            required=True
        )
        # добавляем аргумент, разрешающий только отчеты из списка self.reports.keys(): ["rating", "price"...]
        parser.add_argument(
            "--report",
            choices=list(self.reports.keys()),
            help="Тип отчета",
            required=True
        )

        return parser.parse_args()

    def read_files(self, files: list) -> list | None:
        """
        Читает и парсит данные из нескольких CSV файлов.
        Принимает готовый список из файлов в папке data.
        All_products - список, куда будет сохраняться вся информация из всех переданных файлов.
        Имеет вид list(Product)
        :param files: Список путей к CSV файлам для обработки
        :return: list(Product)
        """
        all_products = []
        cnt_files = 0
        for file in files:
            try:
                with open(file, "r", encoding="utf-8") as fl:
                    # проверка на csv файл.
                    reader = csv.DictReader(fl)

                    file_products = []
                    cnt_files += 1

                    for row in reader:
                        parser_logger.debug("строка row {row}. тип: %s".format(row=row), type(row))
                        # IDE думает что в row строка, но передается тип: <class 'dict'>.
                        # Который преобразуем в модель Product
                        product = Product(
                            name=row.get("name"),
                            brand=row.get("brand"),
                            price=int(row.get("price")),
                            rating=float(row.get("rating")),

                        )
                        parser_logger.debug("product: %s", product)
                        file_products.append(product)
                all_products.extend(file_products)

            except UnicodeDecodeError as ud:
                parser_logger.error(f"Передан некорректный файл: {ud}")
                print("❌ Передан некорректный файл. Проверьте расширение файла. Принимается только csv! ❌")
                return None

            except Exception as e:
                print(f"❌ Ошибка чтения {file}: {e}")
                return None

        parser_logger.info(f"Всего товаров:  {len(all_products)}")
        parser_logger.info(f"Всего файлов:  {cnt_files}")
        return all_products

    def run_parsing(self):
        """
        Основной метод запуска процесса парсинга и генерации отчетов.
        - terminal_args - Парсит аргументы командной строки
        - products - Читает данные из указанных файлов
        - report - Генерирует выбранный отчет
        - Выводит результат в виде форматированной таблицы
        """
        # объект Namespace, (files=['data/products1.csv', 'data/products2.csv'], report='rating')
        terminal_args = self.parser_arguments()
        parser_logger.debug("Получены аргументы из терминала: %s, отчет: %s ", terminal_args, terminal_args.report)

        products = self.read_files(terminal_args.files)

        if not products:
            parser_logger.error(f"Не передано аргументов")
            return

        parser_logger.debug("Получено products: %d", len(products))
        # передаем ключ названия отчета из парсинга терминала
        report = self.reports[terminal_args.report]

        report_data = report.generate(products)

        print(f"\n{report.get_name()}:")
        table = report.get_headers()
        print(tabulate(report_data, headers=table, tablefmt='psql'))
        print(f"\nВсего обработано товаров: {len(products)}")
