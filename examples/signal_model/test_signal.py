import pytest
import numpy as np
from scipy.signal import correlate, welch
from scipy.fft import fft, fftshift

def generate_reference_lfm(fs, fc, bw, tau):
    """Генерация эталонного ЛЧМ сигнала с фиксированным размером"""
    n_samples = int(tau * fs)
    t = np.linspace(0, tau, n_samples)
    chirp = np.exp(1j * np.pi * (bw/tau) * t**2)
    return chirp

def align_signals(ref_signal, test_signal):
    """Выравнивание размеров сигналов"""
    min_len = min(len(ref_signal), len(test_signal))
    return ref_signal[:min_len], test_signal[:min_len]

def compare_signals(ref_signal, test_signal, fs, fc, bw, tau, pri):
    """Сравнение характеристик двух сигналов с выравниванием"""
    # Выравнивание размеров
    ref, test = align_signals(ref_signal, test_signal)
    
    metrics = {}
    
    # 1. Тест на амплитуду
    metrics['amplitude_diff'] = np.abs(np.mean(np.abs(ref)) - np.mean(np.abs(test)))
    
    # 2. Тест на длительность импульса
    def estimate_pulse_duration(signal, fs, threshold=0.1):
        power = np.abs(signal)**2
        above_threshold = power > threshold*np.max(power)
        return np.sum(above_threshold)/fs
    
    metrics['duration_diff'] = np.abs(
        estimate_pulse_duration(ref, fs) - 
        estimate_pulse_duration(test, fs))
    
    # 3. Тест на период повторения
    def estimate_pri(signal, fs):
        corr = correlate(signal, signal, mode='full')
        corr = corr[len(corr)//2:]  # Берем только положительные задержки
        peaks = np.argsort(-corr)[:3]
        return np.mean(np.diff(peaks))/fs
    
    metrics['pri_diff'] = np.abs(pri - estimate_pri(test, fs))
    
    # 4. Тест на спектр
    def compare_spectrum(s1, s2, fs):
        nperseg = min(len(s1), len(s2), 1024)
        f1, p1 = welch(s1, fs, nperseg=nperseg, return_onesided=False)
        f2, p2 = welch(s2, fs, nperseg=nperseg, return_onesided=False)
        p1 = fftshift(p1)
        p2 = fftshift(p2)
        return np.sqrt(np.mean((p1 - p2)**2))
    
    metrics['spectral_diff'] = compare_spectrum(ref, test, fs)
    
    return metrics  # Добавлен возврат результатов

@pytest.fixture
def setup_signals():
    # Параметры сигнала
    fs = 10e9    # Частота дискретизации
    fc = 9410e6    # Несущая частота
    bw = 25e6     # Полоса
    tau = 40e-9  # Длительность импульса
    pri = 250e-6  # Период повторения
    
    # Генерация эталонного сигнала
    ref_signal = generate_reference_lfm(fs, fc, bw, tau)
    
    # Генерация тестового сигнала (заглушка)
    test_signal = np.concatenate([
        generate_reference_lfm(fs, fc, bw, tau),
        np.zeros(int(fs*(pri - tau)))
    ])
    
    return ref_signal, test_signal, fs, fc, bw, tau, pri

# Тестовые функции остаются без изменений
def test_amplitude(setup_signals):
    ref, test, fs, fc, bw, tau, pri = setup_signals
    metrics = compare_signals(ref, test, fs, fc, bw, tau, pri)
    assert metrics['amplitude_diff'] < 0.1, "Отличие амплитуды превышает 10%"

def test_pulse_duration(setup_signals):
    ref, test, fs, fc, bw, tau, pri = setup_signals
    metrics = compare_signals(ref, test, fs, fc, bw, tau, pri)
    assert metrics['duration_diff'] < 0.1*tau, "Отличие длительности импульса > 10%"

def test_pri(setup_signals):
    ref, test, fs, fc, bw, tau, pri = setup_signals
    metrics = compare_signals(ref, test, fs, fc, bw, tau, pri)
    assert 0.01*metrics['pri_diff'] < 0.01*pri, "Отличие PRI > 1%"

def test_spectrum(setup_signals):
    ref, test, fs, fc, bw, tau, pri = setup_signals
    metrics = compare_signals(ref, test, fs, fc, bw, tau, pri)
    assert metrics['spectral_diff'] < 0.1, "Отличие спектра >10%"