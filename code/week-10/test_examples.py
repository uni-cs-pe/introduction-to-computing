"""Comprueba lo que los apuntes afirman sobre los programas de la semana 10."""
import pathlib
import re
import subprocess
import tempfile
import unittest

HERE = pathlib.Path(__file__).parent
BUILD = HERE / "build"
FLAGS = ["-Wall", "-Wextra", "-std=c17"]
SANITIZE = ["-g", "-fsanitize=address,undefined"]


def execute(command, stdin=""):
    done = subprocess.run(
        command, input=stdin, encoding="utf-8", errors="replace",
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=10,
    )
    return done.stdout, done.returncode


def run(program, stdin=""):
    """Ejecuta un programa de build/; devuelve su salida (con errores) y su estado."""
    return execute([str(BUILD / program)], stdin)


def build_source(source, *extra):
    """Compila un archivo; devuelve los mensajes, el estado y el ejecutable."""
    out = pathlib.Path(tempfile.mkdtemp()) / pathlib.Path(source).stem
    done = subprocess.run(
        ["gcc", *FLAGS, *extra, source, "-o", str(out)], cwd=HERE, encoding="utf-8",
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
    )
    return done.stdout, done.returncode, out


class CleanCompile(unittest.TestCase):
    def test_examples_have_no_warnings(self):
        for source in sorted(HERE.glob("*.c")):
            with self.subTest(source=source.name):
                done = subprocess.run(
                    ["gcc", *FLAGS, "-Werror", "-fsyntax-only", str(source)],
                    text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                )
                self.assertEqual(done.returncode, 0, done.stdout)

    def test_string_h_is_not_used_yet(self):
        for source in list(HERE.glob("*.c")) + list((HERE / "errors").glob("*.c")):
            with self.subTest(source=source.name):
                self.assertNotIn("string.h", source.read_text(encoding="utf-8"))


class ArraysInFunctions(unittest.TestCase):
    def test_sum_uses_the_length_it_receives(self):
        self.assertEqual(run("sum_array"), (
            "Suma de las 5 notas: 71\nPromedio: 14.20\nSuma de las 3 primeras: 40\n", 0))

    def test_function_changes_array_but_not_int(self):
        self.assertEqual(run("bonus"), ("grade: 14\ngrades: 16 11 19\n", 0))

    def test_function_sees_the_same_address(self):
        output, _ = run("same_address")
        addresses = re.findall(r"0x[0-9a-f]+", output)
        self.assertEqual(len(addresses), 2)
        self.assertEqual(addresses[0], addresses[1])

    def test_sizeof_of_parameter(self):
        messages, status, binary = build_source("errors/sizeof_param.c")
        self.assertEqual(status, 0)
        self.assertEqual(messages.count("-Wsizeof-array-argument"), 2)
        output, _ = execute([str(binary)])
        sizes = re.findall(r"(\d+) bytes", output)
        self.assertEqual(sizes[0], "20")        # 5 int de 4 bytes en este entorno
        self.assertEqual(sizes[1], sizes[2])    # el 5 del parámetro no cambia nada
        self.assertNotEqual(sizes[1], "20")

    def test_const_is_enforced(self):
        messages, status, _ = build_source("errors/const_write.c")
        self.assertNotEqual(status, 0)
        self.assertIn("read-only location", messages)

    def test_const_accepts_a_normal_array(self):
        self.assertEqual(run("const_param"), ("Nota mayor: 20\n", 0))


class Vector(unittest.TestCase):
    def test_insert_and_remove_with_their_limits(self):
        expected = ["n = 3: 10 20 30", "n = 4: 10 99 20 30", "n = 5: 10 99 20 30 40",
                    "n = 5: 10 99 20 30 40", "n = 4: 99 20 30 40", "n = 3: 99 20 30",
                    "n = 3: 99 20 30"]
        output, status = run("vector")
        self.assertEqual((output.splitlines(), status), (expected, 0))

    def test_moving_from_the_start_loses_a_value(self):
        _, _, binary = build_source("errors/insert_wrong.c")
        self.assertEqual(execute([str(binary)])[0], " 10 99 20 20\n")


class Strings(unittest.TestCase):
    def test_array_sizes_and_bytes(self):
        output, _ = run("string_bytes")
        self.assertIn("sizeof(s) = 5\n", output)
        self.assertIn("s[4] = 0\n", output)
        self.assertIn("sizeof(t) = 8\n 104 111 108 97 0 0 0 0\n", output)
        self.assertIn("'\\0' vale 0 y '0' vale 48\n", output)

    def test_terminator_cuts_the_text_but_not_the_array(self):
        self.assertEqual(run("cut_string")[0], "hola\nHola\nHo\nsizeof(s) sigue siendo 5\n")

    def test_length_counts_bytes(self):
        output, status = run("my_strlen")     # sus assert también corren aquí
        self.assertEqual(status, 0)
        self.assertIn('my_strlen("ano") = 3\n', output)
        self.assertIn('my_strlen("año") = 4\n', output)
        self.assertIn("my_strlen(t) = 4\nsizeof(t) = 8\n", output)

    def test_lowercase_ignores_utf8_with_either_char_sign(self):
        expected = "Hola Mundo: 7\nLIMA 2026: 0\nano: 3\naño: 2\n"
        self.assertEqual(run("count_lowercase")[0], expected)
        for flag in ["-fsigned-char", "-funsigned-char"]:
            with self.subTest(flag=flag):
                _, status, binary = build_source("count_lowercase.c", flag)
                self.assertEqual(status, 0)
                self.assertEqual(execute([str(binary)])[0], expected)

    def test_too_long_initializer_warns_but_one_byte_short_does_not(self):
        messages, _, _ = build_source("errors/too_long.c")
        self.assertIn("is too long", messages)
        messages, status, _ = build_source("errors/no_terminator.c")
        self.assertEqual((messages, status), ("", 0))

    def test_no_terminator_is_detected_when_running(self):
        _, _, binary = build_source("errors/no_terminator.c", *SANITIZE)
        output, status = execute([str(binary)])
        self.assertNotEqual(status, 0)
        self.assertIn("stack-buffer-overflow", output)

    def test_writing_a_literal_compiles_without_warnings(self):
        # Al correr es comportamiento indefinido: de eso no se prueba nada.
        messages, status, _ = build_source("errors/literal_write.c")
        self.assertEqual((messages, status), ("", 0))


class ReadingText(unittest.TestCase):
    def test_width_limits_scanf_and_stops_at_space(self):
        self.assertEqual(run("read_word", "Ana María\n")[0],
                         "Primera lectura: Ana\nSegunda lectura: María\n")
        self.assertEqual(run("read_word", "abcdefghijklmnopqrstuvwxyz\n")[0],
                         "Primera lectura: abcdefghijklmnopqrs\nSegunda lectura: tuvwxyz\n")
        self.assertEqual(run("read_word", ""), ("Entrada inválida\n", 1))

    def test_fgets_four_cases(self):
        cases = {
            "Ana\n": 'leído: "Ana\\n"\nfgets devolvió NULL\n',
            "Ana": 'leído: "Ana"\nfgets devolvió NULL\n',
            "Alejandra\n": 'leído: "Alejand"\nleído: "ra\\n"\nfgets devolvió NULL\n',
            "": "fgets devolvió NULL\n",
        }
        for text, expected in cases.items():
            with self.subTest(text=text):
                self.assertEqual(run("read_line", text), (expected, 0))

    def test_exact_fit_leaves_the_newline_for_later(self):
        self.assertEqual(run("read_line", "Rosaura\n")[0],
                         'leído: "Rosaura"\nleído: "\\n"\nfgets devolvió NULL\n')

    def test_read_name(self):
        self.assertEqual(run("read_name", "Ana María\nLima\n"),
                         ("Nombre: Ana María\nCiudad: Lima\n", 0))
        self.assertEqual(run("read_name", "Maria de los Angeles Quispe\nLima\n"),
                         ("Nombre: Maria de los Angele\nCiudad: Lima\n", 0))
        # 19 bytes justos: el salto de línea que queda no debe llegar a la ciudad.
        self.assertEqual(run("read_name", "abcdefghijklmnopqrs\nLima\n"),
                         ("Nombre: abcdefghijklmnopqrs\nCiudad: Lima\n", 0))
        self.assertEqual(run("read_name", "Ana\n"), ("Entrada inválida\n", 1))
        self.assertEqual(run("read_name", ""), ("Entrada inválida\n", 1))

    def test_scanf_leaves_the_newline(self):
        _, _, binary = build_source("errors/scanf_then_fgets.c")
        self.assertEqual(execute([str(binary)], "18\nAna\n")[0], "Edad: 18\nNombre: \n")
        self.assertEqual(run("age_name", "18\nAna\n")[0], "Edad: 18\nNombre: Ana\n")


class BufferOverflow(unittest.TestCase):
    def test_short_name_works_and_long_name_is_reported(self):
        messages, status, binary = build_source("errors/overflow_scanf.c", *SANITIZE)
        self.assertEqual((messages, status), ("", 0))
        self.assertEqual(execute([str(binary)], "Ana\n"), ("Hola, Ana\n", 0))
        output, status = execute([str(binary)], "Alejandra\n")
        self.assertNotEqual(status, 0)
        for fragment in ["stack-buffer-overflow", "WRITE of size 10",
                         "overflow_scanf.c:7", "'name' (line 5)"]:
            self.assertIn(fragment, output)

    def test_overflow_demos_compile_without_warnings(self):
        for source in ["errors/overflow_scanf.c", "errors/overflow_neighbor.c"]:
            with self.subTest(source=source):
                messages, status, _ = build_source(source)
                self.assertEqual((messages, status), ("", 0))

    def test_neighbor_demo_is_caught_by_the_sanitizer(self):
        # Sin sanitizer el resultado depende de la máquina: no se compara.
        _, _, binary = build_source("errors/overflow_neighbor.c", *SANITIZE)
        self.assertIn("Acceso normal", execute([str(binary)], "Ana\n")[0])
        self.assertIn("stack-buffer-overflow", execute([str(binary)], "Alejandra_Quispe\n")[0])

    def test_copy_text_stays_inside(self):
        self.assertEqual(run("copy_text"), ("sol\nluna\nestr\n", 0))


if __name__ == "__main__":
    unittest.main()
