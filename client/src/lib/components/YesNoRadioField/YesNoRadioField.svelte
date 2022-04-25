<script lang="ts">
  import { createEventDispatcher } from "svelte";
  import RequiredMarker from "../RequiredMarker/RequiredMarker.svelte";

  export let name: string;
  export let value: boolean;
  export let required = false;
  export let error = "";

  const dispatch = createEventDispatcher<{ change: boolean }>();

  const onChange = (event: Event): void => {
    const { value } = event.target as HTMLInputElement;
    dispatch("change", value === "true" ? true : false);
  };
</script>

<fieldset
  class="fr-fieldset fr-fieldset--inline fr-my-4w"
  class:fr-fieldset--error={error}
  aria-describedby={error ? "{name}-desc-error" : null}
>
  <legend class="fr-fieldset__legend fr-text--regular" id="{name}-legend">
    <slot name="label" />
    {#if required}
      <RequiredMarker />
    {/if}
  </legend>

  <div class="fr-fieldset__content">
    <div class="fr-radio-group">
      <input
        type="radio"
        id="{name}-true"
        {name}
        value={true}
        checked={value === true}
        {required}
        on:blur={onChange}
        on:change={onChange}
      />
      <label for="{name}-true"> Oui </label>
    </div>

    <div class="fr-radio-group">
      <input
        type="radio"
        id="{name}-false"
        {name}
        value={false}
        checked={value === false}
        {required}
        on:blur={onChange}
        on:change={onChange}
      />
      <label for="{name}-false"> Non </label>
    </div>
  </div>

  {#if error}
    <p id="{name}-desc-error" class="fr-error-text">
      {error}
    </p>
  {/if}
</fieldset>
