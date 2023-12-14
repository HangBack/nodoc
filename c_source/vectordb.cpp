#include "vectordb.h"
#include <stdio.h>

int search(double *query_matrix, double *query_text, int rows, int columns)
{
    double curr, large;
    int index = 0;
    for (int i = 0; i < rows; i++)
    {
        curr = scalar_product(query_matrix, query_text, i, columns);
        if (curr > large)
        {
            large = curr;
            index = i;
        }
    }
    // printf(" last: %lf\n curr: %lf\n i: %d\n rows: %d\n index: %d\n", last, curr, i, rows, index);
    return index;
}

double scalar_product(double *a, double *b, int now_row, int columns)
{
    double scalar = 0;
    for (int j = 0, i = now_row * columns; j < columns; j++, i++)
        scalar += a[i] * b[j];
    return scalar;
}