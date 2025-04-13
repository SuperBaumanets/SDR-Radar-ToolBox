from PySide6.QtCore import QObject, Signal
from src.core.settings.locator import locators
from src.core.settings.session import file
from src.core.updater.generic_updater import Generic_Updater

class HeadlineActionHandler(QObject):
    locator_updated = Signal()

    def __init__(self):
        super().__init__()
        self.headline_widget = None
        self.headline_updater = None
        self.main_widget = None
        self.main_updater = None

    def set_main_widget(self, updater:Generic_Updater):
        self.headline_widget = updater.updater_headline.headline
        self.headline_updater = updater.updater_headline
        self.main_widget = updater.updater_settings.settings
        self.main_updater = updater.updater_settings
        self._connect_signals()

    def _connect_signals(self):
        self.headline_widget.mode_locator.currentTextChanged.connect(self.on_locator_selected)
        self.headline_widget.name_locator.textChanged.connect(self.update_locator_name)

    def on_locator_selected(self, name: str):
        try:
            locators.current_locator = name
            self.current_index = [loc.locator for loc in locators.locators].index(name)

            self.headline_updater.update_current_locator_list()
            self.headline_updater.update_name_locator()
            self.main_updater.update_settings_fields()

            self.locator_updated.emit()
        except ValueError:
            print(f"Локатор '{name}' не найден")

    def update_locator_name(self):
        if not locators.current_locator:
            return

        new_name = self.headline_widget.name_locator.text().strip()
        old_name = locators.current_locator

        try:
            locators.rename_locator(old_name, new_name)

            self.headline_updater.update_locator_list()

            self.locator_updated.emit()

        except Exception as e:
            print(f"Ошибка обновления имени: {str(e)}")
            self.headline_widget.name_locator.blockSignals(True)
            self.headline_widget.name_locator.setText(old_name)
            self.headline_widget.name_locator.blockSignals(False)