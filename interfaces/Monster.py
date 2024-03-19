from pydantic import BaseModel

from interfaces.Games import Games

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
            "base": [ "Base Species" ],
            "sub": [ "Subspecies", "Rare Species", "Origin Species", "Burst Species" ],
            "variant": [ "Variant", "Risen", "Deviant" ],
            "apex": [ "Apex", "Zenith" ]
        }

    def suborderCategory(self):
        suborder_map = self.suborderMapping()
        reverse_map: dict[str, list] = {v: k for k, values in suborder_map.items() for v in values}
        category = suborder_map[reverse_map.get(self.suborder)]
        return category

    def generation(self):
        generation_map = Games.generationMapping()
        reverse_map = Games.reverseGenerationMapping()
        generation = generation_map[reverse_map.get(self.games[0])]
        return generation