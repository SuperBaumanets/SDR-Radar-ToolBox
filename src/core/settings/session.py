from typing import Dict, Any
from pydantic import BaseModel, Field, ConfigDict

class FileSettings(BaseModel):
    file_location: str = Field(default="src/resources/data/airfield_locators/airfield_locator.toml")
    
    model_config = ConfigDict(
        frozen=False,
        extra="forbid"
    )
    
    def update_settings(self, new_data: Dict[str, Any]) -> None:
        for field_name in self.model_fields:
            if field_name in new_data:
                setattr(self, field_name, new_data[field_name])

file = FileSettings()