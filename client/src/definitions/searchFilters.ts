import type { FilterCategories } from "src/constants";

export type SearchFilter = {
  [key: string]: string[] | null;
};

export type FilterCategoryGroup = {
  [key in FilterCategories]: SearchFilter;
};
