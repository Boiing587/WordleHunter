from pydantic import BaseModel

class Games(BaseModel):
    gen1: list[str]
    gen2: list[str]
    gen3: list[str]
    gen4: list[str]
    gen5: list[str]
    frontier: list[str]

    @staticmethod
    def generationMapping() -> dict[str,list[str]]:
        return {
            'gen1': [ "MH1", "MHG", "MHF1" ],
            'gen2': [ "MH2", "MHF2", "MHFU" ],
            'gen3': [ "MH3", "MHP3", "MH3U" ],
            'gen4': [ "MH4", "MH4U", "MHGen", "MHGU" ],
            'gen5': [ "MHW", "MHWI", "MHR", "MHRS" ]
        }
    
    @staticmethod
    def gameNames() -> dict[str,dict[str,str]]:
        return {
            "gen1": {
                "MH1"   : "Monster Hunter",
                "MHG"   : "Monster Hunter G",
                "MHF1"  : "Monster Hunter Freedom",
            },
            "gen2": {
                "MH2"   : "Monster Hunter Dos",
                "MHF2"  : "Monster Hunter Freedom 2",
                "MHFU"  : "Monster Hunter Freedom Unite",
            },
            "gen3": {
                "MH3"   : "Monster Hunter Tri",
                "MHP3"  : "Monster Hunter Portable 3rd",
                "MH3U"  : "Monster Hunter 3 Ultimate",
            },
            "gen4": {
                "MH4"   : "Monster Hunter 4",
                "MH4U"  : "Monster Hunter 4 Ultimate",
                "MHGen" : "Monster Hunter Generations",
                "MHGU"  : "Monster Hunter Generations Ultimate",
            },
            "gen5": {
                "MHW"   : "Monster Hunter World",
                "MHWI"  : "Monster Hunter World: Iceborne",
                "MHR"   : "Monster Hunter Rise",
                "MHRS"  : "Monster Hunter Rise: Sunbreak",
            }
        }
