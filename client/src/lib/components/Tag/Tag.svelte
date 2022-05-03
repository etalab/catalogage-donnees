<script lang="ts">
  import type { Tag } from "src/definitions/tag";

  import { createEventDispatcher } from "svelte";

  const dispatch = createEventDispatcher<{ click: Tag }>();

  export let name: string;
  export let id: string;
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
