from pydantic import BaseModel, Field

class PropertyProximity(BaseModel):
    status: int = Field(default=2, ge=0, le=2)
    hint: str | None = None

class ProximityResponse(BaseModel):
    """
    correct:
        0: Correct monster
        1: Correct monster, but a different suborder
        2: Incorrect monster

    type:
        0: Same monster type
        2: Different monster type

    suborder:
        0: Same suborder
        1: Similar suborder
        2: Wrong suborder
        
        suborder categories:
            :Base
            :Subspecies/Rare Species
            :Variant/Deviant
            :Apex/Zenith

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

    correct: PropertyProximity = PropertyProximity()
    type: PropertyProximity = PropertyProximity()
    suborder: PropertyProximity = PropertyProximity()
    game: PropertyProximity = PropertyProximity()
    elements: PropertyProximity = PropertyProximity()
    statuses: PropertyProximity = PropertyProximity()
    weaknesses: PropertyProximity = PropertyProximity()
