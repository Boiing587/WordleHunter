<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

import Accordion from 'primevue/accordion'
import AccordionTab from 'primevue/accordiontab'

import Button from 'primevue/button'
import ButtonGroup from 'primevue/buttongroup'

import Divider from 'primevue/divider'
import Dropdown from 'primevue/dropdown'

import type { GameList, GuessResponse, Monster } from '@models/types'

import { apiFetch, getMonsterList, formatGameSelection, generateSeed, getIcon } from '@methods/data'
import {
  responseInfoStyle,
  responseInfoTitle,
  submitGuess,
  filterType,
  filterSuborder,
  filterGames,
  filterElements,
  filterStatuses,
  filterWeaknesses,
  shareResults
} from '@methods/game'

const router = useRouter()

const num_guesses = ref<number>(0)
const guessed_monster = ref<Monster>()
const guess_response = ref<GuessResponse>()
const guess_history = ref<GuessResponse[]>()
const remove_property_state = ref<Boolean>(false)
const ls_selected_games = localStorage.getItem('selected_games')
const casual_mode_enabled = localStorage.getItem('casual_mode') === 'true' ? ref(true) : ref(false)
let seed = localStorage.getItem('seed')
if (ls_selected_games === null || seed === null) {
  router.push('/')
}
const selected_games: GameList = formatGameSelection(JSON.parse(ls_selected_games as string))
const game_list: GameList = formatGameSelection(
  JSON.parse(localStorage.getItem('game_list') as string)
)

const hint1_text = ref<String>('')
const hint2_text = ref<String>('')
const hint1_guesses_required = 5
const hint2_guesses_required = 10
const hint1_used = ref<Boolean>(false)
const hint2_used = ref<Boolean>(false)

async function getHint(hint_num: number) {
  const url = `api/data/hint?seed=${seed}&hint_num=${hint_num}`
  const headers = { 'Content-Type': 'application/json' }
  const body = JSON.stringify(selected_games)
  const res: { hint: string } = await apiFetch(url, 'POST', headers, body)

  if (hint_num === 1) {
    hint1_used.value = true
    hint1_text.value = res.hint
  } else if (hint_num === 2) {
    hint2_used.value = true
    hint2_text.value = res.hint
  }

  return res.hint
}

const monster_list = ref<Monster[]>()
const error = ref<Boolean>(false)
function loadMonsterList(): void {
  getMonsterList(selected_games)
    .then((monsters) => {
      monster_list.value = monsters.sort((a, b) => (a.name > b.name ? 1 : a.name < b.name ? -1 : 0))
    })
    .catch(() => {
      error.value = true
    })
}
loadMonsterList()

function submit() {
  submitGuess((guessed_monster.value as Monster).name, selected_games, seed).then((res) => {
    guess_response.value = res
    if (guess_history.value === undefined) {
      guess_history.value = [guess_response.value]
    } else {
      guess_history.value.push(guess_response.value)
    }

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
      monster_list.value = filterType(
        monster_list.value as Monster[],
        guess_response.value as GuessResponse
      )
      break
    case 'suborder':
      monster_list.value = filterSuborder(
        monster_list.value as Monster[],
        guess_response.value as GuessResponse
      )
      break
    case 'games':
      monster_list.value = filterGames(
        monster_list.value as Monster[],
        guess_response.value as GuessResponse
      )
      break
    case 'elements':
      monster_list.value = filterElements(
        monster_list.value as Monster[],
        guess_response.value as GuessResponse
      )
      break
    case 'statuses':
      monster_list.value = filterStatuses(
        monster_list.value as Monster[],
        guess_response.value as GuessResponse
      )
      break
    case 'weaknesses':
      monster_list.value = filterWeaknesses(
        monster_list.value as Monster[],
        guess_response.value as GuessResponse
      )
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
  hint1_used.value = false
  hint2_used.value = false
  hint1_text.value = ''
  hint2_text.value = ''
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
  if (shareButtonText === null || shareButtonText === undefined) {
    return
  }
  shareButtonText.innerHTML = 'Copied to Clipboard!'
}
</script>

<template>
  <div class="flex flex-col justify-center items-center">
    <div v-if="monster_list" class="flex flex-row justify-center items-center flex-wrap">
      <Dropdown
        v-model="guessed_monster"
        :options="monster_list"
        optionLabel="name"
        placeholder="Select a Monster"
        filter
        showClear
        class="m-2 min-w-64"
        :disabled="searchBarDisabled()"
      >
        <template #value="slotProps">
          <div v-if="slotProps.value" class="flex flex-row items-center">
            <img :src="getIcon('monsters', slotProps.value.name)" class="max-w-6 max-h-6 mr-2" />
            <div>{{ slotProps.value.name }}</div>
          </div>
        </template>
        <template #option="slotProps">
          <div class="flex flex-row items-center">
            <img :src="getIcon('monsters', slotProps.option.name)" class="max-w-6 max-h-6 mr-2" />
            <div>{{ slotProps.option.name }}</div>
          </div>
        </template>
      </Dropdown>
      <ButtonGroup>
        <Button label="Guess!" :onClick="submit" :disabled="guessButtonDisabled()" />
        <Button
          v-if="num_guesses >= hint1_guesses_required - 2 && !hint1_used"
          v-show="num_guesses >= hint1_guesses_required - 2 && !hint1_used"
          :disabled="num_guesses < hint1_guesses_required"
          @click="getHint(1)"
        >
          Hint: {{ Math.min(num_guesses, hint1_guesses_required) }} /
          {{ hint1_guesses_required }}
        </Button>
        <Button
          v-if="num_guesses >= hint2_guesses_required - 2 && !hint2_used"
          :disabled="num_guesses < hint2_guesses_required"
          @click="getHint(2)"
        >
          Hint: {{ Math.min(num_guesses, hint2_guesses_required) }} /
          {{ hint2_guesses_required }}
        </Button>
      </ButtonGroup>
    </div>
    <div v-else-if="error">
      <p>If you can see this, something has probably gone wrong. Please try again later.</p>
    </div>
    <div v-else>
      <p>Loading...</p>
    </div>
    <Accordion v-show="hint1_used || hint2_used" :activeIndex="0">
      <AccordionTab header="Hints">
        <div v-show="hint1_used" class="p-1">
          {{ hint1_text != 'None' ? `Alias: ${hint1_text}` : 'This monster has no official alias' }}
        </div>
        <div v-show="hint2_used" class="p-1">
          {{ hint2_text != '' ? hint2_text : 'This monster has no official description' }}
        </div>
      </AccordionTab>
    </Accordion>
    <div v-if="casual_mode_enabled" class="flex flex-col justify-center items-center pt-2">
      <p>Select one property to filter after each guess!</p>
      <div class="flex flex-row">
        <Button
          class="mb-0 mt-4 mx-2 px-2 py-1"
          :disabled="!remove_property_state.valueOf()"
          @click="casualModeFilter('type')"
          >Type</Button
        >
        <Button
          class="mb-0 mt-4 mx-2 px-2 py-1"
          :disabled="!remove_property_state.valueOf()"
          @click="casualModeFilter('suborder')"
          >Suborder</Button
        >
        <Button
          class="mb-0 mt-4 mx-2 px-2 py-1"
          :disabled="!remove_property_state.valueOf()"
          @click="casualModeFilter('games')"
          >Games</Button
        >
        <Button
          class="mb-0 mt-4 mx-2 px-2 py-1"
          :disabled="!remove_property_state.valueOf()"
          @click="casualModeFilter('elements')"
          >Elements</Button
        >
        <Button
          class="mb-0 mt-4 mx-2 px-2 py-1"
          :disabled="!remove_property_state.valueOf()"
          @click="casualModeFilter('statuses')"
          >Statuses</Button
        >
        <Button
          class="mb-0 mt-4 mx-2 px-2 py-1"
          :disabled="!remove_property_state.valueOf()"
          @click="casualModeFilter('weaknesses')"
          >Weaknesses</Button
        >
      </div>
    </div>
  </div>

  <div
    v-if="guess_response?.result.correct.status === 0"
    class="flex flex-col justify-center items-center text-center"
  >
    <Divider class="my-10" />
    <h1>{{ guess_response.guess.name }}</h1>
    <p class="pb-4">
      Congratulations! You successfully guessed today's monster in {{ num_guesses }} attempt(s)!
    </p>
    <ButtonGroup>
      <Button
        :label="(seed as string).length > 10 ? 'Play again!' : 'Play infinite mode!'"
        @click="replay()"
      />
      <Button label="Share your results!" id="shareButton" @click="shareButton" />
      <Button label="Return to game selection" :onClick="returnToGameSelection" />
    </ButtonGroup>
  </div>

  <div
    v-if="guess_history"
    class="flex flex-col-reverse justify-center items-center cursor-default"
  >
    <div
      v-for="guess in guess_history"
      :key="guess.guess.name"
      class="flex flex-row justify-center items-stretch p-4 w-full text-center guess"
    >
      <div
        :title="responseInfoTitle('name', guess)"
        class="relative flex flex-col justify-center items-center p-4 my-4 min-w-20 border border-solid border-gray-600"
        :class="[`history_name`, responseInfoStyle('name', guess)]"
      >
        <h1 class="absolute bottom-full">Name</h1>
        <div class="flex flex-row items-center">
          <img :src="getIcon('monsters', guess.guess.name)" class="w-6 h-6 mr-2" />
          {{ guess.guess.name }}
        </div>
      </div>

      <div
        :title="responseInfoTitle('type', guess)"
        class="relative flex flex-col justify-center items-center p-4 my-4 min-w-20 border border-solid border-gray-600"
        :class="[`history_type`, responseInfoStyle('type', guess)]"
      >
        <h1 class="absolute bottom-full">Type</h1>
        <div>{{ guess.guess.type }}</div>
      </div>

      <div
        :title="responseInfoTitle('suborder', guess)"
        class="relative flex flex-col justify-center items-center p-4 my-4 min-w-20 border border-solid border-gray-600"
        :class="[`history_suborder`, responseInfoStyle('suborder', guess)]"
      >
        <h1 class="absolute bottom-full">Suborder</h1>
        <div>{{ guess.guess.suborder }}</div>
      </div>

      <div
        :title="responseInfoTitle('games', guess)"
        class="relative flex flex-col justify-center items-center p-4 my-4 min-w-20 border border-solid border-gray-600"
        :class="[`history_games`, responseInfoStyle('games', guess)]"
      >
        <h1 class="absolute bottom-full">Games</h1>
        <div v-if="guess.guess.games.length <= 5" class="text-center">
          <div v-for="game in guess.guess.games" :key="game">{{ game }}</div>
        </div>
        <div v-else class="text-center">
          {{ guess.guess.games[0] }}
          <div :title="guess.guess.games.join('\n')" class="cursor-pointer">
            {{ guess.guess.games.length }} games*
          </div>
        </div>
      </div>

      <div
        :title="responseInfoTitle('elements', guess)"
        class="relative flex flex-col justify-center items-center p-4 my-4 min-w-20 border border-solid border-gray-600"
        :class="[`history_elements`, responseInfoStyle('elements', guess)]"
      >
        <h1 class="absolute bottom-full">Elements</h1>
        <div v-if="guess.guess.elements.length == 0">None</div>
        <div v-else title="">
          <div
            v-for="element in guess.guess.elements"
            :key="element.name"
            class="flex flex-row"
            :class="element.note ? 'cursor-pointer' : ''"
            :title="element.note"
          >
            <img :src="getIcon('attributes', element.name)" class="mr-2 h-5 w-auto" />
            {{ element.name }}{{ element.note ? '*' : '' }}
          </div>
        </div>
      </div>

      <div
        :title="responseInfoTitle('statuses', guess)"
        class="relative flex flex-col justify-center items-center p-4 my-4 min-w-20 border border-solid border-gray-600"
        :class="[`history_statuses`, responseInfoStyle('statuses', guess)]"
      >
        <h1 class="absolute bottom-full">Statuses</h1>
        <div v-if="guess.guess.statuses.length == 0">None</div>
        <div v-else title="">
          <div
            v-for="status in guess.guess.statuses"
            :key="status.name"
            class="flex flex-row"
            :class="status.note ? 'cursor-pointer' : ''"
            :title="status.note"
          >
            <img :src="getIcon('attributes', status.name)" class="mr-2 h-5 w-auto" />
            {{ status.name }}{{ status.note ? '*' : '' }}
          </div>
        </div>
      </div>

      <div
        :title="responseInfoTitle('weaknesses', guess)"
        class="relative flex flex-col justify-center items-center p-4 my-4 min-w-20 border border-solid border-gray-600"
        :class="[`history_weaknesses`, responseInfoStyle('weaknesses', guess)]"
      >
        <h1 class="absolute bottom-full">Weaknesses</h1>
        <div v-if="guess.guess.weaknesses.length == 0">None</div>
        <div v-else title="">
          <div
            v-for="weakness in guess.guess.weaknesses"
            :key="weakness.name"
            class="flex flex-row"
            :class="weakness.note ? 'cursor-pointer' : ''"
            :title="weakness.note"
          >
            <img :src="getIcon('attributes', weakness.name)" class="mr-2 h-5 w-auto" />
            {{ weakness.name }}{{ weakness.note ? '*' : '' }}
          </div>
        </div>
      </div>
    </div>
    <p class="pb-5">Hover over text with asterisks (*) for more specific information.</p>
    <p>Hover over each property to get more information about your guess.</p>
    <Divider class="mt-10 mb-5" />
  </div>
</template>

<style>
@media only screen and (min-width: 1310px) {
  .history_name {
    min-width: 15%;
  }
  .history_type {
    min-width: 10%;
  }
  .history_suborder {
    min-width: 10%;
  }
  .history_games {
    min-width: 20%;
  }
  .history_elements,
  .history_weaknesses {
    min-width: 15%;
  }
  .history_statuses {
    min-width: 15%;
  }
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

@keyframes hint_appear {
  from {
    right: -100%;
  }
}
.hint {
  animation: hint_appear 0.5s ease-out;
}

.p-accordion {
  width: 60%;
}

.p-accordion .p-accordion-header .p-accordion-header-link:not(:hover),
.p-accordion-content {
  background: none;
}

.p-accordion-header a {
  padding: 8px;
  svg {
    margin-left: 8px;
  }
  span {
    margin-left: 8px;
  }
}
</style>
