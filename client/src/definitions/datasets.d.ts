// Matches enum on the backend.
type DataFormat =
  | "file_tabular"
  | "file_gis"
  | "api"
  | "database"
  | "website"
  | "other";

export interface DatasetHeadlines {
  title: string;
  description: string;
}

export interface Dataset {
  id: string;
  title: string;
  description: string;
  formats: DataFormat[];
  headlines?: DatasetHeadlines;
}

export interface DatasetFormData {
  title: string;
  description: string;
  formats: DataFormat[];
}

export type DatasetCreateData = DatasetFormData;
export type DatasetUpdateData = DatasetCreateData;
