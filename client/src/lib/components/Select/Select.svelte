<script lang="ts">
  import type { SelectOption } from "src/definitions/selectOption";

  import RequiredMarker from "../RequiredMarker/RequiredMarker.svelte";
  export let label: string;
  export let id: string;
  export let name: string;
  export let options: SelectOption[];

  export let placeholder: string = "";
  export let required: boolean = false;
  export let error: string = "";
  export let value: string = "";
</script>

<div class="fr-select-group">
  <label class="fr-label" for={id}>
    {label}
    {#if required}
      <RequiredMarker />
    {/if}
  </label>
  <select class="fr-select" {required} bind:value {id} {name} on:change on:blur>
    {#if placeholder}
      <option value="" selected>{placeholder}</option>
    {/if}

    {#each options as { id, value, label }}
      <option {id} {value}>{label}</option>
    {/each}
  </select>

  {#if error}
    <p id="title-desc-error" class="fr-error-text">
      {error}
    </p>
  {/if}
</div>
