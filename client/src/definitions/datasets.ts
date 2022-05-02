import type { CatalogRecord } from "./catalog_records";

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
  description: string;
}

export type Dataset = {
  id: string;
  catalogRecord: CatalogRecord;
  headlines?: DatasetHeadlines;
  title: string;
  description: string;
  formats: DataFormat[];
  producerEmail: string;
  contactEmails: string[];
  service: string;
  lastUpdatedAt: Date | null;
  updateFrequency: UpdateFrequency | null;
  geographicalCoverage: GeographicalCoverage;
  technicalSource: string | null;
  publishedUrl: string | null;
};

export type DatasetFormData = Omit<
  Dataset,
  "id" | "catalogRecord" | "headlines"
>;

export type DatasetCreateData = DatasetFormData;
export type DatasetUpdateData = DatasetCreateData;
