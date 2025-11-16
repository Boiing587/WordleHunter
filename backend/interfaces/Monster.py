from pydantic import BaseModel

from interfaces.Attribute import Attribute
from interfaces.Games import Games


class Monster(BaseModel):
    name: str
    description: str
    games: list[str]
    elements: list[Attribute]
    statuses: list[Attribute]
    weaknesses: list[Attribute]
    type: str
    alias: str
    suborder: str
    related: list[str]

    @staticmethod
    def suborderMapping():
        return {
            "base": ["Base Species"],
            "sub": ["Subspecies", "Rare Species", "Origin Species", "Burst Species"],
            "variant": ["Variant", "Risen", "Deviant", "Guardian"],
            "apex": ["Apex", "Zenith Species"],
        }

    def suborderCategory(self):
        suborder_map = self.suborderMapping()
        reverse_map: dict[str, str] = {
            v: k for k, values in suborder_map.items() for v in values
        }
        category = suborder_map[str(reverse_map.get(self.suborder))]
        return category

    def generation(self):
        generation_map = Games.generationMapping()
        reverse_map = Games.reverseGenerationMapping()
        generation = generation_map[
            str(reverse_map.get(Games.nameToCode(self.games[0])))
        ]
        return generation
