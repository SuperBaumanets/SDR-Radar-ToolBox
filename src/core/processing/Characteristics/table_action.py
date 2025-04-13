from PySide6.QtCore import QObject
from src.estimation.convert_measurement import *
from src.core.settings.locator_characteristics import locator_characteristics
from src.core.settings.locator import locators
from src.core.updater.generic_updater import Generic_Updater

class TableActionHandler(QObject):
    def __init__(self):
        super().__init__()
        self.table_widget = None
        self._prev_range_unit = "м"
        self._prev_speed_unit = "м/c"
        
    def set_main_widget(self, updater:Generic_Updater):
       self.table_widget = updater.updater_table.table
    
    def update_range_resolution(self):
        try:
            if hasattr(self, "_updating") and self._updating:
                return
            self._updating = True

            current_unit =self.table_widget.measurement_range_resolution.currentText()
            previous_unit = getattr(self, "_prev_range_unit", current_unit)

            raw_value_threshold =self.table_widget.data_threshold_range_resolution.text().strip()
            raw_value_objective =self.table_widget.data_objective_range_resolution.text().strip()

            # Обработка пустых значений
            if not raw_value_threshold:
                raw_value_threshold = "0"
            if not raw_value_objective:
                raw_value_objective = "0"

            try:
                value_threshold = float(raw_value_threshold)
                value_objective = float(raw_value_objective)
            except ValueError:
                raise ValueError("Некорректные числовые значения в полях")

            if current_unit != previous_unit:
                try:
                    previous_value_threshold = float(raw_value_threshold)
                    converted_value_threshold = convert_units(
                        previous_value_threshold, 
                        previous_unit, 
                        current_unit, 
                        "length"
                    )

                    previous_value_objective = float(raw_value_objective)
                    converted_value_objective = convert_units(
                        previous_value_objective, 
                        previous_unit, 
                        current_unit, 
                        "length"
                    )

                    self.table_widget.data_threshold_range_resolution.blockSignals(True)
                    self.table_widget.data_threshold_range_resolution.setText(f"{converted_value_threshold:.12g}".rstrip('.'))
                    self.table_widget.data_threshold_range_resolution.blockSignals(False)

                    self.table_widget.data_objective_range_resolution.blockSignals(True)
                    self.table_widget.data_objective_range_resolution.setText(f"{converted_value_objective:.12g}".rstrip('.'))
                    self.table_widget.data_objective_range_resolution.blockSignals(False)

                    raw_value_threshold = str(converted_value_threshold)
                    raw_value_objective = str(converted_value_objective)
                except Exception as e:
                    raise ValueError(f"Ошибка конвертации: {str(e)}")
                
            for locator in locators.locators:
                calc_value = locator_characteristics.calc_range_resolution.get(locator.locator)
                if current_unit != previous_unit:
                        converted_value_calc = convert_units(
                        calc_value, 
                        previous_unit, 
                        current_unit, 
                        "length"
                        )

                        self.table_widget.set_locator_value(locator.locator, 0, str(converted_value_calc))

            value_threshold = float(raw_value_threshold)
            value_objective = float(raw_value_objective)

            self.table_widget.data_objective_range_resolution.blockSignals(True)
            self.table_widget.data_threshold_range_resolution.blockSignals(True)
            try:
               self.table_widget.data_objective_range_resolution.setText(f"{value_objective:.12g}".rstrip('.'))
               self.table_widget.data_threshold_range_resolution.setText(f"{value_threshold:.12g}".rstrip('.'))
            finally:
               self.table_widget.data_objective_range_resolution.blockSignals(False)
               self.table_widget.data_threshold_range_resolution.blockSignals(True)
            self._prev_range_unit = current_unit

            # Основная валидация
            if raw_value_threshold:
                value = float(raw_value_threshold)
                
                base_value_threshold_range = convert_units(value, current_unit, "м", "length")
                locator_characteristics.threshold_range_resolution = base_value_threshold_range
            
            # Основная валидация
            if raw_value_objective:
                value = float(raw_value_objective)

                base_value_objective_range = convert_units(value, current_unit, "м", "length")
                locator_characteristics.objective_range_resolution = base_value_objective_range
               
        except ValueError as e:
            error_msg = f"Ошибка: {str(e)}"
            self.table_widget.data_threshold_range_resolution.setStyleSheet("""
                border: 2px solid red;
                border-radius: 0px;
                background-color: #ffcccc;
            """)
            self.table_widget.data_threshold_range_resolution.setToolTip(error_msg)
            self.table_widget.data_objective_range_resolution.setStyleSheet("""
                border: 2px solid red;
                border-radius: 0px;
                background-color: #ffcccc;
            """)
            self.table_widget.data_objective_range_resolution.setToolTip(error_msg)
        except Exception as e:
            print(f"Критическая ошибка: {str(e)}")
            import traceback
            traceback.print_exc()
        finally:
            self._updating = False

    def update_speed_resolution(self):
        try:
            if hasattr(self, "_updating") and self._updating:
                return
            self._updating = True

            current_unit =self.table_widget.measurement_speed_resolution.currentText()
            previous_unit = getattr(self, "_prev_speed_unit", current_unit)

            raw_value_threshold =self.table_widget.data_threshold_speed_resolution.text().strip()
            raw_value_objective =self.table_widget.data_objective_speed_resolution.text().strip()

            # Обработка пустых значений
            if not raw_value_threshold:
                raw_value_threshold = "0"
            if not raw_value_objective:
                raw_value_objective = "0"

            try:
                value_threshold = float(raw_value_threshold)
                value_objective = float(raw_value_objective)
            except ValueError:
                raise ValueError("Некорректные числовые значения в полях")

            if current_unit != previous_unit:
                try:
                    previous_value_threshold = float(raw_value_threshold)
                    converted_value_threshold = convert_units(
                        previous_value_threshold, 
                        previous_unit, 
                        current_unit, 
                        "speed"
                    )

                    previous_value_objective = float(raw_value_objective)
                    converted_value_objective = convert_units(
                        previous_value_objective, 
                        previous_unit, 
                        current_unit, 
                        "speed"
                    )

                    self.table_widget.data_threshold_speed_resolution.blockSignals(True)
                    self.table_widget.data_threshold_speed_resolution.setText(f"{converted_value_threshold:.12g}".rstrip('.'))
                    self.table_widget.data_threshold_speed_resolution.blockSignals(False)

                    self.table_widget.data_objective_speed_resolution.blockSignals(True)
                    self.table_widget.data_objective_speed_resolution.setText(f"{converted_value_objective:.12g}".rstrip('.'))
                    self.table_widget.data_objective_speed_resolution.blockSignals(False)

                    raw_value_threshold = str(converted_value_threshold)
                    raw_value_objective = str(converted_value_objective)
                except Exception as e:
                    raise ValueError(f"Ошибка конвертации: {str(e)}")
            
            for locator in locators.locators:
                calc_value = locator_characteristics.calc_speed_resolution.get(locator.locator)
                if current_unit != previous_unit:
                        converted_value_calc = convert_units(
                        calc_value, 
                        previous_unit, 
                        current_unit, 
                        "speed"
                        )

                        self.table_widget.set_locator_value(locator.locator, 1, str(converted_value_calc))


            value_threshold = float(raw_value_threshold)
            value_objective = float(raw_value_objective)

            self.table_widget.data_objective_speed_resolution.blockSignals(True)
            self.table_widget.data_threshold_speed_resolution.blockSignals(True)
            try:
               self.table_widget.data_objective_speed_resolution.setText(f"{value_objective:.12g}".rstrip('.'))
               self.table_widget.data_threshold_speed_resolution.setText(f"{value_threshold:.12g}".rstrip('.'))
            finally:
               self.table_widget.data_objective_speed_resolution.blockSignals(False)
               self.table_widget.data_threshold_speed_resolution.blockSignals(True)
            self._prev_speed_unit = current_unit

            # Основная валидация
            if raw_value_threshold:
                value = float(raw_value_threshold)
                
                base_value_threshold_speed = convert_units(value, current_unit, "м/c", "speed")
                locator_characteristics.threshold_speed_resolution = base_value_threshold_speed
            
            # Основная валидация
            if raw_value_objective:
                value = float(raw_value_objective)

                base_value_objective_range = convert_units(value, current_unit, "м/c", "speed")
                locator_characteristics.objective_speed_resolution = base_value_objective_range
        
        except ValueError as e:
            error_msg = f"Ошибка: {str(e)}"
            self.table_widget.data_threshold_speed_resolution.setStyleSheet("""
                border: 2px solid red;
                border-radius: 0px;
                background-color: #ffcccc;
            """)
            self.table_widget.data_threshold_speed_resolution.setToolTip(error_msg)
            self.table_widget.data_objective_speed_resolution.setStyleSheet("""
                border: 2px solid red;
                border-radius: 0px;
                background-color: #ffcccc;
            """)
            self.table_widget.data_objective_speed_resolution.setToolTip(error_msg)
        except Exception as e:
            print(f"Критическая ошибка: {str(e)}")
            import traceback
            traceback.print_exc()
        finally:
            self._updating = False
