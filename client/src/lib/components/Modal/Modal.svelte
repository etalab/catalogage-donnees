<script lang="ts">
  export let triggerId: string;

  import { createEventDispatcher } from "svelte";

  const dispatch = createEventDispatcher<{ save: void }>();
</script>

<dialog
  aria-labelledby="{triggerId}-title"
  id={triggerId}
  class="fr-modal"
  role="dialog"
>
  <div class="fr-container fr-container--fluid fr-container-md">
    <div class="fr-grid-row fr-grid-row--center">
      <div class="fr-col-12 fr-col-md-8 fr-col-lg-6">
        <div class="fr-modal__body">
          <div class="fr-modal__header">
            <button class="fr-btn--close fr-btn" aria-controls={triggerId}
              >Fermer</button
            >
          </div>
          <div class="fr-modal__content">
            <h1 id="{triggerId}-title" class="fr-modal__title">
              <span
                class="fr-icon-error-warning-fill fr-fi--md fr-text-default--error"
                aria-hidden="true"
              />
              Vos modifications n’ont pas eté sauvegardées
            </h1>
            <p>
              Si vous quittez l’édition de cette fiche vos modifications ne
              seront pas sauvegardées. Est-ce vraiment ce que vous souhaitez ?
            </p>
          </div>
          <div class="fr-modal__footer">
            <ul
              class="fr-btns-group fr-btns-group--right fr-btns-group--inline-reverse fr-btns-group--inline-lg fr-btns-group--icon-left"
            >
              <li>
                <button on:click={() => dispatch("save")} class="fr-btn">
                  Sauvegarder et quitter
                </button>
              </li>
              <li>
                <button
                  aria-controls={triggerId}
                  class="fr-btn fr-btn--secondary"
                >
                  Ne pas sauvegarder
                </button>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</dialog>
