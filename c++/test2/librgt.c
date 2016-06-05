#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <stdbool.h>

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
