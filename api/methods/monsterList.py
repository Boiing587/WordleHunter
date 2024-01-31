import json

from interfaces.GameSelection import GameSelection
from interfaces.Monster import Monster

# FIXME include monsters that are present in, but not new in generation
# NOTE Frontier: each season also includes monsters of all previous seasons
def loadMonsterList(game_selection: GameSelection) -> list[Monster]:
    monster_list: list[Monster] = []
    _properties = game_selection.__annotations__
    for generation, _ in _properties.items():
        for game in getattr(game_selection, generation):
            with open(f"./data/{generation}/{game}.json") as f:
                monster_list += json.loads(f.read())
    return monster_list