<script lang="ts" context="module">
  import type { Load } from "@sveltejs/kit";
  import { authGuard } from "$lib/auth/guard";

  export const load: Load = async ({ url }) => {
    return authGuard(url);
  };
</script>

<script lang="ts">
  import Header from "$lib/components/Header/Header.svelte";
  import Footer from "$lib/components/Footer/Footer.svelte";
  import { onMount } from "svelte";
  import "../app.css";
  import "../styles/dsfr-icon-extras.css";

  // DSFR Assets
  import appleTouchFavicon from "@gouvfr/dsfr/dist/favicon/apple-touch-icon.png";
  import svgFavicon from "@gouvfr/dsfr/dist/favicon/favicon.svg";
  import icoFavicon from "@gouvfr/dsfr/dist/favicon/favicon.ico";
  import manifest from "@gouvfr/dsfr/dist/favicon/manifest.webmanifest";

  onMount(async () => {
    // Load the DSFR asynchronously, and only on the browser (not in SSR).
    await import("@gouvfr/dsfr/dist/dsfr/dsfr.module.min.js");
  });
</script>

<svelte:head>
  <link rel="apple-touch-icon" href={appleTouchFavicon} />
  <!-- 180×180 -->
  <link rel="icon" href={svgFavicon} type="image/svg+xml" />
  <link rel="shortcut icon" href={icoFavicon} type="image/x-icon" />
  <!-- 32×32 -->
  <link rel="manifest" href={manifest} crossorigin="use-credentials" />
</svelte:head>

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
  <div class="fr-mb-8w">
    <slot />
  </div>
</main>

<Footer />
