from interfaces.Games import Games
from interfaces.Monster import Monster
from interfaces.Proximity import Proximity

from methods.monster import getMonster

# NOTE removed introduced property
#  first game in list is game monster was introduced
def compareGuess(guess: str, motd: Monster) -> Proximity | None:
    """Compares the user's guess to the monster of the day.

    Args:
        guess: string with the name of the monster the user guessed.
        motd: Monster object for the monster of the day.

    Returns:
        Proximity object with information on how close the guess is.
    """

    if guess == motd.name:
        return {
            'correct': 0,
            'species': 0,
            'category': 0,
            'game': 0,
            'elements': 0,
            'statuses': 0,
            'weaknesses': 0
        }

    if not (monster := getMonster(guess)):
        return None

    return {
        'correct': 1,
        'species': 1,
        'category': 2,
        'game': 2,
        'elements': 2,
        'statuses': 2,
        'weaknesses': 2
    }