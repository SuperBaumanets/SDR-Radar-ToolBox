from PySide6.QtCore import QObject
from src.core.settings.locator import locators

class Settings_Updater(QObject):
    def __init__(self, main_widget):
        super().__init__()
        self.settings = main_widget

    def update_settings_fields(self):
        current_locator = locators.get_locator(locators.current_locator)

        self._update_edit(self.settings.data_bandwidth, f"{current_locator.bandwidth:.12g}")

        self._update_combo(self.settings.mode_freq_wavelength, "Частота")
        self._update_edit(self.settings.data_freq_period, f"{current_locator.frequency:.12g}")
        self._update_combo(self.settings.measurement_freq, "Гц")

        self._update_combo(self.settings.mode_power, "Пиковая мощность")
        self._update_edit(self.settings.data_power, f"{current_locator.transmitter_pulse_power:.12g}")
        self._update_combo(self.settings.measurement_power, "Вт")

        self._update_combo(self.settings.mode_freq_period, "PRF")
        self._update_edit(self.settings.data_PRI_PRF, f"{current_locator.pulse_repetition_frequency:.12g}")
        self._update_combo(self.settings.measurement_freq_repeat, "Гц")

        self._update_combo(self.settings.mode_pulse_duty, "Ширина импульса")
        self._update_edit(self.settings.data_pulse_duty, f"{current_locator.pulse_duration:.12g}")
        self._update_combo(self.settings.measurement_pulse, "c")

    def _update_edit(self, field, value):
        field.blockSignals(True)
        field.setText(value.rstrip('0').rstrip('.') if '.' in value else value)
        field.blockSignals(False) 

    def _update_combo(self, field, value):
        field.blockSignals(True)
        field.setCurrentText(value)
        field.blockSignals(False)
