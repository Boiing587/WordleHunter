<script lang='ts'>
  import { Badge, MultiSelect } from 'flowbite-svelte';

  import type { Games, GameSelection } from '../interfaces/Games';

  import { getGameList, formatGameSelection } from '../functions/games';
  import { importImage } from '../functions/images';

  let game_list: Promise<Games> = getGameList()
  let game_selection: GameSelection = {gen1: [], gen2: [], gen3: [], gen4: [], gen5: [], frontier: []}
  function test() { console.log(game_selection) }

  // TODO select all in generation
</script>

<div class="flex flex-col w-full">
  {#await game_list then fetchedData}
    {#each Object.entries(fetchedData) as [gen, games]}
      <div class="flex flex-col p-4">
        {#await formatGameSelection(games) then formatted_games}
          <h2>{gen.replace('gen', 'Generation ').replace('frontier', 'Frontier')}</h2>
          <MultiSelect items={formatted_games} bind:value={game_selection[gen]} let:item let:clear>
            <Badge color='dark' dismissable params={{ duration: 100 }} on:close={clear} border>
              {#await importImage(item.value) then logo}
                <img src={logo} alt="" class="min-h-24 max-h-24"/>
              {/await}
            </Badge>
          </MultiSelect>
        {/await}
      </div>
    {/each}
  {/await}
</div>

<button on:click={test}>Test</button>