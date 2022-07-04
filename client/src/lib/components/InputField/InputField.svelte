<script lang="ts">
  import RequiredMarker from "../RequiredMarker/RequiredMarker.svelte";
  import BlankWrapper from "./_BlankWrapper.svelte";
  import DateInputWrapper from "./_DateInputWrapper.svelte";

  export let tag = "input";
  export let name: string;
  export let type = "text";
  export let required = false;
  export let value: string | null;
  export let error = "";

  $: id = name;
  $: hintTextId = `${name}-desc-hint`;
  $: errorId = `${name}-desc-error`;
  $: wrapperComponent = type === "date" ? DateInputWrapper : BlankWrapper;
</script>

<div class="fr-input-group fr-mb-4w" class:fr-input-group--error={error}>
  <label class="fr-label" for={id}>
    <slot name="label" />
    {#if required}
      <RequiredMarker />
    {/if}
    {#if $$slots.hintText}
      <span class="fr-hint-text" id={hintTextId}>
        <slot name="hintText" />
      </span>
    {/if}
  </label>

  <svelte:component this={wrapperComponent}>
    <svelte:element
      this={tag}
      class="fr-input"
      class:fr-input--error={error}
      class:textarea-vertical={tag === "textarea"}
      aria-describedby={error ? errorId : undefined}
      {id}
      {name}
      type={tag === "input" ? type : undefined}
      {required}
      {value}
      on:input
      on:blur
    />
  </svelte:component>

  {#if error}
    <p id={errorId} class="fr-error-text">
      {error}
    </p>
  {/if}
</div>

<style>
  .textarea-vertical {
    resize: vertical;
  }
</style>
