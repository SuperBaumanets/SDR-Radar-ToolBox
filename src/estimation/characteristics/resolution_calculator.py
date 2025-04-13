from src.core.settings.locator import locators
from src.core.settings.locator_characteristics import locator_characteristics

class ResolutionCalculator:
    def calculate_resolutions(self):
        """Публичный метод для выполнения всех вычислений"""
        self._calculate_range_resolution()
        self._calculate_speed_resolution()

    def _calculate_range_resolution(self):
        """Внутренний метод для вычисления разрешающей способности по дальности"""
        C = 3e8  # Скорость света м/с
        for locator in locators.locators:
            if locator.pulse_duration > 0:
                resolution = (C * locator.pulse_duration) / 2
                locator_characteristics.update_range(locator.locator, round(resolution, 5))

    def _calculate_speed_resolution(self):
        """Внутренний метод для вычисления разрешающей способности по скорости"""
        for locator in locators.locators:
            if locator.wavelength > 0 and locator.pulse_duration > 0:
                resolution = locator.wavelength / (2 * locator.pulse_duration)
                locator_characteristics.update_speed(locator.locator, round(resolution, 5))