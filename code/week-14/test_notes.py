"""Vuelve a correr los comandos que aparecen en los apuntes y en las diapositivas
y comprueba que el código citado existe de verdad en esta carpeta."""
import pathlib
import re
import subprocess
import unittest

from running_server import HERE, web_server

ROOT = HERE.parent.parent
NOTES = ROOT / "notes" / "week-14.md"
SLIDES = ROOT / "slides" / "week-14.tex"
# Antes de un bloque con fechas, direcciones o rutas. Se corre, pero solo se exigen las líneas estables.
MACHINE_DEPENDENT = "<!-- depende de la corrida -->"
# Antes de un bloque que no se puede repetir aquí: necesita internet, otra terminal o da tiempos.
# Lo que afirman esos bloques se comprueba en test_examples.py y test_lab.py.
NOT_RUN = "<!-- se muestra, no se corre -->"
STABLE = ["AddressSanitizer: stack-buffer-overflow", "index 7 out of bounds", "IndexError:",
          "TypeError:", "signed integer overflow", "BINARY_OP", "positivo", "localhost"]
PORT = "8014"


def normalize(text):
    text = text.replace("‘", "'").replace("’", "'")
    text = re.sub(r"^((?:< )?[Dd]ate:) .*$", r"\1", text, flags=re.M)
    return re.sub(r"0x[0-9a-f]+", "0x", text)


def run_shell(command, port):
    done = subprocess.run(
        ["bash", "-c", command.replace(PORT, str(port))], cwd=HERE, encoding="utf-8",
        errors="replace", stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=120,
    )
    return normalize(done.stdout.replace(str(port), PORT))


def split_commands(lines):
    """Parte un bloque de terminal en pares (comando, líneas de salida)."""
    pairs = []
    for line in lines:
        if line.startswith("$ "):
            pairs.append((line[2:], []))
        elif pairs:
            pairs[-1][1].append(normalize(line.rstrip()))
    return pairs


def note_blocks(language):
    """Devuelve (líneas, marca) de cada bloque de los apuntes."""
    blocks, current, mark, previous = [], None, "", ""
    for raw in NOTES.read_text(encoding="utf-8").splitlines():
        line = re.sub(r"^> ?", "", raw)
        if current is None:
            if line.strip() == "```" + language:
                current, mark = [], previous.strip()
            elif line.strip():
                previous = line
        elif line.strip() == "```":
            blocks.append((current, mark))
            current = None
            previous = ""
        else:
            current.append(line)
    return blocks


def slide_blocks(environments):
    text = SLIDES.read_text(encoding="utf-8")
    pattern = r"\\begin\{(?:%s)\}[^\n]*\n(.*?)\\end\{(?:%s)\}" % (environments, environments)
    return [match.group(1).splitlines() for match in re.finditer(pattern, text, re.S)]


def known_code_lines():
    lines = set()
    sources = []
    for pattern in ["*.c", "*.py"]:
        sources += list(HERE.glob(pattern)) + list((HERE / "errors").glob(pattern))
    for source in sources:
        lines.update(line.strip() for line in source.read_text(encoding="utf-8").splitlines())
    return lines


class NotesAreTrue(unittest.TestCase):
    @unittest.skipUnless(NOTES.exists(), "faltan los apuntes")
    def test_terminal_blocks_in_notes(self):
        checked = 0
        with web_server() as port:
            for lines, mark in note_blocks("text"):
                if not lines or not lines[0].startswith("$ ") or mark == NOT_RUN:
                    continue
                for command, expected in split_commands(lines):
                    actual = run_shell(command, port).rstrip("\n")
                    checked += 1
                    with self.subTest(command=command):
                        if mark == MACHINE_DEPENDENT:
                            self.check_stable(expected, actual)
                        else:
                            lines_got = [line.rstrip() for line in actual.split("\n")]
                            self.assertEqual("\n".join(lines_got), "\n".join(expected))
        self.assertGreater(checked, 12)

    def check_stable(self, expected, actual):
        for line in expected:
            is_http = re.match(r"[<>] \S", line) and not re.match(r"[<>] (User-Agent|Date)", line)
            if is_http:
                self.assertIn(line, [got.rstrip() for got in actual.split("\n")])
            for token in STABLE:
                if token in line:
                    self.assertIn(token, actual)

    @unittest.skipUnless(NOTES.exists(), "faltan los apuntes")
    def test_code_blocks_in_notes_exist(self):
        known = known_code_lines()
        for language in ["c", "python"]:
            for lines, _ in note_blocks(language):
                for line in lines:
                    if line.strip() and line.strip() != "...":
                        with self.subTest(line=line):
                            self.assertIn(line.strip(), known)

    @unittest.skipUnless(NOTES.exists(), "faltan los apuntes")
    def test_notes_flag_what_depends_on_the_machine_or_the_network(self):
        text = " ".join(NOTES.read_text(encoding="utf-8").split())
        for phrase in ["dependen de la máquina", "depende de la red", "2 de noviembre de 2026",
                       "en esta corrida", "sin sanitizers"]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text.replace("**", ""))


class SlidesAreTrue(unittest.TestCase):
    @unittest.skipUnless(SLIDES.exists(), "faltan las diapositivas")
    def test_terminal_blocks_in_slides(self):
        with web_server() as port:
            for block in slide_blocks("terminal|terminalchica"):
                for command, expected in split_commands(block):
                    actual = run_shell(command, port).splitlines()
                    position = 0
                    # Una diapositiva puede omitir líneas, pero no cambiarlas ni reordenarlas.
                    for line in expected:
                        line = line.strip()
                        if not line:
                            continue
                        with self.subTest(command=command, line=line):
                            found = [i for i in range(position, len(actual))
                                     if actual[i].strip() == line]
                            self.assertTrue(found, f"no aparece en la salida real: {line}")
                            if found:
                                position = found[0] + 1

    @unittest.skipUnless(SLIDES.exists(), "faltan las diapositivas")
    def test_code_blocks_in_slides_exist(self):
        known = known_code_lines()
        for block in slide_blocks("codigo|codigochico|codigomini"):
            for line in block:
                if line.strip() and line.strip() != "...":
                    with self.subTest(line=line):
                        self.assertIn(line.strip(), known)


if __name__ == "__main__":
    unittest.main()
