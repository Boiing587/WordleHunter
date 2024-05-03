import type { GameList, GuessResponse, Proximity, Monster } from "@models/types";

const dev = false
const base_url = !dev ? "https://wordlehunter-api.azurewebsites.net" : "http://localhost:5000"

async function submitGuess(guess: string, selected_games: GameList, seed: string | null = null) {
  const body = {
    guess: guess,
    games: selected_games,
    seed: seed
  }
  const res = await fetch(`${base_url}/api/guess`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) })
  if (!res.ok) {
    throw new Error('There was an error while submitting your guess.')
  }
  const guess_response: GuessResponse = await res.json()
  return guess_response
}

function formatMonsterInfoData(property_name: string, property_value: string | string[]) {
  if (typeof property_value === 'string') {
    return [property_value]
  }
  if (property_value.length === 0) {
    return ['None']
  }
  if (property_name == 'games' && property_value.length > 5) { // Only the games property can have more than 5 items
    return [property_value[0], `${property_value.length} games`]
  }
  return property_value
}

function responseInfoStyle(property_name: string, response: GuessResponse) {
  const result = response.result
  switch (property_name) {
    case 'name':
      return `response_status_${result['correct'].status}`
    case 'type':
      return `response_status_${result['type'].status}`
    case 'suborder':
      return `response_status_${result['suborder'].status}`
    case 'games':
      return `response_status_${result['game'].status}`
    case 'elements':
      return `response_status_${result['elements'].status}`
    case 'statuses':
      return `response_status_${result['statuses'].status}`
    case 'weaknesses':
      return `response_status_${result['weaknesses'].status}`
  }
}

function responseInfoTitle(property_name: string, response: GuessResponse) {
  const result: Proximity = response.result
  switch (property_name) {
    case 'name':
      return result['correct'].hint
    case 'type':
      return result['type'].hint
    case 'suborder':
      return result['suborder'].hint
    case 'games':
      return result['game'].hint
    case 'elements':
      return result['elements'].hint
    case 'statuses':
      return result['statuses'].hint
    case 'weaknesses':
      return result['weaknesses'].hint
  }
}

function formatPropertyTitle(property: string | string[]) {
  if (typeof property === 'string') {
    return property
  }
  return property.join(', ')
}

function filterType(monster_list: Monster[], response: GuessResponse): Monster[] {
  const guess = response.guess
  const result = response.result
  switch (result.type.status) {
    case 0:
      monster_list = monster_list.filter(monster => monster.type === guess.type)
      break

    case 2:
      monster_list = monster_list.filter(monster => monster.type !== guess.type)
      break
    }
  return monster_list
}

function filterSuborder(monster_list: Monster[], response: GuessResponse): Monster[] {
  const guess = response.guess
  const result = response.result
  const suborder_category = result.suborder.hint ? result.suborder.hint.split('- ').slice(1).map(category => { return category.trim() }) : null
  switch (result.suborder.status) {
    case 0:
      monster_list = monster_list.filter(monster => monster.suborder === guess.suborder)
      break

    case 1:
      monster_list = monster_list.filter(monster => (suborder_category as string[]).includes(monster.suborder))
      break

    case 2:
      monster_list = monster_list.filter(monster => monster.suborder !== guess.suborder)
      break
  }
  return monster_list
}

function filterGames(monster_list: Monster[], response: GuessResponse): Monster[] {
  const guess = response.guess
  const result = response.result
  function sameGeneration(guess: Monster, comparator: Monster): boolean {
    const generations: string[][] = [
      [ "MH1", "MHG", "MHF1" ],
      [ "MH2", "MHF2", "MHFU" ],
      [ "MH3", "MHP3", "MH3U" ],
      [ "MH4", "MH4U", "MHGen", "MHGU" ],
      [ "MHW", "MHWI", "MHR", "MHRS" ],
      [ "MHF", "MHFF", "MHFG", "MHFZ" ]
    ]
    let return_value = false
    generations.forEach(generation => {
      if (generation.includes(guess.games[0]) && generation.includes(comparator.games[0])) {
        return_value = true
        return
      }
      return return_value
    })
    return return_value
  }
  switch (result.game.status) {
    case 0:
      monster_list = monster_list.filter(monster => monster.games[0] === guess.games[0])
      break

    case 1:
      monster_list = monster_list.filter(monster => sameGeneration(guess, monster))
      break

    case 2:
      monster_list = monster_list.filter(monster => monster.games[0] !== guess.games[0])
      break
  }
  return monster_list
}

function filterElements(monster_list: Monster[], response: GuessResponse): Monster[] {
  const guess = response.guess
  const result = response.result
  const common_elements = result.elements.hint ? result.elements.hint.split('- ').slice(1).map(element => { return element.trim() }) : null
  switch (result.elements.status) {
    case 0:
      monster_list = monster_list.filter(monster => {
        if (guess.elements.length === 0) {
          return monster.elements.length === 0
        } else {
          return guess.elements.every(element => monster.elements.includes(element))
        }
      });
      break

    case 1:
      monster_list = monster_list.filter(monster => (common_elements as string[]).some(element => monster.elements.includes(element)))
      break

    case 2:
      monster_list = monster_list.filter(monster => guess.elements.every(element => !monster.elements.includes(element)))
      break
  }
  return monster_list
}

function filterStatuses(monster_list: Monster[], response: GuessResponse): Monster[] {
  const guess = response.guess
  const result = response.result
  const common_statuses = result.statuses.hint ? result.statuses.hint.split('- ').slice(1).map(status => { return status.trim() }) : null
  switch (result.statuses.status) {
    case 0:
      monster_list = monster_list.filter(monster => {
        if (guess.statuses.length === 0) {
          return monster.statuses.length === 0
        } else {
          return guess.statuses.every(status => monster.statuses.includes(status))
        }
      });
      break

    case 1:
      monster_list = monster_list.filter(monster => (common_statuses as string[]).some(status => monster.statuses.includes(status)))
      break

    case 2:
      monster_list = monster_list.filter(monster => guess.statuses.every(status => !monster.statuses.includes(status)))
      break
  }
  return monster_list
}

function filterWeaknesses(monster_list: Monster[], response: GuessResponse): Monster[] {
  const guess = response.guess
  const result = response.result
  const common_weaknesses = result.weaknesses.hint ? result.weaknesses.hint.split('- ').slice(1).map(weakness => { return weakness.trim() }) : null
  switch (result.weaknesses.status) {
    case 0:
      monster_list = monster_list.filter(monster => {
        if (guess.weaknesses.length === 0) {
          return monster.weaknesses.length === 0
        } else {
          return guess.weaknesses.every(weakness => monster.weaknesses.includes(weakness))
        }
      });
      break

    case 1:
      monster_list = monster_list.filter(monster => (common_weaknesses as string[]).some(weakness => monster.weaknesses.includes(weakness)))
      break

    case 2:
      monster_list = monster_list.filter(monster => guess.weaknesses.every(weakness => !monster.weaknesses.includes(weakness)))
      break
  }
  return monster_list
}

function shareResults(guess_history: GuessResponse[], selected_games: GameList, game_list: GameList) {
  const seed = localStorage.getItem('seed')
  if (seed === null) {
    return
  }
  const date = `${seed.slice(0, 2)}/${seed.slice(2, 4)}/${seed.slice(4, 8)}`

  const mode = seed.length === 8 ? 'daily' : 'unlimited'
  const correct_guess = guess_history[guess_history.length - 1]
  const games = generateShareMessageGames(selected_games, game_list)

  let share_message = 'Wordle Hunter\n'
  share_message += mode === 'daily' ? `Daily - ${date}\n${games}\n\n` : `Unlimited - Seed: ${seed}\n${games}\n\n${correct_guess.guess.name}\n`

  const status_colors = [ '\u{1F7E2}', '\u{1F7E1}', '\u{1F534}']

  // iterate over the guess history
  // for each guess, add red, yellow or green based on the status of each property
  guess_history.forEach((guess) => {
    const result = guess.result
    const name = result.correct.status
    const type = result.type.status
    const suborder = result.suborder.status
    const games = result.game.status
    const elements = result.elements.status
    const statuses = result.statuses.status
    const weaknesses = result.weaknesses.status
    share_message += `${status_colors[name]}${status_colors[type]}${status_colors[suborder]}${status_colors[games]}${status_colors[elements]}${status_colors[statuses]}${status_colors[weaknesses]}\n`
  })

  navigator.clipboard.writeText(share_message)
}

function generateShareMessageGames(selected_games: GameList, game_list: GameList) {
  if (JSON.stringify(selected_games) === JSON.stringify(game_list)) {
    return 'All games'
  }

  const games = []
  for (const gen in selected_games) {
    if (selected_games[gen].length === game_list[gen].length) {
      games.push(gen.replace('gen', 'Gen ').replace('frontier', 'Frontier'))
      continue
    }
    selected_games[gen].forEach(game => games.push(game))
  }

  return games.join(', ')
}

export { formatMonsterInfoData, formatPropertyTitle, responseInfoTitle, submitGuess, responseInfoStyle, filterType, filterSuborder, filterGames, filterElements, filterStatuses, filterWeaknesses, shareResults }