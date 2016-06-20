#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <stdbool.h>


/**
 * Return true, if the regions overlap.
 */
bool overlap(
    const char *chromA,
    const int initialA,
    const int finalA,
    const char *chromB,
    const int initialB,
    const int finalB
) {
    // printf("%s %d %d,", chromA, initialA, finalA);
    // printf("%s %d %d\n", chromB, initialB, finalB);
    if (strcmp(chromA, chromB) == 0) {
        if (initialA <= initialB) {
            if (finalA > initialB) {
                return true;
            }
        } else {
            if (initialA < finalB) {
                return true;
            }
        }
    }
    return false;
}


/**
 *  Comparison of genomic regions:
 *  First compare the chromosome name lexicographically, then the initial position and finally the final position.
 *  
 *  @param const char *chromA The chromosome name of the first genomic region.
 *  @param const int initialA The initial position of the first genomic region.
 *  @param const int finalA   The final position of the first genomic region.
 *  @param const char *chromB The chromosome name of the second genomic region.
 *  @param const int initialB The initial position of the second genomic region.
 *  @param const int finalB   The final position of the second genomic region.
 *  
 *  @return -1 iff the first genomic region is considered to be smaller than the second one.
 *           0 iff the first genomic region is considered to be equal to the second one.
 *           1 iff the first genomic region is considered to be greater than the second one.
 */
int compareGenomicRegions(
    const char *chromA,
    const int initialA,
    const int finalA,
    const char *chromB,
    const int initialB,
    const int finalB
) {
    // First, compare chromosome names.
    const int chromComp = strcmp(chromA, chromB);
    if (chromComp != 0) {
        // If the chrosome name differs, decide based on the chromosome name.
        return chromComp;
    } else {
        // Otherwise, the regions are in the same genomic region.
        // If the initial position of the first genomic region is smaller than the initial position of the second one,
        // the first one is considered smaller.
        // A: [-----
        // B:     [----
        if (initialA < initialB) {
            return -1;
        } else if (initialA > initialB) {
            // If the initial position of the first genomic region is greater than the initial position of the second
            // one, the first one is considered greater.
            // A:     [------
            // B: [----
            return 1;
        } else {
            // Otherwise, the initial position is equal:
            // A: [-----
            // B: [----
            // Then, decide based on the final positions.
            if (finalA < finalB) {
                // If the final position of the first region is smaller than the final position of the second one, the
                // first one is considered smaller.
                // A: [--//--]
                // B: [--//----]
                return -1;
            } else if (finalA > finalB) {
                // If the final position of the first region is greater than the final position of the second one, the
                // first one is considered greater.
                // A: [--//-----]
                // B: [--//--]
                return 1;
            } else {
                // Otherwise, the name of the genomic region, the initial position, and the final position are all
                // equal. Then, the regions are considered equal, as well.
                return 0;
            }
        }
    }
}

/**
 * Returns the minimum of two integer values.
 */
const int min(const int a, const int b) {
    if (a < b) {
        return a;
    } else {
        return b;
    }
}

/**
 * Returns the maximum of two integer values.
 */
const int max(const int a, const int b) {
    if (a > b) {
        return a;
    } else {
        return b;
    }
}


/**
 * Compute the intersection of two genomic region sets using the OVERLAP mode.
 * The region sets have to be sorted and passed as three arrays: the chromsome names of the genomic regions, the initial
 * positions of the genomic regions, and the final positions of the genomic regions.
 * The number of genomic regions per set has to be passed as well.
 *
 * @param const char **chromsA An array of the chromosome names of the genomic regions of the first set.
 * @param const int *initialsA An array of the initial positions of the genomic regions of the first set.
 * @param const int *finalsA   An array of the final positions of the genomic regions of the first set.
 * @param const int sizeA      The number of genomic regions in the first set.
 * @param const char **chromsB An array of the chromosome names of the genomic regions of the second set.
 * @param const int *initialsB An array of the initial positions of the genomic regions of the second set.
 * @param const int *finalsB   An array of the final positions of the genomic regions of the second set.
 * @param const int sizeB      The number of genomic regions in the second set.
 * @param int **indicesR       Used to return the result. An array for the indices of genomic regions of the first set,
 *                             holding the meta data which should be attached to the corresponding genomic region of the
 *                             result set.
 * @param int **initialsR      Used to return the result. The initial positions of the genomic regions of the result
                               set.
 * @param int **finalsR        Used to return the result. The final positions of the genomic regions of the result set.
 * @param int *sizaR           Used to return the result. The number of genomic regions in the result set.
 *
 * @return None
 */
void intersectGenomicRegionSetsOverlap (
    const char **chromsA,
    const int *initialsA,
    const int *finalsA,
    const int sizeA,
    const char **chromsB,
    const int *initialsB,
    const int *finalsB,
    const int sizeB,
    int **indicesR,
    int **initialsR,
    int **finalsR,
    int *sizeR
) {
    // Position in first genomic region set.
    int i = 0;
    // Position in second genomic region set.
    int j = 0;
    // Position in result genomic region set.
    int k = 0;
    // Last valid position in first genomic region set.
    const int last_i = sizeA - 1;
    // Last valid position in second genomic region set.
    const int last_j = sizeB - 1;
    // Flag, whether to continue looping.
    bool cont_loop = true;
    // TODO: What does this express?
    int pre_inter = 0;
    // Flag, whether an overlap continues
    bool cont_overlap = false;
    // Loop
    while (cont_loop) {
        // If the current genomic regions of the first and second set overlap.
        if (overlap(chromsA[i], initialsA[i], finalsA[i], chromsB[j], initialsB[j], finalsB[j])) {
            // Add a region to the result
            (*indicesR)[k] = i;
            // spanning from first position contained in both regions...
            (*initialsR)[k] = max(initialsA[i], initialsB[j]);
            // ... to the last position contained in both regions.
            (*finalsR)[k] = min(finalsA[i], finalsB[j]);
            // Increment position in result set.
            k++;
            // TODO: Remove debug output
            printf("Added genomic region to result set: %s[%d, %d]\n\n", chromsA[i], max(initialsA[i], initialsB[j]),
                min(finalsA[i], finalsB[j]));
            // TODO: What does this do?
            if (!cont_overlap) {
                pre_inter = j;
            }
            // If the second set has unchecked regions
            if (j < last_j) {
                // Go to the next region.
                j++;
            } else { // Otherwise,
                // If the first set has unchecked regions
                if (i < last_i) {
                    // Go to the next region of the first set.
                    i++;
                } else {
                    // Both sets have been sufficiently compared.
                    // Terminate loop.
                    cont_loop = false;
                }
            }
            // If the next comparison delivers an overlap, it is a continuation.
            cont_overlap = true;
        // Otherwise, there is no overlap.
        } else {
            // There is an interrupt of overlap continuation
            cont_overlap = false;
            // Compare the two current regions.
            const int comparison = compareGenomicRegions(chromsA[i], initialsA[i], finalsA[i], chromsB[j], initialsB[j],
                finalsB[j]);
            // If the region of the first set is smaller than the one from the second one.
            if (comparison < 0) {
                // If the first set has unchecked regions
                if (i < last_i) {
                    // Go to the next region.
                    i++;
                    // TODO: What is done here?
                    if ((strcmp(chromsA[i], chromsB[j]) == 0) && (pre_inter > 0)) {
                        j = pre_inter;
                    }
                } else {
                    // There are no more regions in the smaller set: It is safe to terminate.
                    cont_loop = false;
                }
            // If the region of the first set is greater than the one from the second one.
            } else if (comparison > 0) {
                // If the second set has unchecked regions, go to the next region.
                if (j < last_j) {
                    // Go to the next region.
                    j++;
                } else {
                    // There are no more regions in the smaller set: It is safe to terminate.
                    cont_loop = false;
                }
            // If the region of the first set is equal to the one from the second one, but they do not overlap
            // TODO: Is this even possible?
            } else {
                // TODO: Nearly equal to first case!
                // If the first set has unchecked regions
                if (i < last_i) {
                    // Go to the next region.
                    i++;
                } else {
                    // There are no more regions in the smaller set: It is safe to terminate.
                    cont_loop = false;
                }
            }
        }
    }
    // TODO: Remove debug output
    printf("Result contain  %d GenomicRegion\n", k);
    // Return the size of the result set.
    *sizeR = k;
}



/**
 * Compute the intersection of two genomic region sets using the ORIGINAL mode.
 * The region sets have to be sorted and passed as three arrays: the chromsome names of the genomic regions, the initial
 * positions of the genomic regions, and the final positions of the genomic regions.
 * The number of genomic regions per set has to be passed as well.
 *
 * @param const char **chromsA An array of the chromosome names of the genomic regions of the first set.
 * @param const int *initialsA An array of the initial positions of the genomic regions of the first set.
 * @param const int *finalsA   An array of the final positions of the genomic regions of the first set.
 * @param const int sizeA      The number of genomic regions in the first set.
 * @param const char **chromsB An array of the chromosome names of the genomic regions of the second set.
 * @param const int *initialsB An array of the initial positions of the genomic regions of the second set.
 * @param const int *finalsB   An array of the final positions of the genomic regions of the second set.
 * @param const int sizeB      The number of genomic regions in the second set.
 * @param int **indicesR       Used to return the result. An array for the indices of genomic regions of the first set,
 *                             holding the meta data which should be attached to the corresponding genomic region of the
 *                             result set.
 * @param int **initialsR      Used to return the result. The initial positions of the genomic regions of the result
                               set.
 * @param int **finalsR        Used to return the result. The final positions of the genomic regions of the result set.
 * @param int *sizaR           Used to return the result. The number of genomic regions in the result set.
 *
 * @return None
 */
void intersectGenomicRegionSetsOriginal (
    const char **chromsA,
    const int *initialsA,
    const int *finalsA,
    const int sizeA,
    const char **chromsB,
    const int *initialsB,
    const int *finalsB,
    const int sizeB,
    int **indicesR,
    int **initialsR,
    int **finalsR,
    int *sizeR
) {
    // Position in first genomic region set.
    int i = 0;
    // Position in second genomic region set.
    int j = 0;
    // Position in result genomic region set.
    int k = 0;
    // Last valid position in first genomic region set.
    const int last_i = sizeA - 1;
    // Last valid position in second genomic region set.
    const int last_j = sizeB - 1;
    // Flag, whether to continue looping.
    bool cont_loop = true;
    // Loop
    while (cont_loop) {
        // If the current genomic regions of the first and second set overlap.
        if (overlap(chromsA[i], initialsA[i], finalsA[i], chromsB[j], initialsB[j], finalsB[j])) {
            // Add a region to the result
            (*indicesR)[k] = i;
            // spanning from first position contained in both regions...
            (*initialsR)[k] = max(initialsA[i], initialsB[j]);
            // ... to the last position contained in both regions.
            (*finalsR)[k] = min(finalsA[i], finalsB[j]);
            // Increment position in result set.
            k++;
            // If the first set has unchecked regions
            if (i < last_i) {
                // Go to the next region.
                i++;
            } else { // Otherwise,
                // Terminate
                cont_loop = false;
            }
        } else {
            // Compare the two current regions.
            const int comparison = compareGenomicRegions(chromsA[i], initialsA[i], finalsA[i], chromsB[j], initialsB[j], finalsB[j]);
            // If the region of the first set is smaller than the one from the second one.
            if (comparison < 0) {
                // If the first set has unchecked regions
                if (i < last_i) {
                    // Go to the next region.
                    i++;
                } else {
                    // Otherwise, terminate.
                    cont_loop = false;
                }
            // If the region of the first set is greater than the one from the second one.
            } else if (comparison > 0) {
                // If the second set has unchecked regions
                if (j < last_j) {
                    // Go to next region.
                    j++;
                } else {
                    // Otherwise, terminate.
                    cont_loop = false;
                }
            // If the region of the first set is equal to the one from the second one, but they do not overlap
            // TODO: Is this even possible?
            } else {
                // TODO: Equal to first case.
                // If the first set has unchecked regions
                if (i < last_i) {
                    // Go to the next region.
                    i++;
                } else {
                    // Otherwise, terminate.
                    cont_loop = false;
                }
            }
        }
    }
    // Return the size of the result set.
    *sizeR = k;
}


void intersectGenomicRegionSetsCompletelyIncluded (
    const char **chromsA,
    const int *initialsA,
    const int *finalsA,
    const int sizeA,
    const char **chromsB,
    const int *initialsB,
    const int *finalsB,
    const int sizeB,
    int **indicesR,
    int **initialsR,
    int **finalsR,
    int *sizeR
) {
    // Position in first genomic region set.
    int i = 0;
    // Position in second genomic region set.
    int j = 0;
    // Position in result genomic region set.
    int k = 0;
    // Last valid position in first genomic region set.
    const int last_i = sizeA - 1;
    // Last valid position in second genomic region set.
    const int last_j = sizeB - 1;
    // Flag, whether to continue looping.
    bool cont_loop = true;
    // Loop
    while (cont_loop) {
        // If the current genomic regions of the first and second set overlap.
        if (overlap(chromsA[i], initialsA[i], finalsA[i], chromsB[j], initialsB[j], finalsB[j])) {
            // Add a region to the result
            (*indicesR)[k] = i;
            // spanning from first position contained in both regions...
            (*initialsR)[k] = max(initialsA[i], initialsB[j]);
            // ... to the last position contained in both regions.
            (*finalsR)[k] = min(finalsA[i], finalsB[j]);
            // Increment position in result set.
            k++;
            // TODO: What is this?
            if (!cont_overlap) {
                pre_inter = j;
            }
            // If the second set has remaining regions
            if (j < last_j) {
                // Go to the next region
                j++
            } else {
                // If the first set has unchecked regions
                if (i < last_i) {
                    // Go to the next region
                    i++;
                } else {
                    // Otherwise, both sets do not have any more regions.
                    // Thus, terminate.
                    cont_loop = false;
                }
            }
            // The last position was an overlap
            cont_overlap = true;
        } else {
            // The overlap continuation was interrupted
            cont_overlap = false;
            // Compare the two current regions.
            const int comparison = compareGenomicRegions(chromsA[i], initialsA[i], finalsA[i], chromsB[j], initialsB[j], finalsB[j]);
            // If the region of the first set is smaller than the one from the second one.
            if (comparison < 0) {
                // If the first set has unchecked regions
                if (i < last_i) {
                    // Go to the next region.
                    i++;
                    // TODO: What happens here?
                    if ((strcmp(chromsA[i], chromsB[j]) == 0) && (pre_inter > 0)) {
                        j = pre_inter;
                    }
                } else {
                    // Otherwise, terminate.
                    cont_loop = false;
                }
            // If the region of the first set is greater than the one from the second one.
            // If the region of the first set is equal to the one from the second one, but they do not overlap
            // TODO: Is this even possible?
            } else if (comparison > 0) {
                // If the second set has unchecked regions
                if (j < last_j) {
                    // Go to the next region.
                    j++;
                } else {
                    // Otherwise, terminate.
                    cont_loop = false;
                }
            } else {
                // If the first set has unchecked regions
                if (i < last_i) {
                    // Go to the next region.
                    i++;
                } else {
                    // Otherwise, terminate.
                    cont_loop = false;
                }
            }
        }
        // Return the size of the result set.
        *sizeR = k;
    }
}


/**
 * Compute the intersection of two genomic region sets using the OVERLAP mode.
 * The region sets have to be sorted and passed as three arrays: the chromsome names of the genomic regions, the initial
 * positions of the genomic regions, and the final positions of the genomic regions.
 * The number of genomic regions per set has to be passed as well.
 *
 * @param const char **chromsA An array of the chromosome names of the genomic regions of the first set.
 * @param const int *initialsA An array of the initial positions of the genomic regions of the first set.
 * @param const int *finalsA   An array of the final positions of the genomic regions of the first set.
 * @param const int sizeA      The number of genomic regions in the first set.
 * @param const char **chromsB An array of the chromosome names of the genomic regions of the second set.
 * @param const int *initialsB An array of the initial positions of the genomic regions of the second set.
 * @param const int *finalsB   An array of the final positions of the genomic regions of the second set.
 * @param const int sizeB      The number of genomic regions in the second set.
 *
 * @return The total coverage of the intersection of the two genomic regions.
 */
int totalCoverageIntersectGenomicRegionSetsOverlap (
    const char **chromsA,
    const int *initialsA,
    const int *finalsA,
    const int sizeA,
    const char **chromsB,
    const int *initialsB,
    const int *finalsB,
    const int sizeB
) {
    // Position in first genomic region set.
    int i = 0;
    // Position in second genomic region set.
    int j = 0;
    // The total coverage of the intersection
    int total_intersect_coverage = 0;
    // Last valid position in first genomic region set.
    const int last_i = sizeA - 1;
    // Last valid position in second genomic region set.
    const int last_j = sizeB - 1;
    // Flag, whether to continue looping.
    bool cont_loop = true;
    // TODO: What does this express?
    int pre_inter = 0;
    // Flag, whether an overlap continues
    bool cont_overlap = false;
    // Loop
    while (cont_loop) {
        // If the current genomic regions of the first and second set overlap.
        if (overlap(chromsA[i], initialsA[i], finalsA[i], chromsB[j], initialsB[j], finalsB[j])) {
            // Compute coverage of the resulting genomic region.
            const int initial = max(initialsA[i], initialsB[j]);
            const int final = min(finalsA[i], finalsB[j]);
            const int coverage = final - initial;

            // Add coverage to total intersection coverage.
            total_intersect_coverage += coverage;
            // TODO: What does this do?
            if (!cont_overlap) {
                pre_inter = j;
            }
            // If the second set has unchecked regions
            if (j < last_j) {
                // Go to the next region.
                j++;
            } else { // Otherwise,
                // If the first set has unchecked regions
                if (i < last_i) {
                    // Go to the next region of the first set.
                    i++;
                } else {
                    // Both sets have been sufficiently compared.
                    // Terminate loop.
                    cont_loop = false;
                }
            }
            // If the next comparison delivers an overlap, it is a continuation.
            cont_overlap = true;
        // Otherwise, there is no overlap.
        } else {
            // There is an interrupt of overlap continuation
            cont_overlap = false;
            // Compare the two current regions.
            const int comparison = compareGenomicRegions(chromsA[i], initialsA[i], finalsA[i], chromsB[j], initialsB[j],
                finalsB[j]);
            // If the region of the first set is smaller than the one from the second one.
            if (comparison < 0) {
                // If the first set has unchecked regions
                if (i < last_i) {
                    // Go to the next region.
                    i++;
                    // TODO: What is done here?
                    if ((strcmp(chromsA[i], chromsB[j]) == 0) && (pre_inter > 0)) {
                        j = pre_inter;
                    }
                } else {
                    // There are no more regions in the smaller set: It is safe to terminate.
                    cont_loop = false;
                }
            // If the region of the first set is greater than the one from the second one.
            } else if (comparison > 0) {
                // If the second set has unchecked regions, go to the next region.
                if (j < last_j) {
                    // Go to the next region.
                    j++;
                } else {
                    // There are no more regions in the smaller set: It is safe to terminate.
                    cont_loop = false;
                }
            // If the region of the first set is equal to the one from the second one, but they do not overlap
            // TODO: Is this even possible?
            } else {
                // TODO: Nearly equal to first case!
                // If the first set has unchecked regions
                if (i < last_i) {
                    // Go to the next region.
                    i++;
                } else {
                    // There are no more regions in the smaller set: It is safe to terminate.
                    cont_loop = false;
                }
            }
        }
    }
    // Return total coverage
    return total_intersect_coverage;
}


/**
 * Return jaccard index, a value of similarity of two GenomicRegionSet.
 *
 * @param const char **chromsA An array of the chromosome names of the genomic regions of the first set.
  * @param const int *initialsA An array of the initial positions of the genomic regions of the first set.
  * @param const int *finalsA   An array of the final positions of the genomic regions of the first set.
  * @param const int sizeA      The number of genomic regions in the first set.
  * @param const char **chromsB An array of the chromosome names of the genomic regions of the second set.
  * @param const int *initialsB An array of the initial positions of the genomic regions of the second set.
  * @param const int *finalsB   An array of the final positions of the genomic regions of the second set.
  * @param const int sizeB      The number of genomic regions in the second set.
 */
double jaccard (
    const char **chromsA,
    const int *initialsA,
    const int *finalsA,
    const int sizeA,
    const char **chromsB,
    const int *initialsB,
    const int *finalsB,
    const int sizeB
) {
    // Compute coverage of the intersection
    // printf("Compute coverage of the intersection.\n");
    const int inter = totalCoverageIntersectGenomicRegionSetsOverlap(chromsA, initialsA, finalsA, sizeA, chromsB, initialsB, finalsB, sizeB);

    // Compute total coverage of A
    // printf("Compute total coverage of A.\n");
    int totalCoverageA = 0;
    for (int i = 0; i < sizeA; i++) {
        const int coverage = (finalsA[i] - initialsA[i]);
        totalCoverageA += coverage;
    }

    // Compute total coverage of B
    // printf("Compute total coverage of B.\n");
    int totalCoverageB = 0;
    for (int i = 0; i < sizeB; i++) {
        const int coverage = (finalsB[j] - initialsB[j]);
        totalCoverageB += coverage;
    }

    // Size(A u B) = Size(A) + Size(B) - Size(A n B)
    const int uni = totalCoverageA + totalCoverageB - inter;

    // Return jaccard index.
    // printf("Return jaccard index.\n");
    return ((double)inter) / ((double) uni);
}