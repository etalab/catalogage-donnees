// Matches enum on the backend.
type DataFormat =
  | "file_tabular"
  | "file_gis"
  | "api"
  | "database"
  | "website"
  | "other";

type UpdateFrequency =
  | "never"
  | "realtime"
  | "daily"
  | "weekly"
  | "monthly"
  | "yearly";

export interface DatasetHeadlines {
  title: string;
  description: string;
}

export type Dataset = {
  id: string;
  createdAt: Date;
  headlines?: DatasetHeadlines;
  title: string;
  description: string;
  formats: DataFormat[];
  entrypointEmail: string;
  contactEmails: string[];
  service: string;
  updateFrequency: string;
  lastUpdatedAt: string;
};

export type DatasetFormData = Omit<Dataset, "id" | "createdAt" | "headlines">;

export type DatasetCreateData = DatasetFormData;
export type DatasetUpdateData = DatasetCreateData;
