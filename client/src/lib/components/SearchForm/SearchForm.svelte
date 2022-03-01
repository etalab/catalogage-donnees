<script lang="ts">
  import { createEventDispatcher } from "svelte";

  export let size: "default" | "lg" = "default";
  export let value = "";
  export let placeholder = "Rechercher";

  const dispatch = createEventDispatcher<{ submit: string }>();

  const onSubmit = () => dispatch("submit", value);
</script>

<form
  class="fr-search-bar {size === 'lg' ? 'fr-search-bar--lg' : ''}"
  role="search"
  on:submit|preventDefault={onSubmit}
>
  <label for="q" class="fr-label">Rechercher</label>
  <input type="search" class="fr-input" name="q" bind:value {placeholder} />
  <button type="submit" class="fr-btn"> Rechercher </button>
</form>
