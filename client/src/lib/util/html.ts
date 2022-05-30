/**
 * @returns The absolute Y page coordinate of the element.
 */
export const getPageY = (element: HTMLElement): number => {
  let y = 0;
  while (element.offsetParent) {
    y += element.offsetTop;
    element = element.offsetParent as HTMLElement;
  }
  return y;
};
