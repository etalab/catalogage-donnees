<script lang="ts">
  import type { Dataset } from "src/definitions/datasets";
  import DatasetListItem from "../DatasetListItem/DatasetListItem.svelte";

  export let datasets: Dataset[];
</script>

<ul class="fr-raw-list">
  {#each datasets as dataset (dataset.id)}
    <DatasetListItem {dataset} />
  {/each}
</ul>
