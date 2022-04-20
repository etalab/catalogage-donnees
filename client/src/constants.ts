import type {
  DataFormat,
  UpdateFrequency,
  GeographicalCoverage,
} from "./definitions/datasets";

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

export const UPDATE_FREQUENCY_LABELS: { [K in UpdateFrequency]: string } = {
  never: "Aucune (contribution ponctuelle)",
  realtime: "Permanente (temps réel)",
  daily: "Quotidienne (ou plusieures fois par jour)",
  weekly: "Hebdomadaire (ou plusieures fois par semaine)",
  monthly: "Mensuelle (ou plusieures fois pas mois)",
  yearly: "Annuel (ou plusieures fois par an)",
};

export const GEOGRAPHICAL_COVERAGE_LABELS: {
  [K in GeographicalCoverage]: string;
} = {
  municipality: "Communale",
  epci: "EPCI",
  department: "Départementale",
  region: "Régionale",
  national: "Nationale (métropole)",
  national_full_territory: "Nationale (terr Outre-mer inclus)",
  europe: "Européenne",
  world: "Monde",
};
