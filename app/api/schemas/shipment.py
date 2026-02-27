from pydantic import BaseModel, Field

class ShipmentBase(BaseModel):
    content: str = Field(max_length=30)
    weight: float = Field(lt=25, ge=1)
    destination: int | None = Field(default=None)

class ShipmentCreate(ShipmentBase):
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "content": "Books",
                    "weight": 2.5,
                    "destination": 12345
                }
            ]
        }
    }