export interface Game {
  name: string
}

export interface Games {
  [gen: string]: Game
}

export interface GameSelection {
  [gen: string]: []
}
