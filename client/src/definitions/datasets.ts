import type { Maybe } from "$lib/util/maybe";
import type { CatalogRecord } from "./catalog_records";
import type { Tag } from "./tag";
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

export type DatasetFilterCategories =
  | "Informations Générales"
  | "Sources et Formats"
  | "Mots-clés Thématiques";

export type DatasetFilter =
  | "geographical_coverage"
  | "service"
  | "format"
  | "technical_source"
  | "tag_id";

export type DatasetFiltersTranslation =
  | "Couverture géographique"
  | "Service producteur de la donnée"
  | "Formats de mise à disposition"
  | "Système d’information source"
  | "Mots-clés";

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

export type DatasetFilters = {
  geographical_coverage: string[] | null;
  service: string[] | null;
  format: string[] | null;
  technical_source: string[] | null;
  tag_id: Tag[] | null;
};

export type SelectableDatasetFilter = {
  geographical_coverage: SelectOption[] | null;
  service: SelectOption[] | null;
  format: SelectOption[] | null;
  technical_source: SelectOption[] | null;
  tag_id: SelectOption[] | null;
};
