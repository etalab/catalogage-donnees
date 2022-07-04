<script lang="ts">
  import type { SelectOption } from "src/definitions/form";
  import { clickOutside } from "src/lib/actions/clickOutside";
  import { slugify } from "src/lib/util/format";
  import { createEventDispatcher } from "svelte";
  export let buttonPlaceholder: string;
  export let inputPlaceholder: string;
  export let label: string;
  export let options: Array<SelectOption>;
  let macthedOptions: Array<SelectOption> = options;
  let isOverlayOpen = false;
  let buttonText = buttonPlaceholder;

  let searchTerm: string;
  $: macthedOptions = options.filter((item) =>
    item.label.match(new RegExp(searchTerm, "i"))
  );

  $: slug = slugify(label);

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
  const handleClickListItem = (option: SelectOption) => {
    buttonText = option.label;
    dispatch("clickItem", option);
    closeOverlay();
  };
  const handleResetFilter = () => {
    macthedOptions = options;
    buttonText = buttonPlaceholder;
    dispatch("clickItem", null);
    closeOverlay();
  };
</script>

<div use:clickOutside={{ callback: () => closeOverlay() }} class="container">
  <label data-testId={`${slug}-label`} id={`${slug}-label`} for={slug}
    >{label}</label
  >
  <button
    aria-labelledby={`${slug}-label`}
    class="fr-select"
    data-testId={`${slug}-button`}
    on:click={handleOverlayOpening}>{buttonText}</button
  >

  {#if isOverlayOpen}
    <div class="overlay">
      <input
        placeholder={inputPlaceholder}
        class="fr-input"
        bind:value={searchTerm}
        type="search"
      />

      <ul>
        {#if macthedOptions.length > 0}
          <li on:click={handleResetFilter}>Réinitialiser le filtre</li>
        {/if}

        {#each macthedOptions as option}
          <li on:click={() => handleClickListItem(option)}>{option.label}</li>
        {/each}

        {#if macthedOptions.length === 0}
          <li class="no-result">Aucun résultat trouvé</li>
        {/if}
      </ul>
    </div>
  {/if}
</div>

<style>
  button {
    text-align: left;
  }
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
