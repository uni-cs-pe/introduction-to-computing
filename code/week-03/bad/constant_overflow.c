// Error a propósito: el compilador ve el overflow al compilar. No forma parte de make.
#include <limits.h>
#include <stdio.h>

int main(void) {
    int next = INT_MAX + 1;
    printf("%d\n", next);
    return 0;
}
