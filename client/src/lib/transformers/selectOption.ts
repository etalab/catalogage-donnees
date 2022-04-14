import type { SelectOption } from "src/definietions/selectOption";

export const toSelectOption = (source: {
  [key: string]: any;
}): Array<SelectOption> => {
  return Object.keys(source).map((item, index) => ({
    id: `${source[item]}-${index}`,
    label: source[item],
    value: item,
  }));
};
