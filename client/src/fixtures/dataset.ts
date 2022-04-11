import { UPDATE_FREQUENCY } from "src/constants";
import type { Dataset, DatasetFormData } from "src/definitions/datasets";

export const getFakeDataSet = (dataSet: Partial<Dataset>): Dataset => {
  return {
    updateFrequency: dataSet.updateFrequency || UPDATE_FREQUENCY.daily,
    title: dataSet.title || "Mon jeu de donnée",
    contactEmails: dataSet.contactEmails || ["contact@beta.gouv.fr"],
    entrypointEmail: dataSet.entrypointEmail || "jane.doe@beta.gouv.fr",
    id: dataSet.id || "xxx-xxx-xxx",
    formats: dataSet.formats || [],
    description: dataSet.description || "un joli jeu de donnée",
    firstPublishedAt: dataSet.firstPublishedAt || new Date().toISOString(),
    lastUpdatedAt: dataSet.lastUpdatedAt || new Date().toISOString(),
    createdAt: dataSet.createdAt || new Date(),
    service: dataSet.service || "La Drac",
  };
};

export const getFakeDataSetFormData = (
  dataSetFormData: Partial<DatasetFormData>
): DatasetFormData => {
  return {
    updateFrequency: dataSetFormData.updateFrequency || UPDATE_FREQUENCY.daily,
    title: dataSetFormData.title || "Mon jeu de donnée",
    contactEmails: dataSetFormData.contactEmails || ["foo@foo.com"],
    entrypointEmail: dataSetFormData.entrypointEmail || "jane.doe@beta.gouv.fr",
    formats: dataSetFormData.formats || [],
    description: dataSetFormData.description || "un joli jeu de donnée",
    firstPublishedAt:
      dataSetFormData.firstPublishedAt || new Date().toISOString(),
    lastUpdatedAt: dataSetFormData.lastUpdatedAt || new Date().toISOString(),
    service: dataSetFormData.service || "La Drac",
  };
};
