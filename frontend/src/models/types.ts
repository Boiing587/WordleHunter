interface Game {
  name: string
  code: string
}

interface GameNames {
  [gen: string]: Game[]
}

interface GameList {
  [gen: string]: string[]
}

interface Monster {
  name: string
  description: string
  games: string[]
  elements: Attribute[]
  statuses: Attribute[]
  weaknesses: Attribute[]
  type: string
  alias: string
  suborder: string
  related: string[]
}

interface Attribute {
  name: string
  note: string
}

interface Proximity {
  [property: string]: {
    status: number
    hint: string
  }
}

interface GuessResponse {
  guess: Monster
  result: Proximity
}

export type { Game, GameList, GameNames, GuessResponse, Monster, Proximity }
