<script lang="ts">
  import { page } from "$app/stores";
  import type { NavItem } from "src/definitions/navigation";

  export let items: NavItem[];

  $: path = $page.url.pathname;
</script>

<nav
  class="fr-nav"
  role="navigation"
  aria-label="Menu principal"
  id="header-navigation"
  data-fr-js-navigation="true"
>
  <ul class="fr-nav__list">
    {#each items as { label, href }}
      <li class="fr-nav__item" data-fr-js-navigaton-item="true">
        <a
          {href}
          class="fr-nav__link"
          target="_self"
          aria-current={href === path ? "page" : undefined}
        >
          {label}
        </a>
      </li>
    {/each}
  </ul>
</nav>
