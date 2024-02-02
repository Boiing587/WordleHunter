from pydantic import BaseModel

from interfaces.Games import GameSelection

class Guess(BaseModel):
    guess: str
    games: GameSelection