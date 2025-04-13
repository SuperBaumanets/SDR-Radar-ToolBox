from PySide6.QtCore import QObject, QTimer
import adi
import subprocess
from src.core.settings.locator import locators
import numpy as np

class SDRControlHandler(QObject):
    def __init__(self):
        super().__init__()
        self.sdr_widget = None
        self.sdr = None
        self.sdr_connected = False  # Флаг подключения
        self.input_timer = QTimer()
        self.input_timer.setSingleShot(True)
        self.input_timer.timeout.connect(self.setup_ip_sdr)
        
    def set_main_widget(self, updater):
        self.sdr_widget = updater.updater_sdr_control.sdr_control
        self.sdr_updater = updater.updater_sdr_control
        self.sdr_widget.data_sdr.textChanged.connect(self._restart_input_timer)

    def _restart_input_timer(self):
        self.input_timer.stop()
        self.input_timer.start(500)

    def setup_ip_sdr(self):
        ip = self.sdr_widget.data_sdr.text().strip()
        if not ip:
            self.sdr_connected = False
            self.sdr_updater.update_connect(False)
            return
        
        if self.sdr_connected == True:
            return
            
        connect = self._ping_sdr(ip)
        self.sdr_updater.update_connect(connect)
        self.sdr_connected = connect

        if connect:
            try:
                uri = f"ip:{ip}"
                self.sdr = adi.Pluto(uri)
                print(f"Successfully connected to SDR at {uri}")
            except Exception as e:
                print(f"Connection error: {str(e)}")
                self.sdr_connected = False
                self.sdr_updater.update_connect(False)
                self.sdr = None
        else:
            self.sdr = None

    def start_transmission(self):
        if not self.sdr_connected:
            print("SDR not connected. Cannot start transmission.")
            return
            
        try:
            current_locator = locators.get_locator(locators.current_locator)
            self.sdr.sample_rate = int(1e6)
            self.sdr.tx_rf_bandwidth = int(current_locator.bandwidth)
            self.sdr.tx_lo = int(current_locator.frequency)
            self.sdr.tx_hardwaregain_chan0 = -30

            # Рассчет параметров импульса
            pulse_samples = int(100e-6 * 1e6)  
            period_samples = int(current_locator.pulse_repetition_period * 1e6)    
            pause_samples = period_samples - pulse_samples

            # Генерация ЛЧМ импульса
            t_pulse = np.linspace(0, 100e-6, pulse_samples)
            f_start = current_locator.frequency - current_locator.bandwidth/2
            f_end = current_locator.frequency + current_locator.bandwidth/2
            K = (f_end - f_start) / 100e-6  # Скорость изменения частоты
            
            # Формирование фазы ЛЧМ
            phase = 2 * np.pi * (f_start * t_pulse + 0.5 * K * t_pulse**2)
            pulse_signal = 0.5 * np.exp(1.0j * phase)
            
            # Формирование полного периода (импульс + пауза)
            one_period = np.concatenate([
                pulse_signal, 
                np.zeros(pause_samples, dtype=np.complex64)
            ])

            # Создание полного сигнала
            full_signal = np.tile(one_period, 2)
            full_signal *= 2**14  # Масштабирование для PlutoSDR

            # Передача сигнала
            self.sdr.tx(full_signal)

            pass
        except Exception as e:
            print(f"Transmission error: {str(e)}")
            self._handle_sdr_error()

    def stop_transmission(self):
        if not self.sdr_connected:
            return
            
        try:
            # Ваш код для остановки передачи
            pass
        except Exception as e:
            print(f"Stop transmission error: {str(e)}")
            self._handle_sdr_error()

    def _ping_sdr(self, ip: str):
        try:
            subprocess.check_output(["ping", "-c", "1", ip], 
                                  timeout=2,
                                  stderr=subprocess.STDOUT)
            return True
        except subprocess.CalledProcessError:
            return False
        except Exception as e:
            print(f"Ping error: {str(e)}")
            return False

    def _handle_sdr_error(self):
        """Сброс соединения при ошибках"""
        self.sdr_connected = False
        self.sdr_updater.update_connect(False)
        self.sdr = None
        print("SDR connection reset due to error")

    def is_connected(self):
        return self.sdr_connected