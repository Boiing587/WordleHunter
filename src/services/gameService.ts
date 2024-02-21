import axios from 'axios'

import type { SelectOptionType } from 'flowbite-svelte';
import type { Games, Game } from '../models/types'

const baseurl = "http://localhost:5000"

async function getGameList() {
  const response = await fetch(`${baseurl}/api/data/gamelist`);
  if (!response.ok) {
    throw new Error('Network response was not ok');
  }
  const games: Games = await response.json();
  return games;
}

async function formatGameSelection(data: Game) {
  const games: SelectOptionType<string|[]>[] = []
  Object.entries(data).forEach((game) => {
    games.push({ name: game[1], value: game[0] })
  })
  return games
}

export { getGameList, formatGameSelection }