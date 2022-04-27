<script lang="ts">
  import type { SelectOption } from "src/definitions/form";

  import { createEventDispatcher } from "svelte";

  const dispatch = createEventDispatcher<{ search: SelectOption }>();

  export let name: string;
  export let id = `${name}-label`;
  export let options: Array<SelectOption> = [];

  let searchInput: HTMLInputElement;

  const listName = `${name}-list`;

  const handleInput = (e: any) => {
    const selectedOption = options.find(
      (item) => item.label === e.target.value
    );

    if (selectedOption) {
      dispatch("search", selectedOption);
      searchInput.value = "";
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
    bind:this={searchInput}
    on:input|stopPropagation|preventDefault={handleInput}
  />

  <datalist id={listName}>
    {#each options as { label }}
      <option value={label} />
    {/each}
  </datalist>
</div>

<style>
  /* See https://stackoverflow.com/questions/20937475/remove-datalist-dropdown-arrow-in-chrome */
  :global(input::-webkit-calendar-picker-indicator) {
    display: none !important;
  }
</style>
