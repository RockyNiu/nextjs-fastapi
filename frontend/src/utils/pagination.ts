/**
 * Pagination utility functions for generating page number arrays
 * with ellipsis support for large page counts.
 */

export type PaginationItem = number | 'ellipsis';

export interface PaginationConfig {
  /** Current active page (1-indexed) */
  currentPage: number;
  /** Total number of pages */
  totalPages: number;
  /** Number of sibling pages to show on each side of current page. Defaults to 1. */
  siblingCount?: number;
}

/**
 * Generates an array of page numbers and ellipsis markers for pagination UI.
 *
 * The algorithm ensures:
 * - First page is always shown
 * - Last page is always shown (if > 1 page)
 * - Current page and its siblings are shown
 * - Ellipsis is used to indicate gaps
 *
 * @example
 * // With 10 pages, current page 5:
 * getPaginationPages({ currentPage: 5, totalPages: 10 })
 * // Returns: [1, 'ellipsis', 4, 5, 6, 'ellipsis', 10]
 *
 * @example
 * // With 10 pages, current page 1:
 * getPaginationPages({ currentPage: 1, totalPages: 10 })
 * // Returns: [1, 2, 3, 'ellipsis', 10]
 *
 * @example
 * // With 5 pages, current page 3:
 * getPaginationPages({ currentPage: 3, totalPages: 5 })
 * // Returns: [1, 2, 3, 4, 5]
 */
export function getPaginationPages({
  currentPage,
  totalPages,
  siblingCount = 1,
}: PaginationConfig): PaginationItem[] {
  // If only 1 page or less, return just page 1
  if (totalPages <= 1) {
    return [1];
  }

  const pages: PaginationItem[] = [];

  // Calculate the range of pages to show around current page
  const leftSiblingIndex = Math.max(currentPage - siblingCount, 1);
  const rightSiblingIndex = Math.min(currentPage + siblingCount, totalPages);

  // Determine if we need ellipsis
  const showLeftEllipsis = leftSiblingIndex > 2;
  const showRightEllipsis = rightSiblingIndex < totalPages - 1;

  // Always add first page
  pages.push(1);

  // Add left ellipsis if needed
  if (showLeftEllipsis) {
    pages.push('ellipsis');
  } else if (leftSiblingIndex > 1) {
    // Add page 2 if we're not showing ellipsis but there's a gap
    for (let i = 2; i < leftSiblingIndex; i++) {
      pages.push(i);
    }
  }

  // Add sibling pages and current page
  for (let i = leftSiblingIndex; i <= rightSiblingIndex; i++) {
    if (i !== 1 && i !== totalPages) {
      pages.push(i);
    }
  }

  // Add right ellipsis if needed
  if (showRightEllipsis) {
    pages.push('ellipsis');
  } else if (rightSiblingIndex < totalPages - 1) {
    // Add remaining pages if we're not showing ellipsis but there's a gap
    for (let i = rightSiblingIndex + 1; i < totalPages; i++) {
      pages.push(i);
    }
  }

  // Always add last page if more than 1 page
  if (totalPages > 1) {
    pages.push(totalPages);
  }

  return pages;
}

/**
 * Type guard to check if a pagination item is a page number
 */
export function isPageNumber(item: PaginationItem): item is number {
  return typeof item === 'number';
}
