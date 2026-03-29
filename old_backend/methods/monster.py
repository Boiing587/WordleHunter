import json
import random

from os import walk
from os.path import join
from datetime import datetime
from difflib import SequenceMatcher

from interfaces.Games import Games
from interfaces.Monster import Monster


def loadMonsterList(filter: Games | None = None) -> list[Monster]:
    """Loads the entire monster list and filters if options are supplied.

    Args:
        filter (optional): Games object containing what games to pick monsters from

    Returns:
        list of Monster objects
    """

    full_monster_list: list[Monster] = []
    for root, _, files in walk("./data"):
        for file in files:
            if not file.endswith(".json"):
                continue
            file_path = join(root, file)
            with open(file_path) as f:
                full_monster_list += [
                    Monster.model_validate(monster) for monster in json.load(f)
                ]
    if filter is None or not any([gen[1] for gen in filter]):
        return full_monster_list

    generations = [generation for generation, _ in filter.__annotations__.items()]
    games = [game for generation in generations for game in getattr(filter, generation)]

    filtered_monster_list = [
        monster for monster in full_monster_list if set(monster.games) & set(games)
    ]
    return filtered_monster_list


def getMonster(name: str) -> Monster | None:
    """Retrieves a single monster from the full monster list by its name.

    Args:
        name: A string containing the monster's name

    Returns:
        Monster object for the given monster, or None if it doesn't exist
    """

    monster_list = loadMonsterList()
    result = [monster for monster in monster_list if monster.name == name]
    if result:
        return result[0]
    return None


# REFACTOR edgecases
#  e.g. magalas, not all greats are related
def getRelatives(monster: Monster, monster_list: list[Monster]) -> list[Monster]:
    related: list[Monster] = []
    for relative in monster.related:
        if (rel := getMonster(relative)) is not None:
            related.append(rel)
    return related


def monsterOfTheDay(monster_list: list[Monster], seed: str | None = None) -> Monster:
    """Generates a random monster using the current date as a seed

    Args:
        monster_list: A list of monster objects to generate the monster of the day from

    Returns:
        Monster object with today's monster
    """

    monsterNames = [monster.name for monster in monster_list]
    if seed is None:
        seed = datetime.today().strftime("%d/%m/%Y")
    random.seed(seed)
    random.shuffle(monsterNames)
    monster_of_the_day = random.choice(monsterNames)
    return [monster for monster in monster_list if monster.name == monster_of_the_day][
        0
    ]
