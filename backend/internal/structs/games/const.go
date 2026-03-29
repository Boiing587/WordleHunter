package games

const (
	Gen1     Generation = "gen1"
	Gen2     Generation = "gen2"
	Gen3     Generation = "gen3"
	Gen4     Generation = "gen4"
	Gen5     Generation = "gen5"
	Gen6     Generation = "gen6"
	Frontier Generation = "frontier"
)

var fullGameMap = GameMap{
	"gen1":     []string{"MH1", "MHG", "MHF1"},
	"gen2":     []string{"MH2", "MHF2", "MHFU"},
	"gen3":     []string{"MH3", "MHP3", "MH3U"},
	"gen4":     []string{"MH4", "MH4U", "MHGen", "MHGU"},
	"gen5":     []string{"MHWorld", "MHWI", "MHRise", "MHRS"},
	"gen6":     []string{"MHWilds"},
	"frontier": []string{"MHFrontier", "MHFF", "MHFG", "MHFZ"},
}

var fullNameMap = NameMap{
	"gen1": {
		{"code": "MH1", "name": "Monster Hunter"},
		{"code": "MHG", "name": "Monster Hunter G"},
		{"code": "MHF1", "name": "Monster Hunter Freedom"},
	},
	"gen2": {
		{"code": "MH2", "name": "Monster Hunter 2"},
		{"code": "MHF2", "name": "Monster Hunter Freedom 2"},
		{"code": "MHFU", "name": "Monster Hunter Freedom Unite"},
	},
	"gen3": {
		{"code": "MH3", "name": "Monster Hunter 3"},
		{"code": "MHP3", "name": "Monster Hunter Portable 3rd"},
		{"code": "MH3U", "name": "Monster Hunter 3 Ultimate"},
	},
	"gen4": {
		{"code": "MH4", "name": "Monster Hunter 4"},
		{"code": "MH4U", "name": "Monster Hunter 4 Ultimate"},
		{"code": "MHGen", "name": "Monster Hunter Generations"},
		{"code": "MHGU", "name": "Monster Hunter Generations Ultimate"},
	},
	"gen5": {
		{"code": "MHWorld", "name": "Monster Hunter: World"},
		{"code": "MHWI", "name": "Monster Hunter World: Iceborne"},
		{"code": "MHRise", "name": "Monster Hunter Rise"},
		{"code": "MHRS", "name": "Monster Hunter Rise: Sunbreak"},
	},
	"gen6": {
		{"code": "MHWilds", "name": "Monster Hunter Wilds"},
	},
	"frontier": {
		{"code": "MHFrontier", "name": "Monster Hunter Frontier"},
		{"code": "MHFF", "name": "Monster Hunter Frontier Forward"},
		{"code": "MHFG", "name": "Monster Hunter Frontier G"},
		{"code": "MHFZ", "name": "Monster Hunter Frontier Z / Z Zenith"},
	},
}
