from PySide6.QtCore import QObject
from src.core.settings.target import target
from src.estimation.convert_measurement import *
from src.core.updater.generic_updater import Generic_Updater

class MetricActionHandler(QObject):
    def __init__(self):
        super().__init__()
        self.metric_widget = None
        self.metric_updater = None
        self._range_unit = "м"
   
    def set_main_widget(self, updater:Generic_Updater):
        self.metric_widget = updater.updater_range.metric
        self.metric_updater = updater.updater_range

    def update_maximum_range(self):
            try:
                if hasattr(self, "_updating") and self._updating:
                    return
                self._updating = True

                raw_value = self.metric_widget.data_range.text().strip()
                if not raw_value:
                    raise ValueError("Введите значение дальности до цели")
                
                current_unit = self.metric_widget.measurement_range.currentText()
                previous_unit = getattr(self, "_previous_unit", current_unit)

                if current_unit != previous_unit:
                    try:
                        previous_value = float(raw_value)
                        converted_value = convert_units(
                            previous_value, 
                            previous_unit, 
                            current_unit, 
                            "length"
                        )

                        self.metric_widget.data_range.blockSignals(True)
                        self.metric_widget.data_range.setText(f"{converted_value:.12g}".rstrip('.'))
                        self.metric_widget.data_range.blockSignals(False)

                        raw_value = str(converted_value)
                    except Exception as e:
                        raise ValueError(f"Ошибка конвертации: {str(e)}")

                value = float(raw_value)
                max_value = 1e23
                if value <= 0 or value > max_value:
                    raise ValueError(f"Значение должно быть между 0 и {max_value:.0e} {current_unit}")
                
                converted_range = convert_units(value, current_unit, "м", "length")

                self.metric_widget.data_range.blockSignals(True)
                try:
                    target.range = converted_range
                    self.metric_widget.data_range.setText(f"{value:.12g}".rstrip('.'))
                finally:
                    self.metric_widget.data_range.blockSignals(False)

                self._previous_unit = current_unit

                self.metric_widget.data_range.setStyleSheet("")
                self.metric_widget.data_range.setToolTip("")

            except ValueError as e:
                error_msg = f"Ошибка: {str(e)}"
                self.metric_widget.data_range.setStyleSheet("""
                    border: 2px solid red;
                    border-radius: 2px;
                    background-color: #ffcccc;
                """)
                self.metric_widget.data_range.setToolTip(error_msg)
            except Exception as e:
                print(f"Критическая ошибка: {str(e)}")
                import traceback
                traceback.print_exc()
            finally:
                self._updating = False
