interface Game {
    name: string
}

interface Games {
    [gen: string]: Game
}

interface GameSelection {
    [gen: string]: []
}

export type { Game, Games, GameSelection }
