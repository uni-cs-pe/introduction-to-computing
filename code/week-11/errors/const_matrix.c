// const en un parámetro matriz: gcc lo acepta, pero C17 no lo permite.
#include <stdio.h>

#define COLS 3

int first(const int m[][COLS]) {
    return m[0][0];
}

int main(void) {
    int m[2][COLS] = {{1, 2, 3}, {4, 5, 6}};

    printf("%d\n", first(m));
    return 0;
}
