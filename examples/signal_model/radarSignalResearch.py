import numpy as np
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from pyqtgraph import PlotWidget
from scipy.fft import fft, fftshift

class RadarPlotWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Анализ ЛЧМ сигнала")
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        layout = QVBoxLayout()
        self.central_widget.setLayout(layout)

        self.waveform_plot = PlotWidget()
        self.spectrum_plot = PlotWidget()

        layout.addWidget(self.waveform_plot)
        layout.addWidget(self.spectrum_plot)

        self.configure_plots()

    def configure_plots(self):
        for plot in [self.waveform_plot, self.spectrum_plot]:
            plot.setBackground('w')
            plot.showGrid(x=True, y=True, alpha=0.3)
            plot.getAxis('bottom').setPen('k')
            plot.getAxis('left').setPen('k')

def intraPulseLinearChirp(fc: float, B: float, tau: float, PRF: float, N_pulses: float):
    c = 3e8
    PRI = 1 / PRF  # 250 мкс при PRF=4000 Гц

    # Расчет частоты дискретизации
    fs = max(5 * B, 10e9)

    # Генерация комплексного ЛЧМ сигнала
    def generate_pulse(start_time):
        t_segment = np.arange(start_time, start_time + tau, 1/fs)
        phase = 2 * np.pi * (
            (fc - B/2) * (t_segment - start_time) + 
            0.5 * (B/tau) * (t_segment - start_time)**2
        )
        return t_segment, np.exp(1j * phase)

    app = QApplication(sys.argv)
    window = RadarPlotWindow()
    
    # Генерация данных для двух импульсов с разделением NaN
    t_plot = np.array([])
    y_plot = np.array([])
    
    for n in range(2):
        start_time = n * PRI
        t_pulse, tx_pulse = generate_pulse(start_time)
        
        # Добавляем разделитель NaN между импульсами
        if n > 0:
            t_plot = np.append(t_plot, np.nan)
            y_plot = np.append(y_plot, np.nan)
            
        t_plot = np.append(t_plot, t_pulse)
        y_plot = np.append(y_plot, np.real(tx_pulse))

    # Отрисовка формы импульсов
    window.waveform_plot.plot(t_plot*1e6, y_plot, pen='r')
    window.waveform_plot.setTitle(f"Форма ЛЧМ импульсов (PRI = {PRI*1e6:.0f} мкс)", size="12pt")
    window.waveform_plot.setLabel('left', 'Амплитуда')
    window.waveform_plot.setLabel('bottom', 'Время (мкс)')
    window.waveform_plot.setXRange(0, 2*PRI*1e6)

    # Расчет спектра (для первого импульса)
    N_fft = 2097152
    t_pulse, tx_pulse = generate_pulse(0)
    spectrum = fftshift(fft(tx_pulse, N_fft))
    freq = fftshift(np.fft.fftfreq(N_fft, 1/fs)) + fc
    
    # Нормализация и перевод в дБ
    spectrum_db = 20 * np.log10(np.abs(spectrum)/np.max(np.abs(spectrum)))
    freq_mhz = freq / 1e6

    window.spectrum_plot.plot(freq_mhz, spectrum_db, pen='r')
    window.spectrum_plot.setTitle("Спектр ЛЧМ сигнала", size="12pt")
    window.spectrum_plot.setLabel('left', 'Мощность (дБ)')
    window.spectrum_plot.setLabel('bottom', 'Частота (МГц)')
    window.spectrum_plot.setXRange((fc - B)/1e6, (fc + B)/1e6)

    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    intraPulseLinearChirp(
        fc=9410e6,
        B=25e6,
        tau=40e-6,
        PRF=4000,
        N_pulses=2
    )