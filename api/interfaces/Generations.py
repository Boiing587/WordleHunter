from pydantic import BaseModel

class Generations(BaseModel):
    gen1: list[str] | None
    gen2: list[str] | None
    gen3: list[str] | None
    gen4: list[str] | None
    gen5: list[str] | None
    frontier: list[str] | None