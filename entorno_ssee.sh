#!/bin/bash
# entorno_ssee.sh — corre SSEE en CUALQUIER Linux sin tocar el código ni las rutas.
#
# Los scripts, dvc.yaml y las actas de procedencia nombran las rutas con que se
# corrieron (/mnt/datos/SSEE_data, /home/mike/Proyectos/SSEE, /home/mike/cobaya_packages).
# En vez de reescribirlos —lo que obligaría a re-correr toda la cadena— este script abre
# un entorno aislado (bubblewrap, sin permisos de administrador) donde TUS carpetas
# aparecen en esas rutas. Dentro, el código es byte a byte el que produjo cada resultado.
#
# Uso:
#   export SSEE_DATOS=/ruta/a/tus/datos            # lo que baja src/verificacion/baja_externos.py
#   export COBAYA_PACKAGES_PATH=/ruta/a/cobaya      # lo que instala `cobaya-install`
#   export SSEE_HICLASS=/ruta/a/hi_class            # hi_class compilado (lo hace baja_externos.py)
#   ./entorno_ssee.sh                               # abre una terminal dentro
#   ./entorno_ssee.sh .venv/bin/dvc status          # o corre un comando
# Requiere: bwrap (paquete «bubblewrap» en Debian/Ubuntu/Fedora/Arch).
set -euo pipefail
REPO="$(cd "$(dirname "$0")" && pwd)"
: "${SSEE_DATOS:?define SSEE_DATOS (carpeta de datos externos)}"
: "${COBAYA_PACKAGES_PATH:?define COBAYA_PACKAGES_PATH (paquetes de cobaya)}"
: "${SSEE_HICLASS:?define SSEE_HICLASS (hi_class compilado)}"
command -v bwrap >/dev/null || { echo "falta bwrap (paquete bubblewrap)"; exit 1; }
exec bwrap --dev-bind / / \
  --tmpfs /mnt --bind "$SSEE_DATOS" /mnt/datos/SSEE_data \
  --bind "$SSEE_HICLASS" /mnt/datos/hi_class \
  --tmpfs /home --bind "$HOME" "$HOME" \
  --bind "$REPO" /home/mike/Proyectos/SSEE \
  --bind "$COBAYA_PACKAGES_PATH" /home/mike/cobaya_packages \
  --setenv COBAYA_PACKAGES_PATH /home/mike/cobaya_packages \
  --chdir /home/mike/Proyectos/SSEE \
  "${@:-bash}"
