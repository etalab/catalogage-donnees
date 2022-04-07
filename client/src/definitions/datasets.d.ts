// Matches enum on the backend.
type DataFormat =
  | "file_tabular"
  | "file_gis"
  | "api"
  | "database"
  | "website"
  | "other";

type Frequency =
  | "yearly"
  | "daily"
  | "monthly"
  | "never"
  | "realtime"
  | "weekly";

export interface DatasetHeadlines {
  title: string;
  description: string;
}

export type DatasetFormData = {
  title: string;
  description: string;
  formats: DataFormat[];
  entrypointEmail: string;
  contactEmail: string;
  service: string;
  firstPublishedAt: string;
  updateFrequency: string;
  lastUpdatedAt: string;

  description: string;
};

export type Dataset = {
  id: string;
  createdAt: Date;
  headlines?: DatasetHeadlines;
} & DatasetFormData;

export type DatasetCreateData = DatasetFormData;
export type DatasetUpdateData = DatasetCreateData;
