class DriverSummary:
    def __init__(self, driver: Driver, inn: str, ogrn: str):
        self.last_name = driver.get_last_name()
        self.initials = f"{driver.get_first_name()[0]}. {driver.get_patronymic()[0]}."  # Инициалы
        self.inn = inn  # Идентификационный номер налогоплательщика
        self.ogrn = ogrn  # Основной государственный регистрационный номер

    def __str__(self):
        return (f"Driver Summary: {self.last_name} {self.initials}, INN: {self.inn}, OGRN: {self.ogrn}")

    def short_description(self):
        return f"{self.last_name} {self.initials}"

# Пример использования
driver = Driver(1, "Ivanov", "Ivan", "Ivanovich", 5)
summary = DriverSummary(driver, inn="123456789012", ogrn="1234567891234")

# Вывод краткой версии
print(summary)  # Полная информация о кратком представлении
print(summary.short_description())  # Краткое описание