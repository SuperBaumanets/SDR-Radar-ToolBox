from PySide6.QtCore import QObject
from src.core.settings.locator_characteristics import locator_characteristics
from src.core.settings.locator import locators
from src.gui.area.Characteristics.general_Table import TableCharacteristics

class Table_Updater(QObject):
    def __init__(self, table_widget:TableCharacteristics):
        super().__init__()
        self.table = table_widget

    def update_threshold_objective(self):
        self._update_edit(self.table.data_threshold_range_resolution, f"{locator_characteristics.threshold_range_resolution}")
        self._update_edit(self.table.data_objective_range_resolution, f"{locator_characteristics.objective_range_resolution}")
        self._update_combo(self.table.measurement_range_resolution, "м")

        self._update_edit(self.table.data_threshold_speed_resolution, f"{locator_characteristics.threshold_speed_resolution}")
        self._update_edit(self.table.data_objective_speed_resolution, f"{locator_characteristics.objective_speed_resolution}")
        self._update_combo(self.table.measurement_speed_resolution, "м/c")

    def update_characteristics(self):
        for locator in locators.locators:
            self.table.set_locator_value(locator.locator, 0, str(locator_characteristics.calc_range_resolution.get(locator.locator)))
            self.table.set_locator_value(locator.locator, 1, str(locator_characteristics.calc_speed_resolution.get(locator.locator)))

    def _update_edit(self, field, value):
        field.blockSignals(True)
        field.setText(value)
        field.blockSignals(False) 

    def _update_combo(self, field, value):
        field.blockSignals(True)
        field.setCurrentText(value)
        field.blockSignals(False)