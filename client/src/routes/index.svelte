<script context="module" lang="ts">
  export const prerender = true;
</script>

<script lang="ts">
  import { createForm } from "svelte-forms-lib";
  import * as yup from "yup";
  import { getApiUrl } from "$lib/fetch";

  const postData = async (values) => {
    const data = JSON.stringify(values);
    const url = `${getApiUrl()}/datasets/`;
    const response = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: data,
    });
    await new Promise((r) => setTimeout(r, 1000)); // TODO: remove, just for debugging purposes
    return await response.json();
  };

  const { form, errors, handleChange, handleSubmit, isSubmitting } = createForm(
    {
      initialValues: {
        title: "",
        description: "",
      },
      validationSchema: yup.object().shape({
        title: yup.string().required(),
        description: yup.string().required(),
      }),
      onSubmit: (values) => {
        const result = postData(values);
        console.log(result);
        return result;
      },
    }
  );
</script>

<section>
  <form on:submit={handleSubmit}>
    <label for="title">
      Nom du jeu de données. Exemple : "Arbres vivants inventoriés en forêt"
    </label>
    <input
      id="title"
      name="title"
      on:change={handleChange}
      on:blur={handleChange}
      bind:value={$form.title}
    />
    {#if $errors.title}
      <small>{$errors.title}</small>
    {/if}

    <label for="description">
      Présentation du jeu de données. Exemple : "Données brutes de l'inventaire
      forestier correspondant à l'ensemble des données collectées en forêt sur
      le territoire métropolitain par les agents forestiers de terrain de l'IGN.
      Ces données portent sur les caractéristiques des placettes d'inventaire,
      les mesures et observations sur les arbres et les données
      éco-floristiques. Les coordonnées géographiques des placettes sont
      fournies au kilomètre près."
    </label>
    <textarea
      id="description"
      name="description"
      on:change={handleChange}
      on:blur={handleChange}
      bind:value={$form.description}
    />
    {#if $errors.description}
      <small>{$errors.description}</small>
    {/if}

    <button type="submit">
      {#if $isSubmitting}loading...{:else}submit{/if}
    </button>
  </form>

  <div class="fr-col fr-col-lg-8">
    <h1>Exemple de formulaire</h1>

    <div role="alert" class="fr-alert fr-alert--info">
      <p class="fr-alert__title">Information</p>
      <p>On peut afficher des messages d'informations ou d'alerte.</p>
    </div>
    <form action="/" method="POST" data-bitwarden-watching="1">
      <fieldset class="fr-fieldset fr-my-4w">
        <legend class="fr-fieldset__legend" id="text-legend">Champs</legend>
        <div class="fr-input-group">
          <label class="fr-label" for="text-input-text">Texte</label>
          <input
            class="fr-input"
            type="text"
            id="text-input-text"
            name="text-input-text"
          />
        </div>

        <div class="fr-input-group">
          <label class="fr-label" for="text-input-number">Nombre </label>
          <input
            class="fr-input"
            pattern="[0-9]*"
            inputmode="numeric"
            type="number"
            id="text-input-number"
            name="text-input-number"
          />
        </div>

        <div class="fr-input-group">
          <label class="fr-label" for="text-input-calendar">Date </label>
          <div class="fr-input-wrap fr-fi-calendar-line">
            <input
              class="fr-input"
              type="date"
              id="text-input-calendar"
              name="text-input-calendar"
            />
          </div>
        </div>
        <div class="fr-input-group">
          <label class="fr-label" for="text-input-password"
            >Mot de passe :
          </label>
          <input
            class="fr-input"
            type="password"
            id="text-input-password"
            name="text-input-password"
          />
        </div>
        <div class="fr-input-group">
          <label class="fr-label" for="textarea">Texte long : </label>
          <textarea class="fr-input" id="textarea" name="textarea" />
        </div>
      </fieldset>

      <fieldset class="fr-fieldset fr-my-4w">
        <legend class="fr-fieldset__legend" id="text-legend">Champs</legend>
        <div class="fr-upload-group">
          <label class="fr-label" for="file-upload"
            >Ajouter des fichiers
            <span class="fr-hint-text"
              >Taille maximale : 500 Mo. Formats supportés : jpg, png, pdf.
              Plusieurs fichiers possibles. Lorem ipsum dolor sit amet,
              consectetur adipiscing.</span
            >
          </label>
          <input
            class="fr-upload"
            type="file"
            id="file-upload"
            name="file-upload"
          />
        </div>
      </fieldset>

      <fieldset class="fr-fieldset fr-my-4w">
        <legend class="fr-fieldset__legend" id="text-legend">Liste</legend>

        <div class="fr-input-group">
          <div class="fr-select-group">
            <label class="fr-label" for="select-hint"
              >Liste déroulante
              <span class="fr-hint-text" id="select-hint-desc-hint"
                >Texte de description additionnel</span
              >
            </label>
            <select class="fr-select" id="select-hint" name="select-hint">
              <option value="" selected="" disabled="" hidden=""
                >Selectionnez une option</option
              >
              <option value="1">Option 1</option>
              <option value="2">Option 2</option>
              <option value="3">Option 3</option>
              <option value="4">Option 4</option>
            </select>
          </div>
        </div>
      </fieldset>

      <div class="fr-form-group">
        <fieldset class="fr-fieldset">
          <legend
            class="fr-fieldset__legend fr-text--regular"
            id="radio-legend"
          >
            Légende pour l’ensemble de champs
          </legend>
          <div class="fr-fieldset__content">
            <div class="fr-radio-group">
              <input type="radio" id="radio-1" name="radio" />
              <label class="fr-label" for="radio-1">Label radio </label>
            </div>
            <div class="fr-radio-group">
              <input type="radio" id="radio-2" name="radio" />
              <label class="fr-label" for="radio-2">Label radio </label>
            </div>
            <div class="fr-radio-group">
              <input type="radio" id="radio-3" name="radio" />
              <label class="fr-label" for="radio-3">Label radio </label>
            </div>
          </div>
        </fieldset>
      </div>

      <div class="fr-form-group">
        <fieldset class="fr-fieldset" role="group">
          <legend
            class="fr-fieldset__legend fr-text--regular"
            id="checkboxes-hint-legend"
          >
            Légende pour l’ensemble de champs
            <span class="fr-hint-text" id="checkboxes-hint-desc-hint"
              >Texte de description additionnel</span
            >
          </legend>
          <div class="fr-fieldset__content">
            <div class="fr-checkbox-group">
              <input
                type="checkbox"
                id="checkboxes-hint-1"
                name="checkboxes-hint-1"
              />
              <label class="fr-label" for="checkboxes-hint-1"
                >Label checkbox
              </label>
            </div>
            <div class="fr-checkbox-group">
              <input
                type="checkbox"
                id="checkboxes-hint-2"
                name="checkboxes-hint-2"
              />
              <label class="fr-label" for="checkboxes-hint-2"
                >Label checkbox
              </label>
            </div>
            <div class="fr-checkbox-group">
              <input
                type="checkbox"
                id="checkboxes-hint-3"
                name="checkboxes-hint-3"
              />
              <label class="fr-label" for="checkboxes-hint-3"
                >Label checkbox
              </label>
            </div>
          </div>
        </fieldset>
      </div>

      <div class="fr-input-group fr-my-4w">
        <button type="submit" class="fr-btn" title="Réserver ma conférence"
          >Valider ce formulaire</button
        >
        <button
          type=""
          class="fr-btn fr-btn--secondary"
          title="Réserver ma conférence">Annuler</button
        >
      </div>
    </form>
  </div>
</section>
