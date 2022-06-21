type Options = {
  callback: () => void;
};

export const clickOutside = (
  node: HTMLElement,
  { callback }: Options
): {
  destroy: () => void;
} => {
  const handleClick = (event) => {
    if (!node.contains(event.target)) {
      callback();
    }
  };

  document.addEventListener("click", handleClick, true);

  return {
    destroy() {
      document.removeEventListener("click", handleClick, true);
    },
  };
};
