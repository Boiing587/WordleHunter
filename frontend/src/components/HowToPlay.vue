<script setup lang="ts">
import { ref } from 'vue'

import Button from 'primevue/button'
import Divider from 'primevue/divider'
import DataTable from 'primevue/datatable'
import Dialog from 'primevue/dialog'
import Column from 'primevue/column'

defineProps({page: {type: String, default: ''}})

const color_codes = ref([
  {
    'name': 'The monster is incorrect',
    'type': 'The monster is a different type (flying wyvern, elder dragon, etc.)',
    'suborder': 'The monster is in a different suborder category',
    'games': 'The monster was introduced in another generation',
    'elements': 'The monster uses different elements',
    'statuses': 'The monster uses different statuses',
    'weaknesses': 'The monster has different weaknesses'
  },
  {
    'name': 'The monster is related to your guess',
    'type': '',
    'suborder': 'The monster is in the same suborder category (hover over the property for more information)',
    'games': 'The monster was introduced in the same generation, but not the same game',
    'elements': 'The monster shares some elements with your guess (hover for more information)',
    'statuses': 'The monster shares some statuses with your guess (hover)',
    'weaknesses': 'The monster shares some weaknesses with your guess (hover)'
  },
  {
    'name': 'You guessed the correct monster!',
    'type': 'The monster is the same type',
    'suborder': 'The monster is the same suborder',
    'games': 'The monster was introduced in the same game',
    'elements': 'The monster uses the exact same elements',
    'weaknesses': 'The monster uses the exact same statuses',
    'statuses': 'The monster has the exact same weaknesses'
  }
])
const howToPlayVisible = ref(false)
function dialogVisibilityHandler (value: boolean) {
  if (!value) { howToPlayVisible.value = false }
}
</script>

<template>
  <div v-if="page == 'game_select'" class="flex flex-col justify-center items-center text-center py-4">
    <p>Choose your selection of games to get started!</p>
    <Divider class="my-10" />
    <p>Please keep in mind, I am <strong>not</strong> a frontend developer.</p>
    <p>I do this for fun, and even though I want to learn, I much prefer backend.</p>
    <p>I will likely work on the appearance of this site over time, but please do not expect this to look very much better than it already is.</p>
    <p>Thank you!</p>
  </div>

  <div v-else-if="page == 'game'" class="flex flex-col justify-center items-center">
    <Divider class="my-10" />
    <p>Never tried this game before?</p>
    <p class="pb-4">Or maybe you just need a refresher?</p>
    <Button label="How to play!" @click="howToPlayVisible = true" />
    <Dialog :visible="howToPlayVisible" modal dismissable-mask @update:visible="dialogVisibilityHandler" :style="{width: '90%'}">
      <div class="paragraph">
        <header>How to play:</header>
        <p>Your objective is to guess the monster that's been randomly chosen from a list of monsters.</p>
        <p>The list contains all monsters that are <strong>present in any of the games you selected</strong>, not just those first introduced in those games.</p>
        <p><strong>For example:</strong> no matter what selection of games you choose, Rathalos will still be on the list, as he is present in every game, even though he was introduced in Monster Hunter 1.</p>
        <p>To get started, make a guess for any monster in the list!</p>
      </div>
      <div class="paragraph flex flex-col justify-center items-center">
        <header>What am I looking at?</header>
        <p>Once you make a guess, it will appear in the history above, with information on how close or far away you are.</p>
        <p class="pb-4">Let's break down the information!</p>
        <p>In broad terms, the response you receive to your guess is color coded into three possible categories:</p>
        <p><span class="text-red-600">Red: Incorrect</span> | <span class="text-yellow-500">Yellow: Partially correct</span> | <span class="text-green-400">Green: Correct</span></p>
        <p>Descriptions of each property's color code are as follows:</p>
        <DataTable :value="color_codes" class="py-10" size="small">
          <Column field="name" header="Name" />
          <Column field="type" header="Type" />
          <Column field="suborder" header="Suborder" />
          <Column field="games" header="Games" />
          <Column field="elements" header="Elements" />
          <Column field="statuses" header="Statuses" />
          <Column field="weaknesses" header="Weaknesses" />
        </DataTable>
        <p>Maybe that was a lot to take in at once. Let's look at an example:</p>
        <p><strong>(In this example we assume that Rathalos is today's monster of the day)</strong></p>
        <figure class="pb-6">
          <img src="../assets/howtoplay_ex1.png">
          <figcaption>
            While this guess is <em>completely</em> wrong, it can still be helpful. Look at it this way:<br>
            If you know it's not a brute wyvern, and that it has at least one element, you can narrow down what <strong>not</strong> to guess for next time.
          </figcaption>
        </figure>
        <figure class="pb-6">
          <img src="../assets/howtoplay_ex2.png">
          <figcaption>
            We've narrowed it down even further! Now we know it's a fire-elemental flying wyvern that was not introduced in any 5th gen title.<br>
            <strong>TIP!</strong> You can hover over the individual information boxes to read more information. In this case, we can hover over the "Weaknesses" box to see what elemental weaknesses they share.
          </figcaption>
        </figure>
        <figure class="pb-6">
          <img src="../assets/howtoplay_ex3.png">
          <figcaption>
            This is a bit of a hailmary attempt, but it reveals some very useful information, the "Name" property is now partially correct!<br>
            This means that the monster we guessed is related to the correct monster. And since we previously figured out that the correct monster is a base species...
          </figcaption>
        </figure>
        <figure>
          <img src="../assets/howtoplay_ex4.png">
          <figcaption>Bingo!</figcaption>
        </figure>
      </div>
    </Dialog>
  </div>
  <Divider class="my-10" />
</template>

<style>
header {
  font-weight: bold;
  padding-bottom: 1rem;
}

figure {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.paragraph {
  padding-bottom: 4rem;
  text-align: center;
}

table * {
  font-size: 15px;
  background-color: unset;
}


thead * {
  color: var(--color-text) !important;
}

tr:nth-child(1) * {
  color: rgb(220, 38, 38);
}
tr:nth-child(2) * {
  color: rgb(234, 179, 8);
}
tr:nth-child(3) * {
  color: rgb(74, 222, 128);
}
</style>
