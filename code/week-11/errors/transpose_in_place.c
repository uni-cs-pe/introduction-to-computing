// Error: al transponer en el mismo arreglo, cada par se cambia dos veces.
#include <stdio.h>

#define N 3

void transpose_wrong(int m[][N]) {
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            int saved = m[i][j];
            m[i][j] = m[j][i];
            m[j][i] = saved;
        }
    }
}

int main(void) {
    int m[N][N] = {{1, 2, 3}, {4, 5, 6}, {7, 8, 9}};

    transpose_wrong(m);
    for (int i = 0; i < N; i++) {
        printf("%d %d %d\n", m[i][0], m[i][1], m[i][2]);
    }
    return 0;
}
