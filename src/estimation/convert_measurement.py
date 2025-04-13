from math import log10

def frequency_to_wavelength(freq_hz):
    return 3e8 / freq_hz if freq_hz != 0 else 0

def wavelength_to_frequency(wavelength_m):
    return 3e8 / wavelength_m if wavelength_m != 0 else 0

def convert_power_units(value, from_unit, to_unit):
    """Конвертация между линейными и логарифмическими единицами"""
    # Конвертация в ватты
    in_watts = convert_to_watts(value, from_unit)
    
    # Конвертация из ватт в целевую единицу
    if to_unit == "дБВт":
        return 10 * log10(in_watts)
    elif to_unit == "дБм":
        return 10 * log10(in_watts * 1000)
    else:
        return convert_units(in_watts, "Вт", to_unit, "power")

def convert_to_watts(value, unit):
    """Конвертация в абсолютные ватты"""
    if unit == "дБВт":
        return 10 ** (value / 10)
    elif unit == "дБм":
        return 10 ** ((value - 30) / 10)
    else:
        return convert_units(value, unit, "Вт", "power")
    
def convert_units(value, from_unit, to_unit, param_type):
    conversions = {
        "length": {
            "км": 1000,
            "м": 1,          # Метры (базовая единица)
            "см": 0.01,      # Сантиметры
            "мм": 0.001      # Миллиметры
        },
        "frequency": {
            "Гц": 1,        # Герцы
            "кГц": 1e3,      # Килогерцы
            "МГц": 1e6,      # Мегагерцы
            "ГГц": 1e9       # Гигагерцы
        },
        "time": {
            "с": 1,          # Секунды
            "мс": 0.001,     # Миллисекунды
            "мкс": 1e-6      # Микросекунды
        },
        "prf": {
            "Гц": 1,         # Герцы
            "кГц": 1e3,     # Килогерцы
            "МГц": 1e6      # Мегагерцы
        },
        "power": {
            "Вт": 1,
            "кВт": 1e3,
            "МВт": 1e6
        },
        "speed": {
            "м/c": 1.0,          # Метры в секунду (базовая единица)
            "км/ч": 0.2777777778, # 1 км/ч = 1000м/3600с ≈ 0.27778 м/с
        }
    }
    
    # Специальная обработка для логарифмических единиц мощности
    if param_type == "power" and ("дБ" in from_unit or "дБ" in to_unit):
        return convert_power_units(value, from_unit, to_unit)
    
    if param_type == "speed":
        return value * conversions[param_type][from_unit] / conversions[param_type][to_unit]
        
    return value * (conversions[param_type][from_unit] / conversions[param_type][to_unit])