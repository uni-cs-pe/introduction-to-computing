"""Servidor web de la semana 14. Atiende solo a esta computadora (127.0.0.1).

    python3 server.py           HTTP en el puerto 8014
    python3 server.py 9000      HTTP en otro puerto
    python3 server.py --tls     HTTPS en el puerto 8443; antes hay que correr make cert

Se detiene con Ctrl+C. No hace falta entender todo este archivo: es la herramienta del
laboratorio. Lo que importa es lo que responde.
"""
import http.server
import ssl
import sys

PAGES = {
    "/": ("text/html; charset=utf-8",
          "<!DOCTYPE html>\n<html>\n<body>\n<h1>Hola desde el servidor</h1>\n</body>\n</html>\n"),
    "/saludo": ("text/plain; charset=utf-8", "Buenos días, Perú\n"),
}
NOT_FOUND = "No existe esa página\n"
SERVER_ERROR = "Algo falló dentro del servidor\n"


class Handler(http.server.BaseHTTPRequestHandler):
    # Sin esta línea, la biblioteca responde con HTTP/1.0.
    protocol_version = "HTTP/1.1"

    def version_string(self):
        return "ServidorDelCurso/1.0"

    def do_GET(self):
        path = self.path.split("?")[0]
        if path in PAGES:
            content_type, text = PAGES[path]
            self.respond(200, content_type, text)
        elif path == "/error":
            # Un 500 a propósito, para verlo con curl.
            self.respond(500, "text/plain; charset=utf-8", SERVER_ERROR)
        else:
            self.respond(404, "text/plain; charset=utf-8", NOT_FOUND)

    def respond(self, code, content_type, text):
        body = text.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        # Se cuentan bytes, no letras.
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def main():
    args = sys.argv[1:]
    use_tls = "--tls" in args
    numbers = [arg for arg in args if arg != "--tls"]
    port = int(numbers[0]) if numbers else (8443 if use_tls else 8014)
    try:
        server = http.server.ThreadingHTTPServer(("127.0.0.1", port), Handler)
    except OSError as error:
        print(f"No se pudo abrir el puerto {port}: {error}")
        return 1
    scheme = "http"
    if use_tls:
        scheme = "https"
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain("build/cert.pem", "build/key.pem")
        server.socket = context.wrap_socket(server.socket, server_side=True)
    host = "localhost" if use_tls else "127.0.0.1"
    print(f"Servidor en {scheme}://{host}:{port}/ (Ctrl+C para detener)", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor detenido")
    return 0


if __name__ == "__main__":
    sys.exit(main())
