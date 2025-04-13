from pathlib import Path
from PySide6.QtWidgets import QDialog, QFileDialog, QApplication

from src.utils.toml_manager import TomlManager

from src.core.settings.locator import locators, LocatorSettings
from src.core.settings.session import file
from src.core.settings.target import target
from src.core.settings.locator_characteristics import locator_characteristics

from src.gui.styles.settings_management import main_settings
from src.gui.area.Dialog.open_session import CustomSessionDialog
from src.core.updater.generic_updater import Generic_Updater

from src.estimation.characteristics.resolution_calculator import ResolutionCalculator

class FileActionHandler:
    @classmethod
    def set_main_action(cls, updater:Generic_Updater):
        cls.headline_updater = updater.updater_headline
        cls.main_updater = updater.updater_settings
        cls.range_updater = updater.updater_range
        cls.table_updater = updater.updater_table
        cls.table_widget = updater.updater_table.table
    
    @classmethod
    def new_session(cls, menu: None):

        if menu is None:
            if len(locators.locators) > 1:
                dialog = CustomSessionDialog()
                dialog.setStyleSheet("""
                    QDialog { 
                        background-color: #D8D8D8;
                        border: 1px solid #000000;
                    }
                """ + main_settings)
                # Обработчики действий
                def save_and_continue():
                    cls.save_session(None)
                    locators.remove_all_except_first()
                    cls.table_widget.clear_locator_columns()
                    _create_new_session()
                def continue_without_saving():
                    locators.remove_all_except_first()
                    cls.table_widget.clear_locator_columns()
                    _create_new_session()

                def _create_new_session():
                    try:
                        QApplication.processEvents()
                        cls.headline_updater.update_name_locator()
                        cls.headline_updater.update_locator_list()

                        cls.main_updater.update_settings_fields()

                        cls.range_updater.update_range_target()

                        cls.table_widget.add_locator_column(locators.current_locator)

                        cls.table_updater.update_threshold_objective()

                        ResolutionCalculator().calculate_resolutions()
                        cls.table_updater.update_characteristics()

                    except Exception as e:
                        print(f"Ошибка инициализации: {str(e)}")
                # Подключение сигналов
                dialog.save_and_continue.connect(save_and_continue)
                dialog.continue_without_saving.connect(continue_without_saving)
                result = dialog.exec_()
                if result == QDialog.Rejected:
                    print("Создание новой сессии отменено")
                    return
            else:
                try:
                    QApplication.processEvents()
                    cls.headline_updater.update_name_locator()
                    cls.headline_updater.update_locator_list()

                    cls.main_updater.update_settings_fields()

                    cls.range_updater.update_range_target()

                    cls.table_widget.add_locator_column(locators.current_locator)

                    cls.table_updater.update_threshold_objective()

                    ResolutionCalculator().calculate_resolutions()
                    cls.table_updater.update_characteristics()

                except Exception as e:
                        print(f"Ошибка инициализации: {str(e)}")

    @classmethod
    def open_session(cls, menu):
        pass
        if menu == 0:
            file_path, _ = QFileDialog.getOpenFileName(
                None, "Открыть файл локатора", "", "TOML Files (*.toml)"
            )
            if file_path:
                try:
                    locators.remove_all_locators()

                    toml = TomlManager(file_path)
                    cls.load_from_toml(toml, locators, target, locator_characteristics)

                    cls.headline_updater.update_name_locator()
                    cls.headline_updater.update_locator_list()

                    cls.main_updater.update_settings_fields()

                    cls.range_updater.update_range_target()

                    cls.table_updater.update_threshold_objective()
                    ResolutionCalculator().calculate_resolutions()
                    cls.table_updater.update_characteristics()

                except Exception as e:
                    print(f"Ошибка: {str(e)}")

    @classmethod
    def save_session(cls, menu):
        if menu is None:
            if len(locators.locators) < 1:
                return
            
            error_messages = []

            file_path = file.file_location
            toml_manager = TomlManager(file_path)
            toml_manager.delete_all_tables()

            try:
                for locator in locators.locators:
                    locator_data = locator.model_dump()
                    table_name = locator.locator
                    toml_manager.write_all_fields(table_name, locator_data)

                distance_data = target.model_dump()
                toml_manager.write_all_fields("distance", distance_data)

                characteristics_data = locator_characteristics.model_dump()
                toml_manager.write_all_fields("characteristics", characteristics_data)

            except Exception as e:
                error_messages.append(f"{locator.locator}: {str(e)}")

            if error_messages:
                print("Ошибки при сохранении:")
                for error in error_messages:
                    print(f"  • {error}")

        elif menu == 0:
            file_path, _ = QFileDialog.getSaveFileName(
                None,
                "Сохранить как...",
                "",
                "TOML Files (*.toml)",
                options=QFileDialog.DontUseNativeDialog
            )
            if not file_path:
                return

            toml_manager = TomlManager(file_path)

            try:
                for locator in locators.locators:
                    locator_data = locator.model_dump()
                    table_name = locator.locator
                    toml_manager.write_all_fields(table_name, locator_data)

                distance_data = target.model_dump()
                toml_manager.write_all_fields("distance", distance_data)

                characteristics_data = locator_characteristics.model_dump()
                toml_manager.write_all_fields("characteristics", characteristics_data)

            except Exception as e:
                error_messages.append(f"{locator.locator}: {str(e)}")

            if error_messages:
                print("Ошибки при сохранении:")
                for error in error_messages:
                    print(f"  • {error}")

    @classmethod
    def load_from_toml(cls, toml_manager: TomlManager, locator_manager, target_settings, characteristics_settings):
        all_tables = toml_manager.get_table_names()

        locator_tables = [table for table in all_tables if table != "distance" if table != "characteristics"]
        distance_table = "distance" if "distance" in all_tables else None
        characteristics_table = "characteristics" if "characteristics" in all_tables else None

        for table_name in locator_tables:
            try:
                table_data = toml_manager.read_all_fields(table_name)

                if "locator" not in table_data:
                    raise ValueError(f"Отсутствует обязательное поле 'locator' в таблице {table_name}")

                if table_data["locator"] != table_name:
                    raise ValueError(f"Имя таблицы ({table_name}) не совпадает с именем локатора ({table_data['locator']})")

                locator = LocatorSettings(**table_data)

                locator_manager.add_locator(locator)

                cls.table_widget.add_locator_column(locator.locator)

            except Exception as e:
                print(f"Ошибка загрузки локатора из таблицы {table_name}: {str(e)}")
                continue

        if distance_table:
            try:
                distance_data = toml_manager.read_all_fields(distance_table)
                if distance_data:
                    target_settings.update_settings(distance_data)
            except Exception as e:
                print(f"Ошибка загрузки настроек расстояния: {str(e)}")

        if characteristics_table:
            try:
                characteristics_data = toml_manager.read_all_fields(characteristics_table)
                if characteristics_data:
                    characteristics_settings.update_settings(characteristics_data)
            except Exception as e:
                print(f"Ошибка загрузки настроек расстояния: {str(e)}")