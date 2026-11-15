"""Comprueba lo que los apuntes afirman sobre los programas de la semana 13.
Los tiempos dependen de la máquina: aquí se comparan cuentas, nunca segundos."""
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
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=60,
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


def binary_probes(n, value):
    """La misma búsqueda binaria en Python, sobre los pares 0, 2, ..., 2n - 2."""
    low, high, probes = 0, n - 1, 0
    while low <= high:
        mid = low + (high - low) // 2
        probes += 1
        if 2 * mid == value:
            return probes
        if 2 * mid < value:
            low = mid + 1
        else:
            high = mid - 1
    return probes


class CleanCompile(unittest.TestCase):
    def test_examples_have_no_warnings(self):
        for source in sorted(HERE.glob("*.c")):
            with self.subTest(source=source.name):
                done = subprocess.run(
                    ["gcc", *FLAGS, "-Werror", "-fsyntax-only", str(source)],
                    text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                )
                self.assertEqual(done.returncode, 0, done.stdout)

    def test_no_malloc_in_the_course(self):
        for source in list(HERE.glob("*.c")) + list((HERE / "errors").glob("*.c")):
            with self.subTest(source=source.name):
                self.assertNotIn("malloc", source.read_text(encoding="utf-8"))

    def test_timing_programs_have_no_sanitizers(self):
        for program in ["sort_times", "sort_then_search"]:
            with self.subTest(program=program):
                self.assertNotIn(b"__asan", (BUILD / "fast" / program).read_bytes())
        self.assertIn(b"__asan", (BUILD / "selection_sort").read_bytes())


class Searches(unittest.TestCase):
    def test_linear_search(self):
        self.assertEqual(run("linear_search"), (
            "Buscar 17 devuelve 2\nBuscar 13 devuelve -1\n", 0))

    def test_binary_search_asserts(self):
        self.assertEqual(run("binary_search"), ("Todas las pruebas pasaron\n", 0))

    def test_trace_of_a_value_that_is_there(self):
        self.assertEqual(run("binary_trace", "23\n"), (
            "low = 0, high = 9, mid = 4, a[mid] = 16\n"
            "low = 5, high = 9, mid = 7, a[mid] = 56\n"
            "low = 5, high = 6, mid = 5, a[mid] = 23\n"
            "Resultado: 5\n", 0))

    def test_trace_of_a_value_that_is_not_there(self):
        output, code = run("binary_trace", "40\n")
        self.assertEqual(code, 0)
        self.assertEqual(output.splitlines()[-2:], [
            "low = 7, high = 6: ya no queda nada", "Resultado: -1"])

    def test_trace_rejects_bad_input(self):
        self.assertEqual(run("binary_trace", "abc\n"), ("Entrada inválida\n", 1))

    def test_unsorted_data_breaks_binary_search(self):
        _, status, binary = build_source("errors/binary_unsorted.c")
        self.assertEqual(status, 0)
        self.assertEqual(execute([str(binary)]), (
            "El 5 está en el índice 0; binaria responde 0\n"
            "El 1 está en el índice 1; binaria responde -1\n"
            "El 9 está en el índice 2; binaria responde 2\n"
            "El 3 está en el índice 3; binaria responde -1\n"
            "El 7 está en el índice 4; binaria responde -1\n", 0))

    def test_low_less_than_high_misses_values(self):
        _, status, binary = build_source("errors/low_less_high.c")
        self.assertEqual(status, 0)
        self.assertEqual(execute([str(binary)]), (
            "El 10 está en el índice 0; responde -1\n"
            "El 20 está en el índice 1; responde 1\n"
            "El 30 está en el índice 2; responde -1\n", 0))

    def test_sum_of_low_and_high_overflows(self):
        _, status, binary = build_source("errors/mid_overflow.c", *SANITIZE)
        self.assertEqual(status, 0)
        output, _ = execute([str(binary)], "2000000000 2100000000\n")
        self.assertIn("signed integer overflow", output)
        self.assertIn("Fórmula segura: 2050000000", output)

    def test_safe_formula_is_silent_when_nothing_overflows(self):
        _, status, binary = build_source("errors/mid_overflow.c", *SANITIZE)
        self.assertEqual(status, 0)
        output, _ = execute([str(binary)], "4 9\n")
        self.assertNotIn("runtime error", output)
        self.assertEqual(output, "Fórmula segura: 6\nFórmula con la suma: 6\n")


class Counting(unittest.TestCase):
    def test_table_matches_an_independent_simulation(self):
        output, code = run("count_search")
        self.assertEqual(code, 0, output)
        rows = [line.split() for line in output.splitlines()[1:4]]
        for row in rows:
            n, linear, binary, worst = map(int, row)
            with self.subTest(n=n):
                self.assertEqual(linear, n)
                self.assertEqual(binary, binary_probes(n, 2 * n))
                self.assertEqual(worst, max(binary_probes(n, v) for v in range(-1, 2 * n + 1)))
        self.assertEqual([row[0] for row in rows], ["1000", "10000", "100000"])

    def test_averages_with_1000_elements(self):
        output, _ = run("count_search")
        average = sum(binary_probes(1000, 2 * i) for i in range(1000)) / 1000
        self.assertIn(f"lineal {(1000 + 1) / 2:.2f}, binaria {average:.2f}", output)

    def test_one_million_needs_twenty(self):
        output, _ = run("growth")
        self.assertRegex(output, r"1000000\s+20\s+1000000\s+1000000000000\n")
        self.assertEqual(binary_probes(1000000, 2 * 1000000), 20)

    def test_growth_doubling_rows(self):
        output, _ = run("growth")
        first = [list(map(int, line.split())) for line in output.splitlines()[1:5]]
        self.assertEqual([row[0] for row in first], [1000, 2000, 4000, 8000])
        for before, after in zip(first, first[1:]):
            self.assertEqual(after[1], before[1] + 1)      # log suma 1
            self.assertEqual(after[2], before[2] * 2)      # N se duplica
            self.assertEqual(after[3], before[3] * 4)      # N*N se multiplica por 4


class Sorting(unittest.TestCase):
    def test_selection_sort_trace(self):
        self.assertEqual(run("selection_sort"), (
            "Inicio: 29 10 14 37 13\n"
            "i = 0, menor en 1: 10 29 14 37 13\n"
            "i = 1, menor en 4: 10 13 14 37 29\n"
            "i = 2, menor en 2: 10 13 14 37 29\n"
            "i = 3, menor en 4: 10 13 14 29 37\n"
            "Comparaciones: 10\n"
            "Inicio: 10 13 14 29 37\n"
            "i = 0, menor en 0: 10 13 14 29 37\n"
            "i = 1, menor en 1: 10 13 14 29 37\n"
            "i = 2, menor en 2: 10 13 14 29 37\n"
            "i = 3, menor en 3: 10 13 14 29 37\n"
            "Comparaciones: 10\n", 0))

    def test_exact_comparisons_and_real_sorting(self):
        output, code = run("fast/sort_times", "1 2 1000 5000\n")
        self.assertEqual(code, 0, output)
        rows = [line.split() for line in output.splitlines()[1:]]
        self.assertEqual(len(rows), 4)
        for row in rows:
            n = int(row[0])
            with self.subTest(n=n):
                self.assertEqual(int(row[1]), n * (n - 1) // 2)
                self.assertRegex(row[2], r"^\d+\.\d{4}s$")
                self.assertRegex(row[3], r"^\d+\.\d{4}s$")
                self.assertEqual(row[4], "sí")

    def test_sizes_are_checked(self):
        output, code = run("fast/sort_times", "100001\n")
        self.assertEqual(code, 1)
        self.assertIn("Tamaño inválido", output)

    def test_qsort_demo(self):
        self.assertEqual(run("qsort_demo"), (" 9 9 11 14 17 20\n", 0))

    def test_subtracting_to_compare_overflows(self):
        _, status, binary = build_source("errors/compare_subtract.c", *SANITIZE)
        self.assertEqual(status, 0)
        output, _ = execute([str(binary)])
        self.assertIn("signed integer overflow", output)

    def test_sort_then_search_counts(self):
        output, code = run("fast/sort_then_search", "1000 1 10 1000\n")
        self.assertEqual(code, 0, output)
        rows = [line.split() for line in output.splitlines()[1:]]
        for row in rows:
            k = int(row[0])
            with self.subTest(k=k):
                self.assertEqual(int(row[1]), k * 1000)
                expected = sum(binary_probes(1000, 2 * (t % 1000) + 1) for t in range(k))
                self.assertEqual(int(row[2]), expected)


class Recursion(unittest.TestCase):
    def test_factorial_trace(self):
        self.assertEqual(run("factorial"), (
            "entra factorial(4)\nentra factorial(3)\nentra factorial(2)\nentra factorial(1)\n"
            "caso base: factorial(1) devuelve 1\n"
            "factorial(2) devuelve 2\nfactorial(3) devuelve 6\nfactorial(4) devuelve 24\n"
            "factorial(20) = 2432902008176640000\n", 0))

    def test_no_base_case_warns_and_dies(self):
        messages, status, binary = build_source("errors/no_base_case.c")
        self.assertEqual(status, 0)
        self.assertIn("-Winfinite-recursion", messages)
        _, code = execute(["bash", "-c", f"ulimit -s 8192; {binary}"])
        self.assertNotEqual(code, 0)

    def test_no_base_case_with_the_sanitizer(self):
        _, status, binary = build_source("errors/no_base_case.c", *SANITIZE)
        self.assertEqual(status, 0)
        # Siempre muere, pero en x86-64 emulado a veces no alcanza a escribir el informe.
        outputs = []
        for _ in range(12):
            output, code = execute(["bash", "-c", f"ulimit -s 8192; {binary}"])
            self.assertNotEqual(code, 0)
            outputs.append(output)
            if "AddressSanitizer: stack-overflow" in output:
                break
        self.assertRegex(outputs[-1], "AddressSanitizer: stack-overflow")

    def test_deep_recursion(self):
        _, status, binary = build_source("errors/deep_recursion.c")
        self.assertEqual(status, 0)
        self.assertEqual(execute([str(binary)], "1000\n"), ("500500\n", 0))
        _, code = execute(["bash", "-c", f"ulimit -s 8192; echo 10000000 | {binary}"])
        self.assertNotEqual(code, 0)


if __name__ == "__main__":
    unittest.main()
