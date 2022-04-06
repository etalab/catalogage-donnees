<script lang="ts">
  export let contactEmails: string[];
  let contactEmailErrors: string[] = [];

  const handleChange = (index) => {};
  const removeContactEmail = (index: number) => {};
  const addContactEmail = () => {};
</script>

<ul class="fr-fieldset__content fr-raw-list contact-entries fr-mb-3w">
  {#each contactEmails as _, i}
    <li role="presentation">
      <label for="contactEmails-{i}" hidden>Contact {i}</label>
      <input
        class="fr-input"
        class:fr-input--error={contactEmailErrors[i]}
        aria-describedby={contactEmailErrors[i]
          ? `contactEmails-${i}-desc-error`
          : null}
        type="email"
        id="contactEmails-{i}"
        name="contactEmails-{i}"
        on:change={() => handleChange(i)}
        on:blur={handleChange}
        bind:value={contactEmails[i]}
      />
      <button
        type="button"
        class="fr-btn fr-btn--secondary fr-fi-delete-fill"
        title="Supprimer cet e-mail de contact"
        on:click|preventDefault={() => removeContactEmail(i)}
      />
      {#if contactEmailErrors[i]}
        <p id="contactEmails-{i}-desc-error" class="fr-error-text">
          {contactEmailErrors[i]}
        </p>
      {/if}
    </li>
  {/each}
</ul>

<button
  type="button"
  class="fr-btn fr-btn--secondary fr-fi-edit-fill fr-btn--icon-left contact-entries-add"
  on:click|preventDefault={() => addContactEmail()}
>
  Ajouter un contact
</button>

<style>
  .contact-entries {
    display: grid;
    row-gap: 1em;
  }
  .contact-entries > * {
    display: grid;
    grid-template-columns: 1fr auto;
    column-gap: 1em;
  }
  .contact-entries-add {
    float: right;
  }
</style>
