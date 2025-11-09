class ReportRegistry:
    """
    Реестр для регистрации и хранения доступных типов отчетов. Например, отчеты price, rating.
    При регистрации отчет сохраняется в словаре reports для дальнейшего использования.
    """
    reports = {}

    @classmethod
    def register_report(cls, name: str, report_class: object):
        """
        Регистрирует класс отчета в реестре.
        :param name: Уникальное имя отчета (например, "rating", "price")
        :param report_class: Класс отчета, который должен наследоваться от BaseReport

        Регистрация: ReportRegistry.register_report("rating", RatingReport)
        """
        cls.reports[name] = report_class

    @classmethod
    def get_reports(cls):
        """
        Возвращает словарь всех зарегистрированных отчетов.
        :return: dict[str, type]: Словарь, где ключи - названия отчетов,
                                  значения - классы отчетов
        Например, {'rating': <class 'RatingReport'>, 'price': <class 'PriceReport'>}
        """
        return cls.reports
