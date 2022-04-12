import { UPDATE_FREQUENCY } from "src/constants";
import type { Dataset, DatasetFormData } from "src/definitions/datasets";

export const getFakeDataset = (dataset: Partial<Dataset> = {}): Dataset => {
  return {
    updateFrequency: dataset.updateFrequency || UPDATE_FREQUENCY.daily,
    title: dataset.title || "Mon jeu de donnée",
    contactEmails: dataset.contactEmails || ["contact@beta.gouv.fr"],
    entrypointEmail: dataset.entrypointEmail || "jane.doe@beta.gouv.fr",
    id: dataset.id || "xxx-xxx-xxx",
    formats: dataset.formats || [],
    description: dataset.description || "un joli jeu de donnée",
    lastUpdatedAt: dataset.lastUpdatedAt || new Date().toISOString(),
    createdAt: dataset.createdAt || new Date(),
    service: dataset.service || "La Drac",
  };
};

export const getFakeDataSetFormData = (
  datasetFormData: Partial<DatasetFormData> = {}
): DatasetFormData => {
  return {
    updateFrequency: datasetFormData.updateFrequency || UPDATE_FREQUENCY.daily,
    title: datasetFormData.title || "Mon jeu de donnée",
    contactEmails: datasetFormData.contactEmails || ["foo@foo.com"],
    entrypointEmail: datasetFormData.entrypointEmail || "jane.doe@beta.gouv.fr",
    formats: datasetFormData.formats || [],
    description: datasetFormData.description || "un joli jeu de donnée",
    lastUpdatedAt: datasetFormData.lastUpdatedAt || new Date().toISOString(),
    service: datasetFormData.service || "La Drac",
  };
};
