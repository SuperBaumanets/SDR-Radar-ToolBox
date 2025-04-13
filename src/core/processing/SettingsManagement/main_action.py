from PySide6.QtCore import QObject
from src.core.settings.locator import locators
from src.estimation.convert_measurement import *
from src.core.updater.generic_updater import Generic_Updater
from src.estimation.characteristics.resolution_calculator import ResolutionCalculator

class MainActionHandler(QObject):
    def __init__(self):
        super().__init__()
        self.main_widget = None
        self.table_updater = None
        self._prev_mode = "Частота"
        self._prev_wavelength_unit = "м"
        self._prev_freq_unit = "Гц"
        self._previous_unit = "Гц"
        self._prev_pulse_mode = "Ширина импульса"
        self._prev_pulse_unit = "с"
        self._prev_power_mode = "Пиковая мощность"
        self._prev_power_unit = "Вт"
        self._prev_priprf_mode = "PRF"
        self._prev_priprf_unit = "Гц"
        
    def set_main_widget(self, updater:Generic_Updater):
        self.main_widget = updater.updater_settings.settings
        self.table_updater = updater.updater_table
        self.charts_updater = updater.updater_charts
        
    def update_freq_wavelength(self):
        try:
            if getattr(self, "_updating", False):
                return
            self._updating = True

            current_locator = locators.get_locator(locators.current_locator)
            current_mode = self.main_widget.mode_freq_wavelength.currentText()
            c = 3e8

            # Проверка существования текущего локатора
            if not current_locator:
                raise ValueError("Не выбран текущий локатор")

            prev_mode = getattr(self, "_prev_mode", current_mode)
            prev_wavelength_unit = getattr(self, "_prev_wavelength_unit", "м")
            prev_freq_unit = getattr(self, "_prev_freq_unit", "Гц")

            if current_mode == "Длина волны":
                current_unit = self.main_widget.measurement_wavelength.currentText()
                param_type = "length"
                prev_unit = prev_wavelength_unit
            else:
                current_unit = self.main_widget.measurement_freq.currentText()
                param_type = "frequency"
                prev_unit = prev_freq_unit

            raw_value = self.main_widget.data_freq_period.text().strip()

            # Блок конвертации единиц
            if raw_value and current_mode == prev_mode and current_unit != prev_unit:
                value = float(raw_value)
                if value == 0:
                    raise ValueError("Нулевое значение недопустимо для конвертации")

                converted = convert_units(value, prev_unit, current_unit, param_type)
                self._update_data_field(self.main_widget.data_freq_period, f"{converted:.12g}")
                raw_value = str(converted)

            # Блок переключения режимов
            if current_mode != prev_mode and raw_value:
                value = float(raw_value)
                if value == 0:
                    raise ValueError("Нулевое значение недопустимо для переключения режимов")

                if current_mode == "Длина волны":
                    # Конвертация частоты -> длина волны
                    freq_hz = convert_units(value, prev_freq_unit, "Гц", "frequency")
                    if freq_hz == 0:
                        raise ValueError("Частота не может быть нулевой")

                    wavelength_m = c / freq_hz
                    converted = convert_units(wavelength_m, "м", current_unit, "length")
                else:
                    # Конвертация длины волны -> частота
                    wavelength_m = convert_units(value, prev_wavelength_unit, "м", "length")
                    if wavelength_m == 0:
                        raise ValueError("Длина волны не может быть нулевой")

                    freq_hz = c / wavelength_m
                    converted = convert_units(freq_hz, "Гц", current_unit, "frequency")

                self._update_data_field(self.main_widget.data_freq_period, f"{converted:.12g}")
                raw_value = str(converted)

            # Основная валидация
            if raw_value:
                value = float(raw_value)
                max_value = 1e23 if current_mode == "Частота" else 1e15

                if value <= 0:
                    raise ValueError("Значение должно быть больше нуля")

                if value > max_value:
                    raise ValueError(f"Значение не должно превышать {max_value:.0e} {current_unit}")

                # Обновление модели
                if current_mode == "Длина волны":
                    base_value = convert_units(value, current_unit, "м", "length")
                    current_locator.wavelength = base_value
                else:
                    base_value = convert_units(value, current_unit, "Гц", "frequency")
                    current_locator.frequency =  base_value

            # Сохранение состояния
            self._prev_mode = current_mode
            if current_mode == "Длина волны":
                self._prev_wavelength_unit = current_unit
            else:
                self._prev_freq_unit = current_unit

            self.main_widget.data_freq_period.setStyleSheet("")
            ResolutionCalculator().calculate_resolutions()
            self.table_updater.update_characteristics()
            self.charts_updater.update_charts()
            

        except ValueError as e:
            error_msg = str(e)
            self.main_widget.data_freq_period.setStyleSheet("border: 2px solid red; background-color: #ffcccc;")
            self.main_widget.data_freq_period.setToolTip(error_msg)
            print(f"Ошибка: {error_msg}")

        except ZeroDivisionError:
            error_msg = "Попытка деления на ноль"
            self.main_widget.data_freq_period.setStyleSheet("border: 2px solid red; background-color: #ffcccc;")
            self.main_widget.data_freq_period.setToolTip(error_msg)
            print(f"Критическая ошибка: {error_msg}")

        except Exception as e:
            error_msg = f"Непредвиденная ошибка: {str(e)}"
            self.main_widget.data_freq_period.setStyleSheet("border: 2px solid red; background-color: #ffcccc;")
            self.main_widget.data_freq_period.setToolTip(error_msg)
            print(error_msg)
        
        finally:
            self._updating = False

    def update_bandwidth(self):
        try:
            if hasattr(self, "_updating") and self._updating:
                return
            self._updating = True

            # Получаем текущий локатор через менеджер
            current_locator = locators.get_locator(locators.current_locator)

            current_unit = self.main_widget.measurement_bandwidth.currentText()
            previous_unit = getattr(self, "_previous_unit", current_unit)

            raw_value = self.main_widget.data_bandwidth.text().strip()
            if not raw_value:
                raise ValueError("Введите значение полосы пропускания")

            if current_unit != previous_unit:
                try:
                    previous_value = float(raw_value)
                    converted_value = convert_units(
                        previous_value, 
                        previous_unit, 
                        current_unit, 
                        "frequency"
                    )

                    self.main_widget.data_bandwidth.blockSignals(True)
                    self.main_widget.data_bandwidth.setText(f"{converted_value:.12g}".rstrip('.'))
                    self.main_widget.data_bandwidth.blockSignals(False)

                    raw_value = str(converted_value)
                except Exception as e:
                    raise ValueError(f"Ошибка конвертации: {str(e)}")

            value = float(raw_value)
            max_value = 1e23
            if value <= 0 or value > max_value:
                raise ValueError(f"Значение должно быть между 0 и {max_value:.0e} {current_unit}")

            converted_hz = convert_units(value, current_unit, "Гц", "frequency")
            if converted_hz > 1e30:
                raise ValueError("Превышено максимальное допустимое значение")

            self.main_widget.data_bandwidth.blockSignals(True)
            try:
                current_locator.bandwidth = converted_hz
                self.main_widget.data_bandwidth.setText(f"{value:.12g}".rstrip('.'))
            finally:
                self.main_widget.data_bandwidth.blockSignals(False)

            self._previous_unit = current_unit          

            self.main_widget.data_bandwidth.setStyleSheet("")
            self.main_widget.data_bandwidth.setToolTip("")
            ResolutionCalculator().calculate_resolutions()
            self.table_updater.update_characteristics()

            self.charts_updater.update_charts()
              
        except ValueError as e:
            error_msg = f"Ошибка: {str(e)}"
            self.main_widget.data_bandwidth.setStyleSheet("""
                border: 2px solid red;
                border-radius: 2px;
                background-color: #ffcccc;
            """)
            self.main_widget.data_bandwidth.setToolTip(error_msg)
        except Exception as e:
            print(f"Критическая ошибка: {str(e)}")
            import traceback
            traceback.print_exc()
        finally:
            self._updating = False

    def update_pulse_duty(self):
        try:
            if hasattr(self, "_updating") and self._updating:
                return
            self._updating = True

            # Получаем текущий локатор через менеджер
            current_locator = locators.get_locator(locators.current_locator)

            current_mode = self.main_widget.mode_pulse_duty.currentText()
            prev_mode = getattr(self, "_prev_pulse_mode", current_mode)
            prev_unit = getattr(self, "_prev_pulse_unit", "с")  # Значение по умолчанию

            pri = current_locator.pulse_repetition_period  # PRI в секундах

            raw_value = self.main_widget.data_pulse_duty.text().strip()

            # Конвертация единиц внутри одного режима
            if current_mode == "Ширина импульса" and current_mode == prev_mode:
                current_unit = self.main_widget.measurement_pulse.currentText()
                if current_unit != prev_unit and raw_value:
                    value = float(raw_value)
                    converted = convert_units(value, prev_unit, current_unit, "time")
                    self._update_data_field(self.main_widget.data_pulse_duty, f"{converted:.12g}")
                    raw_value = str(converted)

            # Конвертация между режимами
            if current_mode != prev_mode and raw_value:
                try:
                    value = float(raw_value)
                    if current_mode == "Скважность":
                        # Из ширины импульса в скважность (D = T/τ)
                        if prev_mode == "Ширина импульса":
                            tau = convert_units(value, prev_unit, "с", "time")
                            D = pri / tau if tau > 0 else 0
                        else:
                            D = value
                        self._update_data_field(self.main_widget.data_pulse_duty, f"{D:.6f}")
                        current_locator.duty_cycle = D
                    else:
                        # Из скважности в ширину импульса (τ = T/D)
                        current_unit = self.main_widget.measurement_pulse.currentText()
                        tau = pri / value if pri > 0 else 0
                        converted = convert_units(tau, "с", current_unit, "time")
                        self._update_data_field(self.main_widget.data_pulse_duty, f"{converted:.12g}")

                    raw_value = self.main_widget.data_pulse_duty.text()

                except ZeroDivisionError:
                    raise ValueError("PRI не может быть нулевым")

            # Валидация и сохранение
            if raw_value:
                value = float(raw_value)
                if current_mode == "Ширина импульса":
                    current_unit = self.main_widget.measurement_pulse.currentText()
                    max_val = 1e10
                    if value > max_val:
                        raise ValueError(f"Ширина импульса 0 < τ ≤ {max_val:.0e} {current_unit}")

                    tau = float(convert_units(value, current_unit, "с", "time"))
                    current_locator.pulse_duration = tau
                    print(current_locator.pulse_duration)
                    self._prev_pulse_unit = current_unit  # Сохраняем только для режима ширины
                else:
                    if value <= 1 or value > 1e6:
                        raise ValueError("Скважность должна быть 1 < D ≤ 1e6")

            # Сохраняем текущий режим
            self._prev_pulse_mode = current_mode          

            self.main_widget.data_pulse_duty.setStyleSheet("")
            self.main_widget.data_pulse_duty.setToolTip("")
            ResolutionCalculator().calculate_resolutions()
            self.table_updater.update_characteristics()
            
            self.charts_updater.update_charts()

            print(locators)

        except ValueError as e:
            error_msg = f"Ошибка: {str(e)}"
            self.main_widget.data_pulse_duty.setStyleSheet("""
                border: 2px solid red;
                border-radius: 2px;
                background-color: #ffcccc;
            """)
            self.main_widget.data_pulse_duty.setToolTip(error_msg)
        except Exception as e:
            print(f"Критическая ошибка: {str(e)}")
            import traceback
            traceback.print_exc()
        finally:
            self._updating = False

    def update_power(self):
        try:
            if hasattr(self, "_updating") and self._updating:
                return
            self._updating = True

            # Получаем текущий локатор через менеджер
            current_locator = locators.get_locator(locators.current_locator)

            current_mode = self.main_widget.mode_power.currentText()
            current_unit = self.main_widget.measurement_power.currentText()
            prev_mode = getattr(self, "_prev_power_mode", current_mode)
            prev_unit = getattr(self, "_prev_power_unit", current_unit)

            raw_value = self.main_widget.data_power.text().strip()
            duty_cycle = current_locator.duty_cycle

            # Конвертация единиц измерения
            if current_mode == prev_mode and raw_value:
                if current_unit != prev_unit:
                    value = float(raw_value)
                    converted = convert_power_units(value, prev_unit, current_unit)
                    self._update_data_field(self.main_widget.data_power, f"{converted:.12g}")
                    raw_value = str(converted)

            # Конвертация между режимами мощности
            if current_mode != prev_mode and raw_value and duty_cycle > 0:
                value = float(raw_value)

                if current_mode == "Пиковая мощность":
                    # Средняя -> Пиковая: P_peak = P_avg * D
                    converted = value * duty_cycle
                else:
                    # Пиковая -> Средняя: P_avg = P_peak / D
                    converted = value / duty_cycle

                converted = convert_power_units(converted, prev_unit, current_unit)
                self._update_data_field(self.main_widget.data_power, f"{converted:.12g}")
                raw_value = str(converted)

            # Валидация и сохранение
            if raw_value:
                value = float(raw_value)
                if value <= 0:
                    raise ValueError("Мощность должна быть положительной")

                # Конвертация в ватты
                base_value = convert_to_watts(value, current_unit)

                if current_mode == "Пиковая мощность":
                    current_locator.transmitter_pulse_power = base_value
                else:
                    current_locator.average_transmitter_power = base_value

            # Обновление предыдущих значений
            self._prev_power_mode = current_mode
            self._prev_power_unit = current_unit  

            self.main_widget.data_power.setStyleSheet("")
            self.main_widget.data_power.setToolTip("")
            ResolutionCalculator().calculate_resolutions()
            self.table_updater.update_characteristics()
            
            self.charts_updater.update_charts()

        except ValueError as e:
            error_msg = f"Ошибка: {str(e)}"
            self.main_widget.data_power.setStyleSheet("border: 2px solid red; background-color: #ffcccc;")
            self.main_widget.data_power.setToolTip(error_msg)
        except ZeroDivisionError:
            error_msg = "Скважность должна быть больше 0"
            self.main_widget.data_power.setStyleSheet("border: 2px solid red; background-color: #ffcccc;")
            self.main_widget.data_power.setToolTip(error_msg)
        except Exception as e:
            print(f"Критическая ошибка: {str(e)}")
            import traceback
            traceback.print_exc()
        finally:
            self._updating = False

    def update_pri_prf(self):
        try:
            if hasattr(self, "_updating") and self._updating:
                return
            self._updating = True

            # Получаем текущий локатор через менеджер
            current_locator = locators.get_locator(locators.current_locator)

            current_mode = self.main_widget.mode_freq_period.currentText()
            prev_mode = getattr(self, "_prev_priprf_mode", current_mode)

            # Определяем используемые элементы управления
            period_unit_widget = self.main_widget.measurement_period_repeat
            freq_unit_widget = self.main_widget.measurement_freq_repeat

            current_unit = period_unit_widget.currentText() if current_mode == "PRI" else freq_unit_widget.currentText()
            prev_unit = getattr(self, "_prev_priprf_unit", current_unit)

            raw_value = self.main_widget.data_PRI_PRF.text().strip()

            # Конвертация единиц внутри одного режима
            if current_mode == prev_mode and raw_value:
                if current_unit != prev_unit:
                    value = float(raw_value)
                    param_type = "time" if current_mode == "PRI" else "frequency"
                    converted = convert_units(value, prev_unit, current_unit, param_type)
                    self._update_data_field(self.main_widget.data_PRI_PRF, f"{converted:.12g}")
                    raw_value = str(converted)

            # Конвертация между режимами PRI <-> PRF
            if current_mode != prev_mode and raw_value:
                value = float(raw_value)

                try:
                    if current_mode == "PRI":
                        # PRF -> PRI: T = 1/f
                        freq = convert_units(value, prev_unit, "Гц", "frequency")
                        pri = 1 / freq if freq != 0 else 0
                        converted = convert_units(pri, "с", current_unit, "time")
                    else:
                        # PRI -> PRF: f = 1/T
                        period = convert_units(value, prev_unit, "с", "time")
                        freq = 1 / period if period != 0 else 0
                        converted = convert_units(freq, "Гц", current_unit, "frequency")

                    self._update_data_field(self.main_widget.data_PRI_PRF, f"{converted:.12g}")
                    raw_value = str(converted)
                except ZeroDivisionError:
                    raise ValueError("Значение не может быть нулевым")

            # Валидация и сохранение
            if raw_value:
                value = float(raw_value)
                max_value = 1e30 if current_mode == "PRI" else 1e12
                if value < 0 or value > max_value:
                    raise ValueError(f"Некорректное значение {current_mode}")

                # Сохраняем в базовых единицах
                if current_mode == "PRI":
                    base_value = convert_units(value, current_unit, "с", "time")
                    current_locator.pulse_repetition_period = base_value
                else:
                    base_value = convert_units(value, current_unit, "Гц", "frequency")
                    current_locator.pulse_repetition_frequency = base_value

            # Обновляем предыдущие значения
            self._prev_priprf_mode = current_mode
            self._prev_priprf_unit = current_unit

            self.main_widget.data_PRI_PRF.setStyleSheet("")
            self.main_widget.data_PRI_PRF.setToolTip("")
            ResolutionCalculator().calculate_resolutions()
            self.table_updater.update_characteristics()
            
            self.charts_updater.update_charts()

        except ValueError as e:
            error_msg = f"Ошибка: {str(e)}"
            self.main_widget.data_PRI_PRF.setStyleSheet("border: 2px solid red; background-color: #ffcccc;")
            self.main_widget.data_PRI_PRF.setToolTip(error_msg)
        except ZeroDivisionError:
            error_msg = "Невозможно вычислить - деление на ноль"
            self.main_widget.data_PRI_PRF.setStyleSheet("border: 2px solid red; background-color: #ffcccc;")
            self.main_widget.data_PRI_PRF.setToolTip(error_msg)
        except Exception as e:
            print(f"Критическая ошибка: {str(e)}")
            import traceback
            traceback.print_exc()
        finally:
            self._updating = False

    def _update_data_field(self, field, value):
        field.blockSignals(True)
        field.setText(value.rstrip('0').rstrip('.') if '.' in value else value)
        field.blockSignals(False)