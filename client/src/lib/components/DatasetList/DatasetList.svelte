<script lang="ts">
  import type { Dataset } from "src/definitions/datasets";
  import DatasetListItem from "../DatasetListItem/DatasetListItem.svelte";

  export let datasets: Dataset[];
</script>

<ul>
  {#each datasets as dataset, index (dataset.id)}
    {@const lastChild = index === datasets.length - 1}
    <DatasetListItem {dataset} />
    {#if !lastChild}
      <hr />
    {/if}
  {/each}
</ul>

<style>
  ul {
    list-style-type: none;
    margin: 0;
    padding: 0;
  }
</style>
