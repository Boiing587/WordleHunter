package games

func NewGameMap(generations []Generation) GameMap {
	gameMap := GameMap{}

	for _, gen := range generations {
		gameMap[string(gen)] = fullGameMap[string(gen)]
	}

	return gameMap
}

func (g GameMap) Reverse() ReverseMap {
	reverseMap := ReverseMap{}

	for key, value := range g {
		for _, game := range value {
			reverseMap[game] = key
		}
	}

	return reverseMap
}

func (g GameMap) Names() NameMap {
	nameMap := NameMap{}

	for gen := range g {
		nameMap[gen] = fullNameMap[gen]
	}

	return nameMap
}
