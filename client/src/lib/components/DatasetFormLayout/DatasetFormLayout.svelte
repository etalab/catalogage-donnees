<script>
  import { onMount } from "svelte";

  let segment = "";

  let container = undefined;
  let positions = undefined;
  let anchors = [];

  const handleScroll = () => {
    if (anchors === undefined || positions === undefined) return;

    if (window.innerHeight + window.pageYOffset >= document.body.offsetHeight) {
      // scrolled to bottom
      segment = anchors[anchors.length - 1].id;
      return;
    }

    const top = window.scrollY;

    let i = anchors.length;
    let lastId = undefined;
    while (i--) {
      if (positions[i] - top < 40) {
        const { id } = anchors[i];

        if (id !== lastId) {
          segment = id;
          lastId = id;
        }
        return;
      }
    }
  };

  const onresize = () => {
    const { top } = container.getBoundingClientRect();
    positions = [].map.call(anchors, (anchor) => {
      return anchor.getBoundingClientRect().top - top;
    });
  };

  onMount(() => {
    container.querySelectorAll("h2").forEach((anchor) => {
      if (anchor.id !== "") anchors.push(anchor);
    });
    onresize();
  });
</script>

<svelte:window on:scroll={handleScroll} on:resize={onresize} />

<section bind:this={container} class="fr-container">
  <div class="fr-grid-row fr-grid-row--gutters">
    <div class="fr-col-lg-3">
      <nav class="fr-sidemenu fr-sidemenu--sticky" aria-label="Menu latéral">
        <div class="fr-sidemenu__inner">
          <button
            class="fr-sidemenu__btn"
            hidden
            aria-controls="fr-sidemenu-wrapper"
            aria-expanded="false">Dans cette rubrique</button
          >
          <div class="fr-collapse" id="fr-sidemenu-wrapper">
            <ul class="fr-sidemenu__list">
              <li class="fr-sidemenu__item">
                <a
                  aria-current={segment === "information-generales" || !segment
                    ? "page"
                    : undefined}
                  class="fr-sidemenu__link"
                  href="#information-generales"
                  target="_self">Informations générales</a
                >
              </li>
              <li class="fr-sidemenu__item">
                <a
                  aria-current={segment === "source-formats"
                    ? "page"
                    : undefined}
                  class="fr-sidemenu__link"
                  href="#source-formats"
                  target="_self">Sources et formats</a
                >
              </li>
              <li class="fr-sidemenu__item">
                <a
                  aria-current={segment === "contacts" ? "page" : undefined}
                  class="fr-sidemenu__link"
                  href="#contacts"
                  target="_self">Contacts</a
                >
              </li>
              <li class="fr-sidemenu__item">
                <a
                  aria-current={segment === "mise-a-jour" ? "page" : undefined}
                  class="fr-sidemenu__link"
                  href="#mise-a-jour"
                  target="_self">Mise à jour</a
                >
              </li>
              <li class="fr-sidemenu__item">
                <a
                  aria-current={segment === "ouverture" ? "page" : undefined}
                  class="fr-sidemenu__link"
                  href="#ouverture"
                  target="_self">Ouverture</a
                >
              </li>
            </ul>
          </div>
        </div>
      </nav>
    </div>
    <div class="fr-col-lg-9">
      <slot />
    </div>
  </div>
</section>
