// Suma 1 a un int leído con scanf. Con INT_MAX se produce overflow.
#include <stdio.h>

int main(void) {
    int n = 0;
    int read_count = scanf("%d", &n);
    printf("scanf leyó %d dato(s), n = %d\n", read_count, n);

    int next = n + 1;
    printf("n + 1 = %d\n", next);
    return 0;
}
