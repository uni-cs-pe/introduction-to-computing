// Una neurona artificial con dos entradas. Sus pesos se ajustan con los ejemplos:
// cada error mueve los pesos un poco hacia la respuesta correcta.
// Usa enteros para poder seguirla a mano.
#include <stdio.h>

#define MAILS 4
#define MAX_ROUNDS 10

struct example {
    int words;   // palabras sospechosas
    int links;   // enlaces
    int spam;    // la etiqueta
};

struct neuron {
    int w_words;
    int w_links;
    int base;
};

int score(struct neuron n, int words, int links) {
    return n.w_words * words + n.w_links * links + n.base;
}

int predict(struct neuron n, int words, int links) {
    return score(n, words, links) > 0;
}

int main(void) {
    struct example examples[MAILS] = {{3, 2, 1}, {1, 0, 0}, {2, 2, 1}, {0, 1, 0}};
    struct neuron n = {0, 0, 0};

    printf("vuelta correo  puntaje resp etiq  w_pal w_enl  base\n");
    int errors = 1;
    int round = 0;
    while (errors > 0 && round < MAX_ROUNDS) {
        round++;
        errors = 0;
        for (int i = 0; i < MAILS; i++) {
            struct example e = examples[i];
            int answer = predict(n, e.words, e.links);
            int current = score(n, e.words, e.links);
            int change = e.spam - answer;   // 0 si acertó; +1 o -1 si se equivocó
            if (change != 0) {
                errors++;
            }
            n.w_words = n.w_words + change * e.words;
            n.w_links = n.w_links + change * e.links;
            n.base = n.base + change;
            printf("%6d (%d,%d) %8d %4d %4d %6d %5d %5d\n", round, e.words, e.links,
                   current, answer, e.spam, n.w_words, n.w_links, n.base);
        }
    }
    printf("Vueltas: %d. Errores en la última: %d\n", round, errors);
    return 0;
}
