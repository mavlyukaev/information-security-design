#pip install pyyaml - установка библиотеки

import yaml
import os

class MyEntity_rep_yaml:
    def __init__(self, filename):
        self.filename = filename
        self.entities = self.load_entities()

    def load_entities(self):
        """Загрузить данные из YAML-файла."""
        if not os.path.exists(self.filename):
            return []
        with open(self.filename, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)  # Используем safe_load для безопасности
            return [Driver(**item) for item in data]

    def save_entities(self):
        """Сохранить данные в YAML-файл."""
        with open(self.filename, 'w', encoding='utf-8') as file:
            yaml.dump([entity.__dict__ for entity in self.entities], file, allow_unicode=True)

    def get_by_id(self, driver_id):
        """Получить объект по ID."""
        for entity in self.entities:
            if entity.get_driver_id() == driver_id:
                return entity
        return None

    def get_k_n_short_list(self, k, n):
        """Получить список k по счету n объектов класса short."""
        start_index = (n - 1) * k
        end_index = start_index + k
        return [DriverSummary(entity, entity.INN, entity.OGRN) for entity in self.entities[start_index:end_index]]

    def sort_by_field(self, field):
        """Сортировать элементы по выбранному полю."""
        if hasattr(Driver, field):
            self.entities.sort(key=lambda x: getattr(x, field))
        else:
            raise ValueError(f"Поле {field} не существует в классе Driver.")

    def add_entity(self, driver):
        """Добавить объект в список с новым ID."""
        new_id = max(entity.get_driver_id() for entity in self.entities) + 1 if self.entities else 1
        driver.set_driver_id(new_id)
        self.entities.append(driver)
        self.save_entities()

    def replace_entity_by_id(self, driver_id, updated_driver):
        """Заменить элемент списка по ID."""
        for index, entity in enumerate(self.entities):
            if entity.get_driver_id() == driver_id:
                updated_driver.set_driver_id(driver_id)
                self.entities[index] = updated_driver
                self.save_entities()
                return
        raise ValueError(f"Объект с ID {driver_id} не найден.")

    def delete_entity_by_id(self, driver_id):
        """Удалить элемент списка по ID."""
        self.entities = [entity for entity in self.entities if entity.get_driver_id() != driver_id]
        self.save_entities()

    def get_count(self):
        """Получить количество элементов."""
        return len(self.entities)

# Пример использования
if __name__ == "__main__":
    repo = MyEntity_rep_yaml("drivers.yaml")

    # Пример добавления нового водителя
    new_driver = Driver(LastName="Петров", FirstName="Петр", Patronymic="Петрович", Experience=3)
    repo.add_entity(new_driver)

    # Получение водителя по ID
    driver = repo.get_by_id(1)
    print(driver)

    # Получение 20 водителей, начиная со второго
    short_list = repo.get_k_n_short_list(20, 2)
    print(short_list)

    # Сортировка по опыту
    repo.sort_by_field('Experience')

    # Количество водителей
    count = repo.get_count()
    print(f"Количество водителей: {count}")
