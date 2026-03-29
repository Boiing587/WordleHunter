from typing import Optional
from pydantic import BaseModel

from interfaces.Games import Games

class Guess(BaseModel):
    guess: str
    games: Games
    seed: Optional[str] = None