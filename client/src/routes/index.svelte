<script context="module" lang="ts">
  export const prerender = true;
</script>

<script lang="ts">
  import { createForm } from "svelte-forms-lib";
  import * as yup from "yup";

  const postData = async (values) => {
    const data = JSON.stringify(values);
    const response = await fetch("http://127.0.0.1:3579/datasets/", {
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
</section>
