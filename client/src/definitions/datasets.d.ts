// Matches enum on the backend.
type DataFormat =
  | "file_tabular"
  | "file_gis"
  | "api"
  | "database"
  | "website"
  | "other";

type Frequency = "yearly" | "daily" | "monthly" | "never" | "realtime" | "weekly"

export interface DatasetHeadlines {
  title: string;
  description: string;
}

export type Dataset = {
  id: string;
  createdAt: Date;
  title: string;
  description: string;
  formats: DataFormat[];
  entrypointEmail: string;
  contactEmails: string[];
  headlines?: DatasetHeadlines;
  firstPublishedAt: string,
  lastPublishedAt: string,
  updateFrequency: string,
  lastUpdateAt: string
}

export interface DatasetFormData {
  title: string;
  description: string;
  formats: DataFormat[];
  entrypointEmail: string;
  contactEmails: string[];
  service: string;
  firstPublishedAt: string
  updateFrequency: string;
}

export type DatasetCreateData = DatasetFormData;
export type DatasetUpdateData = DatasetCreateData;
