import type { Maybe } from "$lib/util/maybe";
import type { CatalogRecord } from "./catalog_records";
import type { Tag } from "./tag";
import type { FilterCategories } from "src/constants";
import type { SelectOption } from "./form";

// Matches enum on the backend.
export type DataFormat =
  | "file_tabular"
  | "file_gis"
  | "api"
  | "database"
  | "website"
  | "other";

export type UpdateFrequency =
  | "never"
  | "realtime"
  | "daily"
  | "weekly"
  | "monthly"
  | "yearly";

export type GeographicalCoverage =
  | "municipality"
  | "epci"
  | "department"
  | "region"
  | "national"
  | "national_full_territory"
  | "europe"
  | "world";

export interface DatasetHeadlines {
  title: string;
  description: Maybe<string>;
}

export type Dataset = {
  id: string;
  catalogRecord: CatalogRecord;
  headlines?: DatasetHeadlines;
  title: string;
  description: string;
  formats: DataFormat[];
  producerEmail: string | null;
  contactEmails: string[];
  service: string;
  lastUpdatedAt: Date | null;
  updateFrequency: UpdateFrequency | null;
  geographicalCoverage: GeographicalCoverage;
  technicalSource: string | null;
  publishedUrl: string | null;
  tags: Tag[];
};

export type DatasetFormData = Omit<
  Dataset,
  "id" | "catalogRecord" | "headlines"
>;

export type DatasetCreateData = Omit<DatasetFormData, "tags"> & {
  tagIds: string[];
};
export type DatasetUpdateData = DatasetCreateData;

export type SearchFilter = {
  geographical_coverage: string[] | null;
  service: string[] | null;
  format: string[] | null;
  technical_source: string[] | null;
  tag_id: Tag[] | null;
};

export type SelectableSearchFilter = {
  geographical_coverage: SelectOption[] | null;
  service: SelectOption[] | null;
  format: SelectOption[] | null;
  technical_source: SelectOption[] | null;
  tag_id: SelectOption[] | null;
};

export type SelectableSearchFilterGroup = {
  [key in FilterCategories]: Partial<SelectableSearchFilter>;
};
