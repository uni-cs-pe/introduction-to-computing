// Tres modelos para decidir si un correo es spam, a partir de un solo dato: cuántas
// palabras sospechosas tiene. Los correos son inventados para este ejemplo.
#include <stdio.h>

#define TRAIN_SIZE 11
#define TEST_SIZE 8
#define MAX_WORDS 9
#define HAND_THRESHOLD 2

struct mail {
    int words;   // palabras sospechosas
    int spam;    // la etiqueta: 1 si es spam, 0 si no
};

// Regla de umbral: es spam si tiene u palabras sospechosas o más.
int predict_threshold(int words, int u) {
    return words >= u;
}

// Cuenta los errores de la regla de umbral en un conjunto de correos.
int errors_threshold(const struct mail mails[], int n, int u) {
    int errors = 0;
    for (int i = 0; i < n; i++) {
        if (predict_threshold(mails[i].words, u) != mails[i].spam) {
            errors++;
        }
    }
    return errors;
}

// Entrenar: probar cada umbral y quedarse con el primero que comete menos errores.
int train_threshold(const struct mail mails[], int n) {
    int best_u = 0;
    int best_errors = errors_threshold(mails, n, 0);
    for (int u = 1; u <= MAX_WORDS; u++) {
        int errors = errors_threshold(mails, n, u);
        if (errors < best_errors) {
            best_errors = errors;
            best_u = u;
        }
    }
    return best_u;
}

// El memorizador copia la etiqueta del correo de entrenamiento más parecido.
// Si hay empate, se queda con el primero que encontró.
int predict_memorizer(const struct mail train[], int n, int words) {
    int best = 0;
    int best_distance = -1;
    for (int i = 0; i < n; i++) {
        int distance = train[i].words - words;
        if (distance < 0) {
            distance = -distance;
        }
        if (best_distance == -1 || distance < best_distance) {
            best_distance = distance;
            best = i;
        }
    }
    return train[best].spam;
}

int errors_memorizer(const struct mail train[], int n, const struct mail mails[], int m) {
    int errors = 0;
    for (int i = 0; i < m; i++) {
        if (predict_memorizer(train, n, mails[i].words) != mails[i].spam) {
            errors++;
        }
    }
    return errors;
}

int main(void) {
    struct mail train[TRAIN_SIZE] = {
        {0, 0}, {0, 0}, {1, 0}, {1, 0}, {2, 0}, {3, 0}, {4, 1}, {5, 1}, {6, 0}, {7, 1}, {8, 1},
    };
    struct mail test[TEST_SIZE] = {
        {0, 0}, {1, 0}, {2, 0}, {2, 0}, {3, 1}, {4, 1}, {6, 1}, {6, 1},
    };

    printf("Errores en entrenamiento según el umbral\n");
    for (int u = 0; u <= MAX_WORDS; u++) {
        printf("u = %d: %d\n", u, errors_threshold(train, TRAIN_SIZE, u));
    }
    int learned = train_threshold(train, TRAIN_SIZE);
    printf("Umbral aprendido: %d\n\n", learned);

    printf("%-22s %14s %10s\n", "Modelo", "entrenamiento", "prueba");
    printf("%-22s %11d/%d %8d/%d\n", "Regla a mano (u = 2)",
           errors_threshold(train, TRAIN_SIZE, HAND_THRESHOLD), TRAIN_SIZE,
           errors_threshold(test, TEST_SIZE, HAND_THRESHOLD), TEST_SIZE);
    printf("%-22s %11d/%d %8d/%d\n", "Umbral aprendido",
           errors_threshold(train, TRAIN_SIZE, learned), TRAIN_SIZE,
           errors_threshold(test, TEST_SIZE, learned), TEST_SIZE);
    printf("%-22s %11d/%d %8d/%d\n", "Memorizador",
           errors_memorizer(train, TRAIN_SIZE, train, TRAIN_SIZE), TRAIN_SIZE,
           errors_memorizer(train, TRAIN_SIZE, test, TEST_SIZE), TEST_SIZE);
    return 0;
}
