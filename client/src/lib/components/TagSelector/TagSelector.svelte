<script lang="ts">
  import type { SelectOption } from "src/definitions/form";
  import type { Tag as TagType } from "src/definitions/tag";
  import { transformTagToSelectOption } from "src/lib/transformers/form";
  import { createEventDispatcher } from "svelte";
  import Search from "../Search/Search.svelte";
  import Tag from "../Tag/Tag.svelte";

  export let tags: TagType[];
  export let name: string;
  export let id: string = name;

  export let selectedTags: TagType[] = [];

  const dispatch = createEventDispatcher<{ change: TagType[] }>();

  const handleSearch = (e: CustomEvent<SelectOption>) => {
    const tag = tags.find((item) => item.id === e.detail.value);

    const tagHasBeenAlreadySelected = selectedTags.find(
      (item) => item.id === e.detail.value
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

<Search
  on:search={handleSearch}
  {id}
  {name}
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
