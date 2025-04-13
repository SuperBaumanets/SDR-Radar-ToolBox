from typing import Dict, Any
from pydantic import BaseModel, ConfigDict, Field

class LocatorCharacteristics(BaseModel):
    objective_range_resolution: float = Field(default=0)
    objective_speed_resolution: float = Field(default=0)

    threshold_range_resolution: float = Field(default=0)
    threshold_speed_resolution: float = Field(default=0)

    calc_speed_resolution: Dict[str, float] = Field(
        default_factory=dict
    )
    
    calc_range_resolution: Dict[str, float] = Field(
        default_factory=dict
    )

    model_config = ConfigDict(
        frozen=False,
        extra="forbid"
    )
    
    def update_settings(self, new_data: Dict[str, Any]) -> None:
        for field_name in self.model_fields:
            if field_name in new_data:
                setattr(self, field_name, new_data[field_name])
    
    def update_range(self, locator_name: str, range: float):
        self.calc_range_resolution[locator_name] = range

    def update_speed(self, locator_name: str, speed: float):
        self.calc_speed_resolution[locator_name] = speed

    def remove_locator_data(self, locator_name: str) -> None:
        if locator_name in self.calc_speed_resolution:
            del self.calc_speed_resolution[locator_name]
            
        if locator_name in self.calc_range_resolution:
            del self.calc_range_resolution[locator_name]



locator_characteristics = LocatorCharacteristics()