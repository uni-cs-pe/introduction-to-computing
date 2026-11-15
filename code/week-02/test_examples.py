"""Pruebas de los ejemplos de los apuntes. Corren cada programa en una terminal de
verdad, comparan su salida y comprueban que los apuntes y las diapositivas muestran
exactamente lo que salió. Si cambia el código o la versión de gcc, estas pruebas lo
avisan."""
import os
import pty
import re
import select
import subprocess
import time
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
COURSE = HERE.parent.parent
NOTES = COURSE / "notes" / "week-02.md"
SLIDES = COURSE / "slides" / "week-02.tex"

GCC = "gcc -Wall -Wextra -std=c17"


def clean(text):
    """Quita colores y lo que cambia entre máquinas: nombres temporales y desplazamientos."""
    text = re.sub(r"\x1b\[[0-9;]*m", "", text)      # colores de la terminal
    text = re.sub(r"/tmp/cc\w+\.o", "/tmp/cc.o", text)
    return re.sub(r"\.text\+0x[0-9a-f]+", ".text", text)


def run_in_terminal(command, dialog=(), eof=False):
    """Ejecuta un comando en una terminal: `dialog` son pares (mensaje, respuesta),
    y lo escrito aparece en la salida, igual que cuando lo escriben ustedes."""
    master, slave = pty.openpty()
    env = dict(os.environ, TERM="dumb", LANG="C.UTF-8")
    process = subprocess.Popen(["sh", "-c", command], stdin=slave, stdout=slave,
                               stderr=slave, cwd=HERE, env=env)
    os.close(slave)
    output = b""

    def read_until(done):
        nonlocal output
        limit = time.time() + 30
        while not done():
            if time.time() > limit:
                raise TimeoutError(output.decode())
            ready, _, _ = select.select([master], [], [], 0.05)
            if ready:
                try:
                    data = os.read(master, 4096)
                except OSError:     # el programa ya terminó
                    return
                if not data:
                    return
                output += data

    for prompt, answer in dialog:
        read_until(lambda: output.endswith(prompt.encode()))
        os.write(master, answer.encode() + b"\n")
    if eof:
        read_until(lambda: output != b"")
        os.write(master, b"\x04")
    read_until(lambda: False)
    process.wait()
    os.close(master)
    text = output.decode().replace("\r\n", "\n")
    return clean(f"$ {command}\n{text}")


# nombre: (comando, diálogo, fin de entrada, lo que debe salir)
GRADES = [("Examen parcial: ", "13"), ("Examen final: ", "15"),
          ("Promedio de prácticas: ", "14")]
TWO = "Dos enteros: "
SESSIONS = {
    "balance": ("build/balance", (), False, "Después de la recarga: 12\n"),
    "not_a_formula": ("build/not_a_formula", (), False, "total = 6\n"),
    "swap_values": ("build/swap_values", (), False, "left = 9, right = 4\n"),
    "sizes": ("build/sizes", (), False,
              "int: 4 bytes\ndouble: 8 bytes\nchar: 1 bytes\n"),
    "arithmetic": ("build/arithmetic", (), False, "7 + 8 % 3 * 2 = 11\n"),
    "division": ("build/division", (), False, "-17 % 5 = -2\n17 % -5 = 2\n"),
    "conversions": ("build/conversions", (), False, "(int) -3.99 = -3\n"),
    "char_codes": ("build/char_codes", (), False, "A tiene el código 65\n"),
    "printf_formats": ("build/printf_formats", (), False,
                       "2.675 con dos decimales: 2.67\n"),
    "read_grade": ("build/read_grade", [("Nota: ", "15")], False, "sería 17\n"),
    "check_ok": ("build/read_check", [(TWO, "4 9")],
                 False, "scanf devolvió 2\n"),
    "check_second": ("build/read_check", [(TWO, "4 hola")], False,
                     "scanf devolvió 1\nfirst = 4, second = 0\n"),
    "check_first": ("build/read_check", [(TWO, "hola")], False,
                    "scanf devolvió 0\nfirst = 0, second = 0\n"),
    "check_decimal": ("build/read_check", [(TWO, "3.7 5")], False,
                      "scanf devolvió 1\nfirst = 3, second = 0\n"),
    "check_eof": ("build/read_check", [], True, "scanf devolvió -1\n"),
    "leftover": ("build/leftover", [("Un entero: ", "hola")], False,
                 "Lo siguiente en la entrada es h\n"),
    "char_trap": ("build/char_trap", [("Cantidad: ", "3")], False,
                  "Leí 3 y un carácter de código 10\n"),
    "char_fixed": ("build/char_fixed", [("Cantidad: ", "3"), ("Talla: ", "M")], False,
                   "Leí 3 y la talla M\n"),
    "final_grade": ("build/final_grade", GRADES, False, "Promedio final: 14.25\n"),
    "final_grade_bug": ("build/final_grade_bug", GRADES, False,
                        "Promedio final: 14.00\n"),
    "igv_hola": ("build/igv_price", [("Precio sin IGV: ", "hola")], False,
                 "IGV: 0.00\nTotal: 0.00\n"),
    "igv_price": ("build/igv_price", [("Precio sin IGV: ", "50")], False,
                  "IGV: 9.00\nTotal: 59.00\n"),
    "change_780": ("build/change", [("Vuelto en céntimos: ", "780")], False,
                   "Sin cubrir: 0 céntimos\n"),
    "change_785": ("build/change", [("Vuelto en céntimos: ", "785")], False,
                   "Sin cubrir: 5 céntimos\n"),
    "math_demo": ("build/math_demo", [("x: ", "2.5")], False,
                  "sqrt(x)   = 1.581139\npow(x, 3) = 15.625000\nfabs(x)   = 2.500000\n"
                  "floor(x)  = 2.000000\nceil(x)   = 3.000000\nround(x)  = 3.000000\n"),
    "diagonal": ("build/diagonal", [("Ancho y alto en metros: ", "3 4")], False,
                 "Diagonal: 5.00 metros\n"),
    "compound_interest": ("build/compound_interest",
                          [("Capital en soles: ", "1000"), ("Tasa anual en %: ", "5"),
                           ("Años: ", "3")], False, "Monto final: 1157.63 soles\n"),
    "double_by_zero": ("build/double_by_zero", [("Dos números: ", "5 0")], False,
                       "Cociente: inf\n"),
    "redirect_in": ("build/final_grade < grades.txt", (), False,
                    "Promedio final: 14.25\n"),
    "redirect_out": ("build/final_grade < grades.txt > build/result.txt", (), False, ""),
    "redirect_cat": ("cat build/result.txt", (), False, "Promedio final: 14.25\n"),
    "uninitialized": (f"{GCC} broken/uninitialized.c -o build/uninitialized", (), False,
                      "is used uninitialized"),
    "missing_ampersand": (f"{GCC} broken/missing_ampersand.c -o build/missing_ampersand",
                          (), False, "expects argument of type ‘int *’"),
    "scanf_float": (f"{GCC} broken/scanf_float_format.c -o build/scanf_float_format",
                    (), False, "%lf\n"),
    "printf_wrong": (f"{GCC} broken/printf_wrong_format.c -o build/printf_wrong_format",
                     (), False, "%f\n"),
    "mod_double": (f"{GCC} broken/mod_double.c -o build/mod_double", (), False,
                   "invalid operands to binary %"),
    "missing_lm": (f"{GCC} diagonal.c -o build/diagonal_no_lm", (), False,
                   "undefined reference to `sqrt'"),
}


# Los apuntes dan estos resultados en una frase o una tabla, sin la sesión completa.
ONLY_IN_PROSE = {"check_ok", "check_first", "check_decimal", "change_785", "char_fixed",
                 "mod_double", "double_by_zero", "printf_wrong", "math_demo",
                 "compound_interest"}


def first_part(transcript, marker):
    """Lo que viene después de `marker` depende del procesador: no se compara."""
    end = transcript.index(marker)
    return transcript[:transcript.index("\n", end) + 1]


def session_transcripts():
    """Corre todas las sesiones una vez, y las reutilizan las demás pruebas."""
    subprocess.run(["mkdir", "-p", "build"], cwd=HERE, check=True)
    result = {}
    for name in ("redirect_in", "redirect_out", "redirect_cat"):
        command, dialog, eof, _ = SESSIONS[name]
        result[name] = run_in_terminal(command, dialog, eof)
    for name, (command, dialog, eof, _) in SESSIONS.items():
        if name not in result:
            result[name] = run_in_terminal(command, dialog, eof)
    # Por procesador cambian el resto de la salida y el segundo aviso de gcc.
    result["division_by_zero"] = first_part(
        run_in_terminal("build/division_by_zero", [(TWO, "5 0")]), "runtime error")
    accent = run_in_terminal(f"{GCC} broken/accent_char.c -o build/accent_char")
    result["accent_char"] = accent[:accent.index("broken/accent_char.c:5:19: warning: ",
                                                 accent.index("^~~"))]
    return result


TRANSCRIPTS = session_transcripts()


class Sessions(unittest.TestCase):
    def test_each_program_prints_what_the_notes_say(self):
        for name, (_, _, _, expected) in SESSIONS.items():
            with self.subTest(name):
                self.assertIn(expected, TRANSCRIPTS[name])

    def test_integer_division_by_zero_is_reported(self):
        self.assertIn("division_by_zero.c:12:22: runtime error: division by zero\n",
                      TRANSCRIPTS["division_by_zero"])

    def test_accent_char_warns_about_multichar(self):
        self.assertIn("multi-character character constant", TRANSCRIPTS["accent_char"])


class Compilation(unittest.TestCase):
    def compile(self, source, flags=("-Wall", "-Wextra")):
        return subprocess.run(["gcc", *flags, "-std=c17", "-c", str(source),
                               "-o", "/dev/null"], capture_output=True, text=True, cwd=HERE)

    def test_programs_have_no_warnings(self):
        sources = [*HERE.glob("*.c"), *HERE.glob("lab/*.c"), *HERE.glob("solution/*.c")]
        self.assertTrue(sources)
        for source in sources:
            with self.subTest(source.name):
                self.assertEqual(self.compile(source).stderr, "")

    def test_broken_programs_do_warn(self):
        for source in HERE.glob("broken/*.c"):
            with self.subTest(source.name):
                self.assertRegex(self.compile(source).stderr, "warning:|error:")

    def test_without_wall_gcc_says_nothing_about_uninitialized(self):
        self.assertEqual(self.compile("broken/uninitialized.c", ()).stderr, "")

    def test_sanitizers_do_not_detect_uninitialized(self):
        subprocess.run(f"{GCC} -w -fsanitize=address,undefined broken/uninitialized.c "
                       "-o build/uninitialized_san", shell=True, cwd=HERE, check=True)
        result = subprocess.run(["build/uninitialized_san"], cwd=HERE, capture_output=True)
        self.assertEqual(result.stderr, b"")

    def test_m_pi_is_not_available_with_c17(self):
        self.assertIn("M_PI", self.compile("broken/uses_m_pi.c").stderr)

    def test_assignment_to_const_and_expression_do_not_compile(self):
        source = HERE / "build" / "const_check.c"
        for body in ("const double RATE = 0.18; RATE = 0.2; return (int) RATE;",
                     "int b = 1; b - 3 = b; return b;",
                     "int b = 1; int b = 7; return b;"):
            with self.subTest(body):
                source.write_text(f"int main(void) {{ {body} }}\n", encoding="utf-8")
                self.assertIn("error:", self.compile(source).stderr)


class Crash(unittest.TestCase):
    def test_missing_ampersand_crashes_at_run_time(self):
        subprocess.run(f"{GCC} -w broken/missing_ampersand.c -o build/missing_ampersand",
                       shell=True, cwd=HERE, check=True)
        result = subprocess.run(["build/missing_ampersand"], input=b"15\n", cwd=HERE,
                                capture_output=True)
        self.assertNotEqual(result.returncode, 0)


@unittest.skipUnless(NOTES.exists(), "no están los apuntes")
class Notes(unittest.TestCase):
    def setUp(self):
        self.notes = clean(NOTES.read_text(encoding="utf-8"))

    def test_notes_show_real_output(self):
        for name, transcript in TRANSCRIPTS.items():
            if name in ONLY_IN_PROSE:
                continue
            with self.subTest(name):
                self.assertIn(transcript, self.notes)

    def test_terminal_blocks_only_show_real_output(self):
        for block in re.findall(r"```console\n(.*?)```", self.notes, re.S):
            real = [t for t in TRANSCRIPTS.values() if t in block]
            rest = block
            for transcript in sorted(real, key=len, reverse=True):
                rest = rest.replace(transcript, "")
            with self.subTest(block[:50]):
                self.assertEqual(rest.strip(), "")

    def test_programs_in_notes_are_the_real_files(self):
        files = {p.read_text(encoding="utf-8") for p in
                 [*HERE.glob("*.c"), *HERE.glob("broken/*.c")]}
        blocks = re.findall(r"^```c\n(.*?)```", self.notes, re.S | re.M)
        complete = [b for b in blocks if "int main" in b]
        self.assertTrue(complete)
        for block in complete:
            with self.subTest(block[:50]):
                self.assertIn(block, files)


@unittest.skipUnless(SLIDES.exists(), "no están las diapositivas")
class Slides(unittest.TestCase):
    def test_terminal_lines_are_real(self):
        tex = SLIDES.read_text(encoding="utf-8")
        real = {line for t in TRANSCRIPTS.values() for line in t.split("\n")}
        for env in ("terminal", "terminalancha"):
            for block in re.findall(rf"\\begin\{{{env}\}}(?:\[.*?\])?\n(.*?)\\end\{{{env}\}}",
                                    tex, re.S):
                for line in clean(block).strip("\n").split("\n"):
                    with self.subTest(line):
                        self.assertIn(line, real)


if __name__ == "__main__":
    unittest.main()
