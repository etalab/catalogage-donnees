<script lang="ts">
  import { createEventDispatcher } from "svelte";
  export let triggerId: string;

  const dispatch = createEventDispatcher<{ cancel: void; save: void }>();
</script>

<dialog aria-labelledby="fr-modal-2-title" id={triggerId} class="fr-modal">
  <div class="fr-container fr-container--fluid fr-container-md">
    <div class="fr-grid-row fr-grid-row--center">
      <div class="fr-col-12 fr-col-md-8 fr-col-lg-6">
        <div class="fr-modal__body">
          <div class="fr-modal__header">
            <button class="fr-btn--close fr-btn" aria-controls="fr-modal-2"
              >Fermer</button
            >
          </div>
          <div class="fr-modal__content">
            <h1 id="fr-modal-2-title" class="fr-modal__title">
              <span
                class="fr-fi-arrow-right-line fr-fi--lg"
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
                <button class="fr-btn" on:click={() => dispatch("save")}>
                  Sauvgader et quitter
                </button>
              </li>
              <li>
                <button
                  on:click={() => dispatch("cancel")}
                  class="fr-btn  fr-btn--secondary"
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
