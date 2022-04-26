<script lang="ts">
  import { createEventDispatcher } from "svelte";

  const dispatch = createEventDispatcher();
  type SelectOption = {
    label: string;
    value: string;
  };

  export let name: string;

  let searchTerm = "";

  export let id = `${name}-label`;
  export let options: Array<SelectOption> = [];

  let myInput: HTMLInputElement;

  const listName = `${name}-list`;

  const handleInput = (e: any) => {
    const selectedOption = options.find(
      (item) => item.label === e.target.value
    );

    if (selectedOption) {
      dispatch("search", selectedOption);
      myInput.value = "";
    }
  };
</script>

<div class="fr-select-group">
  <input
    role="search"
    class="fr-select"
    list={listName}
    {id}
    {name}
    bind:this={myInput}
    on:input|stopPropagation|preventDefault={handleInput}
  />

  <datalist id={listName}>
    {#each options as { label }}
      <option value={label} />
    {/each}
  </datalist>
</div>

<style>
  :global(input::-webkit-calendar-picker-indicator) {
    display: none !important;
  }
</style>
