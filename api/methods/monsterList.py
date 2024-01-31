import json

from interfaces.GameSelection import GameSelection
from interfaces.Monster import Monster

# TODO include monsters that are present in, but not new in generation
def loadMonsterList(generations: GameSelection) -> list[Monster]:
    monsterList: list[Monster] = []
    _properties = generations.__annotations__
    for generation, _ in _properties.items():
        for game in getattr(generations, generation):
            with open(f"./data/{generation}/{game}.json") as f:
                monsterList += json.loads(f.read())
    return monsterList