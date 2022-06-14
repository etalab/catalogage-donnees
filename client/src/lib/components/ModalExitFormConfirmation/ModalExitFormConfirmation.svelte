<script lang="ts">
  import { createEventDispatcher } from "svelte";

  import Modal from "../GenericModal/GenericModal.svelte";

  export let controlId: string;

  const dispatch = createEventDispatcher<{ save: void; cancel: void }>();
</script>

<Modal {controlId}>
  <div slot="modal-content">
    <h1 id="{controlId}-title" class="fr-modal__title">
      <span
        class="fr-icon-error-warning-fill fr-fi--md fr-text-default--error"
        aria-hidden="true"
      />
      Vos modifications n’ont pas eté sauvegardées
    </h1>
    <p>
      Si vous quittez l’édition de cette fiche vos modifications ne seront pas
      sauvegardées. Est-ce vraiment ce que vous souhaitez ?
    </p>
  </div>

  <div slot="modal-footer" class="fr-modal__footer">
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
          on:click={() => dispatch("cancel")}
          aria-controls={controlId}
          class="fr-btn fr-btn--secondary"
        >
          Ne pas sauvegarder
        </button>
      </li>
    </ul>
  </div>
</Modal>
