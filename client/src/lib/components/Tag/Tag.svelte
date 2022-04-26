<script lang="ts">
  import { createEventDispatcher } from "svelte";

  const dispatch = createEventDispatcher();

  export let name: string;
  export let id: number | string;
  export let role = "listitem";

  let handleClickTag = () => {
    dispatch("click", { id, name });
  };
</script>

<button
  class="fr-tag fr-tag--dismiss"
  type="button"
  {role}
  on:click|preventDefault|stopPropagation={handleClickTag}
>
  {name}
</button>
