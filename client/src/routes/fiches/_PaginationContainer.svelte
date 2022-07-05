<script lang="ts">
  import { page as pageStore } from "$app/stores";
  import Pagination from "src/lib/components/Pagination/Pagination.svelte";
  import { makePageParam } from "$lib/util/pagination";
  import { patchQueryString } from "$lib/util/urls";

  export let currentPage: number;
  export let totalPages: number;

  $: getPageLink = (page: number): string => {
    return patchQueryString($pageStore.url.searchParams, [makePageParam(page)]);
  };
</script>

<div class="pagination-container fr-mt-2w ">
  <Pagination {currentPage} {totalPages} {getPageLink} />
</div>

<style>
  .pagination-container {
    display: flex;
    justify-content: space-around;
  }
</style>
