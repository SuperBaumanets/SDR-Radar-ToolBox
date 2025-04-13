from typing import Dict, Any, List
from pydantic import BaseModel, ConfigDict, Field
from pydantic import model_validator

class LocatorSettings(BaseModel):
    locator: str = Field(default="Локатор по умолчанию")    # Имя
    frequency: float = Field(default=0)                     # Частота
    bandwidth: float = Field(default=0)                     # Полоса пропускания
    wavelength: float = Field(default=0)                    # Длина волны
    pulse_repetition_period: float = Field(default=0)       # PRI
    pulse_repetition_frequency: float = Field(default=0)    # PRF
    pulse_duration: float = Field(default=0)                # Ширина импульса
    duty_cycle: float = Field(default=0)                    # Скважность
    transmitter_pulse_power: float = Field(default=0)       # Пиковая мощность 
    average_transmitter_power: float = Field(default=0)     # Средняя мощность
    number_pulse: float = Field(default=0)                  # Количество импульсов

    model_config = ConfigDict(
        frozen=False,  
        extra="forbid"
    )

class LocatorManager(BaseModel):
    locators: List[LocatorSettings] = Field(default_factory=list)
    current_locator: str = Field(default="Локатор по умолчанию")

    @model_validator(mode='after')
    def _init_default_locator(self):
        """Автоматически создает дефолтный локатор при инициализации"""
        if not self.locators:
            default_locator = LocatorSettings()
            self.locators.append(default_locator)
            self.current_locator = default_locator.locator
        return self

    def add_first_locator(self) -> None:
        if not self.locators:
            default_locator = LocatorSettings()
            self.add_locator(default_locator)

    def add_locator(self, locator: LocatorSettings):
        
        if len(self.locators) > 0:
            locator.locator = f"Локатор по умолчанию {len(self.locators)}"
        else:
            locator.locator = f"Локатор по умолчанию"
            
        self.locators.append(locator)
        self.current_locator = locator.locator

    def rename_locator(self, old_name: str, new_name: str) -> None:
        if old_name == new_name:
            return 
        
        if any(loc.locator == new_name for loc in self.locators):
            raise ValueError(f"Локатор с именем '{new_name}' уже существует")
            
        loc = self.get_locator(old_name)
        loc.locator = new_name
        
        if self.current_locator == old_name:
            self.current_locator = new_name

    def get_locator(self, name: str) -> LocatorSettings:
        for loc in self.locators:
            if loc.locator == name:
                return loc
        raise ValueError(f"Локатор '{name}' не найден")

    def update_locator(self, name: str, new_data: Dict[str, Any]):
        loc = self.get_locator(name)
        valid_fields = loc.model_fields.keys()
        filtered_data = {k: v for k, v in new_data.items() if k in valid_fields}
        for key, value in filtered_data.items():
            setattr(loc, key, value)

    def remove_all_except_first(self):
        if len(self.locators) > 1:
            first_locator = self.locators[0]
            
            self.locators.clear()
            self.locators.append(first_locator)
            
            self.current_locator = first_locator.locator

    def remove_all_locators(self):
        self.locators.clear()
        self.current_locator = ""

    def remove_current_locator(self) -> None:
        if len(self.locators) <= 1:
            raise ValueError("Невозможно удалить последний оставшийся локатор")
        
        try:
            current_index = next(i for i, loc in enumerate(self.locators) 
                               if loc.locator == self.current_locator)
        except StopIteration:
            raise ValueError("Текущий локатор не найден в списке") from None

        del self.locators[current_index]

        new_index = max(0, current_index - 1)
        if new_index >= len(self.locators):
            new_index = len(self.locators) - 1

        self.current_locator = self.locators[new_index].locator

locators = LocatorManager()