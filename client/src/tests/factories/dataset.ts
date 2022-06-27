import { GEOGRAPHICAL_COVERAGE_LABELS } from "src/constants";
import type {
  Dataset,
  DatasetFormData,
  SearchFilter,
  SelectableSearchFilter,
} from "src/definitions/datasets";
import { buildFakeTag } from "./tags";

export const getFakeDataset = (dataset: Partial<Dataset> = {}): Dataset => {
  return {
    id: dataset.id || "xxx-xxx-xxx",
    catalogRecord: dataset.catalogRecord || { createdAt: new Date() },
    title: dataset.title || "Mon jeu de donnée",
    description: dataset.description || "un joli jeu de donnée",
    formats: dataset.formats || [],
    producerEmail: dataset.producerEmail || "jane.doe@beta.gouv.fr",
    contactEmails: dataset.contactEmails || ["contact@beta.gouv.fr"],
    service: dataset.service || "La Drac",
    technicalSource: dataset.technicalSource || null,
    updateFrequency: dataset.updateFrequency || "daily",
    lastUpdatedAt: dataset.lastUpdatedAt || new Date(),
    geographicalCoverage: dataset.geographicalCoverage || "europe",
    publishedUrl: dataset.publishedUrl || null,
    tags: dataset.tags || [buildFakeTag()],
  };
};

export const getFakeDataSetFormData = (
  datasetFormData: Partial<DatasetFormData> = {}
): DatasetFormData => {
  return {
    title: datasetFormData.title || "Mon jeu de donnée",
    description: datasetFormData.description || "un joli jeu de donnée",
    formats: datasetFormData.formats || [],
    producerEmail: datasetFormData.producerEmail || "jane.doe@beta.gouv.fr",
    contactEmails: datasetFormData.contactEmails || ["contact@beta.gouv.fr"],
    service: datasetFormData.service || "La Drac",
    technicalSource: datasetFormData.technicalSource || null,
    updateFrequency: datasetFormData.updateFrequency || "daily",
    lastUpdatedAt: datasetFormData.lastUpdatedAt || new Date(),
    geographicalCoverage: datasetFormData.geographicalCoverage || "europe",
    publishedUrl: datasetFormData.publishedUrl || null,
    tags: datasetFormData.tags || [buildFakeTag()],
  };
};

export const getFakeSearchFilter = (
  searchFilter: Partial<SearchFilter> = {}
): SearchFilter => {
  return {
    tags: searchFilter.tags || [buildFakeTag(), buildFakeTag()],
    geographical_coverage: searchFilter.geographical_coverage || [
      "department",
      "epci",
    ],
    service: searchFilter.service || ["DINUM", "ADEME"],
    technical_source: searchFilter.technical_source || ["foo", "bar"],
    format: searchFilter.format || ["CSV", "XLSX"],
  };
};

export const getFakeSelectableSearchFilter = (
  searchFilter: Partial<SelectableSearchFilter> = {}
): SelectableSearchFilter => {
  const tag1 = buildFakeTag();
  const tag2 = buildFakeTag();

  return {
    tags: searchFilter.tags || [
      {
        label: tag1.name,
        value: tag1.id,
      },
      {
        label: tag2.name,
        value: tag2.id,
      },
    ],
    geographical_coverage: searchFilter.geographical_coverage || [
      {
        label: GEOGRAPHICAL_COVERAGE_LABELS.epci,
        value: "epci",
      },
    ],
    service: searchFilter.service || [{ label: "DINUM", value: "DINUM" }],
    technical_source: searchFilter.technical_source || [
      { label: "foo", value: "foo" },
    ],
    format: searchFilter.format || [
      {
        label: "XLS",
        value: "XLS",
      },
    ],
  };
};
