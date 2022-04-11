<script lang="ts">
  export let contactEmails: string[] = [""];
  export let errors: string[] = [];
  export let onChange: (event: Event) => any;

  const add = () => {
    contactEmails = contactEmails.concat("");
    errors = errors.concat("");
  };

  const remove = (i: number) => {
    contactEmails = contactEmails.filter((_, itemIndex) => {
      return i !== itemIndex;
    });
    errors = errors.filter((u, j) => j !== i);
  };
</script>

<fieldset class="fr-fieldset fr-my-4w" aria-labelledby="contactEmails-legend">
  <legend
    class="fr-fieldset__legend fr-text--regular"
    id="contactEmails-legend"
  >
    E-mail(s) de contact
    <span class="fr-hint-text" id="contactEmails-desc-hint">
      Vous pouvez ajouter des adresses e-mail personnelles en complément
      l'dresse fonctionnelle. Ces emails seront régulièrement vérifiés afin
      d'assurer la bonne maintenabilité des jeux de données.
    </span>
  </legend>

  <ul class="fr-fieldset__content fr-raw-list  fr-mb-3w">
    {#each contactEmails as _, i}
      <li>
        <div class="contact-entries">
          <label for="contactEmails-{i}" hidden>Contact {i}</label>
          <input
            class="fr-input"
            class:fr-input--error={errors[i]}
            aria-describedby={errors[i]
              ? `contactEmails-${i}-desc-error`
              : null}
            type="email"
            id="contactEmails-{i}"
            data-testid="contactEmails"
            placeholder="email"
            name={`contactEmails[${i}]`}
            on:change={onChange}
            on:blur={onChange}
            bind:value={contactEmails[i]}
          />
          <button
            type="button"
            class="fr-btn fr-btn--secondary fr-fi-delete-fill"
            title="Supprimer cet e-mail de contact"
            on:click|preventDefault={() => remove(i)}
          />
        </div>

        {#if errors[i]}
          <p id="entrypoint-email-desc-error" class="fr-error-text">
            {errors[i]}
          </p>
        {/if}
      </li>
    {/each}
  </ul>

  <button
    type="button"
    class="fr-btn fr-btn--secondary fr-fi-edit-fill fr-btn--icon-left contact-entries-add"
    on:click|preventDefault={() => add()}
  >
    Ajouter un contact
  </button>
</fieldset>

<style>
  .contact-entries {
    display: flex;
    margin: 8px 0;
  }
</style>
