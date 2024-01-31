from pydantic import BaseModel

class Games(BaseModel):
    Gen1: list[str] = [ "MH1", "MHG", "MHF1" ]
    Gen2: list[str] = [ "MH2", "MHF2", "MHFU" ]
    Gen3: list[str] = [ "MH3", "MHP3", "MH3U" ]
    Gen4: list[str] = [ "MH4", "MH4U", "MHGen", "MHGU" ]
    Gen5: list[str] = [ "MHW", "MHWI", "MHR", "MHRS" ]
    # TODO Frontier