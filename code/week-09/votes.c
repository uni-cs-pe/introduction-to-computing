#include <stdio.h>

#define CANDIDATES 3

// Lee votos (1, 2 o 3) hasta un 0 y cuenta los de cada candidato.
int main(void) {
    int counts[CANDIDATES] = {0};
    int invalid = 0;
    int vote;

    if (scanf("%d", &vote) != 1) {
        printf("Entrada inválida\n");
        return 1;
    }
    while (vote != 0) {
        if (vote >= 1 && vote <= CANDIDATES) {
            counts[vote - 1]++;
        } else {
            invalid++;
        }
        if (scanf("%d", &vote) != 1) {
            printf("Entrada inválida\n");
            return 1;
        }
    }

    for (int i = 0; i < CANDIDATES; i++) {
        printf("Candidato %d: %d\n", i + 1, counts[i]);
    }
    printf("Inválidos: %d\n", invalid);
    return 0;
}
