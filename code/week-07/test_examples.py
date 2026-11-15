"""Comprueba lo que los apuntes afirman sobre los programas de la semana 7."""
import pathlib
import re
import signal
import subprocess
import tempfile
import unittest

HERE = pathlib.Path(__file__).parent
BUILD = HERE / "build"
FLAGS = ["-Wall", "-Wextra", "-std=c17"]


def run(program, stdin=""):
    """Ejecuta un programa de build/; devuelve su salida (con errores) y su estado."""
    done = subprocess.run(
        [str(BUILD / program)], input=stdin, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=10,
    )
    return done.stdout, done.returncode


def compile_demo(source, *extra):
    """Compila un programa; devuelve los mensajes, el estado y el ejecutable."""
    out = pathlib.Path(tempfile.mkdtemp()) / "demo"
    done = subprocess.run(
        ["gcc", *FLAGS, *extra, source, "-o", str(out)], cwd=HERE,
        text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
    )
    return done.stdout, done.returncode, out


def run_demo(binary, stdin=""):
    done = subprocess.run(
        [str(binary)], input=stdin, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=10,
    )
    return done.stdout, done.returncode


def digit_sum(n):
    return sum(int(c) for c in str(n))


class CleanCompile(unittest.TestCase):
    def test_examples_have_no_warnings(self):
        for source in sorted(HERE.glob("*.c")):
            with self.subTest(source=source.name):
                done = subprocess.run(
                    ["gcc", *FLAGS, "-Werror", "-fsyntax-only", str(source)],
                    text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                )
                self.assertEqual(done.returncode, 0, done.stdout)

    def test_gdb_build_has_no_warnings(self):
        for source in ["digit_sum_bug.c", "call_chain.c"]:
            with self.subTest(source=source):
                messages, status, _ = compile_demo(source, "-g", "-O0")
                self.assertEqual((messages, status), ("", 0))


class Functions(unittest.TestCase):
    def test_square(self):
        self.assertEqual(run("square", "5")[0], "5 al cuadrado es 25\n40\n")
        self.assertEqual(run("square", "-3")[0], "-3 al cuadrado es 9\n8\n")
        self.assertEqual(run("square", "abc"), ("Entrada inválida\n", 1))

    def test_square_overflow_is_reported(self):
        self.assertIn("signed integer overflow", run("square", "50000")[0])

    def test_max_of_three(self):
        for a, b, c in [(3, 9, 5), (9, 3, 5), (3, 5, 9), (5, 5, 1), (1, 5, 5), (2, 2, 2), (-1, -2, -3)]:
            with self.subTest(values=(a, b, c)):
                self.assertEqual(run("max_of_three", f"{a} {b} {c}")[0], f"{max(a, b, c)}\n")

    def test_print_line(self):
        dashes = "-" * 20
        self.assertEqual(run("print_line")[0],
                         f"{dashes}\nBoleta de notas\n{dashes}\nPromedio: 14\n-----\n")

    def test_roll_die_stays_in_range(self):
        # No se comparan números exactos: dependen de la semilla y del sistema.
        values = run("roll_die")[0].split()
        self.assertEqual(len(values), 5)
        for value in values:
            self.assertIn(int(value), range(1, 7))

    def test_prototype(self):
        self.assertEqual(run("prototype")[0], "27\n")

    def test_has_digit(self):
        cases = {"2026 6": True, "2026 2": True, "2026 1": False, "26 2": True, "7 7": True,
                 "100 1": True, "100 0": True, "5 0": False}
        for text, found in cases.items():
            with self.subTest(text=text):
                self.assertEqual(run("has_digit", text)[0], "Sí aparece\n" if found else "No aparece\n")

    def test_has_digit_rejects(self):
        for text in ["0 5", "-3 3", "abc", "5"]:
            with self.subTest(text=text):
                self.assertEqual(run("has_digit", text), ("Entrada inválida\n", 1))

    def test_has_digit_wrong_only_looks_at_one_digit(self):
        _, _, binary = compile_demo("errors/has_digit_wrong.c")
        self.assertEqual(run_demo(binary, "26 6")[0], "Sí aparece\n")
        self.assertEqual(run_demo(binary, "26 2")[0], "No aparece\n")


class ByValueAndScope(unittest.TestCase):
    def test_by_value(self):
        self.assertEqual(run("by_value")[0],
                         "En add_one, x vale 2\nEn main, x vale 1\nDespués de plus_one, x vale 2\n")

    def test_try_swap_does_not_swap(self):
        self.assertEqual(run("try_swap")[0],
                         "En try_swap: a = 8, b = 3\nEn main:     a = 3, b = 8\n")

    def test_scope(self):
        self.assertEqual(run("scope")[0], "25\n")

    def test_locals_do_not_remember(self):
        self.assertEqual(run("count_calls")[0], "1\n1\n1\n")

    def test_call_chain(self):
        self.assertEqual(run("call_chain")[0], "25\n")


class Discount(unittest.TestCase):
    def test_boundaries(self):
        cases = {"0": "0.00", "8000": "80.00", "9999": "99.99", "10000": "90.00", "12050": "108.45"}
        for total, price in cases.items():
            for program in ["discount", "discount_mixed"]:
                with self.subTest(program=program, total=total):
                    self.assertEqual(run(program, total), (f"A pagar: {price} soles\n", 0))

    def test_rejects(self):
        for text in ["abc", "", "-1"]:
            for program in ["discount", "discount_mixed"]:
                with self.subTest(program=program, text=text):
                    self.assertEqual(run(program, text), ("Entrada inválida\n", 1))

    def test_tests_pass(self):
        self.assertEqual(run("discount_tests"), ("Todas las pruebas pasaron\n", 0))

    def test_tests_use_the_same_function(self):
        pattern = r"int price_after_discount\(int total\) \{.*?\n\}"
        program = re.search(pattern, (HERE / "discount.c").read_text(encoding="utf-8"), re.S)
        tests = re.search(pattern, (HERE / "discount_tests.c").read_text(encoding="utf-8"), re.S)
        self.assertEqual(program.group(0), tests.group(0))


class Asserts(unittest.TestCase):
    def test_bug_stops_at_first_failed_assert(self):
        output, status = run("count_digits_bug")
        self.assertIn("count_digits_bug.c:17: main: Assertion `count_digits(0) == 1' failed.", output)
        self.assertNotIn("-42", output)
        self.assertNotIn("Todas las pruebas", output)
        self.assertEqual(status, -signal.SIGABRT)

    def test_fixed_version_passes(self):
        self.assertEqual(run("count_digits"), ("Todas las pruebas pasaron\n", 0))

    def test_assert_is_active_by_default(self):
        output, status = run("ndebug_demo")
        self.assertIn("Assertion `1 + 1 == 3' failed.", output)
        self.assertNotIn("Llegué", output)
        self.assertEqual(status, -signal.SIGABRT)

    def test_ndebug_turns_assert_off(self):
        _, status, binary = compile_demo("ndebug_demo.c", "-DNDEBUG")
        self.assertEqual(status, 0)
        self.assertEqual(run_demo(binary), ("Llegué al final\n", 0))


class DigitSum(unittest.TestCase):
    def test_bug_loses_the_leftmost_digit(self):
        for n in [5, 23, 407, 9, 10, 2026]:
            with self.subTest(n=n):
                wrong = digit_sum(n) - int(str(n)[0])
                self.assertEqual(run("digit_sum_bug", str(n))[0],
                                 f"La suma de las cifras de {n} es {wrong}\n")

    def test_fix(self):
        for n in list(range(0, 120)) + [407, 999, 1000, 2026, 2147483647]:
            with self.subTest(n=n):
                self.assertEqual(run("digit_sum", str(n))[0],
                                 f"La suma de las cifras de {n} es {digit_sum(n)}\n")

    def test_input_file_of_the_notes(self):
        self.assertEqual((HERE / "entrada.txt").read_text(encoding="utf-8").strip(), "407")

    def test_fix_changes_only_the_condition(self):
        wrong = (HERE / "digit_sum_bug.c").read_text(encoding="utf-8").splitlines()
        fixed = (HERE / "digit_sum.c").read_text(encoding="utf-8").splitlines()
        changed = [(a, b) for a, b in zip(wrong, fixed) if a != b]
        self.assertEqual(len(wrong), len(fixed))
        self.assertIn(("    while (n > 9) {", "    while (n > 0) {"), changed)
        self.assertEqual(len(changed), 2)  # la condición y el comentario


class GdbSessionsMatchTheSource(unittest.TestCase):
    """Las sesiones de gdb no se comparan, pero sus números de línea sí deben existir."""

    def line(self, source, number):
        return (HERE / source).read_text(encoding="utf-8").splitlines()[number - 1].strip()

    def test_digit_sum_lines(self):
        expected = {5: "int sum = 0;", 6: "while (n > 9) {", 7: "int last = n % 10;",
                    8: "sum = sum + last;", 9: "n = n / 10;", 11: "return sum;"}
        for number, text in expected.items():
            with self.subTest(line=number):
                self.assertEqual(self.line("digit_sum_bug.c", number), text)

    def test_call_chain_lines(self):
        expected = {4: "int result = x * x;", 9: "int first = square(a);",
                    15: "int total = sum_of_squares(3, 4);"}
        for number, text in expected.items():
            with self.subTest(line=number):
                self.assertEqual(self.line("call_chain.c", number), text)


class CompilerMessages(unittest.TestCase):
    def assert_error(self, name, text):
        messages, status, _ = compile_demo(f"errors/{name}.c")
        self.assertNotEqual(status, 0)
        self.assertIn(text, messages)

    def assert_silent(self, name):
        messages, status, binary = compile_demo(f"errors/{name}.c")
        self.assertEqual((messages, status), ("", 0))
        return binary

    def test_wrong_count(self):
        self.assert_error("wrong_count", "too few arguments")

    def test_void_value(self):
        self.assert_error("void_value", "void value not ignored")

    def test_no_prototype(self):
        self.assert_error("no_prototype", "implicit declaration of function")

    def test_void_parens(self):
        self.assert_error("void_parens", "too many arguments")

    def test_local_not_visible(self):
        self.assert_error("local_not_visible", "undeclared")

    def test_empty_parens_is_silent(self):
        # No se ejecuta en la prueba: esa llamada es comportamiento indefinido.
        self.assert_silent("empty_parens")

    def test_double_argument_is_silent(self):
        self.assertEqual(run_demo(self.assert_silent("double_argument")), ("4\n", 0))

    def test_ignored_result_is_silent(self):
        self.assertEqual(run_demo(self.assert_silent("ignored_result")), ("5\n", 0))

    def test_has_digit_wrong_is_silent(self):
        self.assert_silent("has_digit_wrong")

    def test_missing_return_warns_and_still_compiles(self):
        # No se ejecuta: usar ese valor es comportamiento indefinido.
        messages, status, _ = compile_demo("errors/missing_return.c")
        self.assertEqual(status, 0)
        self.assertIn("control reaches end of non-void function", messages)


if __name__ == "__main__":
    unittest.main()
