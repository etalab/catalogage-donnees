<script lang="ts">
  import type { InputEvent } from "src/definitions/event";
  import { createEventDispatcher } from "svelte";

  const dispatch = createEventDispatcher();
  type SelectOption = {
    label: string;
    value: string;
  };

  export let label: string;
  export let name: string;
  const listName = `${name}-list`;
  const id = `${name}-label`;
  export let options: Array<SelectOption> = [];

  const handlInput = (e: InputEvent) => {
    const selectedOption = options.find(
      (item) => item.label === e.currentTarget.currentValue
    );

    if (selectedOption) {
      dispatch("search", selectedOption);
    }
  };
</script>

<div class="fr-select-group">
  <label class="fr-label" for={id}>{label}</label>

  <div class="select-search-input">
    <input
      role="search"
      class="fr-select"
      list={listName}
      {id}
      {name}
      on:input={handlInput}
    />

    <datalist id={listName}>
      {#each options as { label }}
        <option value={label} />
      {/each}
    </datalist>
  </div>
</div>
