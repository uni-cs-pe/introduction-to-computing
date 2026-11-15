"""Comprueba lo que los apuntes afirman de los programas: lo que escriben, lo que
dice gcc y cómo responde la terminal. Las líneas de gcc se buscan también en
notes/week-01.md, así que un cambio en el código o en los apuntes rompe la prueba."""
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
NOTES = HERE.parent.parent / "notes" / "week-01.md"
FLAGS = ["-Wall", "-Wextra", "-std=c17"]
SANITIZE = ["-g", "-fsanitize=address,undefined"]


def compile_as(source, name, cwd, extra=()):
    """Copia el programa con otro nombre, como quien edita hola.c, y lo compila."""
    shutil.copy(HERE / source, Path(cwd) / f"{name}.c")
    return subprocess.run(["gcc", *FLAGS, *extra, f"{name}.c", "-o", name],
                          cwd=cwd, capture_output=True, text=True)


def run(cwd, name):
    return subprocess.run([f"./{name}"], cwd=cwd, capture_output=True, text=True, timeout=5)


def shell(script, cwd):
    return subprocess.run(["bash", "-c", script], cwd=cwd, capture_output=True, text=True)


class ProgramsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.dir = self.tmp.name

    def test_programs_compile_without_warnings(self):
        for source in ("hola", "change_780", "exit_code"):
            result = compile_as(f"{source}.c", source, self.dir, ["-Werror"])
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stderr, "")

    def test_hola(self):
        compile_as("hola.c", "hola", self.dir)
        result = run(self.dir, "hola")
        self.assertEqual(result.stdout, "Hola, mundo\n")
        self.assertEqual(result.returncode, 0)

    def test_change_780_adds_up(self):
        compile_as("change_780.c", "change", self.dir)
        lines = run(self.dir, "change").stdout.splitlines()
        coins = [round(float(line.removeprefix("S/ ")) * 100) for line in lines[1:-1]]
        self.assertEqual(coins, [500, 200, 50, 20, 10])
        self.assertEqual(sum(coins), 780)
        self.assertEqual(lines[-1], "Total: 5 monedas")

    def test_wrong_change_compiles_but_is_wrong(self):
        result = compile_as("errors/wrong_change.c", "wrong", self.dir)
        self.assertEqual((result.returncode, result.stderr), (0, ""))
        lines = run(self.dir, "wrong").stdout.splitlines()
        coins = [round(float(line.removeprefix("S/ ")) * 100) for line in lines[1:-1]]
        self.assertEqual(sum(coins), 880)

    def test_exit_code(self):
        compile_as("exit_code.c", "exit_code", self.dir)
        result = shell("./exit_code > /dev/null; echo $?", self.dir)
        self.assertEqual(result.stdout, "7\n")

    def test_no_newline(self):
        compile_as("errors/no_newline.c", "hola", self.dir)
        self.assertEqual(run(self.dir, "hola").stdout, "Hola, mundo")

    def test_failed_compilation_keeps_old_executable(self):
        compile_as("hola.c", "hola", self.dir)
        result = compile_as("errors/missing_semicolon.c", "hola", self.dir)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(run(self.dir, "hola").stdout, "Hola, mundo\n")

    def test_link_error_removes_old_executable(self):
        compile_as("hola.c", "hola", self.dir)
        result = compile_as("errors/misspelled_main.c", "hola", self.dir)
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((Path(self.dir) / "hola").exists())

    def test_failed_compilation_creates_nothing(self):
        result = compile_as("errors/missing_quote.c", "hola", self.dir)
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((Path(self.dir) / "hola").exists())

    def test_divide_by_zero_warns_and_reports_when_run(self):
        result = compile_as("errors/divide_by_zero.c", "divide_by_zero", self.dir, SANITIZE)
        self.assertEqual(result.returncode, 0)
        self.assertIn("warning: division by zero", result.stderr)
        report = run(self.dir, "divide_by_zero")
        self.assertIn("divide_by_zero.c:6:23: runtime error: division by zero", report.stderr)


class CompilerMessagesTest(unittest.TestCase):
    """Cada línea debe salir de gcc y estar copiada tal cual en los apuntes."""

    CASES = {
        "errors/missing_semicolon.c": ["hola.c:4:28: error: expected ‘;’ before ‘return’"],
        "errors/missing_quote.c": [
            'hola.c:4:12: warning: missing terminating " character',
            'hola.c:4:12: error: missing terminating " character',
            "hola.c:5:5: error: expected expression before ‘return’",
            "hola.c:5:14: error: expected ‘;’ before ‘}’ token",
        ],
        "errors/misspelled_printf.c": [
            "hola.c:4:5: error: implicit declaration of function ‘print’; "
            "did you mean ‘printf’? [-Wimplicit-function-declaration]",
        ],
        "errors/missing_include.c": [
            "hola.c:2:5: error: implicit declaration of function ‘printf’ "
            "[-Wimplicit-function-declaration]",
            "hola.c:1:1: note: include ‘<stdio.h>’ or provide a declaration of ‘printf’",
        ],
        "errors/misspelled_main.c": ["undefined reference to `main'"],
    }

    def test_messages(self):
        # Sin los apuntes (el repositorio de trabajo no los trae) se comprueba solo el compilador.
        notes = NOTES.read_text(encoding="utf-8") if NOTES.exists() else None
        for source, lines in self.CASES.items():
            with self.subTest(source), tempfile.TemporaryDirectory() as tmp:
                result = compile_as(source, "hola", tmp)
                self.assertNotEqual(result.returncode, 0)
                self.assertFalse((Path(tmp) / "hola").exists())
                for line in lines:
                    self.assertIn(line, result.stderr)
                    if notes is not None:
                        self.assertIn(line, notes)


class TerminalTest(unittest.TestCase):
    """Los comandos de la sección de la terminal, en una carpeta temporal."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.dir = Path(self.tmp.name).resolve()

    def test_mkdir_ls_cd_pwd(self):
        result = shell("ls; mkdir lab01; ls; cd lab01; pwd; ls; cd ..; pwd", self.dir)
        self.assertEqual(result.stdout, f"lab01\n{self.dir}/lab01\n{self.dir}\n")

    def test_cd_dot_dot_twice(self):
        (self.dir / "ana" / "lab01").mkdir(parents=True)
        result = shell("cd ana/lab01; cd ../..; pwd", self.dir)
        self.assertEqual(result.stdout, f"{self.dir}\n")

    def test_cd_to_missing_folder(self):
        result = shell("cd labo1", self.dir)
        self.assertIn("cd: labo1: No such file or directory", result.stderr)

    def test_spaces_in_a_folder_name(self):
        (self.dir / "mi").mkdir()
        (self.dir / "carpeta").mkdir()
        result = shell("cd mi carpeta", self.dir)
        self.assertIn("cd: too many arguments", result.stderr)

    def test_commands_distinguish_case(self):
        result = shell("Ls", self.dir)
        self.assertEqual(result.returncode, 127)
        self.assertIn("Ls: command not found", result.stderr)

    def test_executable_needs_dot_slash(self):
        compile_as("hola.c", "hola", self.dir)
        result = shell("hola", self.dir)
        self.assertEqual(result.returncode, 127)
        self.assertIn("hola: command not found", result.stderr)
        self.assertEqual(shell("./hola", self.dir).stdout, "Hola, mundo\n")

    def test_source_file_is_not_executable(self):
        compile_as("hola.c", "hola", self.dir)
        result = shell("./hola.c", self.dir)
        self.assertEqual(result.returncode, 126)
        self.assertIn("./hola.c: Permission denied", result.stderr)

    def test_running_before_compiling(self):
        result = shell("./hola", self.dir)
        self.assertEqual(result.returncode, 127)
        self.assertIn("./hola: No such file or directory", result.stderr)


if __name__ == "__main__":
    unittest.main()
