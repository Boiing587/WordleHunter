from pydantic import BaseModel

class Generations(BaseModel):
    gen1: list[str] = [ "MH1", "MHG", "MHF1" ]
    gen2: list[str] = [ "MH2", "MHF2", "MHFU" ]
    gen3: list[str] = [ "MH3", "MHP3", "MH3U" ]
    gen4: list[str] = [ "MH4", "MH4U", "MHGen", "MHGU" ]
    gen5: list[str] = [ "MHW", "MHWI", "MHR", "MHRS" ]
    # TODO Frontier

class GameSelection(BaseModel):
    gen1: list[str] | None
    gen2: list[str] | None
    gen3: list[str] | None
    gen4: list[str] | None
    gen5: list[str] | None
    frontier: list[str] | None