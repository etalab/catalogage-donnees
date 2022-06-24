export type SearchFilter = {
  [key: string]: string[] | null;
};

export type FilterCategories =
  | "Informations Générales"
  | "Sources et Formats"
  | "Mots-clés Thématiques";

export type FilterCategoryGroup = {
  [key in FilterCategories]: SearchFilter;
};
