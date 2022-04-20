<script lang="ts">
  import { createEventDispatcher } from "svelte";

  export let size: "default" | "lg" = "default";
  export let labelId = "";
  export let value = "";
  export let placeholder = "Rechercher";

  const dispatch = createEventDispatcher<{ search: string }>();

  const handleSearch = () => {
    dispatch("search", value);
  };
</script>

<div
  class="fr-search-bar {size === 'lg' ? 'fr-search-bar--lg' : ''}"
  role="search"
>
  <label for="q" id={labelId} class="fr-label">Rechercher</label>
  <input type="search" class="fr-input" name="q" bind:value {placeholder} />
  <button on:click={handleSearch} class="fr-btn"> Rechercher </button>
</div>
