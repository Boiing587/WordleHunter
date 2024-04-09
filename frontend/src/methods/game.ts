import type { GameList, GuessResponse, Proximity, Monster } from "@models/types";

const dev = false
const base_url = !dev ? "https://wordlehunter-api.azurewebsites.net" : "http://localhost:5000"

async function guess(guess: string, game_selection: GameList, seed: string | null = null) {
  const body = {
    guess: guess,
    games: game_selection,
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

function casualModeFilter(monster_list: Monster[], response: GuessResponse) {
  const guess = response.guess
  const result = response.result
  // Type
  switch (result.type.status) {
    case 0:
      monster_list = monster_list.filter(monster => monster.type === guess.type)
      break

    case 2:
      monster_list = monster_list.filter(monster => monster.type !== guess.type)
      break
  }

  // Suborder
  const suborder_category = result.suborder.hint ? result.suborder.hint.split('- ').slice(1) : null
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

  // Games
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

  // Elements
  const common_elements = result.elements.hint ? result.elements.hint.split('- ').slice(1) : null
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

  // Statuses
  const common_statuses = result.statuses.hint ? result.statuses.hint.split('- ').slice(1) : null
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


  // Weaknesses
  const common_weaknesses = result.weaknesses.hint ? result.weaknesses.hint.split('- ').slice(1) : null
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

export { formatMonsterInfoData, formatPropertyTitle, responseInfoTitle, guess, responseInfoStyle, casualModeFilter }