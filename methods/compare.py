from interfaces.Games import Games
from interfaces.Monster import Monster
from interfaces.Proximity import ProximityResponse, PropertyProximity

from methods.monster import getRelatives, loadMonsterList #, inSameCategory, inSameGeneration

# NOTE removed introduced property
#  first game in list is game monster was introduced
def compareGuess(guess: Monster, motd: Monster) -> ProximityResponse | None:
    """Compares the user's guess to the monster of the day.

    Args:
        guess: Monster object the player guessed.
        motd: Monster object for the monster of the day.

    Returns:
        Proximity object with information on how close the guess is, or None if the guessed monster doesn't exist.
    """

    if not guess:
        return None

    comparison = ProximityResponse()
    newline_list = '\n - '

    if guess == motd:
        comparison.correct.status = 0
        comparison.type.status = 0
        comparison.suborder.status = 0
        comparison.game.status = 0
        comparison.elements.status = 0
        comparison.statuses.status = 0
        comparison.weaknesses.status = 0
        return comparison

    monster_list = loadMonsterList()
    motd_relatives = getRelatives(motd, monster_list)

    if guess in motd_relatives:
        comparison.correct.status = 1
        comparison.correct.hint = "The monster is related to your guess."
    else:
        comparison.correct.status = 2
        comparison.correct.hint = "Incorrect monster."

    if guess.type == motd.type:
        comparison.type.status = 0
        comparison.type.hint = "The monster is of the same type."
    else:
        comparison.type.status = 2
        comparison.type.hint = "The monster is of a different type."

    if guess.suborder == motd.suborder:
        comparison.suborder.status = 0
        comparison.suborder.hint = "The monster is of the same suborder."
    elif (suborder_category := guess.suborderCategory()) == motd.suborderCategory():
        comparison.suborder.status = 1
        comparison.suborder.hint = f"The monster is in the same suborder category:\n - {newline_list.join(suborder for suborder in suborder_category)}"
    else:
        comparison.suborder.status = 2
        comparison.suborder.hint = "The monster is of a different suborder."

    if guess.games[0] == motd.games[0]:
        comparison.game.status = 0
        comparison.game.hint = "The monster was introduced in the same game."
    elif guess.generation() == motd.generation():
        comparison.game.status = 1
        comparison.game.hint = "The monster was introduced in the same generation, but not the same game."
    else:
        comparison.game.status = 2
        comparison.game.hint = "The monster was introduced in a different generation"

    if guess.elements == motd.elements:
        comparison.elements.status = 0
        comparison.elements.hint = "The monster uses the same elements."
    elif (common_elements := list(set(guess.elements).intersection(set(motd.elements)))):
        comparison.elements.status = 1
        comparison.elements.hint = f"The monster shares the following elements:\n - {newline_list.join(element for element in common_elements)}"
    else:
        comparison.elements.status = 2
        comparison.elements.hint = "The monster has no elements in common."

    if guess.statuses == motd.statuses:
        comparison.statuses.status = 0
        comparison.statuses.hint = "The monster uses the same statuses."
    elif (common_statuses := set(guess.statuses).intersection(set(motd.statuses))):
        comparison.statuses.status = 1
        comparison.statuses.hint = f"The monster shares the following statuses:\n - {newline_list.join(status for status in common_statuses)}"
    else:
        comparison.statuses.status = 2
        comparison.statuses.hint = "The monster has no statuses in common."

    if guess.weaknesses == motd.weaknesses:
        comparison.weaknesses.status = 0
        comparison.weaknesses.hint = "The monster has the same weaknesses."
    elif (common_weaknesses := set(guess.weaknesses).intersection(set(motd.weaknesses))):
        comparison.weaknesses.status = 1
        comparison.weaknesses.hint = f"The monster shares the following weaknesses:\n - {newline_list.join(weakness for weakness in common_weaknesses)}"
    else:
        comparison.weaknesses.status = 2
        comparison.weaknesses.hint = "The monster has no weaknesses in common."

    return comparison