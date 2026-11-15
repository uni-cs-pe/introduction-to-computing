"""Comprueba lo que los apuntes afirman sobre los programas de la semana 9."""
import pathlib
import re
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


def compile_demo(name, *extra):
    """Compila un programa de errors/; devuelve los mensajes, el estado y el ejecutable."""
    out = pathlib.Path(tempfile.mkdtemp()) / name
    done = subprocess.run(
        ["gcc", *FLAGS, *extra, f"errors/{name}.c", "-o", str(out)], cwd=HERE,
        text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
    )
    return done.stdout, done.returncode, out


def run_binary(binary, stdin=""):
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


class Addresses(unittest.TestCase):
    def test_variable_addresses_show_sizes(self):
        out, status = run("variable_addresses")
        self.assertEqual(status, 0)
        self.assertRegex(out, r"age     vale 19, ocupa \d+ bytes, está en 0x[0-9a-f]+\n")
        self.assertIn("average vale 14.5", out)
        self.assertIn("section vale A, ocupa 1 byte,", out)

    def test_elements_of_an_array_are_contiguous(self):
        out, status = run("array_addresses")
        self.assertEqual(status, 0)
        size = int(re.search(r"sizeof\(int\) = (\d+)", out).group(1))
        addresses = [int(a, 16) for a in re.findall(r"está en 0x([0-9a-f]+)", out)]
        self.assertEqual(len(addresses), 4)
        for i, address in enumerate(addresses):
            self.assertEqual(address, addresses[0] + i * size)


class Arrays(unittest.TestCase):
    def test_first_array(self):
        out, _ = run("first_array")
        self.assertEqual(out.split("\n")[1], "grades[1] = 12")
        self.assertEqual(out.split("\n")[4], "grades[4] = 19")

    def test_missing_initializers_are_zero(self):
        out, _ = run("array_init")
        self.assertIn("i = 2: full 4, partial 0, zeros 0", out)
        self.assertIn("i = 4: full 5, partial 0, zeros 0", out)

    def test_element_count_does_not_depend_on_int_size(self):
        out, _ = run("array_init")
        self.assertIn("elementos de full    = 5", out)
        self.assertIn("elementos de counted = 3", out)

    def test_copy_is_independent(self):
        self.assertEqual(run("copy_array")[0], "original[0] = 5, copy[0] = 99\n")

    def test_assigning_an_array_does_not_compile(self):
        messages, status, _ = compile_demo("assign_array")
        self.assertNotEqual(status, 0)
        self.assertIn("assignment to expression with array type", messages)

    def test_comparing_arrays_warns_and_says_different(self):
        messages, status, binary = compile_demo("compare_arrays")
        self.assertEqual(status, 0)
        self.assertIn("-Warray-compare", messages)
        self.assertEqual(run_binary(binary)[0], "distintos\n")


class Patterns(unittest.TestCase):
    def test_temperatures(self):
        self.assertEqual(run("temperatures"),
                         ("Suma: 3\nPromedio: 0.43\nMayor: 4, en el día 2\n", 0))

    def test_reverse(self):
        self.assertEqual(run("reverse", "3 10 20 30"), ("30\n20\n10\n", 0))
        self.assertEqual(run("reverse", "1 7"), ("7\n", 0))

    def test_reverse_full_array(self):
        values = list(range(100))
        text = "100 " + " ".join(map(str, values))
        expected = "".join(f"{v}\n" for v in reversed(values))
        self.assertEqual(run("reverse", text), (expected, 0))

    def test_reverse_rejects_what_does_not_fit(self):
        for n in [0, -1, 101, 200]:
            with self.subTest(n=n):
                self.assertEqual(run("reverse", f"{n} 1 2"), ("n debe estar entre 1 y 100\n", 1))

    def test_reverse_bad_input(self):
        for text in ["", "abc", "3 10 20", "3 10 x"]:
            with self.subTest(text=text):
                self.assertEqual(run("reverse", text), ("Entrada inválida\n", 1))

    def test_votes(self):
        out, status = run("votes", "1 2 2 3 7 2 0")
        self.assertEqual(status, 0)
        self.assertEqual(out, "Candidato 1: 1\nCandidato 2: 3\nCandidato 3: 1\nInválidos: 1\n")

    def test_votes_rejects_indexes_out_of_the_array(self):
        out, status = run("votes", "4 -1 100000 -100000 3 0")
        self.assertEqual(status, 0)
        self.assertEqual(out, "Candidato 1: 0\nCandidato 2: 0\nCandidato 3: 1\nInválidos: 4\n")

    def test_votes_bad_input(self):
        for text in ["", "abc", "1 2", "1 x"]:
            with self.subTest(text=text):
                self.assertEqual(run("votes", text), ("Entrada inválida\n", 1))


class OutOfBounds(unittest.TestCase):
    """Sin sanitizer no se compara nada: el resultado es comportamiento indefinido."""

    def test_compiling_says_nothing(self):
        for name in ["off_by_one", "write_out", "fixed_constant"]:
            with self.subTest(name=name):
                messages, status, _ = compile_demo(name)
                self.assertEqual((messages, status), ("", 0))

    def test_address_sanitizer_reports_the_read(self):
        messages, status, binary = compile_demo("off_by_one", "-g", "-fsanitize=address")
        self.assertEqual((messages, status), ("", 0))
        out, status = run_binary(binary)
        self.assertNotEqual(status, 0)
        self.assertNotIn("grades[5] =", out)
        self.assertIn("stack-buffer-overflow", out)
        self.assertIn("READ of size 4", out)
        self.assertIn("errors/off_by_one.c:11", out)

    def test_address_sanitizer_reports_the_write_next_to_the_array(self):
        _, _, binary = compile_demo("write_out", "-g", "-fsanitize=address")
        out, status = run_binary(binary, "4")
        self.assertNotEqual(status, 0)
        self.assertIn("stack-buffer-overflow", out)
        self.assertIn("WRITE of size 4", out)

    def test_valid_index_gives_no_report(self):
        _, _, binary = compile_demo("write_out", "-g", "-fsanitize=address")
        self.assertEqual(run_binary(binary, "3"),
                         ("values[3] = 99\nbefore = 111, after = 222\n", 0))

    def test_undefined_sanitizer_checks_the_index(self):
        _, _, binary = compile_demo("write_out", "-g", "-fsanitize=address,undefined")
        out, status = run_binary(binary, "4")
        self.assertNotEqual(status, 0)
        self.assertIn("runtime error: index 4 out of bounds for type 'int [4]'", out)
        self.assertIn("stack-buffer-overflow", out)

    def test_debug_flag_adds_the_line_number(self):
        _, _, without_g = compile_demo("off_by_one", "-fsanitize=address")
        self.assertNotIn("errors/off_by_one.c:11", run_binary(without_g)[0])


class Assembly(unittest.TestCase):
    def test_the_sum_stays_in_the_assembly(self):
        # Una suma entre dos registros: add de tres operandos en ARM, addl de dos en x86-64.
        # Con -O2 el compilador calcula el resultado y la suma desaparece.
        sum_of_registers = r"\badd\s+w\d+, w\d+, w\d+|\baddl\s+%\w+, %\w+"
        folder = pathlib.Path(tempfile.mkdtemp())
        for level, check in (("-O0", self.assertRegex), ("-O2", self.assertNotRegex)):
            target = folder / f"add_two{level}.s"
            subprocess.run(["gcc", "-S", level, "add_two.c", "-o", str(target)], cwd=HERE, check=True)
            check(target.read_text(), sum_of_registers)
        self.assertEqual(run("add_two")[0], "5\n")


if __name__ == "__main__":
    unittest.main()
