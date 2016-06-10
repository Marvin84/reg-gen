#ifndef _LIBRGT_H_
#define _LIBRGT_H_

/*
char *
test_get_data(unsigned int len);

char *
test_get_data_nulls(int *len);

void
test_data_print(char *data, int len);

void
test_get_data_nulls_out(char **data, int *len);

void
test_get_fixed_array_size_2(double *data);
*/

bool overlap(const char *chromA, const int initialA, const int finalA, const char *chromB, const int initialB, const int finalB);

int compareGenomicRegions(const char *chromA, const int initialA, const int finalA, const char *chromB, const int initialB, const int finalB);

void intersectGenomicRegionSetsOverlap (
    const char **chromsA,
    const int *initialsA,
    const int *finalsA,
    const int sizeA,
    const char **chromsB,
    const int *initialsB,
    const int *finalsB,
    const int sizeB,
    inr** indicesR,
    int** initialsR,
    int** finalsR,
    int* sizeR
)

#endif // _LIBRGT_H_
