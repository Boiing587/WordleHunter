from pydantic import BaseModel, Field

class Proximity(BaseModel):
    """
    correct:
        0: Guess is correct
        1: Guess is incorrect

    species:
        0: Same species
        1: Different species

    category:
        0: Same category
        1: Similar category
        2: Wrong category
        
        categories:
            :Base
            :Subspecies/Rare Species
            :Variant/Deviant

    game:
        0: Introduced in same game
        1: Introduced in same gen, not same game
        2: Introduced in different gen

    elements:
        0: Exact same elements
        1: Shares some elements
        2: No elements in common

    statuses:
        0: Exact same statuses
        1: Shares some statuses
        2: No statuses in common

    weaknesses:
        0: Exact same weaknesses
        1: Shares some weaknesses
        2: No weaknesses in common
    """
    correct: int = Field(ge=0, le=1)
    species: int = Field(ge=0, le=1)
    category: int = Field(ge=0, le=2)
    game: int = Field(ge=0, le=2)
    elements: int = Field(ge=0, le=2)
    statuses: int = Field(ge=0, le=2)
    weaknesses: int = Field(ge=0, le=2)
