<script setup lang="ts">
  import { ref, capitalize } from 'vue'
  import { useRouter } from 'vue-router'

  import Button from 'primevue/button'
  import Divider from 'primevue/divider'
  import Dropdown from 'primevue/dropdown'
  import ButtonGroup from 'primevue/buttongroup'

  import type { GameList, GuessResponse, Monster } from '@models/types'

  import { getMonsterList, formatGameSelection, generateSeed } from '@methods/data'
  import { casualModeFilter, formatMonsterInfoData, responseInfoStyle, responseInfoTitle, guess } from '@methods/game'

  const router = useRouter()

  const num_guesses = ref<number>(0)
  const guessed_monster = ref<Monster>()
  const guess_response = ref<GuessResponse>()
  const guess_history = ref<GuessResponse[]>()
  const ls_game_selection = localStorage.getItem('game_selection')
  const casual_mode_enabled = localStorage.getItem('casual_mode') === "true" ? ref(true) : ref(false)
  let seed = localStorage.getItem('seed')
  if (ls_game_selection === null || seed === null) {
    router.push('/')
  }
  const game_selection: GameList = formatGameSelection(JSON.parse(ls_game_selection as string))

  const monster_list = ref<Monster[]>()
  const error = ref<Boolean>(false)
  function loadMonsterList(): void {
    getMonsterList(game_selection)
      .then((monsters) => {
        monster_list.value = monsters.sort((a, b) => (a.name > b.name ? 1 : a.name < b.name ? -1 : 0))
      })
      .catch(() => { error.value = true })
  }
  loadMonsterList()

  function submit() {
    guess((guessed_monster.value as Monster).name, game_selection, seed)
      .then((res) => {
        guess_response.value = res
        if (guess_history.value === undefined) { guess_history.value = [guess_response.value] }
        else { guess_history.value.push(guess_response.value) }

        if (casual_mode_enabled.value === true) {
          monster_list.value = casualModeFilter(monster_list.value as Monster[], guess_response.value)
        }
      })
    num_guesses.value++
  }

  function guessButtonDisabled(): boolean {
    if (!guessed_monster.value) return true
    if (guess_response.value?.result.correct.status === 0) return true
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
    }
  }

  function returnToGameSelection() {
    router.push('/')
  }
</script>

<template>
  <div class="flex flex-row justify-center items-center">
    <div v-if="monster_list" class="flex flex-row justify-center items-center flex-wrap">
      <Dropdown v-model="guessed_monster" :options="monster_list" optionLabel="name" placeholder="Select a Monster" filter showClear class="m-2 min-w-64" />
      <Button label="Guess!" :onClick="submit" :disabled="guessButtonDisabled()" class="m-2" />
    </div>
    <div v-else-if="error">
      <p>If you can see this, something has probably gone wrong. Please try again later.</p>
    </div>
    <div v-else>
      <p>Loading...</p>
    </div>
  </div>
  
  <div v-if="guess_response?.result.correct.status === 0" class="flex flex-col justify-center items-center text-center">
    <Divider class="py-10" />
    <h1>{{ guess_response.guess.name }}</h1>
    <p class="pb-4">Congratulations! You successfully guessed today's monster in {{ num_guesses }} attempt(s)!</p>
    <ButtonGroup>
      <Button :label="(seed as string).length > 10 ? 'Play again!' : 'Play infinite mode!'" @click="replay()" />
      <Button label="Return to game selection" :onClick="returnToGameSelection" />
    </ButtonGroup>
    
  </div>

  <div v-if="guess_history" class="flex flex-col-reverse justify-center items-center">
    <div v-for="guess in guess_history" :key="guess.guess.name" class="flex flex-row flex-wrap justify-center items-stretch p-4">
      <div v-for="(response_value, response_name) in guess.guess" :key="response_name" :title="responseInfoTitle(response_name, guess)" class="relative flex flex-col justify-center items-center p-4 my-4 min-w-20 border border-solid border-gray-600" :class="[`history_${response_name}`, responseInfoStyle(response_name, guess)]">
        <h1 class="absolute bottom-full">{{ capitalize(response_name) }}</h1>
        <div v-for="item in formatMonsterInfoData(response_name, response_value)" :id="response_name" :key="item">
          {{ item }}
        </div>
      </div>
    </div>
    <p class="pb-5">Hover over each property to get more information!</p>
    <Divider class="pt-10 pb-5" />
  </div>
</template>

<style>
.p-dropdown-clear-icon, .p-dropdown-filter-icon {
  top: 32% !important;
}

.m-2 {
  margin: .5rem !important;
}

.my-4{
  margin-top: 1rem !important;
  margin-bottom: 1rem !important;
}

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