from PySide6.QtCore import QObject
from src.core.settings.locator import locators

class Headline_Updater(QObject):
    def __init__(self, headline_widget):
        super().__init__()
        self.headline = headline_widget

    def update_name_locator(self):
        current_locator = locators.get_locator(locators.current_locator)
        self._update_edit(self.headline.name_locator, f"{current_locator.locator}")

    def update_locator_list(self):
        self.headline.mode_locator.blockSignals(True)

        self.headline.mode_locator.clear()
        locators_dict = {loc.locator: loc for loc in locators.locators}
        self.headline.mode_locator.addItems(locators_dict.keys())

        self.headline.mode_locator.blockSignals(False)

    def update_current_locator_list(self):
        self.headline.mode_locator.blockSignals(True)

        current_locator = locators.get_locator(locators.current_locator)
        print(current_locator.locator)
        self._update_combo( self.headline.mode_locator, f"{current_locator.locator}")
    
        self.headline.mode_locator.blockSignals(False)

    def _update_edit(self, field, value):
        field.blockSignals(True)
        field.setText(value)
        field.blockSignals(False) 

    def _update_combo(self, field, value):
        field.blockSignals(True)
        field.setCurrentText(value)
        field.blockSignals(False)