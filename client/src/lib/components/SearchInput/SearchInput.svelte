<script lang="ts">
  import type { SelectOption } from "src/definitions/form";

  import { createEventDispatcher } from "svelte";

  const dispatch = createEventDispatcher<{ search: SelectOption }>();

  export let name: string;
  export let id = name;
  export let options: Array<SelectOption> = [];
  export let placeholder = "";

  let searchInput: HTMLInputElement;

  const listName = `${name}-list`;

  let selectedOption: SelectOption | undefined;

  const handleInput = (e: any) => {
    const foundOption = options.find((item) => item.label === e.target.value);

    if (foundOption) {
      selectedOption = foundOption;
    }
  };

  const handleKeypress = (e: KeyboardEvent) => {
    if (e.key === "Enter") {
      e.preventDefault();
    }

    if (selectedOption && e.key === "Enter") {
      dispatch("search", selectedOption);
      searchInput.value = "";
      selectedOption = undefined;
    }
  };
</script>

<div class="fr-input-group">
  <input
    role="search"
    autocomplete="off"
    class="fr-input"
    {placeholder}
    list={listName}
    {id}
    {name}
    on:keypress={handleKeypress}
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

  input:focus::placeholder {
    color: transparent;
  }
</style>
