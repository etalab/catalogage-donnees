import { range } from "./array";

export type PaginationOptions = {
  currentPage: number;
  totalPages: number;
  numSiblings: number;
};

type Pagination = {
  firstPage: number;
  hasPrevious: boolean;
  previousPage: number;
  hasFirstPageLandmark: boolean;
  hasLeftTruncature: boolean;
  windowPages: number[];
  hasRightTruncature: boolean;
  hasLastPageLandmark: boolean;
  hasNext: boolean;
  nextPage: number;
  lastPage: number;
};

export const makePagination = (options: PaginationOptions): Pagination => {
  const { currentPage, totalPages, numSiblings } = options;

  // Example result with { currentPage: 6, totalPages: 13, numSiblings: 2 }:
  //
  //                  ┌ currentPage
  // |<  <  1 ... 4 5 6 7 8 ... 13  >  >|
  //  leftSibling ┘       └ rightSibling
  //

  const firstPage = 1;
  const lastPage = totalPages;

  const leftSibling = Math.max(currentPage - numSiblings, firstPage);
  const rightSibling = Math.min(currentPage + numSiblings, lastPage);
  const windowPages = range(leftSibling, rightSibling + 1);

  return {
    firstPage,
    hasPrevious: currentPage > firstPage,
    previousPage: currentPage - 1,
    hasFirstPageLandmark: leftSibling >= firstPage + 1,
    hasLeftTruncature: leftSibling >= firstPage + 2,
    windowPages,
    hasRightTruncature: rightSibling <= lastPage - 2,
    hasLastPageLandmark: rightSibling <= lastPage - 1,
    hasNext: currentPage < lastPage,
    nextPage: currentPage + 1,
    lastPage,
  };
};
