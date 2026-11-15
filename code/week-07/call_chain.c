#include <stdio.h>

int square(int x) {
    int result = x * x;
    return result;
}

int sum_of_squares(int a, int b) {
    int first = square(a);
    int second = square(b);
    return first + second;
}

int main(void) {
    int total = sum_of_squares(3, 4);
    printf("%d\n", total);
    return 0;
}
