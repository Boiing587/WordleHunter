<script setup lang="ts">
import WordleHunter from '../components/WordleHunter.vue'
import HowToPlay from '../components/HowToPlay.vue';
import DisclaimerItem from '../components/DisclaimerItem.vue'
</script>

<template>
  <main class="w-11/12">
    <WordleHunter />
    <HowToPlay page="game" />
    <DisclaimerItem />
  </main>
</template>