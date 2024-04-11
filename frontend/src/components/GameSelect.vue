<script setup lang="ts">
  import { ref } from 'vue';
  import { useRouter } from 'vue-router'
  import { useConfirm } from 'primevue/useconfirm'
  
  import Button from 'primevue/button'
  import ButtonGroup from 'primevue/buttongroup'
  import ConfirmDialog from 'primevue/confirmdialog'
  import Divider from 'primevue/divider'
  import MultiSelect from 'primevue/multiselect'
  import ToggleButton from 'primevue/togglebutton'

  import type { GameNames } from '@models/types'
  import type { Booleanish } from 'primevue/ts-helpers'
  
  import { getGameList, getDate } from '@methods/data'

  const router = useRouter()
  const confirm = useConfirm()

  localStorage.removeItem('seed')

  let game_list = ref<GameNames>()
  getGameList()
    .then((games) => {
      game_list.value = games
    })

  let game_selection = ref<GameNames>({gen1: [], gen2: [], gen3: [], gen4: [], gen5: [], frontier: []})

  function clearGameSelection(): void {
    game_selection.value = {gen1: [], gen2: [], gen3: [], gen4: [], gen5: [], frontier: []}
  }

  function selectAll(): void {
    if (game_list.value === undefined) { return }
    game_selection.value = game_list.value
  }

  function anyGamesSelected(): Booleanish {
    const flattened_selection: string[] = []
    for (const gen in game_selection.value) {
      game_selection.value[gen].forEach((game) => {
        flattened_selection.push(game.code)
      })
    }
    return !(flattened_selection.some(Boolean))
  }

  function submitGameSelection(mode: string): void {
    localStorage.setItem('game_selection', JSON.stringify(game_selection.value))
    localStorage.setItem('seed', getDate(mode))
    router.push('/play')
  }

  const casual_mode_enabled = localStorage.getItem('casual_mode') === "true" ? ref(true) : ref(false)
  function casualModeToggle(event: Event) {
    interface _Event {
      _value: boolean
    }
    const value: boolean = (event.currentTarget as unknown as _Event)._value
    if (!value) {
      confirm.require({
        message: "If you are new to the Monster Hunter franchise, or simply don't have a lot of intricate knowledge on monsters, you might want to try Casual mode.\n\nThis will remove monsters from the list of options when they cannot be correct based on your previous guesses.\n\nNOTE: This is not the intended way to play, and can in some cases make the game trivially easy.\nYou will be ineligible to gain any bragging rights by playing on Casual mode.",
        header: 'Enable Casual mode?',
        rejectClass: 'p-button-secondary p-button-outlined',
        rejectLabel: 'Cancel',
        acceptLabel: 'Enable',
        accept: () => {
          casual_mode_enabled.value = true
      localStorage.setItem('casual_mode', 'true')
        },
        reject: () => {
          casual_mode_enabled.value = false
      localStorage.setItem('casual_mode', 'false')
        }
      })
    } else {
      casual_mode_enabled.value = false
      localStorage.setItem('casual_mode', 'false')
    }
  }
</script>

<template>
  <div class="flex flex-col justify-center items-center">
    <div v-if="game_list" class="flex flex-row justify-evenly flex-wrap pb-6">
      <div v-for="(games, gen) in game_list" :key="gen" class="min-w-56 game-select-dropdown p-4 text-center">
        <h1 class="pb-4">{{ gen.toString().replace('gen', 'Generation ').replace('frontier', 'Frontier') }}</h1>
        <MultiSelect :id="gen" v-model="game_selection[gen]" :options="games" optionLabel="name" placeholder="Select games" :maxSelectedLabels="0" />
      </div>
    </div>
    <div v-else>
      Loading...
    </div>

    <Button :label="anyGamesSelected() ? 'Select all' : 'Clear all'" :onClick="anyGamesSelected() ? selectAll : clearGameSelection" />
    <Divider class="py-10" />

    <ConfirmDialog style="width: 50%;"></ConfirmDialog>
    <ToggleButton :model-value="casual_mode_enabled" off-label="Normal mode" on-label="Casual mode" @change="casualModeToggle" />
    <ButtonGroup class="p-4">
      <Button label="Daily" @click="submitGameSelection('daily')" :disabled="anyGamesSelected()" />
      <Button label="Unlimited" @click="submitGameSelection('unlimited')" :disabled="anyGamesSelected()" />
    </ButtonGroup>
  </div>
</template>

<style>
  .p-checkbox {
    margin-right: 10px;
  }

  .p-confirm-dialog-message {
    white-space: pre-line;
  }
</style>
