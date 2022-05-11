<script lang="ts">
  import type { GetPageLink } from "src/definitions/pagination";
  import { Pager } from "$lib/util/pagination";

  export let currentPage: number;
  export let totalPages: number;
  export let getPageLink: GetPageLink;

  $: pager = new Pager({ currentPage, totalPages, numSiblings: 2 });
</script>

<nav role="navigation" class="fr-pagination" aria-label="Pagination">
  <ul class="fr-pagination__list" data-testid="pagination-list">
    <li>
      <a
        class="fr-pagination__link fr-pagination__link--first"
        href={pager.hasPrevious ? getPageLink(pager.firstPage) : undefined}
        aria-disabled={!pager.hasPrevious ? true : undefined}
        title="Première page"
      >
        Première page
      </a>
    </li>

    <li>
      <a
        class="fr-pagination__link fr-pagination__link--prev fr-pagination__link--lg-label"
        href={pager.hasPrevious ? getPageLink(pager.previousPage) : undefined}
        aria-disabled={!pager.hasPrevious ? true : undefined}
        title="Page précédente"
      >
        Page précédente
      </a>
    </li>

    {#if pager.hasFirstPageLandmark}
      <li>
        <a
          class="fr-pagination__link"
          title="Page {pager.firstPage}"
          href={getPageLink(pager.firstPage)}
        >
          {pager.firstPage}
        </a>
      </li>
    {/if}

    {#if pager.hasLeftTruncature}
      <li data-testid="left-truncature">
        <a class="fr-pagination__link fr-displayed-lg"> ... </a>
      </li>
    {/if}

    {#each pager.windowPages as page}
      <li>
        <a
          class="fr-pagination__link"
          class:fr-displayed-lg={page > pager.firstPage &&
            page != currentPage &&
            page < pager.lastPage}
          title="Page {page}"
          aria-current={page === currentPage ? "page" : undefined}
          href={page === currentPage ? undefined : getPageLink(page)}
        >
          {page}
        </a>
      </li>
    {/each}

    {#if pager.hasRightTruncature}
      <li data-testid="right-truncature">
        <a class="fr-pagination__link fr-displayed-lg"> ... </a>
      </li>
    {/if}

    {#if pager.hasLastPageLandmark}
      <li>
        <a
          class="fr-pagination__link"
          title="Page {pager.lastPage}"
          href={getPageLink(pager.lastPage)}
        >
          {pager.lastPage}
        </a>
      </li>
    {/if}

    <li>
      <a
        class="fr-pagination__link fr-pagination__link--next fr-pagination__link--lg-label"
        href={pager.hasNext ? getPageLink(pager.nextPage) : undefined}
        aria-disabled={!pager.hasNext ? true : undefined}
        title="Page suivante"
      >
        Page suivante
      </a>
    </li>

    <li>
      <a
        class="fr-pagination__link fr-pagination__link--last"
        href={pager.hasNext ? getPageLink(pager.lastPage) : undefined}
        aria-disabled={!pager.hasNext ? true : undefined}
        title="Dernière page"
      >
        Dernière page
      </a>
    </li>
  </ul>
</nav>
