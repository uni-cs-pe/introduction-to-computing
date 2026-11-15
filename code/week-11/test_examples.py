"""Comprueba lo que los apuntes afirman sobre los programas de la semana 11."""
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
        # Se compila de verdad: -Wstringop-truncation no sale solo revisando la sintaxis.
        for source in sorted(HERE.glob("*.c")):
            with self.subTest(source=source.name):
                messages, status, _ = build_source(
                    source.name, *SANITIZE, "-Werror", *(["-c"] if source.name == "check_lab.c" else []))
                self.assertEqual(status, 0, messages)

    def test_no_pointer_variables_or_pointer_arithmetic_in_examples(self):
        # La GUIA deja los punteros para cursos posteriores.
        for source in sorted(HERE.glob("*.c")) + sorted((HERE / "solution").glob("*.c")):
            if source.name == "check_lab.c":
                continue
            code = re.sub(r"//[^\n]*", "", source.read_text(encoding="utf-8"))
            with self.subTest(source=source.name):
                self.assertNotRegex(code, r"\b(?:char|int|double)\s*\*\s*\w")
                self.assertNotRegex(code, r"str(?:str|chr)\([^;]*\)\s*[-+]")


class Lengths(unittest.TestCase):
    def test_lengths(self):
        self.assertEqual(run("lengths"), (
            'strlen(t) = 4\nsizeof(t) = 8\nstrlen("") = 0\nstrlen("año") = 4\naloh\n', 0))

    def test_subtracting_from_zero_wraps(self):
        messages, status, binary = build_source("errors/strlen_wrap.c")
        self.assertEqual(status, 0)
        self.assertIn("-Wtype-limits", messages)
        output, _ = execute([str(binary)])
        value = int(re.search(r"= (\d+)", output).group(1))
        self.assertGreater(value, 2 ** 31)      # el valor exacto depende del tamaño de size_t
        self.assertEqual((value + 1) & value, 0)  # es 2^n - 1
        self.assertIn("siempre se cumple", output)

    def test_last_char_of_empty_string_is_reported(self):
        messages, status, binary = build_source("errors/last_char.c", *SANITIZE)
        self.assertEqual(status, 0)
        self.assertEqual(messages, "")          # gcc no avisa
        output, code = execute([str(binary)])
        self.assertIn("AddressSanitizer", output)
        self.assertNotEqual(code, 0)

    def test_sign_compare_warning(self):
        messages, status, _ = build_source("errors/sign_compare.c")
        self.assertEqual(status, 0)
        self.assertIn("-Wsign-compare", messages)


class Comparing(unittest.TestCase):
    def test_equal_arrays(self):
        messages, status, binary = build_source("errors/equal_arrays.c")
        self.assertEqual(status, 0)
        self.assertIn("-Warray-compare", messages)
        self.assertEqual(execute([str(binary)]), ("distintas\n", 0))

    def test_equal_params_is_silent(self):
        messages, status, binary = build_source("errors/equal_params.c")
        self.assertEqual((messages, status), ("", 0))
        self.assertEqual(execute([str(binary)]), ("a con b: 0\na con a: 1\n", 0))

    def test_equal_literals_warns_and_its_result_is_not_tested(self):
        messages, status, binary = build_source("errors/equal_literals.c")
        self.assertEqual(status, 0)
        self.assertIn("unspecified behavior", messages)
        output, _ = execute([str(binary)])
        self.assertIn(output, ("0\n", "1\n"))

    def test_strcmp_order(self):
        output, code = run("compare")
        self.assertEqual(code, 0)
        self.assertEqual(output.splitlines(), [
            '"ana" y "ana" son iguales',
            '"ana" va antes que "ano"',
            '"an" va antes que "ana"',
            '"sol" va después de "luna"',
            '"Z" va antes que "a"',
            '"z" va antes que "ñ"',
        ])

    def test_strcmp_order_does_not_depend_on_char_signedness(self):
        expected, _ = run("compare")
        for option in ["-fsigned-char", "-funsigned-char"]:
            with self.subTest(option=option):
                _, status, binary = build_source("compare.c", option)
                self.assertEqual(status, 0)
                self.assertEqual(execute([str(binary)]), (expected, 0))

    def test_strcmp_in_an_if_reads_backwards(self):
        _, status, binary = build_source("errors/strcmp_wrong.c")
        self.assertEqual(status, 0)
        self.assertEqual(execute([str(binary)]), ("distintas\n", 0))


class Copying(unittest.TestCase):
    def test_strncpy_bytes(self):
        output, code = run("strncpy_bytes")
        self.assertEqual(code, 0)
        rows = [line.split() for line in output.splitlines()]
        self.assertEqual(rows[0], ["115", "111", "108", "0", "0"])       # sol, con relleno
        self.assertEqual(rows[1], ["108", "117", "110", "97", "0"])      # luna, justo
        self.assertEqual(rows[2], ["101", "115", "116", "114", "101"])   # sin '\0'
        self.assertNotIn("0", rows[2])

    def test_gcc_warns_only_when_it_sees_the_text(self):
        messages, status, _ = build_source("errors/strncpy_warn.c")
        self.assertEqual(status, 0)
        self.assertIn("-Wstringop-truncation", messages)
        messages, status, _ = build_source("errors/strncpy_no_null.c")
        self.assertEqual((messages, status), ("", 0))

    def test_strncpy_without_terminator_is_reported(self):
        _, status, binary = build_source("errors/strncpy_no_null.c", *SANITIZE)
        self.assertEqual(status, 0)
        output, code = execute([str(binary)])
        self.assertIn("AddressSanitizer: stack-buffer-overflow", output)
        self.assertIn("READ of size", output)
        self.assertNotEqual(code, 0)

    def test_safe_copy(self):
        self.assertEqual(run("safe_copy"), ("sol\nluna\nestr\n", 0))

    def test_append(self):
        self.assertEqual(run("append"), ("Ana Quispe\nAna Qui\n", 0))

    def test_strcat_overflows_only_with_long_input(self):
        messages, status, binary = build_source("errors/strcat_overflow.c", *SANITIZE)
        self.assertEqual((messages, status), ("", 0))
        self.assertEqual(execute([str(binary)], "Li\n"), ("Ana Li\n", 0))
        output, code = execute([str(binary)], "Quispe_Huaman\n")
        self.assertIn("AddressSanitizer: stack-buffer-overflow", output)
        self.assertIn("WRITE of size 14", output)
        self.assertNotEqual(code, 0)
        self.assertEqual(execute([str(binary)], ""), ("Entrada inválida\n", 1))

    def test_strcat_overlap(self):
        messages, status, binary = build_source("errors/strcat_overlap.c", *SANITIZE)
        self.assertEqual(status, 0)
        self.assertIn("-Wrestrict", messages)
        output, code = execute([str(binary)])
        self.assertIn("strcat-param-overlap", output)
        self.assertNotEqual(code, 0)


class Searching(unittest.TestCase):
    def test_find_text(self):
        self.assertEqual(run("find_text"), (
            "Tiene @: @example.com\nNo tiene #\nDesde Lima: Lima\n"
            "lima, en minúsculas, no aparece\nDesde la ñ: ño pasado llovió en Lima\n"
            "Desde el byte 3: año pasado llovió en Lima\n"
            "Desde el byte 0 hay un el\nDesde el byte 1 no hay ninguno\n", 0))

    def test_null_result_used_without_checking_does_not_exit_cleanly(self):
        # Es comportamiento indefinido: no se prueba cómo muere, solo con el sanitizer.
        _, status, binary = build_source("errors/strstr_null.c", *SANITIZE)
        self.assertEqual(status, 0)
        output, code = execute([str(binary)])
        self.assertNotEqual(code, 0)
        self.assertIn("null", output)


class Matrices(unittest.TestCase):
    def test_layout_sizes(self):
        output, code = run("matrix_layout")
        self.assertEqual(code, 0)
        self.assertIn("sizeof(m) = 48\nsizeof(m[0]) = 16\nsizeof(m[0][0]) = 4\nm[1][2] = 7\n", output)

    def test_layout_is_row_by_row(self):
        output, _ = run("matrix_layout")
        cells = re.findall(r"m\[(\d)\]\[(\d)\] = +(\d+) está en (0x[0-9a-f]+)", output)
        self.assertEqual(len(cells), 12)
        self.assertEqual([int(c[2]) for c in cells], list(range(1, 13)))
        addresses = [int(c[3], 16) for c in cells]
        for row, column, _, _ in cells:
            position = int(row) * 4 + int(column)   # la fórmula de los apuntes
            self.assertEqual(addresses[position] - addresses[0], position * 4)

    def test_grades_table(self):
        self.assertEqual(run("grades_table")[0].splitlines(), [
            "Estudiante 0: suma 52, promedio 13.00",
            "Estudiante 1: suma 48, promedio 12.00",
            "Estudiante 2: suma 63, promedio 15.75",
            "Curso 0: suma 43, promedio 14.33",
            "Curso 1: suma 35, promedio 11.67",
            "Curso 2: suma 40, promedio 13.33",
            "Curso 3: suma 45, promedio 15.00",
        ])

    def test_matrix_param_changes_only_the_rows_it_receives(self):
        lines = run("matrix_param")[0].splitlines()
        self.assertEqual(lines[3:5], ["Suma del curso 0: 43", "Suma del curso 0, solo 2 filas: 25"])
        self.assertEqual(lines[5:], [" 15 10 18 13", " 12 17  9 14", " 18 10 15 20"])

    def test_missing_columns_do_not_compile(self):
        messages, status, _ = build_source("errors/matrix_no_columns.c")
        self.assertNotEqual(status, 0)
        self.assertIn("must have bounds for all dimensions except the first", messages)

    def test_wrong_columns_are_noticed(self):
        messages, _, _ = build_source("errors/matrix_wrong_columns.c")
        self.assertIn("incompatible pointer type", messages)

    def test_const_matrix_is_only_seen_with_pedantic(self):
        messages, status, _ = build_source("errors/const_matrix.c")
        self.assertEqual((messages, status), ("", 0))
        messages, status, _ = build_source("errors/const_matrix.c", "-Wpedantic")
        self.assertEqual(status, 0)
        self.assertIn("before C23", messages)

    def test_no_example_uses_const_matrix_parameters(self):
        for source in sorted(HERE.glob("*.c")) + sorted((HERE / "solution").glob("*.c")):
            with self.subTest(source=source.name):
                self.assertNotRegex(source.read_text(encoding="utf-8"), r"const\s+\w+\s+\w+\[\]\[")

    def test_comma_warns(self):
        messages, status, _ = build_source("errors/matrix_comma.c")
        self.assertEqual(status, 0)
        self.assertIn("left-hand operand of comma", messages)

    def test_column_out_of_bounds_seen_by_undefined_not_by_address(self):
        _, status, binary = build_source("errors/matrix_bounds.c", *SANITIZE)
        self.assertEqual(status, 0)
        self.assertEqual(execute([str(binary)], "2\n"), ("m[0][2] = 3\n", 0))
        output, _ = execute([str(binary)], "3\n")
        self.assertIn("runtime error: index 3 out of bounds for type 'int [3]'", output)
        self.assertNotIn("AddressSanitizer", output)
        # Solo con address, nada avisa en este acceso.
        _, status, binary = build_source("errors/matrix_bounds.c", "-g", "-fsanitize=address")
        self.assertEqual(status, 0)
        output, _ = execute([str(binary)], "3\n")
        self.assertNotIn("AddressSanitizer", output)
        self.assertEqual(execute([str(binary)], "x\n"), ("Entrada inválida\n", 1))

    def test_names(self):
        self.assertEqual(run("names"), (
            "sizeof(names) = 48\n"
            "names[0] = Rosa, 4 bytes de texto\nnames[1] = Ana, 3 bytes de texto\n"
            "names[2] = Luis, 4 bytes de texto\nnames[3] = Zoila, 5 bytes de texto\n"
            "Primero: Ana\nnames[1] = Maria de lo\nPrimero: Luis\n", 0))

    def test_matrix_add(self):
        self.assertEqual(run("matrix_add"), (" 11 22 33\n 44 55 66\n", 0))

    def test_transposing_in_place_over_every_cell_changes_nothing(self):
        messages, status, binary = build_source("errors/transpose_in_place.c")
        self.assertEqual((messages, status), ("", 0))
        self.assertEqual(execute([str(binary)]), ("1 2 3\n4 5 6\n7 8 9\n", 0))


if __name__ == "__main__":
    unittest.main()
