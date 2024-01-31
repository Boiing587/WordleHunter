from pydantic import BaseModel

class Monster(BaseModel):
    name: str
    species: str
    category: str
    games: list[str]
    elements: list[str] | None
    statuses: list[str] | None
    weaknesses: list[str] | None