import { range } from "./array";

export type PagerOptions = {
  currentPage: number;
  totalPages: number;
  numSiblings: number;
};

export class Pager {
  private readonly currentPage: number;
  private readonly totalPages: number;
  private readonly leftSibling: number;
  private readonly rightSibling: number;

  public readonly windowPages: number[];

  constructor(options: PagerOptions) {
    this.currentPage = options.currentPage;
    this.totalPages = options.totalPages;

    //                  ┌ currentPage
    // |<  <  1 ... 4 5 6 7 8 ... 13  >  >|
    //  leftSibling ┘       └ rightSibling
    //

    // 5 pages max in window, as per DSFR.
    // => 2 pages on the left, 2 pages on the right.
    const numSiblings = 2;

    this.leftSibling = Math.max(this.currentPage - numSiblings, this.firstPage);
    this.rightSibling = Math.min(this.currentPage + numSiblings, this.lastPage);
    this.windowPages = range(this.leftSibling, this.rightSibling + 1);
  }

  get firstPage(): number {
    return 1;
  }

  get hasPrevious(): boolean {
    return this.currentPage > this.firstPage;
  }

  get previousPage(): number {
    return this.currentPage - 1;
  }

  get hasFirstPageLandmark(): boolean {
    return this.leftSibling >= this.firstPage + 1;
  }

  get hasLeftTruncature(): boolean {
    return this.leftSibling - this.firstPage >= 2;
  }

  get hasRightTruncature(): boolean {
    return this.totalPages - this.rightSibling >= 2;
  }

  get hasLastPageLandmark(): boolean {
    return this.rightSibling <= this.totalPages - 1;
  }

  get hasNext(): boolean {
    return this.currentPage < this.lastPage;
  }

  get nextPage(): number {
    return this.currentPage + 1;
  }

  get lastPage(): number {
    return this.totalPages;
  }
}
