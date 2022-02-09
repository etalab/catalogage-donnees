<script lang="ts">
  import { navigationItems } from "src/lib/helpers/navigation";

  import HeaderNav from "../HeaderNav/HeaderNav.svelte";
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

      <HeaderNav items={navigationItems} />
    </div>
  </div>
</header>
