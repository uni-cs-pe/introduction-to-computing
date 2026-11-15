"""Vuelve a correr los comandos que aparecen en los apuntes y en las diapositivas
y comprueba que el código citado existe de verdad en esta carpeta."""
import pathlib
import re
import subprocess
import unittest

HERE = pathlib.Path(__file__).parent
ROOT = HERE.parent.parent
NOTES = ROOT / "notes" / "week-04.md"
SLIDES = ROOT / "slides" / "week-04.tex"
# Antes de un bloque cuya salida cambia con el procesador. Solo se exigen sus
# líneas con "runtime error".
MACHINE_DEPENDENT = "<!-- depende del procesador -->"


def normalize(text):
    # Según el idioma del entorno, gcc usa comillas tipográficas o rectas.
    return text.replace("‘", "'").replace("’", "'")


def run_shell(command):
    done = subprocess.run(
        ["bash", "-c", command], cwd=HERE, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=60,
    )
    return normalize(done.stdout)


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
    """Devuelve (líneas, depende_del_procesador) de cada bloque de los apuntes."""
    blocks, current, flagged, previous = [], None, False, ""
    for raw in NOTES.read_text(encoding="utf-8").splitlines():
        line = re.sub(r"^> ?", "", raw)
        if current is None:
            if line.strip() == "```" + language:
                current, flagged = [], previous.strip() == MACHINE_DEPENDENT
            elif line.strip():
                previous = line
        elif line.strip() == "```":
            blocks.append((current, flagged))
            current = None
        else:
            current.append(line)
    return blocks


def slide_blocks(environments):
    text = SLIDES.read_text(encoding="utf-8")
    pattern = r"\\begin\{(?:%s)\}[^\n]*\n(.*?)\\end\{(?:%s)\}" % (environments, environments)
    return [match.group(1).splitlines() for match in re.finditer(pattern, text, re.S)]


def known_code_lines():
    lines = set()
    for source in list(HERE.glob("*.c")) + list((HERE / "errors").glob("*.c")):
        lines.update(line.strip() for line in source.read_text(encoding="utf-8").splitlines())
    return lines


class NotesAreTrue(unittest.TestCase):
    @unittest.skipUnless(NOTES.exists(), "faltan los apuntes")
    def test_terminal_blocks_in_notes(self):
        checked = 0
        for lines, flagged in note_blocks("text"):
            if not lines or not lines[0].startswith("$ "):
                continue
            for command, expected in split_commands(lines):
                actual = run_shell(command).rstrip("\n")
                checked += 1
                with self.subTest(command=command):
                    if flagged:
                        wanted = [line for line in expected if "runtime error" in line]
                        for line in wanted:
                            self.assertIn(line, actual)
                    else:
                        self.assertEqual(actual, "\n".join(expected))
        self.assertGreater(checked, 10)

    @unittest.skipUnless(NOTES.exists(), "faltan los apuntes")
    def test_code_blocks_in_notes_exist(self):
        known = known_code_lines()
        for lines, _ in note_blocks("c"):
            for line in lines:
                if line.strip() and line.strip() != "...":
                    with self.subTest(line=line):
                        self.assertIn(line.strip(), known)


class SlidesAreTrue(unittest.TestCase):
    @unittest.skipUnless(SLIDES.exists(), "faltan las diapositivas")
    def test_terminal_blocks_in_slides(self):
        for block in slide_blocks("terminal|salidalarga"):
            for command, expected in split_commands(block):
                actual = run_shell(command).splitlines()
                position = 0
                # Una diapositiva puede omitir líneas, pero no cambiarlas ni reordenarlas.
                for line in expected:
                    line = line.strip()
                    if not line:
                        continue
                    with self.subTest(command=command, line=line):
                        found = [i for i in range(position, len(actual)) if actual[i].strip() == line]
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
