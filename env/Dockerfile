# Entorno del curso de Introducción a la Computación: C, Git, Python y las
# herramientas de los laboratorios. La misma imagen sirve para GitHub Codespaces
# (.devcontainer/) y para Docker en una laptop, en amd64 y arm64.
FROM python:3.14-slim-trixie

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential gdb valgrind make git ca-certificates curl vim nano less tree file man-db procps xxd dnsutils traceroute \
    && rm -rf /var/lib/apt/lists/*

# Los repositorios montados pertenecen a otro usuario; sin esto, git (que corre
# como root) los rechaza por "dubious ownership".
RUN git config --system --add safe.directory '*'

CMD ["bash"]
