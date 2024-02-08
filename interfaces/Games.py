from pydantic import BaseModel

class Games(BaseModel):
    gen1: list[str]
    gen2: list[str]
    gen3: list[str]
    gen4: list[str]
    gen5: list[str]
    frontier: list[str]

    @staticmethod
    def generationMapping():
        return {
            'gen1': [ "MH1", "MHG", "MHF1" ],
            'gen2': [ "MH2", "MHF2", "MHFU" ],
            'gen3': [ "MH3", "MHP3", "MH3U" ],
            'gen4': [ "MH4", "MH4U", "MHGen", "MHGU" ],
            'gen5': [ "MHW", "MHWI", "MHR", "MHRS" ]
        }