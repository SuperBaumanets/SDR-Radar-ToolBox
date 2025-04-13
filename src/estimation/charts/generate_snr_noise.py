from typing import Tuple
import numpy as np
from src.core.settings.locator import LocatorSettings
from src.core.settings.target import target

def generate_snr_vs_range(
    locator: LocatorSettings, 
    num_points: int = 1000
) -> Tuple[np.ndarray, np.ndarray]:
    # Константы
    N0 = 1e-20            # Спектральная плотность шума (Вт/Гц)
    R_min = 1.0           # Минимальное расстояние (м)
    R_max = target.range  # Максимальное расстояние из TargetSettings
    
    # Параметры локатора
    Pt = locator.transmitter_pulse_power  # Мощность передатчика (Вт)
    λ = locator.wavelength                # Длина волны (м)
    B = locator.bandwidth                 # Ширина полосы (Гц)

    # Генерация расстояний в метрах
    distances = np.linspace(R_min, R_max, num_points)
    
    # Радиолокационное уравнение
    snr_linear = (Pt * λ**2) / ((4 * np.pi * distances)**2 * N0 * B)
    snr_db = 10 * np.log10(snr_linear, where=snr_linear > 0)
    
    # Обработка некорректных значений
    snr_db = np.nan_to_num(snr_db, nan=-300, posinf=-300, neginf=-300)
    snr_db = np.clip(snr_db, -300, 300)
    
    return snr_db, distances/1000  # Конвертация метров в километры
