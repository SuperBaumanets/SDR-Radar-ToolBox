from src.core.settings.locator import LocatorSettings
from src.core.settings.locator import locators
from typing import Tuple
import numpy as np

def generate_fft(tx_signals: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    current_locator = locators.get_locator(locators.current_locator)

    f_max = current_locator.frequency + current_locator.bandwidth 
    fs = 2 * f_max * 1.1  # Запас 10% выше Найквиста
    if fs < 10e12:
        fs = 10e12  # Минимальная частота дискретизации
    N_fft = 262144
    
    # Проверка входных данных
    if tx_signals.size == 0:
        return np.array([]), np.array([])
    
    # Выбор первого канала для многоканальных сигналов
    signal = tx_signals[0] if tx_signals.ndim > 1 else tx_signals
    
    # Расчет FFT и амплитуды спектра
    spectrum = np.fft.fftshift(np.fft.fft(signal, N_fft))
    spectrum_abs = np.abs(spectrum)  # Преобразуем комплексные значения в амплитуду
    
    # Расчет частотной оси
    freq = np.fft.fftshift(np.fft.fftfreq(N_fft, 1/fs)) + current_locator.frequency
    
    # Преобразование в децибелы с защитой от нуля
    max_amp = np.max(spectrum_abs)
    if max_amp == 0:
        max_amp = 1e-12
    spectrum_db = 20 * np.log10(spectrum_abs / max_amp + 1e-12)
    
    return freq / 1e6, spectrum_db