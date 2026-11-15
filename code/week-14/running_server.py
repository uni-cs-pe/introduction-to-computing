"""Ayuda de las pruebas: levanta server.py o spy.py en un puerto libre y lo detiene al salir."""
import contextlib
import pathlib
import socket
import subprocess
import sys

HERE = pathlib.Path(__file__).parent


def free_port():
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        return probe.getsockname()[1]


@contextlib.contextmanager
def tool(*args):
    """Corre una herramienta hasta que anuncia que ya escucha; devuelve el proceso."""
    process = subprocess.Popen(
        [sys.executable, "-u", *args], cwd=HERE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
        text=True,
    )
    try:
        process.banner = process.stdout.readline()
        yield process
    finally:
        process.terminate()
        process.wait(timeout=10)
        process.stdout.close()


@contextlib.contextmanager
def web_server(*options):
    """Levanta server.py; devuelve el puerto."""
    port = free_port()
    with tool("server.py", *options, str(port)):
        yield port
