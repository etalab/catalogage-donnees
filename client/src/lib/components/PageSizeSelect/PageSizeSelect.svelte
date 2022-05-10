<script lang="ts">
  export let value: number;

  const pageSizes = [1, 2, 3, 5, 10, 25, 50, 100];
</script>

<div class="fr-select-group">
  <label for="pageSize" class="fr-label"> Nombre d'éléments par page </label>

  <select name="pageSize" id="pageSize" class="fr-select" {value} on:change>
    {#each pageSizes as value}
      <option {value}>{value}</option>
    {/each}
  </select>
</div>
