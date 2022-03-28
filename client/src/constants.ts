import type { DataFormat } from "./definitions/datasets";

export const PUBLIC_PAGES = ["/login"];

export const DATA_FORMAT_LABELS: { [K in DataFormat]: string } = {
  file_tabular: "Fichier tabulaire (XLS, XLSX, CSV, ...)",
  file_gis: "Fichier SIG (Shapefile, ...)",
  api: "API (REST, GraphQL, ...)",
  database: "Base de données",
  website: "Site web",
  other: "Autre",
};

export const DATA_FORMAT_SHORT_NAMES: { [K in DataFormat]: string } = {
  file_tabular: "CSV",
  file_gis: "SIG",
  api: "API",
  database: "BDD",
  website: "Web",
  other: "Autre",
};
