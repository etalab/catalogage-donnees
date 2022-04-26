import type { Dataset, DatasetFormData } from "src/definitions/datasets";
import { buildFakeTag } from "./tag";

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
