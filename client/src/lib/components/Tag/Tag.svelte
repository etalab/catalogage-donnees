<script lang="ts">
  import { createEventDispatcher } from "svelte";

  const dispatch = createEventDispatcher();

  export let name: string;

  let handleClickTag = () => {
    dispatch("select", name);
  };
</script>

<button class="fr-tag fr-tag--dismiss" on:click={handleClickTag}>{name}</button>
