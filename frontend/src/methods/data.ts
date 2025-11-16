import type { GameList, GameNames, Monster } from '@models/types'

const dev = true
const base_url = !dev ? 'https://wordlehunter-api.azurewebsites.net' : 'http://localhost:5000'

async function apiFetch(
  path: string,
  method: string = 'GET',
  headers: HeadersInit | undefined = undefined,
  body: BodyInit | undefined = undefined
) {
  const res = await fetch(`${base_url}/${path}`, { method: method, headers: headers, body: body })
  if (!res.ok) {
    throw new Error(`Error while fetching data!`)
  }
  const _res: any = await res.json()
  return _res
}

async function getGameList() {
  const url = `api/data/gamelist`
  const games: GameNames = await apiFetch(url)
  return games
}

async function getMonsterList(game_selection: GameList) {
  const url = `api/data/monsters`
  const headers = { 'Content-Type': 'application/json' }
  const body = JSON.stringify(game_selection)
  const monsters: Monster[] = await apiFetch(url, 'POST', headers, body)
  return monsters
}

function formatGameSelection(game_selection: GameNames) {
  const formatted_game_selection: GameList = {}
  for (const gen in game_selection) {
    formatted_game_selection[gen] = game_selection[gen].map((game) => game.name)
  }
  return formatted_game_selection
}

function generateSeed(mode: string = 'daily'): string {
  const now = new Date()
  const day = ('0' + now.getDate()).slice(-2)
  const month = ('0' + (now.getMonth() + 1)).slice(-2)
  const year = now.getFullYear()
  const hours = ('0' + now.getHours()).slice(-2)
  const minutes = ('0' + now.getMinutes()).slice(-2)
  const seconds = ('0' + now.getSeconds()).slice(-2)

  switch (mode) {
    case 'daily':
      return `${day}${month}${year}`

    case 'unlimited':
      return `${day}${month}${year}${hours}${minutes}${seconds}`

    default:
      return ''
  }
}

function getIcon(location: string, name: string) {
  const url = new URL(`../../icons/${location}/${name.replaceAll(' ', '_')}.webp`, import.meta.url)
    .href
  return url
}

function getRandomBackground() {
  const locales = [
    'Ancient Forest',
    'Citadel',
    'Coral Highlands',
    "Elder's Recess",
    'Flooded Forest',
    'Frost Islands',
    'Guiding Lands',
    'Hoarfrost Reach',
    'Iceshard Cliffs',
    'Jungle',
    'Lava Caverns',
    'Oilwell Basin',
    'Rotten Vale',
    'Sandy Plains',
    'Scarlet Forest',
    'Shrine Ruins',
    'Wildspire Waste',
    'Windward Plains',
    'Wyveria'
  ]

  const random_locale = locales[Math.floor(Math.random() * locales.length)]
  const url = new URL(`../../backgrounds/${random_locale.replace(' ', '_')}.webp`, import.meta.url)
    .href
  return url
}

export {
  apiFetch,
  formatGameSelection,
  getGameList,
  getMonsterList,
  generateSeed,
  getIcon,
  getRandomBackground
}
