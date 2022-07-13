import type { SelectOption } from "./form";
import type { Tag } from "./tag";

export type DatasetFiltersInfo = {
  geographicalCoverage: string[];
  service: string[];
  format: string[];
  technicalSource: string[];
  tagId: Tag[];
  license: string[];
};

export type DatasetFiltersValue = {
  geographicalCoverage: string | null;
  service: string | null;
  format: string | null;
  technicalSource: string | null;
  tagId: string | null;
  license: string | null;
};

export type DatasetFiltersOptions = {
  [K in keyof DatasetFiltersValue]: SelectOption<DatasetFiltersValue[K]>[];
};
