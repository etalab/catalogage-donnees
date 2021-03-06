import type { Maybe } from "$lib/util/maybe";
import type { CatalogRecord } from "./catalog_records";
import type { Tag } from "./tag";

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
  geographicalCoverage: string;
  technicalSource: string | null;
  url: string | null;
  license: string | null;
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
