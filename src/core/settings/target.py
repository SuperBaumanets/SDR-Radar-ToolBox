from typing import Dict, Any
from pydantic import BaseModel, ConfigDict, Field

class TargetSettings(BaseModel):
    range: float = Field(default=0)                        # Максимальная дальность 

    model_config = ConfigDict(
        frozen=False,  
        extra="forbid"
    )

    def update_settings(self, new_data: Dict[str, Any]) -> None:
        valid_fields = self.model_fields.keys()
        filtered_data = {k: v for k, v in new_data.items() if k in valid_fields}
        for key, value in filtered_data.items():
            setattr(self, key, value)

target = TargetSettings()