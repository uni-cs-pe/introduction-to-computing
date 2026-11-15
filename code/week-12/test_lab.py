"""Pruebas del laboratorio. LAB_DIR dice dónde está el código: lab o solution."""
import os
import pathlib
import resource
import shutil
import subprocess
import tempfile
import unittest

HERE = pathlib.Path(__file__).parent
LAB_DIR = os.environ.get("LAB_DIR", "solution")
SOURCE = HERE / LAB_DIR / "process_students.c"
CHECK = HERE / "build" / LAB_DIR / "check_students"
PROGRAM = HERE / "build" / LAB_DIR / "process_students"
TOO_MANY = "Demasiados estudiantes: solo se leen 4"


def malformed(number):
    return f"Línea {number}: mal formada, se omite\n"


def few_open_files():
    # Con este límite, un programa que no cierra sus archivos se queda sin poder abrir.
    resource.setrlimit(resource.RLIMIT_NOFILE, (64, 64))


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = pathlib.Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)

    def write(self, name, text):
        (self.tmp / name).write_bytes(text.encode("utf-8"))
        return name

    def call(self, *args, limit=False):
        """Llama a una función. Devuelve (salida, errores, estado)."""
        done = subprocess.run(
            [str(CHECK), *args], cwd=self.tmp, encoding="utf-8", errors="replace",
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=20,
            preexec_fn=few_open_files if limit else None,
        )
        return done.stdout, done.stderr, done.returncode

    def program(self, stdin):
        """Corre el programa completo dentro de la carpeta temporal."""
        done = subprocess.run(
            [str(PROGRAM)], input=stdin, cwd=self.tmp, encoding="utf-8", errors="replace",
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=20,
        )
        return done.stdout, done.stderr, done.returncode

    def output_file(self, name="salida.txt"):
        return (self.tmp / name).read_text(encoding="utf-8")


@unittest.skipUnless((HERE / LAB_DIR).is_dir(), f"no existe {LAB_DIR}/")
class Functions(Base):
    def test_no_warnings(self):
        done = subprocess.run(
            ["gcc", "-Wall", "-Wextra", "-std=c17", "-Werror", "-fsyntax-only", str(SOURCE)],
            text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        )
        self.assertEqual(done.returncode, 0, done.stdout)

    def test_read_line(self):
        # El programa de prueba usa un buffer de 8 bytes: caben 7 bytes de texto.
        cases = {
            "Ana\n": 'ok "Ana"\nend\n',
            "Ana": 'ok "Ana"\nend\n',
            "": "end\n",
            "\n": 'ok ""\nend\n',
            "Rosaura\nLi\n": 'ok "Rosaura"\nok "Li"\nend\n',
            "Rosaura": 'ok "Rosaura"\nend\n',
            "Alejandra\nLi\n": 'long\nok "Li"\nend\n',
            "Alejandr\nLi\n": 'long\nok "Li"\nend\n',
            "Alejandra": "long\nend\n",
            "uno\ndos\n": 'ok "uno"\nok "dos"\nend\n',
        }
        for text, expected in cases.items():
            with self.subTest(text=text):
                self.write("datos.txt", text)
                self.assertEqual(self.call("line", "datos.txt"), (expected, "", 0))

    def test_parse_valid_lines(self):
        cases = {
            "Ana 14 9 17": "Ana 14 9 17",
            "  Ana   14 9   17  ": "Ana 14 9 17",
            "Begoña 0 20 10": "Begoña 0 20 10",
            "abcdefghijklmnopqrs 1 2 3": "abcdefghijklmnopqrs 1 2 3",
        }
        for line, expected in cases.items():
            with self.subTest(line=line):
                self.assertEqual(self.call("parse", line), (f"1\n{expected}\n", "", 0))

    def test_parse_invalid_lines(self):
        lines = ["", "   ", "Ana", "Ana 14", "Ana 14 9", "Ana diez 9 17", "Ana 14.5 9 17",
                 "Ana 14 9 17 5", "Ana 14 9 17 x", "Ana 21 9 17", "Ana 14 9 21", "Ana 14 -1 17",
                 "abcdefghijklmnopqrst 1 2 3"]
        for line in lines:
            with self.subTest(line=line):
                self.assertEqual(self.call("parse", line), ("0\n", "", 0))

    def test_average_has_decimals(self):
        cases = {("14", "9", "17"): "13.3333", ("10", "11", "12"): "11.0000",
                 ("0", "0", "1"): "0.3333", ("0", "0", "0"): "0.0000", ("20", "20", "20"): "20.0000"}
        for grades, expected in cases.items():
            with self.subTest(grades=grades):
                self.assertEqual(self.call("average", *grades), (expected + "\n", "", 0))

    def test_is_passed(self):
        cases = {("11", "11", "11"): "1", ("10", "11", "12"): "1", ("20", "13", "0"): "1",
                 ("11", "11", "10"): "0", ("12", "10", "10"): "0", ("0", "0", "0"): "0"}
        for grades, expected in cases.items():
            with self.subTest(grades=grades):
                self.assertEqual(self.call("passed", *grades), (expected + "\n", "", 0))

    def test_read_students(self):
        self.write("datos.txt", "Ana 14 9 17\nBruno 8 10 11\n")
        self.assertEqual(self.call("read", "datos.txt"),
                         ("2\nAna 14 9 17\nBruno 8 10 11\n", "", 0))

    def test_read_last_line_without_newline(self):
        self.write("datos.txt", "Ana 14 9 17\nBruno 8 10 11")
        self.assertEqual(self.call("read", "datos.txt"),
                         ("2\nAna 14 9 17\nBruno 8 10 11\n", "", 0))

    def test_read_empty_file(self):
        self.write("datos.txt", "")
        self.assertEqual(self.call("read", "datos.txt"), ("0\n", "", 0))

    def test_read_missing_file(self):
        output, errors, status = self.call("read", "no_hay.txt")
        self.assertEqual((output, status), ("-1\n", 0))
        self.assertTrue(errors.startswith("no_hay.txt: "), errors)

    def test_read_numbers_the_bad_lines(self):
        self.write("datos.txt", "Ana 14 9 17\nmal\n\nBruno 8 10 11\nCarla 11 11\n")
        self.assertEqual(self.call("read", "datos.txt"), (
            "2\nAna 14 9 17\nBruno 8 10 11\n", malformed(2) + malformed(3) + malformed(5), 0))

    def test_read_long_line_is_one_bad_line(self):
        # Lo que no cupo parece una línea válida: no debe leerse como otro estudiante.
        self.write("datos.txt", "x" * 70 + " Zoila 11 11 11\nAna 14 9 17\nmal\n")
        self.assertEqual(self.call("read", "datos.txt"),
                         ("1\nAna 14 9 17\n", malformed(1) + malformed(3), 0))

    def test_read_long_line_that_would_look_valid_if_cut(self):
        # Los primeros bytes forman una línea válida, pero la línea completa no lo es.
        self.write("datos.txt", "Ana 14 9 17" + " " * 60 + "basura\nBruno 8 10 11\n")
        self.assertEqual(self.call("read", "datos.txt"),
                         ("1\nBruno 8 10 11\n", malformed(1), 0))

    def test_read_exact_capacity_gives_no_warning(self):
        lines = [f"E{i} 11 11 11" for i in range(4)]
        self.write("datos.txt", "\n".join(lines) + "\n")
        self.assertEqual(self.call("read", "datos.txt"),
                         ("4\n" + "\n".join(lines) + "\n", "", 0))

    def test_read_does_not_pass_the_capacity(self):
        lines = [f"E{i} 11 11 11" for i in range(6)]
        self.write("datos.txt", "\n".join(lines) + "\n")
        output, errors, status = self.call("read", "datos.txt")
        self.assertEqual(status, 0, errors)
        self.assertEqual(output, "4\n" + "\n".join(lines[:4]) + "\n")
        self.assertEqual(errors.count(TOO_MANY), 1, errors)

    def test_read_closes_the_file(self):
        self.write("datos.txt", "Ana 14 9 17\n")
        self.assertEqual(self.call("many", "datos.txt", limit=True), ("200\n", "", 0))

    def test_write_closes_and_keeps_only_passed(self):
        self.assertEqual(self.call("write", "salida.txt"),
                         ("2\nAna 13.33\nCarla 11.00\n", "", 0))

    def test_write_replaces_the_old_file(self):
        self.write("salida.txt", "algo viejo\n")
        self.assertEqual(self.call("write", "salida.txt")[0], "2\nAna 13.33\nCarla 11.00\n")

    def test_write_cannot_open(self):
        output, errors, status = self.call("write", "no_hay/salida.txt")
        self.assertEqual((output, status), ("-1\n", 0))
        self.assertTrue(errors.startswith("no_hay/salida.txt: "), errors)


@unittest.skipUnless((HERE / LAB_DIR).is_dir(), f"no existe {LAB_DIR}/")
class WholeProgram(Base):
    def setUp(self):
        super().setUp()
        for name in ["estudiantes.txt", "estudiantes_vacio.txt", "estudiantes_malos.txt"]:
            shutil.copy(HERE / name, self.tmp / name)

    def test_student_file(self):
        self.assertEqual(self.program("estudiantes.txt\nsalida.txt\n"),
                         ("Leídos: 8. Aprobados: 5.\n", "", 0))
        self.assertEqual(self.output_file(),
                         "Ana 13.33\nCarla 11.00\nElena 19.00\nBegoña 13.67\nGisela 11.00\n")

    def test_file_with_bad_lines(self):
        warnings = "".join(malformed(n) for n in [2, 3, 5, 6, 7])
        self.assertEqual(self.program("estudiantes_malos.txt\nsalida.txt\n"),
                         ("Leídos: 3. Aprobados: 2.\n", warnings, 0))
        self.assertEqual(self.output_file(), "Ana 13.33\nGisela 11.00\n")

    def test_no_one_passed(self):
        self.write("datos.txt", "Ana 1 2 3\n")
        self.assertEqual(self.program("datos.txt\nsalida.txt\n"),
                         ("Leídos: 1. Aprobados: 0.\n", "", 0))
        self.assertEqual(self.output_file(), "")

    def test_more_students_than_capacity(self):
        self.write("datos.txt", "".join(f"E{i} 11 11 11\n" for i in range(60)))
        output, errors, status = self.program("datos.txt\nsalida.txt\n")
        self.assertEqual((output, status), ("Leídos: 50. Aprobados: 50.\n", 0), errors)
        self.assertEqual(errors, "Demasiados estudiantes: solo se leen 50\n")
        self.assertEqual(len(self.output_file().splitlines()), 50)

    def test_missing_file_keeps_the_old_output(self):
        self.write("salida.txt", "resultado anterior\n")
        output, errors, status = self.program("no_hay.txt\nsalida.txt\n")
        self.assertEqual((output, status), ("", 1))
        self.assertTrue(errors.startswith("no_hay.txt: "), errors)
        self.assertEqual(self.output_file(), "resultado anterior\n")

    def test_empty_file_creates_nothing(self):
        self.assertEqual(self.program("estudiantes_vacio.txt\nsalida.txt\n"),
                         ("", "estudiantes_vacio.txt: no hay estudiantes\n", 1))
        self.assertFalse((self.tmp / "salida.txt").exists())

    def test_only_bad_lines(self):
        self.write("datos.txt", "mal\n")
        self.assertEqual(self.program("datos.txt\nsalida.txt\n"),
                         ("", malformed(1) + "datos.txt: no hay estudiantes\n", 1))
        self.assertFalse((self.tmp / "salida.txt").exists())

    def test_output_cannot_be_created(self):
        output, errors, status = self.program("estudiantes.txt\nno_hay/salida.txt\n")
        self.assertEqual((output, status), ("", 1))
        self.assertTrue(errors.startswith("no_hay/salida.txt: "), errors)

    def test_missing_names(self):
        for stdin in ["", "estudiantes.txt\n"]:
            with self.subTest(stdin=stdin):
                self.assertEqual(self.program(stdin),
                                 ("", "Faltan los nombres de los archivos\n", 1))


if __name__ == "__main__":
    unittest.main()
