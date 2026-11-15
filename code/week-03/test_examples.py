"""Pruebas de los ejemplos de la semana 3: comparan la salida real de cada programa
con lo que dicen los apuntes. Se corren con `make test`."""
import re
import subprocess
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
BUILD = HERE / "build"
PROGRAMS = sorted(p for p in HERE.glob("*.c"))


def run(name, stdin=""):
    if isinstance(stdin, str):
        stdin = stdin.encode()
    return subprocess.run([str(BUILD / name)], input=stdin, capture_output=True, timeout=20)


def out(name, stdin=""):
    result = run(name, stdin)
    return result.stdout.decode()


def compile_c(source, target, *flags):
    return subprocess.run(["gcc", "-Wall", "-Wextra", "-std=c17", *flags, "-o", str(target), str(source)],
                          capture_output=True, text=True, cwd=HERE)


class Warnings(unittest.TestCase):
    def test_no_warnings(self):
        for source in PROGRAMS:
            with self.subTest(source=source.name):
                result = subprocess.run(["gcc", "-Wall", "-Wextra", "-Werror", "-std=c17", "-fsyntax-only", str(source)],
                                        capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)


class Bases(unittest.TestCase):
    def test_to_binary(self):
        self.assertEqual(out("to_binary", "202\n"), "scanf leyó 1 dato(s)\n11001010\n")
        self.assertEqual(out("to_binary", "182\n"), "scanf leyó 1 dato(s)\n10110110\n")

    def test_to_binary_bad_input(self):
        self.assertEqual(out("to_binary", "hola\n"), "scanf leyó 0 dato(s)\n00000000\n")

    def test_from_binary(self):
        self.assertEqual(out("from_binary", "10110110\n"),
                         "scanf leyó 8 dígitos\ndecimal: 182\nhexadecimal: b6\n")

    def test_bases(self):
        self.assertEqual(out("bases"), "202 en decimal\n"
                                       "ca en hexadecimal, con minúsculas\n"
                                       "CA en hexadecimal, con mayúsculas\n"
                                       "0xCA vale 202\n")

    def test_multiples(self):
        self.assertEqual(f"{500 * 10**9 / 2**30:.2f}", "465.66")
        self.assertEqual(100 * 10**6 / 8 / 10**6, 12.5)
        self.assertEqual(2**31 - 1, 2147483647)


class Integers(unittest.TestCase):
    def test_sizes(self):
        self.assertEqual(out("sizes"), "bits en un byte: 8\n"
                                       "sizeof(char)   = 1\n"
                                       "sizeof(int)    = 4\n"
                                       "sizeof(double) = 8\n"
                                       "INT_MAX = 2147483647\n"
                                       "INT_MIN = -2147483648\n")

    def test_twos_complement(self):
        table = {5: ("00000101", "00000005"), -1: ("11111111", "ffffffff"),
                 -3: ("11111101", "fffffffd"), -128: ("10000000", "ffffff80"),
                 127: ("01111111", "0000007f")}
        for x, (bits, word) in table.items():
            with self.subTest(x=x):
                self.assertEqual(out("twos_complement", f"{x}\n"),
                                 f"scanf leyó 1 dato(s)\n{x} en 8 bits: {bits}\n{x} en un int: {word}\n")

    def test_overflow_reported(self):
        result = run("overflow", "2147483647\n")
        self.assertIn("overflow.c:9:9: runtime error: signed integer overflow: "
                      "2147483647 + 1 cannot be represented in type 'int'", result.stderr.decode())

    def test_no_overflow(self):
        result = run("overflow", "41\n")
        self.assertEqual(result.stdout.decode(), "scanf leyó 1 dato(s), n = 41\nn + 1 = 42\n")
        self.assertEqual(result.stderr, b"")

    def test_overflow_bad_input(self):
        self.assertEqual(out("overflow", "hola\n"), "scanf leyó 0 dato(s), n = 0\nn + 1 = 1\n")

    def test_constant_overflow_warns(self):
        result = compile_c("bad/constant_overflow.c", BUILD / "constant_overflow")
        self.assertIn("warning: integer overflow in expression", result.stderr)

    def test_unsigned_wrap(self):
        result = run("unsigned_wrap")
        self.assertEqual(result.stdout.decode(), "b = 255\nb = 0\n")
        self.assertEqual(result.stderr, b"")


class Floats(unittest.TestCase):
    def test_float_sum(self):
        self.assertEqual(out("float_sum"), "con %f:     0.300000\n"
                                           "0.1       = 0.10000000000000000555\n"
                                           "0.2       = 0.20000000000000001110\n"
                                           "0.3       = 0.29999999999999998890\n"
                                           "0.1 + 0.2 = 0.30000000000000004441\n"
                                           "diferencia = 0.00000000000000005551\n"
                                           "sum == c vale 0\n")

    def test_float_limits(self):
        self.assertEqual(out("float_limits"), "0.5 + 0.25     = 0.75000000000000000000\n"
                                              "diez veces 0.1 = 0.99999999999999988898\n"
                                              "big            = 9007199254740992.0\n"
                                              "big + 1        = 9007199254740992.0\n")

    def test_compare_doubles(self):
        self.assertEqual(out("compare_doubles"), "sum == target vale 0\n"
                                                 "fabs(sum - target) < tolerance vale 1\n")

    def test_money(self):
        self.assertEqual(out("money"), "3 x 1.10 con double: 3.30000000000000026645\n"
                                       "lo mismo con %.2f:   3.30\n"
                                       "saldo con double:    0.00000000000000013878\n"
                                       "3 x 110 céntimos:    330\n"
                                       "en soles:            S/ 3.30\n"
                                       "saldo en céntimos:   0\n")

    def test_fraction_to_binary(self):
        self.assertEqual(out("fraction_to_binary", "0.1\n"), "scanf leyó 1 dato(s)\n0.000110011...\n")
        self.assertEqual(out("fraction_to_binary", "0.75\n"), "scanf leyó 1 dato(s)\n0.110000000...\n")

    def test_tenth_doubling(self):
        # Los bits de 0.1 de la tabla de los apuntes, con fracciones exactas.
        from fractions import Fraction
        x = Fraction(1, 10)
        bits = ""
        for _ in range(9):
            x *= 2
            bits += str(int(x))
            x -= int(x)
        self.assertEqual(bits, "000110011")


class Text(unittest.TestCase):
    def test_char_codes(self):
        self.assertEqual(out("char_codes"), "A tiene el código 65\n"
                                            "B tiene el código 66\n"
                                            "'a' - 'A' = 32\n"
                                            "minúscula de A: a\n"
                                            "7 tiene el código 55\n"
                                            "'7' - '0' = 7\n")

    def test_char_sign_both_platforms(self):
        # El signo de char depende de la plataforma: se comprueban las dos variantes.
        cases = {"-fsigned-char": ("CHAR_MIN = -128, CHAR_MAX = 127", "como char:          -61"),
                 "-funsigned-char": ("CHAR_MIN = 0, CHAR_MAX = 255", "como char:          195")}
        for flag, (limits, value) in cases.items():
            with self.subTest(flag=flag):
                target = BUILD / f"char_sign{flag}"
                self.assertEqual(compile_c("char_sign.c", target, flag).returncode, 0)
                result = subprocess.run([str(target)], input="ñ".encode(), capture_output=True).stdout.decode()
                self.assertIn(limits, result)
                self.assertIn(value, result)
                self.assertIn("como unsigned char: 195", result)

    def test_read_bytes(self):
        self.assertEqual(out("read_bytes", "año"), "scanf leyó 4 byte(s)\n61 c3 b1 6f\n")

    def test_utf8_two_bytes_matches_python(self):
        for code in (128, 193, 201, 205, 209, 211, 218, 225, 233, 237, 241, 243, 250, 2047):
            with self.subTest(code=code):
                first, second = chr(code).encode("utf-8")
                self.assertEqual(out("utf8_two_bytes", f"{code}\n"),
                                 f"scanf leyó 1 dato(s)\nbytes: {first:x} {second:x}\n"
                                 f"carácter: {chr(code)}\n")

    def test_utf8_table(self):
        table = {"A": "41", "n": "6e", "ñ": "c3b1", "€": "e282ac", "😀": "f09f9880"}
        for char, encoded in table.items():
            with self.subTest(char=char):
                self.assertEqual(char.encode("utf-8").hex(), encoded)
        self.assertEqual((ord("ñ"), ord("€"), ord("😀")), (0xF1, 0x20AC, 0x1F600))

    def test_xxd(self):
        result = subprocess.run(["xxd"], input="año\n".encode(), capture_output=True, text=False)
        self.assertEqual(result.stdout.decode(), "00000000: 61c3 b16f 0a                             a..o.\n")

    def test_five_characters_seven_bytes(self):
        self.assertEqual((len("ñandú"), len("ñandú".encode())), (5, 7))

    def test_mojibake(self):
        self.assertEqual("ñ".encode().decode("latin-1"), "Ã±")

    def test_enye_constant_warns(self):
        target = BUILD / "char_enye"
        result = compile_c("bad/char_enye.c", target)
        self.assertRegex(result.stderr, re.compile(r"bad/char_enye\.c:5:14: warning: multi-character character constant"))
        self.assertIn("changes value from ‘50097’", result.stderr)


if __name__ == "__main__":
    unittest.main()
