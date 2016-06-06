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
 *  First compare the chromosome, then the initial position and finally the final position.
 */
int compareGenomicRegions(
    const char *chromA,
    const int initialA,
    const int finalA,
    const char *chromB,
    const int initialB,
    const int finalB
) {
    const int chromComp = strcmp(chromA, chromB);
    if (chromComp != 0) {
        return chromComp;
    } else {
        if (initialA < initialB) {
            return -1;
        } else if (initialA > initialB) {
            return 1;
        } else {
            if (finalA < finalB) {
                return -1;
            } else if (finalA > finalB) {
                return 1;
            } else {
                return 0;
            }
        }
    }
}

const int min(const int a, const int b) {
    if (a < b) {
        return a;
    } else {
        return b;
    }
}

const int max(const int a, const int b) {
    if (a > b) {
        return a;
    } else {
        return b;
    }
}


/**
 * RegionSets have to be sorted
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
    char*** chromsR,
    int** initialsR,
    int** finalsR,
    int* sizeR
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
            (*chromsR)[k] = chromsA[i];
            (*initialsR)[k] = max(initialsA[i], initialsB[j]);
            (*finalsR)[k] = min(finalsA[i], finalsB[j]);
            k++;
            /* TODO: add to result
            z.add( GenomicRegion(chrom=s.chrom,
                                              initial=max(s.initial, b[j].initial),
                                              final=min(s.final, b[j].final),
                                              name=s.name,
                                              orientation=s.orientation,
                                              data=s.data,
                                              proximity=s.proximity) )
            */
            // printf("Overlapping regions: [%d,%d] and [%d, %d]\n", initialsA[i],finalsA[i],initialsB[j],finalsB[j]);
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