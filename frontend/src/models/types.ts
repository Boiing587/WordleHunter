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
  type: string
  suborder: string
  games: string[]
  elements: string[]
  statuses: string[]
  weaknesses: string[]
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
