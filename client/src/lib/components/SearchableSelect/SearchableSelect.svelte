<script lang="ts">
  import type { SelectOption } from "src/definitions/form";
  import { createEventDispatcher } from "svelte";
  import { clickOutside } from "src/lib/actions/clickOutside";

  export let buttonPlaceholder: string;
  export let inputPlaceholder: string;
  export let options: Array<SelectOption>;

  let macthedOptions: Array<SelectOption> = options;
  let isOverlayOpen = false;
  let buttonText = buttonPlaceholder;

  const openOverlay = () => {
    isOverlayOpen = true;
  };

  const closeOverlay = () => {
    macthedOptions = options;
    isOverlayOpen = false;
  };

  const handleOverlayOpening = () => {
    if (!isOverlayOpen) {
      openOverlay();
      return;
    }

    if (isOverlayOpen) {
      closeOverlay();
      return;
    }
  };

  const dispatch = createEventDispatcher<{
    clickItem: SelectOption | null;
  }>();

  const handleInput = (e: Event) => {
    const searchTerm = (e.target as HTMLInputElement).value;

    macthedOptions = options.filter((item) =>
      item.label.match(new RegExp(searchTerm, "i"))
    );
  };

  const handleClickListItem = (option: SelectOption) => {
    buttonText = option.label;
    dispatch("clickItem", option);
    closeOverlay();
  };

  const handleResetFilter = () => {
    macthedOptions = options;
    buttonText = buttonPlaceholder;
    dispatch("clickItem", null);
  };
</script>

<div class="container" use:clickOutside={{ callback: handleOverlayOpening }}>
  <button class="fr-select" on:click={handleOverlayOpening}>{buttonText}</button
  >

  {#if isOverlayOpen}
    <div class="overlay">
      <input
        placeholder={inputPlaceholder}
        class="fr-input"
        on:input={handleInput}
        type="search"
      />
      <ul>
        {#each macthedOptions as option}
          <li on:click={() => handleClickListItem(option)}>{option.label}</li>
        {/each}

        {#if macthedOptions.length > 0}
          <li on:click={handleResetFilter}>Réinitiliser le filtre</li>
        {/if}

        {#if macthedOptions.length === 0}
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
    width: 100%;
  }
  .overlay {
    padding: 10px;
    background-color: var(--grey-1000-75);
    box-shadow: 0 0 10px var(--grey-925);
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
