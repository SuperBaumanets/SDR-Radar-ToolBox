from src.core.settings.locator import locators, LocatorSettings

from src.core.updater.generic_updater import Generic_Updater

from src.estimation.characteristics.resolution_calculator import ResolutionCalculator

class LocatorActionHandler:
    @classmethod
    def set_main_action(cls, updater:Generic_Updater):
        cls.headline_updater = updater.updater_headline
        cls.main_updater = updater.updater_settings
        cls.table_updater = updater.updater_table
        cls.table_widget = updater.updater_table.table

    @classmethod
    def add_locator(cls):
        """Добавляет новый локатор с привязкой к файлу"""
        try:
            # Создаем новый локатор и Добавляем в менеджер локаторов
            locators.add_locator(LocatorSettings())

            cls.table_widget.add_locator_column(locators.current_locator)
            ResolutionCalculator().calculate_resolutions()
            
            # Обновляем GUI
            cls.headline_updater.update_current_locator_list()
            cls.headline_updater.update_name_locator()
            cls.headline_updater.update_locator_list()

            cls.main_updater.update_settings_fields()

            cls.table_updater.update_characteristics()
            
        except Exception as e:
            print(f"Критическая ошибка: {str(e)}")

    @classmethod
    def delete_locator(cls):
        """Удаляет текущий активный локатор"""
        try:
            locators.remove_current_locator()

            cls.table_widget.remove_locator_column(locators.current_locator)

            cls.headline_updater.update_current_locator_list()
            cls.headline_updater.update_name_locator()
            cls.headline_updater.update_locator_list()

            cls.main_updater.update_settings_fields()
        

        except Exception as e:
            print(f"Критическая ошибка при удалении: {str(e)}")

    @classmethod
    def duplicate_locator():
        print("Функция: Дублировать локатор")