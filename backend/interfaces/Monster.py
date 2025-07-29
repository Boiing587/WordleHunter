from pydantic import BaseModel

from interfaces.Games import Games

class Monster(BaseModel):
    name: str
    type: str
    suborder: str
    games: list[str]
    elements: list[str]
    statuses: list[str]
    weaknesses: list[str]

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
        reverse_map: dict[str, str] = {v: k for k, values in suborder_map.items() for v in values}
        category = suborder_map[str(reverse_map.get(self.suborder))]
        return category

    def generation(self):
        generation_map = Games.generationMapping()
        reverse_map = Games.reverseGenerationMapping()
        generation = generation_map[str(reverse_map.get(self.games[0]))]
        return generation