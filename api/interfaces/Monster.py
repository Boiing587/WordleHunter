from pydantic import BaseModel

class Monster(BaseModel):
    name: str
    type: str
    suborder: str
    games: list[str]
    elements: list[str] | None
    statuses: list[str] | None
    weaknesses: list[str] | None

    @staticmethod
    def suborderMapping():
        return {
            "base": [ "Base species" ],
            "sub": [ "Subspecies", "Rare Species" ],
            "variant": [ "Variant", "Devian" ],
            "apex": [ "Apex", "Zenith" ]
        }
