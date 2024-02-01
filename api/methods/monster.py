import json
import random

from os import walk
from os.path import join
from datetime import datetime

from interfaces.GameSelection import GameSelection
from interfaces.Monster import Monster

# FIXME include monsters that are present in, but not new in generation
# NOTE Frontier: each season also includes monsters of all previous seasons
def loadSelectedMonsterList(game_selection: GameSelection) -> list[Monster]:
    """Loads a list of monsters given the selected games.

    Args:
        game_selection: GameSelection object with information on what games to get monsters from.

    Returns:
        list of Monster objects.
    """

    monster_list: list[Monster] = []
    _properties = game_selection.__annotations__
    for generation, _ in _properties.items():
        for game in getattr(game_selection, generation):
            with open(f"./data/{generation}/{game}.json") as f:
                monster_list += [Monster.model_validate(monster) for monster in json.load(f)]
    return monster_list


def loadFullMonsterList() -> list[Monster]:
    """Loads the entire list of monsters.

    Returns:
        List of all Monster objects
    """

    monster_list: list[Monster] = []
    for root, _, files in walk('./data'):
        for file in files:
            if not file.endswith('.json'): continue
            file_path = join(root, file)
            with open(file_path) as f:
                monster_list += [Monster.model_validate(monster) for monster in json.load(f)]
    return monster_list

def getMonster(name: str) -> Monster | None:
    """Retrieves a single monster from the full monster list by its name.

    Args:
        name: A string containing the monster's name

    Returns:
        Monster object for the given monster, or None if it doesn't exist
    """

    monster_list = loadFullMonsterList()
    result = [monster for monster in monster_list if monster.name == name]
    if result:
        return result[0]
    return None

def monsterOfTheDay(monster_list: list[Monster]) -> Monster:
    """Generates a random monster using the current date as a seed

    Args:
        monster_list: A list of monster objects to generate the monster of the day from

    Returns:
        Monster object with today's monster
    """

    monsterNames = [monster.name for monster in monster_list]
    seed = datetime.today().strftime("%d/%m/%Y")
    random.seed(seed)
    random.shuffle(monsterNames)
    monster_of_the_day = random.choice(monsterNames)
    return [monster for monster in monster_list if monster.name == monster_of_the_day][0]