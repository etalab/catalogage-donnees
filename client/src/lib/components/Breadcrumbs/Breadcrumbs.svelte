<script lang="ts">
  export let url: URL;

  const capitalize = (str: string) => str[0].toUpperCase() + str.substring(1);

  type Crumb = { label: string; href: string };

  const makeCrumbs = (url: URL): Crumb[] => {
    // Remove zero-length tokens.
    const tokens = url.pathname
      .split("/")
      .filter((token: string) => token !== "");

    // Create { label, href } pairs for each token.
    let tokenPath = "";
    const crumbs: Crumb[] = tokens.map((token: string) => {
      tokenPath += "/" + token;
      return {
        label: capitalize(token),
        href: tokenPath,
      };
    });

    // Add a way to get home too.
    crumbs.unshift({ label: "Accueil", href: "/" });

    return crumbs;
  };

  $: crumbs = makeCrumbs(url);
</script>

<nav
  role="navigation"
  class="fr-breadcrumb"
  aria-label="vous êtes ici :"
  data-fr-js-breadcrumb="true"
>
  <button
    class="fr-breadcrumb__button"
    aria-expanded="false"
    aria-controls="breadcrumb"
    data-fr-js-collapse-button="true">Voir le fil d’Ariane</button
  >
  <div class="fr-collapse" id="breadcrumb" data-fr-js-collapse="true">
    <ol class="fr-breadcrumb__list">
      <!-- Display the parent pages, except current page -->
      {#each crumbs.slice(0, -1) as { label, href }}
        <li class="fr-breadcrumb__item">
          <a {href} class="fr-breadcrumb__link">{label}</a>
        </li>
      {/each}

      <!-- Display the current page-->
      <li>
        <a class="fr-breadcrumb__link" aria-current="page" href="#">
          {crumbs[crumbs.length - 1].label}
        </a>
      </li>
    </ol>
  </div>
</nav>
