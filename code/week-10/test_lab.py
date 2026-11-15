"""Pruebas del laboratorio. LAB_DIR dice dónde está el código: lab o solution."""
import os
import pathlib
import subprocess
import unittest

HERE = pathlib.Path(__file__).parent
LAB_DIR = os.environ.get("LAB_DIR", "solution")


def run(program, stdin=""):
    done = subprocess.run(
        [str(HERE / "build" / LAB_DIR / program)], input=stdin, encoding="utf-8", errors="replace",
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=10,
    )
    return done.stdout, done.returncode


def call(*args):
    """Llama a una función de my_strings.c y devuelve lo que imprime el programa de prueba."""
    done = subprocess.run(
        [str(HERE / "build" / LAB_DIR / "check_strings")] + [a.encode("utf-8") for a in args],
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=10,
    )
    return done.stdout.decode("utf-8", "replace").strip()


@unittest.skipUnless((HERE / LAB_DIR).is_dir(), f"no existe {LAB_DIR}/")
class LabTests(unittest.TestCase):
    def test_no_warnings(self):
        for name in ["my_strings", "greet"]:
            with self.subTest(name=name):
                done = subprocess.run(
                    ["gcc", "-Wall", "-Wextra", "-std=c17", "-Werror", "-fsyntax-only",
                     str(HERE / LAB_DIR / f"{name}.c")],
                    text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                )
                self.assertEqual(done.returncode, 0, done.stdout)

    def test_does_not_use_string_h(self):
        text = (HERE / LAB_DIR / "my_strings.c").read_text(encoding="utf-8")
        self.assertNotRegex(text, r"#\s*include\s*<string\.h>")

    def test_your_own_asserts_pass(self):
        output, code = run("my_strings")
        self.assertEqual((output, code), ("Todas las pruebas pasaron\n", 0))

    def test_my_strlen(self):
        for text, expected in {"": "0", "a": "1", "hola": "4", "dos palabras": "12",
                               "año": "4", "ñandú": "7"}.items():
            with self.subTest(text=text):
                self.assertEqual(call("l", text), expected)

    def test_my_strcmp_equal(self):
        for text in ["", "a", "ana", "año"]:
            with self.subTest(text=text):
                self.assertEqual(call("c", text, text), "0")

    def test_my_strcmp_order(self):
        # Solo importa el signo. Cada par (a, b) cumple que a va antes que b.
        pairs = [("ana", "ano"), ("Z", "a"), ("an", "ana"), ("", "a"), ("a", "b"), ("z", "ñ")]
        for a, b in pairs:
            with self.subTest(a=a, b=b):
                self.assertLess(int(call("c", a, b)), 0)
                self.assertGreater(int(call("c", b, a)), 0)

    def test_to_upper(self):
        cases = {"hola": "HOLA", "": "", "Ya ES": "YA ES", "lima 2026!": "LIMA 2026!",
                 "az{`": "AZ{`", "año": "AñO"}
        for text, expected in cases.items():
            with self.subTest(text=text):
                self.assertEqual(call("u", text), expected)

    def test_is_palindrome(self):
        cases = {"": "1", "a": "1", "aa": "1", "ab": "0", "abba": "1", "reconocer": "1",
                 "abca": "0", "Ana": "0", "ana ana": "1", "a a": "1", "ana a": "0",
                 "aña": "0"}
        for text, expected in cases.items():
            with self.subTest(text=text):
                self.assertEqual(call("p", text), expected)

    def test_is_palindrome_text(self):
        cases = {"": "1", "   ": "1", "a": "1", " a ": "1", "Ana": "1", "ANA": "1", "ab": "0",
                 "Anita lava la tina": "1", "  a b  B A": "1", "Hola": "0", "a b c": "0"}
        for text, expected in cases.items():
            with self.subTest(text=text):
                self.assertEqual(call("t", text), expected)

    def test_greet(self):
        cases = {"Ana\n": "Hola, Ana\n", "Ana": "Hola, Ana\n", "Ana Li\n": "Hola, Ana Li\n",
                 "Rosaura\n": "Hola, Rosaura\n", "Alejandra\n": "Hola, Alejand\n"}
        for text, expected in cases.items():
            with self.subTest(text=text):
                self.assertEqual(run("greet", text), (expected, 0))

    def test_greet_no_name(self):
        for text in ["", "\n"]:
            with self.subTest(text=text):
                self.assertEqual(run("greet", text), ("Entrada inválida\n", 1))


if __name__ == "__main__":
    unittest.main()
