from interfaces.Games import Games
from interfaces.Monster import Monster
from interfaces.Proximity import Proximity

# NOTE removed introduced property
#  first game in list is game monster was introduced
def compareGuess(guess: str, motd: Monster) -> Proximity:
    """Compares the user's guess to the monster of the day.

    Args:
        guess: string with the name of the monster the user guessed.
        motd: Monster object for the monster of the day.

    Returns:
        Proximity object with information on how close the guess is.
    """

    return "wrong lmao"