<script lang="ts">
  import type { Tag as TagType } from "src/definitions/tag";
  import { transformTagToSelectOption } from "src/lib/transformers/form";
  import { createEventDispatcher } from "svelte";
  import Select from "../Select/Select.svelte";
  import Tag from "../Tag/Tag.svelte";

  export let tags: TagType[];
  export let name: string;
  export let id: string = name;
  export let error = "";
  export let selectedTags: TagType[] = [];

  $: tags = tags.sort((a, b) => a.name.localeCompare(b.name));

  const dispatch = createEventDispatcher<{ change: TagType[] }>();

  const handleChange = (e: FocusEvent) => {
    const target = e.target as HTMLInputElement;

    const tag = tags.find((item) => item.id === target.value);

    const tagHasBeenAlreadySelected = selectedTags.find(
      (item) => item.id === target.value
    );

    if (!tag || tagHasBeenAlreadySelected) return;

    selectedTags = [...selectedTags, tag];

    dispatch("change", selectedTags);
  };

  const handleSelectTag = (e: CustomEvent<TagType>) => {
    selectedTags = selectedTags.filter((item) => item.id !== e.detail.id);
    dispatch("change", selectedTags);
  };
</script>

<Select
  {error}
  on:change={handleChange}
  on:blur={handleChange}
  required
  label={"Mot-clés"}
  hintText={"Les mot-clés seront utilisés par les réutilisateurs pour affiner leur recherche. Sélectionnez ceux qui vous semblent les plus représentatifs de vos données."}
  {id}
  {name}
  placeholder="Rechercher un mot clé"
  options={tags.map(transformTagToSelectOption)}
/>

<div role="list">
  {#each selectedTags as { id, name }}
    <Tag role={"listitem"} on:click={handleSelectTag} {name} {id} />
  {/each}
</div>

<style>
  div[role="list"] {
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 10px;
  }
</style>
