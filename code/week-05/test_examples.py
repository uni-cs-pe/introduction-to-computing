"""Comprueba lo que los apuntes afirman sobre los programas de la semana 5."""
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


def first_lines(binary, stdin, count):
    """Lee las primeras líneas de un programa que no termina solo, y lo detiene."""
    process = subprocess.Popen(
        [str(binary)], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True,
    )
    process.stdin.write(stdin)
    process.stdin.close()
    lines = [process.stdout.readline() for _ in range(count)]
    still_running = process.poll() is None
    process.kill()
    process.stdout.close()
    process.wait()
    return lines, still_running


class CleanCompile(unittest.TestCase):
    def test_examples_have_no_warnings(self):
        for source in sorted(HERE.glob("*.c")):
            with self.subTest(source=source.name):
                done = subprocess.run(
                    ["gcc", *FLAGS, "-Werror", "-fsyntax-only", str(source)],
                    text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                )
                self.assertEqual(done.returncode, 0, done.stdout)


class WhileLoops(unittest.TestCase):
    def test_coins(self):
        self.assertEqual(run("coins", "1780")[0], "3 monedas de S/ 5; quedan 280 céntimos\n")
        self.assertEqual(run("coins", "500")[0], "1 monedas de S/ 5; quedan 0 céntimos\n")
        self.assertEqual(run("coins", "499")[0], "0 monedas de S/ 5; quedan 499 céntimos\n")
        self.assertEqual(run("coins", "abc"), ("Entrada inválida\n", 1))

    def test_sum_matches_the_formula(self):
        for n in [0, 1, 2, 4, 10, 100, 65535]:
            with self.subTest(n=n):
                self.assertEqual(run("sum_to_n", str(n))[0],
                                 f"La suma de 1 a {n} es {n * (n + 1) // 2}\n")

    def test_sum_with_no_turns(self):
        self.assertEqual(run("sum_to_n", "-3")[0], "La suma de 1 a -3 es 0\n")

    def test_sum_overflow_is_reported(self):
        # Solo el aviso: lo que escribe después es comportamiento indefinido.
        self.assertIn("signed integer overflow", run("sum_to_n", "70000")[0])
        self.assertNotIn("runtime error", run("sum_to_n", "65535")[0])

    def test_no_update_never_ends(self):
        messages, status, binary = compile_error_demo("no_update")
        self.assertEqual((messages, status), ("", 0))
        lines, still_running = first_lines(binary, "", 50)
        self.assertEqual(lines, ["3\n"] * 50)
        self.assertTrue(still_running)


class ForLoops(unittest.TestCase):
    def test_for_equals_its_while(self):
        expected = "i vale 0\ni vale 3\ni vale 6\ni vale 9\nAl salir, i vale 12\n"
        self.assertEqual(run("for_trace")[0], expected)
        self.assertEqual(run("for_as_while")[0], expected)

    def test_mult_table(self):
        for n in [7, -3, 0, 1000]:
            lines = run("mult_table", str(n))[0].splitlines()
            self.assertEqual(len(lines), 12)
            self.assertEqual(lines[0], f"{n} x  1 = {n}")
            self.assertEqual(lines[11], f"{n} x 12 = {n * 12}")

    def test_mult_table_rejects(self):
        self.assertEqual(run("mult_table", "1001"), ("Número fuera de rango\n", 1))
        self.assertEqual(run("mult_table", "abc"), ("Entrada inválida\n", 1))

    def test_to_binary_all_values(self):
        for n in range(256):
            self.assertEqual(run("to_binary", str(n))[0], f"{n:08b}\n")

    def test_to_binary_rejects(self):
        for text in ["-1", "256", "300"]:
            self.assertEqual(run("to_binary", text), ("Número fuera de rango\n", 1))

    def test_semicolon_for(self):
        messages, status, binary = compile_error_demo("semicolon_for")
        self.assertEqual(status, 0)
        self.assertIn("-Wmisleading-indentation", messages)
        self.assertEqual(subprocess.run([str(binary)], text=True, stdout=subprocess.PIPE).stdout, "4\n")

    def test_off_by_one(self):
        messages, status, binary = compile_error_demo("off_by_one")
        self.assertEqual((messages, status), ("", 0))
        self.assertEqual(subprocess.run([str(binary)], text=True, stdout=subprocess.PIPE).stdout,
                         "1\n2\n3\n4\n")

    def test_turn_counts_of_the_table(self):
        # Las cuatro filas de la tabla de "Salirse por uno", calculadas con C.
        for bounds, turns in [("int i = 0; i < n; i++", "n"), ("int i = 1; i <= n; i++", "n"),
                              ("int i = 0; i <= n; i++", "n + 1"), ("int i = 1; i < n; i++", "n - 1")]:
            source = ('#include <stdio.h>\nint main(void) { int n = 7; int t = 0;\n'
                      f'for ({bounds}) {{ t++; }}\nprintf("%d %d\\n", t, {turns}); return 0; }}\n')
            folder = pathlib.Path(tempfile.mkdtemp())
            (folder / "t.c").write_text(source)
            subprocess.run(["gcc", *FLAGS, str(folder / "t.c"), "-o", str(folder / "t")], check=True)
            first, second = subprocess.run([str(folder / "t")], text=True,
                                           stdout=subprocess.PIPE).stdout.split()
            with self.subTest(bounds=bounds):
                self.assertEqual(first, second)


class DoubleLoops(unittest.TestCase):
    def test_never_equal(self):
        _, status, binary = compile_error_demo("double_never_equal")
        self.assertEqual(status, 0)
        lines, _ = first_lines(binary, "", 12)
        self.assertEqual(lines[10], "0.99999999999999989\n")
        self.assertEqual(lines[11], "1.09999999999999987\n")

    def test_extra_turn(self):
        _, _, binary = compile_error_demo("double_extra_turn")
        self.assertEqual(subprocess.run([str(binary)], text=True, stdout=subprocess.PIPE).stdout,
                         "Vueltas: 11\n")

    def test_integer_counter(self):
        lines = run("double_steps")[0].splitlines()
        self.assertEqual(lines, [f"{i / 10:.1f}" for i in range(11)])


class DoWhile(unittest.TestCase):
    def test_runs_once(self):
        self.assertEqual(run("while_vs_do")[0], "do while: entré\nn vale 6\n")

    def test_read_month_retries(self):
        self.assertEqual(run("read_month", "13 0 7"),
                         ("Mes fuera de rango, escriba otro\n" * 2 + "Mes elegido: 7\n", 0))
        for month in [1, 12]:
            self.assertEqual(run("read_month", str(month)), (f"Mes elegido: {month}\n", 0))

    def test_read_month_ends_on_bad_input(self):
        self.assertEqual(run("read_month", "abc"), ("Entrada inválida\n", 1))
        self.assertEqual(run("read_month", ""), ("Entrada inválida\n", 1))
        self.assertEqual(run("read_month", "13"),
                         ("Mes fuera de rango, escriba otro\nEntrada inválida\n", 1))

    def test_read_forever_does_not_end(self):
        for text in ["abc", ""]:
            _, status, binary = compile_error_demo("read_forever")
            self.assertEqual(status, 0)
            lines, still_running = first_lines(binary, text, 500)
            self.assertEqual(lines, ["Mes fuera de rango\n"] * 500)
            self.assertTrue(still_running)

    def test_do_scope_does_not_compile(self):
        messages, status, _ = compile_error_demo("do_scope")
        self.assertNotEqual(status, 0)
        self.assertIn("undeclared", messages)


class Patterns(unittest.TestCase):
    def test_count_passed(self):
        grades = (HERE / "grades.txt").read_text()
        self.assertEqual(grades.split(), ["14", "9", "11", "20", "10"])
        self.assertEqual(run("count_passed", grades), ("Aprobaron 3 de 5\n", 0))
        self.assertEqual(run("count_passed", ""), ("Aprobaron 0 de 0\n", 0))
        self.assertEqual(run("count_passed", "14 abc"), ("Entrada inválida\n", 1))

    def test_not_eof_spins_only_on_bad_data(self):
        _, status, binary = compile_error_demo("not_eof")
        self.assertEqual(status, 0)
        lines, still_running = first_lines(binary, "abc", 500)
        self.assertEqual(lines[2], "Llevo 3 datos; el último es 0\n")
        self.assertTrue(still_running)
        done = subprocess.run([str(binary)], input="4\n", text=True, stdout=subprocess.PIPE, timeout=10)
        self.assertEqual(done.stdout, "Llevo 1 datos; el último es 4\n")

    def test_sentinel(self):
        self.assertEqual(run("sentinel_sum", "1250 300 4050 0"), ("3 productos: 56.00 soles\n", 0))
        self.assertEqual(run("sentinel_sum", "0"), ("0 productos: 0.00 soles\n", 0))
        self.assertEqual(run("sentinel_sum", "5 0 7 0"), ("1 productos: 0.05 soles\n", 0))

    def test_sentinel_ends_on_bad_input(self):
        for text in ["", "1250 300", "1250 abc", "abc"]:
            with self.subTest(text=text):
                self.assertEqual(run("sentinel_sum", text), ("Entrada inválida\n", 1))

    def test_max_of_n(self):
        cases = {"3 -3 -7 -1": -1, "3 8 -7 12": 12, "1 -5": -5, "3 5 5 5": 5, "3 9 1 2": 9, "3 1 2 9": 9}
        for text, expected in cases.items():
            with self.subTest(text=text):
                self.assertEqual(run("max_of_n", text), (f"La mayor es {expected}\n", 0))

    def test_max_of_n_rejects(self):
        for text in ["", "abc", "0", "-1", "3 1 2", "2 1 abc"]:
            with self.subTest(text=text):
                self.assertEqual(run("max_of_n", text), ("Entrada inválida\n", 1))

    def test_max_from_zero_is_wrong(self):
        _, status, binary = compile_error_demo("max_from_zero")
        self.assertEqual(status, 0)
        done = subprocess.run([str(binary)], input="3 -3 -7 -1", text=True, stdout=subprocess.PIPE)
        self.assertEqual(done.stdout, "La mayor es 0\n")


class Getchar(unittest.TestCase):
    def test_count_bytes(self):
        self.assertEqual(run("count_bytes", "")[0], "0 bytes\n")
        self.assertEqual((HERE / "cities.txt").read_bytes(), b"Puno\nCusco\nPiura\n")
        self.assertEqual(run("count_bytes", "Puno\nCusco\nPiura\n")[0], "17 bytes\n")
        self.assertEqual(run("count_bytes", "ñ\n")[0], "3 bytes\n")

    def test_to_upper_only_ascii(self):
        self.assertEqual(run("to_upper", "hola mundo\n")[0], "HOLA MUNDO\n")
        self.assertEqual(run("to_upper", "ñandú\n")[0], "ñANDú\n")
        self.assertEqual(run("to_upper", "az AZ 09 `{\n")[0], "AZ AZ 09 `{\n")

    def test_copy_keeps_every_byte(self):
        data = bytes(range(256)) * 3
        done = subprocess.run([str(BUILD / "copy")], input=data, stdout=subprocess.PIPE, timeout=10)
        self.assertEqual(done.stdout, data)

    def test_missing_parentheses(self):
        messages, status, binary = compile_error_demo("getchar_no_parens")
        self.assertEqual(status, 0)
        self.assertIn("-Wparentheses", messages)
        done = subprocess.run([str(binary)], input="a\nb\n", text=True, stdout=subprocess.PIPE, timeout=10)
        self.assertEqual(done.stdout, "0 saltos de línea\n")

    def test_char_without_sign_never_ends(self):
        # -funsigned-char da el mismo comportamiento en ARM y en x86-64.
        messages, status, binary = compile_error_demo("char_eof", "-funsigned-char")
        self.assertEqual(status, 0)
        self.assertIn("comparison is always true due to limited range of data type", messages)
        with self.assertRaises(subprocess.TimeoutExpired):
            subprocess.run([str(binary)], input="a\n", text=True, stdout=subprocess.PIPE, timeout=1)

    def test_char_with_sign_stops_at_0xff(self):
        messages, status, binary = compile_error_demo("char_eof", "-fsigned-char")
        self.assertEqual((messages, status), ("", 0))
        done = subprocess.run([str(binary)], input=b"a\xffb\n", stdout=subprocess.PIPE, timeout=10)
        self.assertEqual(done.stdout, b"1 bytes\n")


if __name__ == "__main__":
    unittest.main()
