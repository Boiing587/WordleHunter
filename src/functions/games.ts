import axios from 'axios'

import type { SelectOptionType } from 'flowbite-svelte';
import type { Games, Game } from '../interfaces/Games'

export async function getGameList() {
  const response = await axios.get<Games>('http://localhost:5000/api/data/gamelist');
  return response.data;
}

export async function formatGameSelection(data: Game) {
  const games: SelectOptionType<string|[]>[] = []
  Object.entries(data).forEach((game) => {
    games.push({ name: game[1], value: game[0] })
  })
  return games
}