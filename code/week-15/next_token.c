// Un modelo de lenguaje de juguete. Cuenta en corpus.txt qué palabra viene después de
// cada palabra. Para continuar un texto, elige siempre la siguiente más frecuente, y
// en un empate, la que apareció primero. Lee de la entrada un texto inicial por línea.
#include <stdio.h>
#include <string.h>

#define MAX_LINE 200
#define MAX_WORD 32
#define MAX_PAIRS 100
#define MAX_STEPS 12

struct pair {
    char first[MAX_WORD];
    char second[MAX_WORD];
    int count;
};

// Copia en word la palabra que empieza en line[start] o después.
// Devuelve la posición donde sigue la línea, o -1 si ya no hay palabras.
int read_word_at(const char line[], int start, char word[], int size) {
    int i = start;
    while (line[i] == ' ' || line[i] == '\n') {
        i++;
    }
    if (line[i] == '\0') {
        return -1;
    }
    int length = 0;
    while (line[i] != '\0' && line[i] != ' ' && line[i] != '\n') {
        if (length < size - 1) {
            word[length] = line[i];
            length++;
        }
        i++;
    }
    word[length] = '\0';
    return i;
}

// Suma 1 al par (first, second), o lo agrega. Devuelve el nuevo número de pares.
int add_pair(struct pair pairs[], int n, const char first[], const char second[]) {
    for (int i = 0; i < n; i++) {
        if (strcmp(pairs[i].first, first) == 0 && strcmp(pairs[i].second, second) == 0) {
            pairs[i].count++;
            return n;
        }
    }
    if (n == MAX_PAIRS) {
        return n;
    }
    strcpy(pairs[n].first, first);
    strcpy(pairs[n].second, second);
    pairs[n].count = 1;
    return n + 1;
}

// Entrenar es contar. Devuelve cuántos pares distintos hay, o -1 si no hay archivo.
int train(const char path[], struct pair pairs[]) {
    FILE *file = fopen(path, "r");
    if (file == NULL) {
        perror(path);
        return -1;
    }
    int n = 0;
    char line[MAX_LINE];
    while (fgets(line, MAX_LINE, file) != NULL) {
        char previous[MAX_WORD];
        char word[MAX_WORD];
        int position = read_word_at(line, 0, previous, MAX_WORD);
        while (position != -1) {
            position = read_word_at(line, position, word, MAX_WORD);
            if (position != -1) {
                n = add_pair(pairs, n, previous, word);
                strcpy(previous, word);
            }
        }
    }
    fclose(file);
    return n;
}

// Devuelve la posición del par más frecuente que empieza con word, o -1 si no hay.
int most_frequent(const struct pair pairs[], int n, const char word[]) {
    int best = -1;
    for (int i = 0; i < n; i++) {
        if (strcmp(pairs[i].first, word) == 0) {
            if (best == -1 || pairs[i].count > pairs[best].count) {
                best = i;
            }
        }
    }
    return best;
}

void print_counts(const struct pair pairs[], int n, const char word[]) {
    int total = 0;
    for (int i = 0; i < n; i++) {
        if (strcmp(pairs[i].first, word) == 0) {
            total = total + pairs[i].count;
        }
    }
    printf("tras \"%s\":", word);
    for (int i = 0; i < n; i++) {
        if (strcmp(pairs[i].first, word) == 0) {
            printf(" %s %d/%d", pairs[i].second, pairs[i].count, total);
        }
    }
    printf("\n");
}

// Continúa el texto desde word, hasta el punto o hasta MAX_STEPS palabras.
void generate(const struct pair pairs[], int n, const char word[]) {
    char current[MAX_WORD];
    strcpy(current, word);
    int steps = 0;
    while (strcmp(current, ".") != 0 && steps < MAX_STEPS) {
        int best = most_frequent(pairs, n, current);
        if (best == -1) {
            printf(" [sin datos]");
            return;
        }
        printf(" %s", pairs[best].second);
        strcpy(current, pairs[best].second);
        steps++;
    }
}

int main(void) {
    struct pair pairs[MAX_PAIRS];
    int n = train("corpus.txt", pairs);
    if (n == -1) {
        return 1;
    }

    char line[MAX_LINE];
    while (fgets(line, MAX_LINE, stdin) != NULL) {
        char last[MAX_WORD];
        char word[MAX_WORD];
        int position = read_word_at(line, 0, word, MAX_WORD);
        if (position == -1) {
            continue;
        }
        while (position != -1) {
            strcpy(last, word);
            position = read_word_at(line, position, word, MAX_WORD);
        }
        print_counts(pairs, n, last);
        line[strcspn(line, "\n")] = '\0';
        printf("%s", line);
        generate(pairs, n, last);
        printf("\n");
    }
    return 0;
}
