from pydantic import BaseModel

from interfaces.GameSelection import GameSelection

class Guess(BaseModel):
    guess: str
    games: GameSelection