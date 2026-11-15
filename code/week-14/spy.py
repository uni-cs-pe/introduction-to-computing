"""Un espía de la semana 14: se pone en medio de una conexión e imprime lo que pasa por ahí.

    python3 spy.py 8015 8014    escucha en 8015 y reenvía todo al puerto 8014

Hace en pequeño lo que puede hacer cualquier equipo por donde pasan sus paquetes. Solo sirve
para esta computadora. Lo que no se puede imprimir se muestra como un punto. Se detiene con Ctrl+C.
"""
import socket
import sys
import threading


def printable(data):
    return "".join(chr(b) if 32 <= b < 127 or b == 10 else "." for b in data)


def pump(source, target, label):
    """Copia bytes de una punta a la otra y los muestra."""
    while True:
        data = source.recv(4096)
        if not data:
            break
        print(f"--- {label}, {len(data)} bytes\n{printable(data)}", flush=True)
        target.sendall(data)
    target.shutdown(socket.SHUT_WR)


def attend(client, target_port):
    with client, socket.create_connection(("127.0.0.1", target_port)) as server:
        answer = threading.Thread(target=pump, args=(server, client, "servidor a cliente"))
        answer.start()
        pump(client, server, "cliente a servidor")
        answer.join()


def main():
    listen_port, target_port = int(sys.argv[1]), int(sys.argv[2])
    with socket.create_server(("127.0.0.1", listen_port)) as listener:
        print(f"Espía en el puerto {listen_port}, reenvía al {target_port}", flush=True)
        try:
            while True:
                client, _ = listener.accept()
                attend(client, target_port)
        except KeyboardInterrupt:
            print("\nEspía detenido")


if __name__ == "__main__":
    main()
