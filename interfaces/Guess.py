from pydantic import BaseModel

from interfaces.Games import Games

class Guess(BaseModel):
    guess: str
    games: Games