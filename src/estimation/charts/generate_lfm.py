from src.core.settings.locator import LocatorSettings
from typing import Tuple
import numpy as np

def generate_lfm_signal(locator: LocatorSettings) -> Tuple[np.ndarray, np.ndarray]:
    # Получаем параметры из настроек
    tau = locator.pulse_duration        # Длительность импульса
    T = locator.pulse_repetition_period # Полный период
    f0 = locator.frequency              # Центральная частота
    B = locator.bandwidth               # Полоса ЛЧМ
    
    f_max = f0 + B
    fs = 2 * f_max * 1.1  # Запас 10% выше Найквиста
    if fs < 10e12:
        fs = 10e12  # Минимальная частота дискретизации
        
    t_impulse = np.linspace(0, tau, int(tau*fs))  # Время импульса
    #t_pause = np.linspace(tau, T, int((T-tau)*fs)) # Время паузы
    
    K = B / tau  # Скорость изменения частоты
    chirp_signal = np.sin(2*np.pi*(f0*t_impulse + 0.5*K*t_impulse**2))
    
    #full_signal = np.concatenate([chirp_signal, np.zeros_like(t_pause)])
    #full_time = np.concatenate([t_impulse, t_pause])
    full_signal = chirp_signal
    full_time = t_impulse
    
    return full_time, full_signal