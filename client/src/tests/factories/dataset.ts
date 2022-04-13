import type { Dataset, DatasetFormData } from "src/definitions/datasets";

export const getFakeDataset = (dataset: Partial<Dataset> = {}): Dataset => {
  return {
    id: dataset.id || "xxx-xxx-xxx",
    createdAt: dataset.createdAt || new Date(),
    title: dataset.title || "Mon jeu de donnée",
    description: dataset.description || "un joli jeu de donnée",
    formats: dataset.formats || [],
    entrypointEmail: dataset.entrypointEmail || "jane.doe@beta.gouv.fr",
    contactEmails: dataset.contactEmails || ["contact@beta.gouv.fr"],
    service: dataset.service || "La Drac",
    updateFrequency: dataset.updateFrequency || "daily",
    lastUpdatedAt: dataset.lastUpdatedAt || new Date(),
    geographicalCoverage: dataset.geographicalCoverage || "europe",
  };
};

export const getFakeDataSetFormData = (
  datasetFormData: Partial<DatasetFormData> = {}
): DatasetFormData => {
  return {
    title: datasetFormData.title || "Mon jeu de donnée",
    description: datasetFormData.description || "un joli jeu de donnée",
    formats: datasetFormData.formats || [],
    entrypointEmail: datasetFormData.entrypointEmail || "jane.doe@beta.gouv.fr",
    contactEmails: datasetFormData.contactEmails || ["contact@beta.gouv.fr"],
    service: datasetFormData.service || "La Drac",
    updateFrequency: datasetFormData.updateFrequency || "daily",
    lastUpdatedAt: datasetFormData.lastUpdatedAt || new Date(),
    geographicalCoverage: datasetFormData.geographicalCoverage || "europe",
  };
};
