<script lang="ts">
  import Pagination from "src/lib/components/Pagination/Pagination.svelte";
  export let currentPage: number;
  export let totalPages: number;
  export let getPageLink: (page: number) => string;
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
