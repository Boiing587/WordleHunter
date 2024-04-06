<script setup lang="ts">
import GameSelect from '../components/GameSelect.vue';
import HowToPlay from '../components/HowToPlay.vue';
import DisclaimerItem from '../components/DisclaimerItem.vue';
</script>

<template>
  <main class="w-11/12">
    <GameSelect />
    <HowToPlay page="game_select" />
    <DisclaimerItem />
  </main>
</template>
