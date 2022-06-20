<script lang="ts">
  import type { SelectOption } from "src/definitions/form";
  import { createEventDispatcher } from "svelte";

  export let buttonPlaceholder: string;
  export let inputPlaceholder: string;
  export let options: Array<SelectOption>;

  let filteredOptions: Array<SelectOption> = options;
  let displayOptions = false;

  const dispatch = createEventDispatcher<{
    clickItem: SelectOption;
  }>();

  const handleInput = (e: Event) => {
    const searchTerm = (e.target as HTMLInputElement).value;

    filteredOptions = options.filter((item) => item.label.match(searchTerm));
  };

  const handleClickListItem = (option: SelectOption) => {
    buttonPlaceholder = option.label;

    dispatch("clickItem", option);
  };
</script>

<div class="container">
  <button class="fr-select" on:click={() => (displayOptions = !displayOptions)}
    >{buttonPlaceholder}</button
  >

  {#if displayOptions}
    <div class="overlay">
      <input
        placeholder={inputPlaceholder}
        class="fr-input"
        on:input={handleInput}
        type="search"
      />
      <ul>
        {#each filteredOptions as option}
          <li on:click={() => handleClickListItem(option)}>{option.label}</li>
        {/each}

        {#if filteredOptions.length === 0}
          <li class="no-result">Aucun résultat trouvé</li>
        {/if}
      </ul>
    </div>
  {/if}
</div>

<style>
  .container {
    position: relative;
    box-sizing: border-box;
  }
  .overlay {
    padding: 10px;
    background-color: var(--grey-1000-75);
    box-shadow: 0 0 10px var(--grey-925);
    position: absolute;
    z-index: 10;
    width: 100%;
    max-height: 32vh;
    overflow: scroll;
    position: absolute;
    border: 1px solid var(--background-contrast-grey);
  }

  input {
    margin: 0;
    margin-top: 5px;
  }

  ul {
    list-style-type: none;
    padding: 0;
    margin: 0;
  }

  li {
    cursor: pointer;
    padding: 8px 16px;
    margin: 0;
    border-top: 1px solid var(--background-contrast-grey);
  }

  li:hover {
    background-color: var(--background-contrast-grey);
  }

  .no-result {
    cursor: not-allowed;
  }
</style>
