<script lang="ts">
  import { onMount } from "svelte";
  import { getPageY } from "$lib/util/html";

  type Anchor = {
    element: HTMLElement;
    id: string;
    label: string;
    y: number;
  };

  let slotContent: HTMLElement;
  let anchors: Anchor[] = [];
  let activeAnchorId = "";
  // Make anchor active when it passes below this fraction of the screen.
  const triggerFraction = 1 / 4;

  const handleScroll = () => {
    const hasReachedBottom =
      window.pageYOffset + window.innerHeight >= document.body.offsetHeight;

    if (hasReachedBottom) {
      activeAnchorId = anchors[anchors.length - 1].id;
      return;
    }

    const triggerY = window.pageYOffset + window.innerHeight * triggerFraction;

    const anchorsBelowTrigger = anchors.filter((anchor) => anchor.y < triggerY);

    if (anchorsBelowTrigger.length > 0) {
      activeAnchorId = anchorsBelowTrigger[anchorsBelowTrigger.length - 1].id;
    }
  };

  const onresize = () =>
    anchors.forEach((anchor) => (anchor.y = getPageY(anchor.element)));

  onMount(() => {
    slotContent.querySelectorAll<HTMLElement>("h2[id]").forEach((element) => {
      const anchor = {
        element,
        id: element.id,
        label: element.textContent!,
        y: getPageY(element),
      };
      anchors = [...anchors, anchor];
    });

    activeAnchorId = anchors[0].id;
  });
</script>

<svelte:window on:scroll={handleScroll} on:resize={onresize} />

<section class="fr-container">
  <div class="fr-grid-row fr-grid-row--gutters">
    <div class="fr-col-md-3">
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
              {#each anchors as anchor}
                <li class="fr-sidemenu__item">
                  <a
                    aria-current={anchor.id === activeAnchorId
                      ? "page"
                      : undefined}
                    class="fr-sidemenu__link"
                    href="#{anchor.id}"
                    target="_self"
                  >
                    {anchor.label}
                  </a>
                </li>
              {/each}
            </ul>
          </div>
        </div>
      </nav>
    </div>
    <div bind:this={slotContent} class="fr-col-md-9">
      <slot />
    </div>
  </div>
</section>
