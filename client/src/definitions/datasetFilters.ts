import type { GeographicalCoverage } from "./datasets";
import type { SelectOption } from "./form";
import type { Tag } from "./tag";

export type DatasetFiltersInfo = {
  geographicalCoverage: GeographicalCoverage[];
  service: string[];
  format: string[];
  technicalSource: string[];
  tagId: Tag[];
};

export type DatasetFiltersValue = {
  geographicalCoverage: GeographicalCoverage | null;
  service: string | null;
  format: string | null;
  technicalSource: string | null;
  tagId: string | null;
};

export type DatasetFiltersOptions = {
  [K in keyof DatasetFiltersValue]: SelectOption<DatasetFiltersValue[K]>[];
};
