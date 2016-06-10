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
        // If the initial position of the first genomic region is smaller than the initial position of the second one, the first one is considered smaller.
        // A: [-----
        // B:     [----
        if (initialA < initialB) {
            return -1;
        } else if (initialA > initialB) {
            // If the initial position of the first genomic region is greater than the initial position of the second one, the first one is considered greater.
            // A:     [------
            // B: [----
            return 1;
        } else {
            // Otherwise, the initial position is equal:
            // A: [-----
            // B: [----
            // Then, decide based on the final positions.
            if (finalA < finalB) {
                // If the final position of the first region is smaller than the final position of the second one, the first one is considered smaller.
                // A: [--//--]
                // B: [--//----]
                return -1;
            } else if (finalA > finalB) {
                // If the final position of the first region is greater than the final position of the second one, the first one is considered greater.
                // A: [--//-----]
                // B: [--//--]
                return 1;
            } else {
                // Otherwise, the name of the genomic region, the initial position, and the final position are all equal.
                // Then, the regions are considered equal, as well.
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
 * Compute the intersection of two genomic region sets.
 * The region sets have to be sorted and passed as three arrays: the chromsome names of the genomic regions, the initial positions of the genomic regions, and the final positions of the genomic regions.
 * The number of genomic regions per set has to be passed as well.
 *
 * @param const char **chromsA An array of the chromosome names of the genomic regions of the first set.
 * @param const int *initialsA An array of the initial positions of the genomic regions of the first set.
 * @param comst int *finalsA   An array of the final positions of the genomic regions of the first set.
 * @param const int sizeA      The number of genomic regions in the first set.
 * @param const char **chromsB An array of the chromosome names of the genomic regions of the second set.
 * @param const int *initialsB An array of the initial positions of the genomic regions of the second set.
 * @param const int *finalsB   An array of the final positions of the genomic regions of the second set.
 * @param const int sizeB      The number of genomic regions in the second set.
 * @param int **indicesR       Used to return the result. An array for the indices of genomic regions of the first set, holding the meta data which should be attached to the corresponding genomic region of the result set.
 * @param int **initialsR      Used to return the result. The initial positions of the genomic regions of the result set.
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
    int i = 0; // iter_a = iter(a); s = iter_a.next()
    int j = 0;
    int k = 0;
    const int last_j = sizeB - 1;
    bool cont_loop = true;
    int pre_inter = 0;
    bool cont_overlap = false;
    //printf("sizeA=%d\n", sizeA);
    while (cont_loop) {
        //printf("i=%d\n", i);
        if (overlap(chromsA[i], initialsA[i], finalsA[i], chromsB[i], initialsB[j], finalsB[j])) {
            (*indicesR)[k] = i;
            (*initialsR)[k] = max(initialsA[i], initialsB[j]);
            (*finalsR)[k] = min(finalsA[i], finalsB[j]);
            k++;
            printf("Added genomic region to result set: %s[%d, %d]\n\n", chromsA[i], max(initialsA[i], initialsB[j]), min(finalsA[i], finalsB[j]));
            if (!cont_overlap) {
                pre_inter = j;
            }
            if (j == last_j) {
                if (i < sizeA-1) {
                    //printf("i increased (A)\n");
                    i++;
                } else {
                    cont_loop = false;
                }
            } else {
                j++;
            }
            cont_overlap = true;
        } else if (compareGenomicRegions(chromsA[i], initialsA[i], finalsA[i], chromsB[i], initialsB[j], finalsB[j]) < 0) {
            if (i < sizeA-1) {
                //printf("i increased (B)\n");
                i++;
                if ((strcmp(chromsA[i], chromsB[j]) == 0) && (pre_inter > 0)) {
                    j = pre_inter;
                }
                cont_overlap = false;
            } else {
                cont_loop = false;
            }
        } else if (compareGenomicRegions(chromsA[i], initialsA[i], finalsA[i], chromsB[i], initialsB[j], finalsB[j]) > 0) {
            if (j == last_j) {
                cont_loop = false;
            } else {
                j++;
                cont_overlap = false;
            }
        } else {
            if (i < sizeA-1) {
                //printf("i increased (C)\n");
                i++;
            } else {
                cont_loop = false;
            }
        }
    }
    printf("Result contain  %d GenomicRegion\n", k);
    *sizeR = k;
}




/* From example */
/*
char *
test_get_data(unsigned int len)
{
    return malloc(len);
}

char *
test_get_data_nulls(int *len)
{
    *len = 5;
    char *d = malloc(5);
    d[0] = 'a';
    d[1] = 'b';
    d[2] = '\0';
    d[3] = 'c';
    d[4] = '\0';
    return d;
}

void
test_data_print(char *data, int len)
{
    int i;
    for (i = 0; i < len; i++)
        printf("%x (%c),",data[i],data[i]);
    printf("\n");
}

void
test_get_data_nulls_out(char **data, int *len)
{
    *data = test_get_data_nulls(len);
}

void
test_get_fixed_array_size_2(double *data)
{
    data[0] = 1.0;
    data[1] = 2.0;
}
*/
