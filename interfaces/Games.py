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
            "gen1": [
                { "code": "MH1", "name": "Monster Hunter" },
                { "code": "MHG", "name": "Monster Hunter G" },
                { "code": "MHF1", "name": "Monster Hunter Freedom" }
            ],
            "gen2": [
                { "code": "MH2", "name": "Monster Hunter Dos" },
                { "code": "MHF2", "name": "Monster Hunter Freedom 2" },
                { "code": "MHFU", "name": "Monster Hunter Freedom Unite" }
            ],
            "gen3": [
                { "code": "MH3", "name": "Monster Hunter Tri" },
                { "code": "MHP3", "name": "Monster Hunter Portable 3rd" },
                { "code": "MH3U", "name": "Monster Hunter 3 Ultimate" }
            ],
            "gen4": [
                { "code": "MH4", "name": "Monster Hunter 4" },
                { "code": "MH4U", "name": "Monster Hunter 4 Ultimate" },
                { "code": "MHGen", "name": "Monster Hunter Generations" },
                { "code": "MHGU", "name": "Monster Hunter Generations Ultimate" }
            ],
            "gen5": [
                { "code": "MHW", "name": "Monster Hunter World" },
                { "code": "MHWI", "name": "Monster Hunter World: Iceborne" },
                { "code": "MHR", "name": "Monster Hunter Rise" },
                { "code": "MHRS", "name": "Monster Hunter Rise: Sunbreak" }
            ],
            "frontier": [
                { "code": "MHF", "name": "Monster Hunter Frontier" },
                { "code": "MHFF", "name": "Monster Hunter Frontier Forward" },
                { "code": "MHFG", "name": "Monster Hunter Frontier G" },
                { "code": "MHFZ", "name": "Monster Hunter Frontier Z / Z Zenith" }
            ]
        }
