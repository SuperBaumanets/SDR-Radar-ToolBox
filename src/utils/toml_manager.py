import tomli
import tomli_w
import os
from typing import Any, Optional, Dict, List

class TomlManager:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.data = self._load_file()

    def _load_file(self) -> Dict:
        # Загружает данные из TOML-файла"""
        if not os.path.exists(self.file_path):
            return {}
        
        with open(self.file_path, "rb") as f:
            return tomli.load(f)

    def _save_file(self):
        # Сохраняет данные в TOML-файл"""
        with open(self.file_path, "wb") as f:
            tomli_w.dump(self.data, f)

    def read_all_fields(self, table_name: str) -> Optional[Dict]:
        # Читает все поля указанной таблицы
        return self.data.get(table_name)

    def read_field(self, table_name: str, field: str) -> Optional[Any]:
        # Читает конкретное поле из таблицы
        table = self.data.get(table_name)
        return table.get(field) if table else None

    def write_all_fields(self, table_name: str, fields: Dict):
        # Записывает/обновляет поля в таблице
        if table_name not in self.data:
            self.data[table_name] = {}
        self.data[table_name].update(fields)
        self._save_file()

    def add_table(self, table_name: str, fields: Dict):
        # Добавляет новую таблицу
        if table_name in self.data:
            raise ValueError(f"Table '{table_name}' already exists")
        self.data[table_name] = fields
        self._save_file()

    def delete_table(self, table_name: str):
        # Удаляет таблицу
        if table_name in self.data:
            del self.data[table_name]
            self._save_file()

    def delete_all_tables(self):
        self.data.clear()
        self._save_file()

    def get_table_names(self) -> List[str]:
        # Возвращает список названий таблиц
        return list(self.data.keys())