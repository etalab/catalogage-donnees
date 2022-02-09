<script lang="ts">
  import Breadcrumbs from "$lib/components/Breadcrumbs/Breadcrumbs.svelte";
  import Header from "$lib/components/Header/Header.svelte";
  import Footer from "$lib/components/Footer/Footer.svelte";
  import { page } from "$app/stores";
  import "../app.css";
</script>

<div class="fr-skiplinks">
  <nav class="fr-container" role="navigation" aria-label="Accès rapide">
    <ul class="fr-skiplinks__list">
      <li>
        <a class="fr-nav__link" href="#contenu">Contenu</a>
      </li>
      <li>
        <a class="fr-nav__link" href="#header-navigation">Menu</a>
      </li>
      <li>
        <a class="fr-nav__link" href="#footer">Pied de page</a>
      </li>
    </ul>
  </nav>
</div>

<Header />

<main id="contenu" role="main">
  <div class="fr-container fr-mb-8w">
    <Breadcrumbs url={$page.url} />
    <div class="fr-grid-row fr-grid-row--center fr-grid-row--gutters">
      <slot />
    </div>
  </div>
</main>

<Footer />
