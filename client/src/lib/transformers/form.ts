import type { SelectOption } from "src/definitions/form";

import type { Tag } from "src/definitions/tag";

export const toSelectOptions = (labelsMap: {
  [key: string]: string;
}): Array<SelectOption> => {
  return Object.keys(labelsMap).map(
    (item): SelectOption => ({
      label: labelsMap[item],
      value: item,
    })
  );
};

export const transformTagToSelectOption = (tag: Tag): SelectOption => ({
  label: tag.name,
  value: `${tag.id}`,
});
