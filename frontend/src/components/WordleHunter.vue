<script setup lang="ts">
  import { ref, capitalize } from 'vue'
  import { useRouter } from 'vue-router'

  import Button from 'primevue/button'
  import Divider from 'primevue/divider'
  import Dropdown from 'primevue/dropdown'
  import ButtonGroup from 'primevue/buttongroup'

  import type { GameList, GuessResponse, Monster } from '@models/types'

  import { getMonsterList, formatGameSelection, generateSeed } from '@methods/data'
  import { formatMonsterInfoData, responseInfoStyle, responseInfoTitle, submitGuess, filterType, filterSuborder, filterGames, filterElements, filterStatuses, filterWeaknesses, shareResults } from '@methods/game'

  const router = useRouter()

  const num_guesses = ref<number>(0)
  const guessed_monster = ref<Monster>()
  const guess_response = ref<GuessResponse>()
  const guess_history = ref<GuessResponse[]>()
  const remove_property_state = ref<Boolean>(false)
  const ls_selected_games = localStorage.getItem('selected_games')
  const casual_mode_enabled = localStorage.getItem('casual_mode') === "true" ? ref(true) : ref(false)
  let seed = localStorage.getItem('seed')
  if (ls_selected_games === null || seed === null) {
    router.push('/')
  }
  const selected_games: GameList = formatGameSelection(JSON.parse(ls_selected_games as string))
  const game_list: GameList = formatGameSelection(JSON.parse(localStorage.getItem('game_list') as string))

  const monster_list = ref<Monster[]>()
  const error = ref<Boolean>(false)
  function loadMonsterList(): void {
    getMonsterList(selected_games)
      .then((monsters) => {
        monster_list.value = monsters.sort((a, b) => (a.name > b.name ? 1 : a.name < b.name ? -1 : 0))
      })
      .catch(() => { error.value = true })
  }
  loadMonsterList()

  function submit() {
    submitGuess((guessed_monster.value as Monster).name, selected_games, seed)
      .then((res) => {
        guess_response.value = res
        if (guess_history.value === undefined) { guess_history.value = [guess_response.value] }
        else { guess_history.value.push(guess_response.value) }

        if (casual_mode_enabled.value === true) {
          remove_property_state.value = guess_response.value.result.correct.status === 0 ? false : true
          // monster_list.value = casualModeFilter(monster_list.value as Monster[], guess_response.value)
        }
      })
    guessed_monster.value = undefined
    num_guesses.value++
  }

  function casualModeFilter(property: string) {
    switch (property) {
      case 'type':
        monster_list.value = filterType(monster_list.value as Monster[], guess_response.value as GuessResponse)
        break
      case 'suborder':
        monster_list.value = filterSuborder(monster_list.value as Monster[], guess_response.value as GuessResponse)
        break
      case 'games':
        monster_list.value = filterGames(monster_list.value as Monster[], guess_response.value as GuessResponse)
        break
      case 'elements':
        monster_list.value = filterElements(monster_list.value as Monster[], guess_response.value as GuessResponse)
        break
      case 'statuses':
        monster_list.value = filterStatuses(monster_list.value as Monster[], guess_response.value as GuessResponse)
        break
      case 'weaknesses':
        monster_list.value = filterWeaknesses(monster_list.value as Monster[], guess_response.value as GuessResponse)
        break
    }
    remove_property_state.value = false
  }

    function searchBarDisabled(): boolean {
      if (guess_response.value?.result.correct.status === 0) return true
      if (remove_property_state.value === true) return true
      return false
    }

  function guessButtonDisabled(): boolean {
    if (!guessed_monster.value) return true
    if (guess_response.value?.result.correct.status === 0) return true
    if (remove_property_state.value === true) return true
    return false
  }

  function replay(): void {
    seed = generateSeed('unlimited')
    localStorage.setItem('seed', seed)
    guessed_monster.value = undefined
    guess_response.value = undefined
    guess_history.value = undefined
    num_guesses.value = 0
    if (casual_mode_enabled.value === true) {
      loadMonsterList()
      remove_property_state.value = false
    }
  }

  function returnToGameSelection() {
    router.push('/')
  }

  async function shareButton() {
    shareResults(guess_history.value as GuessResponse[], selected_games, game_list)
    const shareButtonText = document.getElementById('shareButton')?.firstElementChild
    if (shareButtonText === null || shareButtonText === undefined) { return }
    shareButtonText.innerHTML = 'Copied to Clipboard!'
  }
</script>

<template>
  <div class="flex flex-col justify-center items-center">
    <div v-if="monster_list" class="flex flex-row justify-center items-center flex-wrap">
      <Dropdown v-model="guessed_monster" :options="monster_list" optionLabel="name" placeholder="Select a Monster" filter showClear class="m-2 min-w-64" :disabled="searchBarDisabled()" />
      <Button label="Guess!" :onClick="submit" :disabled="guessButtonDisabled()" class="m-2" />
    </div>
    <div v-else-if="error">
      <p>If you can see this, something has probably gone wrong. Please try again later.</p>
    </div>
    <div v-else>
      <p>Loading...</p>
    </div>
    <div v-if="casual_mode_enabled" class="flex flex-col justify-center items-center pt-2">
      <p>Select one property to filter after each guess!</p>
      <div class="flex flex-row">
        <Button class="mb-0 mt-4 mx-2 px-2 py-1" :disabled="!remove_property_state.valueOf()" @click="casualModeFilter('type')" >Type</Button>
        <Button class="mb-0 mt-4 mx-2 px-2 py-1" :disabled="!remove_property_state.valueOf()" @click="casualModeFilter('suborder')" >Suborder</Button>
        <Button class="mb-0 mt-4 mx-2 px-2 py-1" :disabled="!remove_property_state.valueOf()" @click="casualModeFilter('games')" >Games</Button>
        <Button class="mb-0 mt-4 mx-2 px-2 py-1" :disabled="!remove_property_state.valueOf()" @click="casualModeFilter('elements')" >Elements</Button>
        <Button class="mb-0 mt-4 mx-2 px-2 py-1" :disabled="!remove_property_state.valueOf()" @click="casualModeFilter('statuses')" >Statuses</Button>
        <Button class="mb-0 mt-4 mx-2 px-2 py-1" :disabled="!remove_property_state.valueOf()" @click="casualModeFilter('weaknesses')" >Weaknesses</Button>
      </div>
    </div>
  </div>
  
  <div v-if="guess_response?.result.correct.status === 0" class="flex flex-col justify-center items-center text-center">
    <Divider class="my-10" />
    <h1>{{ guess_response.guess.name }}</h1>
    <p class="pb-4">Congratulations! You successfully guessed today's monster in {{ num_guesses }} attempt(s)!</p>
    <ButtonGroup>
      <Button :label="(seed as string).length > 10 ? 'Play again!' : 'Play infinite mode!'" @click="replay()" />
      <Button label="Share your results!" id="shareButton" @click="shareButton" />
      <Button label="Return to game selection" :onClick="returnToGameSelection" />
    </ButtonGroup>
    
  </div>

  <div v-if="guess_history" class="flex flex-col-reverse justify-center items-center">
    <div v-for="guess in guess_history" :key="guess.guess.name" class="flex flex-row flex-wrap justify-center items-stretch p-4 guess" >
      <div v-for="(response_value, response_name) in guess.guess" :key="response_name" :title="responseInfoTitle(response_name, guess)" class="relative flex flex-col justify-center items-center p-4 my-4 min-w-20 border border-solid border-gray-600" :class="[`history_${response_name}`, responseInfoStyle(response_name, guess)]">
        <h1 class="absolute bottom-full">{{ capitalize(response_name) }}</h1>
        <div v-for="item in formatMonsterInfoData(response_name, response_value)" :id="response_name" :key="item">
          {{ item }}
        </div>
      </div>
    </div>
    <p class="pb-5">Hover over each property to get more information!</p>
    <Divider class="mt-10 mb-5" />
  </div>
</template>

<style>
@media only screen and (min-width: 1310px) {
  .history_name       { min-width: 14rem; }
  .history_type       { min-width: 9rem; }
  .history_suborder   { min-width: 8rem; }
  .history_games      { min-width: 6rem; }
  .history_elements,
  .history_weaknesses { min-width: 10rem; }
  .history_statuses   { min-width: 12rem; }
}

.response_status_0 {
  background-color: #006411;
}
.response_status_1 {
  background-color: #805e00;
}
.response_status_2 {
  background-color: #610000;
}
</style>