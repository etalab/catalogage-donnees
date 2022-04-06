import type { DataFormat, Frequency } from "./definitions/datasets";

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

export const UPDATE_FREQUENCY: { [K in Frequency]: string } = {
  monthly: "Mensuelle (ou plusieures fois pas mois)",
  daily: "Quotidienne (ou plusieures fois par jour)",
  weekly: "Hebdomadaire (ou plusieures fois par semaine)",
  realtime: "Permanente (temps réel)",
  never: "Aucune (contribution ponctuelle)",
  yearly: "Annuel (ou plusieures fois par an)",
};
