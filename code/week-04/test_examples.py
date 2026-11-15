"""Comprueba lo que los apuntes afirman sobre los programas de la semana 4."""
import pathlib
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


def compile_error_demo(name, *extra):
    """Compila un programa de errors/; devuelve los mensajes, el estado y el ejecutable."""
    out = pathlib.Path(tempfile.mkdtemp()) / name
    done = subprocess.run(
        ["gcc", *FLAGS, *extra, f"errors/{name}.c", "-o", str(out)], cwd=HERE,
        text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
    )
    return done.stdout, done.returncode, out


def run_demo(binary, stdin=""):
    done = subprocess.run(
        [str(binary)], input=stdin, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=10,
    )
    return done.stdout, done.returncode


class CleanCompile(unittest.TestCase):
    def test_examples_have_no_warnings(self):
        for source in sorted(HERE.glob("*.c")):
            with self.subTest(source=source.name):
                done = subprocess.run(
                    ["gcc", *FLAGS, "-Werror", "-fsyntax-only", str(source)],
                    text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                )
                self.assertEqual(done.returncode, 0, done.stdout)


class Decisions(unittest.TestCase):
    def test_discount_boundary(self):
        self.assertEqual(run("discount", "9999")[0], "A pagar: 99.99 soles\n")
        self.assertEqual(run("discount", "10000")[0], "A pagar: 90.00 soles\n")
        self.assertEqual(run("discount", "12050")[0], "A pagar: 108.45 soles\n")

    def test_discount_rejects(self):
        self.assertEqual(run("discount", "abc"), ("Entrada inválida\n", 1))
        self.assertEqual(run("discount", ""), ("Entrada inválida\n", 1))
        self.assertEqual(run("discount", "-5")[1], 1)

    def test_parity_with_negatives(self):
        self.assertEqual(run("parity", "7")[0], "7 es impar\n")
        self.assertEqual(run("parity", "-3")[0], "-3 es impar\n")
        self.assertEqual(run("parity", "-4")[0], "-4 es par\n")
        self.assertEqual(run("parity", "0")[0], "0 es par\n")

    def test_parity_wrong_fails_on_negatives(self):
        _, _, binary = compile_error_demo("parity_wrong")
        self.assertEqual(run_demo(binary, "-3")[0], "-3 es par\n")

    def test_max_of_three_all_orders_and_ties(self):
        for a, b, c in [(4, 9, 2), (9, 4, 2), (2, 4, 9), (5, 5, 1), (1, 5, 5), (5, 1, 5), (3, 3, 3), (-1, -2, -3)]:
            with self.subTest(values=(a, b, c)):
                self.assertEqual(run("max_of_three", f"{a} {b} {c}")[0], f"{max(a, b, c)}\n")

    def test_mention_boundaries(self):
        expected = {-1: "Promedio fuera de rango", 0: "Insuficiente", 10: "Insuficiente",
                    11: "Regular", 13: "Regular", 14: "Bueno", 16: "Bueno",
                    17: "Excelente", 20: "Excelente", 21: "Promedio fuera de rango"}
        for grade, text in expected.items():
            with self.subTest(grade=grade):
                self.assertEqual(run("mention", str(grade))[0], text + "\n")

    def test_mention_wrong_order_says_regular(self):
        _, _, binary = compile_error_demo("mention_wrong_order")
        self.assertEqual(run_demo(binary, "18")[0], "Regular\n")


class Logic(unittest.TestCase):
    def test_relational_are_one_or_zero(self):
        lines = run("relational")[0].splitlines()
        self.assertEqual([line.split()[-1] for line in lines], ["1", "0", "0", "1", "1", "0"])

    def test_nonzero_is_true(self):
        self.assertEqual(run("truthy", "-7")[0], "-7 cuenta como verdadero\n!n vale 0\n")
        self.assertEqual(run("truthy", "0")[0], "0 cuenta como falso\n!n vale 1\n")

    def test_precedence_values(self):
        self.assertEqual(run("precedence")[0].split(), ["0", "1", "1", "1", "0"])

    def test_truth_table(self):
        rows = run("truth_table")[0].splitlines()[1:]
        cells = [row.replace("|", " ").split() for row in rows]
        for a, b, conj, disj, neg in (map(int, cell) for cell in cells):
            self.assertEqual(conj, a and b)
            self.assertEqual(disj, a or b)
            self.assertEqual(neg, 1 - a)

    def test_de_morgan_on_a_grid(self):
        for x in range(-2, 13):
            for y in [-1, 0, 1, 9, 10, 11]:
                values = [line.split()[-1] for line in run("de_morgan", f"{x} {y}")[0].splitlines()]
                with self.subTest(x=x, y=y):
                    self.assertEqual(values[0], values[1])
                    self.assertEqual(values[2], values[3])

    def test_short_circuit_avoids_division(self):
        output, status = run("short_circuit", "0")
        self.assertEqual((output, status), ("No se cumple\n", 0))
        self.assertEqual(run("short_circuit", "5")[0], "10 / 5 es mayor que 1\n")
        self.assertEqual(run("short_circuit", "20")[0], "No se cumple\n")

    def test_swapped_operands_divide_by_zero(self):
        _, _, binary = compile_error_demo("unsafe_division", "-g", "-fsanitize=undefined")
        self.assertIn("runtime error: division by zero", run_demo(binary, "0")[0])

    def test_read_in_range(self):
        self.assertEqual(run("read_in_range", "12"), ("Mes válido: 12\n", 0))
        for text in ["0", "13", "abc", ""]:
            with self.subTest(text=text):
                self.assertEqual(run("read_in_range", text), ("Mes inválido\n", 1))

    def test_double_comparison(self):
        self.assertEqual(run("compare_double")[0], "Con ==: distintos\nCon tolerancia: iguales\n")


class Switch(unittest.TestCase):
    def test_month_days(self):
        days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        for month, count in enumerate(days, start=1):
            with self.subTest(month=month):
                self.assertEqual(run("month_days", str(month)), (f"{count} días\n", 0))
        self.assertEqual(run("month_days", "13"), ("Mes inválido\n", 1))
        self.assertEqual(run("month_days", "0"), ("Mes inválido\n", 1))

    def test_combo(self):
        self.assertEqual(run("combo", "1")[0], "Precio: 1200 céntimos\n")
        self.assertEqual(run("combo", "2")[0], "Precio: 1500 céntimos\n")
        self.assertEqual(run("combo", "3")[0], "Precio: 1800 céntimos\n")
        self.assertEqual(run("combo", "4"), ("Opción inválida\n", 1))

    def test_missing_break_falls_through(self):
        messages, status, binary = compile_error_demo("combo_no_break")
        self.assertEqual(status, 0)
        self.assertIn("-Wimplicit-fallthrough", messages)
        self.assertEqual(run_demo(binary, "1")[0], "Precio: 1800 céntimos\n")

    def test_vowel(self):
        for text in ["a", "E", "  u"]:
            with self.subTest(text=text):
                self.assertEqual(run("vowel", text)[0], "Vocal\n")
        for text in ["b", "7", "ñ", "á"]:
            with self.subTest(text=text):
                self.assertEqual(run("vowel", text)[0], "No es vocal\n")


class Gates(unittest.TestCase):
    def test_gates(self):
        for a in (0, 1):
            for b in (0, 1):
                with self.subTest(a=a, b=b):
                    self.assertEqual(
                        run("gates", f"{a} {b}")[0],
                        f"AND {a & b}\nOR  {a | b}\nNOT {1 - a}\nXOR {a ^ b}\n",
                    )
        self.assertEqual(run("gates", "2 0"), ("Los bits deben ser 0 o 1\n", 1))

    def test_full_adder_all_inputs(self):
        for a in (0, 1):
            for b in (0, 1):
                for c in (0, 1):
                    total = a + b + c
                    with self.subTest(a=a, b=b, c=c):
                        self.assertEqual(run("full_adder", f"{a} {b} {c}")[0],
                                         f"suma {total % 2}, acarreo {total // 2}\n")

    def test_adder4_all_inputs(self):
        for a in range(16):
            for b in range(16):
                text = f"{a:04b} {b:04b}"
                lines = run("adder4", text)[0].splitlines()
                with self.subTest(text=text):
                    self.assertEqual(lines[1], f"suma:     {(a + b) % 16:04b}")
                    self.assertEqual(lines[0].split()[1], str((a + b) // 16))

    def test_adder4_rejects(self):
        self.assertEqual(run("adder4", "0102 0011"), ("Los bits deben ser 0 o 1\n", 1))
        self.assertEqual(run("adder4", "01 01"), ("Entrada inválida\n", 1))


class CompilerMessages(unittest.TestCase):
    """Cada error a propósito da el aviso que dicen los apuntes y se comporta como dicen."""

    def check(self, name, message, stdin, expected):
        messages, status, binary = compile_error_demo(name)
        self.assertEqual(status, 0, messages)
        self.assertIn(message, messages)
        self.assertEqual(run_demo(binary, stdin)[0], expected)

    def test_assignment(self):
        self.check("assign_in_if", "-Wparentheses", "", "otro\nx vale 0\n")

    def test_chained(self):
        self.check("chained_compare", "do not have their mathematical meaning", "25", "En rango\n")

    def test_semicolon(self):
        self.check("semicolon_if", "-Wempty-body", "-3", "-3 es positivo\n")

    def test_indentation(self):
        self.check("misleading_indent", "-Wmisleading-indentation", "15", "Rechazada\n")

    def test_dangling(self):
        self.check("dangling_else", "-Wdangling-else", "5 -1", "a no es positivo\n")
        self.check("dangling_else", "-Wdangling-else", "-5 1", "")

    def test_not(self):
        self.check("not_precedence", "-Wlogical-not-parentheses", "", "a es igual a b\n")

    def test_and_or(self):
        self.check("and_or_no_parens", "within", "", "1\n")

    def test_or_constant_is_silent(self):
        messages, status, binary = compile_error_demo("or_constant")
        self.assertEqual((messages, status), ("", 0))
        self.assertEqual(run_demo(binary, "7")[0], "Opción 1 o 2\n")

    def test_char_vs_string(self):
        messages, _, _ = compile_error_demo("char_vs_string")
        self.assertIn("comparison between pointer and integer", messages)

    def test_errors_that_do_not_compile(self):
        messages, status, _ = compile_error_demo("block_scope")
        self.assertNotEqual(status, 0)
        self.assertIn("undeclared", messages)
        messages, status, _ = compile_error_demo("switch_double")
        self.assertNotEqual(status, 0)
        self.assertIn("switch quantity not an integer", messages)


if __name__ == "__main__":
    unittest.main()
