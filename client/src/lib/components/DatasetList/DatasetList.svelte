<script lang="ts">
  import type { Dataset } from "src/definitions/datasets";

  export let datasets: Dataset[];
</script>

<ul>
  {#each datasets as dataset (dataset.id)}
    <li>
      {dataset.title}
    </li>
  {/each}
</ul>
