<script lang="ts">
  export let contactEmails: string[];
  let contactEmailErrors: string[] = [];

  const handleChange = (
    index: number,
    event: Event & {
      currentTarget: EventTarget & HTMLInputElement;
    }
  ) => {
    contactEmails[index] = event.currentTarget.value;
  };
  const removeContactEmail = (index: number) => {
    const filtered = contactEmails.filter((_, itemIndex) => {
      return index !== itemIndex;
    });

    contactEmails = filtered;
  };
  const addContactEmail = () => {
    contactEmails = [...contactEmails, ""];
  };
</script>

<ul class="fr-fieldset__content fr-raw-list  fr-mb-3w">
  {#if contactEmails.length === 0}
    <li class="contact-entries">
      <label for="contactEmail-input" id="contactEmail" hidden
        >Contact {0}</label
      >
      <input
        data-testid="contactEmail"
        aria-labelledby="contactEmail"
        id="contactEmail-input"
        class="fr-input fr-mr-1w"
        class:fr-input--error={contactEmailErrors[0]}
        type="email"
        on:change={(event) => handleChange(0, event)}
        on:blur={(event) => handleChange(0, event)}
      />
      <button
        type="button"
        class="fr-btn fr-btn--secondary fr-fi-delete-fill"
        title="Supprimer cet e-mail de contact"
        on:click|preventDefault={() => removeContactEmail(0)}
      />
    </li>
  {:else}
    {#each contactEmails as _, i}
      <li class="contact-entries">
        <label for="contactEmail" hidden>Contact {i}</label>
        <input
          data-testid="contactEmail"
          class="fr-input fr-mr-1w"
          class:fr-input--error={contactEmailErrors[i]}
          type="email"
          on:change={(event) => handleChange(i, event)}
          on:blur={(event) => handleChange(i, event)}
        />
        <button
          type="button"
          class="fr-btn fr-btn--secondary fr-fi-delete-fill"
          title="Supprimer cet e-mail de contact"
          on:click|preventDefault={() => removeContactEmail(i)}
        />
      </li>
    {/each}
  {/if}
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
    display: flex;
    margin: 8px 0;
  }
</style>
