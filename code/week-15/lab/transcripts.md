# Transcripciones para la actividad guiada

Úsenlas si en el laboratorio no hay un asistente permitido o no hay internet.

**Son ejemplos escritos para esta actividad. No son la salida real de ningún asistente.** Sirven
para practicar lo mismo que con uno real: leer la respuesta sin creerla, y comprobarla. Las salidas de `gcc` y de los programas
que aparecen aquí sí son reales, del entorno del curso.

Con cada transcripción, sigan los pasos de la hoja `lab/activity_sheet.md`. El código está en
`lab/transcripts/`. Sin computadora, sigan la función a mano en papel, con una tabla de variables.

## Transcripción A (ejemplo escrito para la actividad)

**Estudiante:** Escribe en C una función que cuente cuántas notas de un arreglo están aprobadas.
Se aprueba con 11 o más, en escala de 0 a 20.

**Asistente:** Claro. Esta función es correcta para cualquier arreglo de notas:

```c
int count_passing(const int grades[], int n) {
    int count = 0;
    for (int i = 0; i < n; i++) {
        if (grades[i] > 11) {
            count++;
        }
    }
    return count;
}
```

Y aquí tienes una prueba, que pasa:

```c
int grades[5] = {14, 9, 17, 8, 20};
assert(count_passing(grades, 5) == 3);
```

**Salida real** con `lab/transcripts/count_passing.c`:

```text
Pruebas pasadas
```

**Para ustedes:** ¿basta con esa prueba? Escojan notas que busquen un error, y sigan la función a mano.

## Transcripción B (ejemplo escrito para la actividad)

**Estudiante:** Escribe en C una función que cuente cuántas veces aparece un byte en una cadena.

**Asistente:** Aquí está. Recorre la cadena hasta el `'\0'`:

```c
int count_char(const char s[], char c) {
    int count = 0;
    for (int i = 0; s[i] != '\0'; i++) {
        if (s[i] == c) {
            count++;
        }
    }
    return count;
}
```

```c
assert(count_char("banana", 'a') == 3);
```

**Salida real** con `lab/transcripts/count_char.c`:

```text
Pruebas pasadas
```

**Para ustedes:** ¿qué casos faltan por probar? Piensen en la cadena vacía, en un byte que no aparece y en
uno que está al principio o al final. Decidan si encuentran un error. No todas las respuestas lo tienen,
y sus pruebas deben poder decir eso también, hasta donde pueden: una prueba muestra lo que pasa solo en los casos que revisa.

## Transcripción C (ejemplo escrito para la actividad)

**Estudiante:** ¿Cómo invierto una cadena en C?

**Asistente:** Es muy fácil. La biblioteca estándar lo trae en `string.h`:

```c
char word[] = "hola";
strrev(word);
printf("%s\n", word);
```

**Salida real** de `gcc -Wall -Wextra -std=c17 -g -fsanitize=address,undefined` con `lab/transcripts/reverse_text.c`:

```text
lab/transcripts/reverse_text.c: In function ‘main’:
lab/transcripts/reverse_text.c:7:5: error: implicit declaration of function ‘strrev’; did you mean ‘strlen’? [-Wimplicit-function-declaration]
    7 |     strrev(word);
      |     ^~~~~~
      |     strlen
```

**Para ustedes:** ¿qué dice el mensaje? `strrev` no es parte del estándar de C, aunque la respuesta sonaba
segura y algunos entornos la traen como extra. Escriban la función a mano. En la semana 10 hay un ejercicio que la pide.
