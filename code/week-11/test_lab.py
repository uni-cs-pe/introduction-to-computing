"""Pruebas del laboratorio. LAB_DIR dice dónde está el código: lab o solution."""
import os
import pathlib
import re
import subprocess
import tempfile
import unittest

HERE = pathlib.Path(__file__).parent
LAB_DIR = os.environ.get("LAB_DIR", "solution")

# Cuatro filas de tres cursos. Las notas 99 están en una fila que no se usa: solo importan
# si la función lee más filas de las que recibió.
GRADES = [14, 9, 17,
          11, 16, 8,
          18, 10, 15,
          12, 20, 7]
THREE_ROWS = [14, 9, 17,
              11, 16, 8,
              18, 10, 15,
              99, 99, 99]
TIED = [14, 0, 20,
        14, 0, 20,
        10, 0, 5,
        13, 0, 20]
TRANSPOSED = [14, 11, 18, 12,
              9, 16, 10, 20,
              17, 8, 15, 7]


def run(program):
    done = subprocess.run(
        [str(HERE / "build" / LAB_DIR / program)], encoding="utf-8", errors="replace",
        stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=10,
    )
    return done.stdout, done.returncode


def call(*args):
    """Llama a una función con check_lab y devuelve lo que imprime, sin los bordes."""
    done = subprocess.run(
        [str(HERE / "build" / LAB_DIR / "check_lab")] + [str(a).encode("utf-8") for a in args],
        stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=10,
    )
    return done.stdout.decode("utf-8", "replace").strip()


def code_without_comments(name):
    text = (HERE / LAB_DIR / name).read_text(encoding="utf-8")
    return re.sub(r"//[^\n]*", "", text)


@unittest.skipUnless((HERE / LAB_DIR).is_dir(), f"no existe {LAB_DIR}/")
class LabTests(unittest.TestCase):
    def test_no_warnings(self):
        # Se compila de verdad: algunas advertencias no salen solo revisando la sintaxis.
        with tempfile.TemporaryDirectory() as folder:
            for name in ["words", "grades"]:
                with self.subTest(name=name):
                    done = subprocess.run(
                        ["gcc", "-Wall", "-Wextra", "-std=c17", "-Werror", "-c",
                         str(HERE / LAB_DIR / f"{name}.c"), "-o", f"{folder}/{name}.o"],
                        text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                    )
                    self.assertEqual(done.returncode, 0, done.stdout)

    def test_your_own_asserts_pass(self):
        for name in ["words", "grades"]:
            with self.subTest(name=name):
                self.assertEqual(run(name), ("Todas las pruebas pasaron\n", 0))

    def test_count_word_uses_strstr(self):
        self.assertRegex(code_without_comments("words.c"), r"\bstrstr\s*\(")

    def test_grades_main_checks_with_assert(self):
        self.assertRegex(code_without_comments("grades.c"), r"assert\s*\(\s*is_transpose\s*\(")

    def test_constants_were_not_changed(self):
        code = code_without_comments("grades.c")
        self.assertRegex(code, r"#define\s+STUDENTS\s+4\b")
        self.assertRegex(code, r"#define\s+COURSES\s+3\b")

    def test_count_word(self):
        cases = [
            ("sol y luna", "sol", "1"),
            ("sol y sol", "sol", "2"),
            ("luna y sol", "sol", "1"),      # al final
            ("sol", "sol", "1"),             # el texto completo
            ("solsolsol", "sol", "3"),       # seguidas
            ("sol y luna", "mar", "0"),
            ("so", "sol", "0"),              # la palabra es más larga que el texto
            ("", "sol", "0"),
            ("Sol sol SOL", "sol", "1"),     # byte por byte
            ("girasol y sol", "sol", "2"),   # no hace falta una palabra completa
            ("banana", "ana", "1"),          # no se pisan
            ("aaaaa", "aa", "2"),
            ("año y ñandú", "ñ", "2"),       # bytes de UTF-8
        ]
        for text, word, expected in cases:
            with self.subTest(text=text, word=word):
                self.assertEqual(call("w", text, word), expected)

    def test_count_word_with_empty_word(self):
        for text in ["", "sol"]:
            with self.subTest(text=text):
                self.assertEqual(call("w", text, ""), "0")

    def test_student_averages(self):
        self.assertEqual(call("s", 4, *GRADES), "13.33 11.67 14.33 13.00")

    def test_student_averages_uses_the_rows_it_receives(self):
        # La cuarta casilla no se debe tocar: check_lab la deja en -1.
        self.assertEqual(call("s", 3, *THREE_ROWS), "13.33 11.67 14.33 -1.00")

    def test_course_averages(self):
        self.assertEqual(call("c", 4, *GRADES), "13.75 13.75 11.75")

    def test_course_averages_uses_the_rows_it_receives(self):
        self.assertEqual(call("c", 3, *THREE_ROWS), "14.33 11.67 13.33")
        self.assertEqual(call("c", 1, *THREE_ROWS), "14.00 9.00 17.00")

    def test_best_students(self):
        self.assertEqual(call("b", 4, *GRADES), "2 3 0")

    def test_best_students_uses_the_rows_it_receives(self):
        self.assertEqual(call("b", 3, *THREE_ROWS), "2 1 0")
        self.assertEqual(call("b", 1, *THREE_ROWS), "0 0 0")

    def test_best_students_ties_and_zeros(self):
        # Empates: gana el de índice menor. El curso 1 tiene solo ceros, y aun así hay mejor.
        self.assertEqual(call("b", 4, *TIED), "0 0 0")

    def test_best_students_restarts_in_each_course(self):
        # Si el máximo no se reinicia, el 20 del curso 0 tapa a los demás cursos.
        self.assertEqual(call("b", 4, 20, 1, 2, 3, 5, 6, 4, 9, 8, 7, 8, 9), "0 2 3")

    def test_transpose(self):
        expected = "14 11 18 12 \n9 16 10 20 \n17 8 15 7"
        self.assertEqual(call("t", 4, *GRADES), expected)

    def test_is_transpose_accepts_the_right_one(self):
        self.assertEqual(call("i", 4, *GRADES, *TRANSPOSED), "1")

    def test_is_transpose_finds_any_wrong_cell(self):
        for position in [0, 5, 11]:
            wrong = list(TRANSPOSED)
            wrong[position] = 0
            with self.subTest(position=position):
                self.assertEqual(call("i", 4, *GRADES, *wrong), "0")

    def test_is_transpose_rejects_the_same_values_in_rows(self):
        # Las mismas notas sin transponer: fila por fila, igual que grades.
        self.assertEqual(call("i", 4, *GRADES, *GRADES), "0")


if __name__ == "__main__":
    unittest.main()
