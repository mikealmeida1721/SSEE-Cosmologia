#!/usr/bin/env bash
# Lanza UNA configuracion de KiDS-Legacy con 4 cadenas MPI.
#
#   uso:  lanzar_kids_legacy.sh {ssee|sseefijo|lcdmfijo|lcdm} [covmat_semilla]
#
# Reglas de la casa que este script cumple por construccion:
#   1. preflight.py verde en la MISMA linea de comando (&&).
#   2. las tres variables de hilos en 1: sin esto cada proceso MPI toma ~2.3
#      nucleos y la carga se va a 52 sobre 12.
#   4. presupuesto 12 nucleos: 4 procesos = 4 nucleos por configuracion.
#   6. se lanza desde disco con `exec mpirun`, nunca inline: medido el
#      2026-09-07, la version inline murio en silencio dos veces.
set -eu

if [ $# -lt 1 ]; then
  echo "uso: $0 {ssee|sseefijo|lcdmfijo|lcdm} [covmat_semilla]" >&2; exit 2
fi
MODELO="$1"
COVMAT="${2:-}"
case "$MODELO" in ssee|sseefijo|lcdmfijo|lcdm) ;; *) echo "modelo desconocido: $MODELO" >&2; exit 2 ;; esac

ROOT=/home/mike/Proyectos/SSEE
BASE=/mnt/datos/SSEE_data/chains_p6/kids_legacy_v2   # HDD, nunca el SSD; v2 = evaluador corregido (2026-10-26)
LOGDIR=$ROOT/results/logs
mkdir -p "$BASE" "$LOGDIR"

export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export PYTHONPATH=$ROOT/src:${PYTHONPATH:-}
# KIDS_REANUDAR=1 retoma las cadenas desde su checkpoint (sin esto, se borran
# y se empieza de cero). Uso: KIDS_REANUDAR=1 lanzar_kids_legacy.sh ssee
export KIDS_REANUDAR=${KIDS_REANUDAR:-0}

cd "$ROOT"
"$ROOT/.venv/bin/python3" src/verificacion/preflight.py

echo "$(date '+%F %T')  lanzando kids_legacy/$MODELO  (4 cadenas MPI, reanudar=$KIDS_REANUDAR)"
exec mpirun -np 4 "$ROOT/.venv/bin/python3" \
     src/p06_growth/cobaya_kids_legacy.py "$MODELO" "$BASE" $COVMAT
