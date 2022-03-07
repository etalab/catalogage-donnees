<script lang="ts">
  import { goto } from "$app/navigation";
  import { page } from "$app/stores";
  import { isLoggedIn, logout } from "$lib/stores/auth";

  type NavItem = {
    label: string;
    href: string;
  };

  const navigationItems: NavItem[] = [
    {
      label: "Rechercher",
      href: "/fiches/search",
    },
    {
      label: "Contribuer",
      href: "/contribuer",
    },
    {
      label: "Mon espace",
      href: "#",
    },
  ];

  $: path = $page.url.pathname;

  const onClickLogout = async () => {
    logout();
    await goto("/login");
  };
</script>

<header role="banner" class="fr-header">
  <div class="fr-header__body">
    <div class="fr-container">
      <div class="fr-header__body-row">
        <div class="fr-header__brand fr-enlarge-link">
          <div class="fr-header__brand-top">
            <div class="fr-header__logo">
              <p class="fr-logo">
                Catalogage
                <br />des
                <br />données
              </p>
            </div>
            <div class="fr-header__navbar">
              <button
                class="fr-btn--menu fr-btn"
                data-fr-opened="false"
                aria-controls="modal-menu"
                aria-haspopup="menu"
                title="Menu"
                id="fr-btn-menu-mobile"
              >
                Menu
              </button>
            </div>
          </div>
          <div class="fr-header__service">
            <a href="/" title="Accueil - Catalogage des données">
              <p class="fr-header__service-title">Catalogage des données</p>
            </a>
            <p class="fr-header__service-tagline">
              Un outil pour cataloguer les jeux de données des différents
              ministères
            </p>
          </div>
        </div>
        <div class="fr-header__tools">
          <div class="fr-header__tools-links">
            <ul class="fr-links-group">
              <li>
                <a href="/" class="fr-link" title="Accéder aux réglages">
                  Réglages
                </a>
              </li>
              <li>
                {#if $isLoggedIn}
                  <button class="fr-link" on:click={onClickLogout}>
                    Déconnexion
                  </button>
                {:else}
                  <a href="/login" class="fr-link" title="Se connecter">
                    Se connecter
                  </a>
                {/if}
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div
    class="fr-header__menu fr-modal"
    id="modal-menu"
    data-fr-js-modal="true"
    data-fr-js-header-modal="true"
  >
    <div class="fr-container">
      <button
        class="fr-link--close fr-link"
        aria-controls="modal-menu"
        data-fr-js-modal-button="true">Fermer</button
      >

      <div class="fr-header__menu-links" />

      {#if $isLoggedIn}
        <nav
          class="fr-nav"
          role="navigation"
          aria-label="Menu principal"
          id="header-navigation"
          data-fr-js-navigation="true"
        >
          <ul class="fr-nav__list">
            {#each navigationItems as { label, href }}
              <li class="fr-nav__item" data-fr-js-navigaton-item="true">
                <a
                  {href}
                  class="fr-nav__link"
                  aria-current={href === path ? "page" : undefined}
                >
                  {label}
                </a>
              </li>
            {/each}
          </ul>
        </nav>
      {/if}
    </div>
  </div>
</header>
