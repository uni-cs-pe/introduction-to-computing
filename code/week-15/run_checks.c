// Parte de make test-lab: corre un solo grupo de pruebas de tests.c.
#include <stdio.h>
#include <string.h>

void check_is_prime(void);
void check_max_of_array(void);
void check_copy_text(void);

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "uso: run_checks prime|max|copy\n");
        return 2;
    }
    if (strcmp(argv[1], "prime") == 0) {
        check_is_prime();
    } else if (strcmp(argv[1], "max") == 0) {
        check_max_of_array();
    } else if (strcmp(argv[1], "copy") == 0) {
        check_copy_text();
    } else {
        return 2;
    }
    return 0;
}
