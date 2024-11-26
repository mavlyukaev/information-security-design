import os
import json
import yaml

class MyEntityRepository:
    def __init__(self, filename):
        self.filename = filename
        self.entities = self.load_entities()

    def load_entities(self):
        """Загрузить данные из файла. Реализовать в дочерних классах."""
        raise NotImplementedError("Метод load_entities должен быть реализован в дочернем классе.")

    def save_entities(self):
        """Сохранить данные в файл. Реализовать в дочерних классах."""
        raise NotImplementedError("Метод save_entities должен быть реализован в дочернем классе.")

    def get_by_id(self, driver_id):
        """Получить объект по ID."""
        for entity in self.entities:
            if entity.get_driver_id() == driver_id:
                return entity
        return None

    def get_k_n_short_list(self, k, n):
        """Получить список k по счету n объектов класса short."""
        start_index = (k - 1) * n
        end_index = start_index + n
        return [DriverSummary(entity) for entity in self.entities[start_index:end_index]]

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

class MyEntity_rep_json(MyEntityRepository):
    def load_entities(self):
        """Загрузить данные из JSON-файла."""
        if not os.path.exists(self.filename):
            return []
        with open(self.filename, 'r', encoding='utf-8') as file:
            return [Driver(**data) for data in json.load(file)]

    def save_entities(self):
        """Сохранить данные в JSON-файл."""
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump([entity.__dict__ for entity in self.entities], file, ensure_ascii=False, indent=4)

class MyEntity_rep_yaml(MyEntityRepository):
    def load_entities(self):
        """Загрузить данные из YAML-файла."""
        if not os.path.exists(self.filename):
            return []
        with open(self.filename, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
            return [Driver(**item) for item in data]

    def save_entities(self):
        """Сохранить данные в YAML-файл."""
        with open(self.filename, 'w', encoding='utf-8') as file:
            yaml.dump([entity.__dict__ for entity in self.entities], file, allow_unicode=True)
