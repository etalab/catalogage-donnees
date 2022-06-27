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
  daily: "Quotidienne (ou plusieurs fois par jour)",
  weekly: "Hebdomadaire (ou plusieurs fois par semaine)",
  monthly: "Mensuelle (ou plusieurs fois pas mois)",
  yearly: "Annuel (ou plusieurs fois par an)",
};

export const GEOGRAPHICAL_COVERAGE_LABELS: {
  [K in GeographicalCoverage]: string;
} = {
  municipality: "Communale",
  epci: "EPCI",
  department: "Départementale",
  region: "Régionale",
  national: "Nationale (métropole)",
  national_full_territory: "Nationale (territoires d'Outre-mer inclus)",
  europe: "Européenne",
  world: "Monde",
};


export type FilterCategories =
  | "Informations Générales"
  | "Sources et Formats"


export const SEARCH_FILTERS_CATEGORIES: {
  [K in FilterCategories]: string[];
} = {
  "Informations Générales": ["geographical_coverage", "service"],
  "Sources et Formats": ["format", "technical_source"],
};


export type DatasetFilters = "Couverture géographique" |
  "Service producteur de la donnée" |
  "Formats de mise à disposition" |
  "Système d’information source" |
  "Mots-clés";


export const DATASET_FILTERS: { [K: string]: DatasetFilters } =
{
  geographical_coverage: "Couverture géographique",
  service: "Service producteur de la donnée",
  format: "Formats de mise à disposition",
  technical_source: "Système d’information source",
  tags: "Mots-clés",
};



export const DATASETS_PER_PAGE = 50;
