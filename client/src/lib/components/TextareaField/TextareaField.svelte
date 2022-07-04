<script lang="ts">
  import RequiredMarker from "../RequiredMarker/RequiredMarker.svelte";

  export let name: string;
  export let label: string;
  export let hintText = "";
  export let required = false;
  export let value: string | null;
  export let error = "";

  $: id = name;
  $: hintTextId = `${name}-desc-hint`;
  $: errorId = `${name}-desc-error`;
</script>

<div class="fr-input-group fr-mb-4w" class:fr-input-group--error={error}>
  <label class="fr-label" for={id}>
    {label}
    {#if required}
      <RequiredMarker />
    {/if}
    {#if hintText}
      <span class="fr-hint-text" id={hintTextId}>
        {hintText}
      </span>
    {/if}
  </label>

  <textarea
    class="fr-input"
    class:fr-input--error={error}
    aria-describedby={error ? errorId : undefined}
    {id}
    {name}
    {required}
    {value}
    on:input
    on:blur
  />

  {#if error}
    <p id={errorId} class="fr-error-text">
      {error}
    </p>
  {/if}
</div>

<style>
  textarea {
    resize: vertical;
  }
</style>
