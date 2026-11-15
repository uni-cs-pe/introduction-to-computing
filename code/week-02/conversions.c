// Conversiones entre int y double, automáticas y pedidas con un cast.
#include <stdio.h>

int main(void) {
    int sum = 7;
    int count = 2;

    double late = sum / count;              // divide enteros y luego convierte
    double cast_first = (double) sum / count;
    double cast_late = (double) (sum / count);
    double from_int = count;                // de int a double: 2.0

    int truncated = 3.99;                   // de double a int: se pierden los decimales
    int cast_positive = (int) 3.99;
    int cast_negative = (int) -3.99;

    printf("sum / count = %f\n", late);
    printf("(double) sum / count = %f\n", cast_first);
    printf("(double) (sum / count) = %f\n", cast_late);
    printf("from_int = %f\n", from_int);
    printf("truncated = %d\n", truncated);
    printf("(int) 3.99 = %d\n", cast_positive);
    printf("(int) -3.99 = %d\n", cast_negative);
    return 0;
}
