from pydantic import BaseModel, Field

class Proximity(BaseModel):
    game: int = Field(ge=0, le=2)