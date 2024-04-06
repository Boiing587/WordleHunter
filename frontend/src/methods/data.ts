import type { GameList, GameNames, Monster } from "@models/types";

const dev = false
const base_url = !dev ? "https://wordlehunter-api.azurewebsites.net" : "http://localhost:5000"

async function apiFetch(url: string, method: string = 'GET', headers: HeadersInit | undefined = undefined, body: BodyInit | undefined = undefined) {
  const res = await fetch(url, {method: method, headers: headers, body: body})
  if (!res.ok) {
    throw new Error(`Error while fetching data!`)
  }
  const _res: any = await res.json()
  return _res
}

async function getGameList() {
  const url = `${base_url}/api/data/gamelist`
  const games: GameNames = await apiFetch(url)
  return games
}

async function getMonsterList(game_selection: GameList) {
  const url = `${base_url}/api/data/monsters`
  const headers = { 'Content-Type': 'application/json' }
  const body = JSON.stringify(game_selection)
  const monsters: Monster[] = await apiFetch(url, 'POST', headers, body)
  return monsters
}

function formatGameSelection(game_selection: GameNames) {
  const formatted_game_selection: GameList = {}
  for (const gen in game_selection) {
    formatted_game_selection[gen] = game_selection[gen].map(game => game.code)
  }
  return formatted_game_selection
}

export { apiFetch, formatGameSelection, getGameList, getMonsterList }