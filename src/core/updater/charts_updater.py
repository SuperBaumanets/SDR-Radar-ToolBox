import pyqtgraph as pg
from PySide6.QtCore import QObject
from src.core.settings.locator import locators
from src.core.settings.target import target
from src.estimation.charts.generate_lfm import *
from src.estimation.charts.generate_fft import *
from src.estimation.charts.generate_snr_noise import *
from src.gui.area.Сharts.general_Charts import GeneralCharts

class Charts_Updater(QObject):
    def __init__(self, charts_widget:GeneralCharts):
        super().__init__()
        self.charts = charts_widget

    def update_charts(self):
        for locator in locators.locators:
            # Проверка корректности параметров
            if (locator.pulse_duration > 0 
                and locator.pulse_repetition_period > 0
                and locator.frequency > 0 
                and locator.bandwidth > 0
                and locator.transmitter_pulse_power > 0
                and target.range > 0):

                try:
                    # Генерация сигнала
                    t, s = generate_lfm_signal(locator)
                    s_n, r = generate_snr_vs_range(locator, 1000)
                    freq, spectrum_db = generate_fft(s)

                    # Получаем виджет графика
                    radar_plot_signal = self.charts.right_charts.get_plot_widget("radar_signal")
                    radar_plot_fft = self.charts.right_charts.get_plot_widget("radar_signal_spectrum")

                    # Обновляем или добавляем кривую
                    if locator.locator in self.charts.left_charts.plot.curves:
                        self.charts.left_charts.plot.update_curve(locator.locator, r, s_n)
                    else:
                        self.charts.left_charts.plot.add_curve(
                            locator.locator, 
                            pen=pg.mkPen(color=pg.intColor(len(self.charts.left_charts.plot.curves)), 
                            name=locator.locator)
                        )
                        self.charts.left_charts.plot.update_curve(locator.locator, r, s_n)

                    # Обновляем или добавляем кривую
                    if locator.locator in radar_plot_signal.curves:
                        radar_plot_signal.update_curve(locator.locator, t, s)
                    else:
                        radar_plot_signal.add_curve(
                            locator.locator, 
                            pen=pg.mkPen(color=pg.intColor(len(radar_plot_signal.curves)), 
                            name=locator.locator)
                        )
                        radar_plot_signal.update_curve(locator.locator, t, s)

                    # Обновляем или добавляем кривую
                    if locator.locator in radar_plot_fft.curves:
                        radar_plot_fft.update_curve(locator.locator, freq, spectrum_db)
                    else:
                        radar_plot_fft.add_curve(
                            locator.locator, 
                            pen=pg.mkPen(color=pg.intColor(len(radar_plot_fft.curves)), 
                            name=locator.locator)
                        )
                        radar_plot_fft.update_curve(locator.locator, freq, spectrum_db)

                except Exception as e:
                    print(f"Ошибка при обновлении графика для {locator.locator}: {str(e)}")