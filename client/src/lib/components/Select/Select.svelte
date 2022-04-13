<script lang="ts">
  import type { SelectOption } from "src/definitions/selectOption";

  import RequiredMarker from "../RequiredMarker/RequiredMarker.svelte";
  export let label: string;
  export let id: string;
  export let name: string;
  export let options: SelectOption[];

  export let placeholder = "";
  export let hintText = "";
  export let required = false;
  export let error = "";
  export let value = "";
</script>

<div class="fr-select-group" class:fr-select-group--error={error}>
  <label class="fr-label" for={id}>
    {label}
    {#if required}
      <RequiredMarker />
    {/if}

    {#if hintText}
      <span class="fr-hint-text" id="description-desc-hint">
        {hintText}
      </span>
    {/if}
  </label>
  <select
    aria-describedby={error ? "select-error-desc-error" : ""}
    class="fr-select"
    class:fr-select--error={error}
    {required}
    bind:value
    {id}
    {name}
    on:change
    on:blur
  >
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
