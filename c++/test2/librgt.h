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

bool
overlap(const char *chromA, const int initialA, const int finalA, const char *chromB, const int initialB, const int finalB);