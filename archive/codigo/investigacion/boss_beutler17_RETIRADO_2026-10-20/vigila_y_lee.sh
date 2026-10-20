#!/bin/bash
# vigila_y_lee.sh — espera a que la conjunta termine y LA LEE sola.
#
# POR QUE EXISTE. Los monitores viven dentro de la sesion de Claude y mueren
# con ella. Este corre fuera: se desacopla con setsid/nohup, asi que sobrevive
# al cierre de la sesion, de la terminal y del login. Cuando la conjunta muere
# --sea por convergencia o por lo que sea-- corre el lector y deja el resultado
# escrito en disco. El resultado se produce aunque no haya nadie delante.
D=/mnt/datos/SSEE_data/chains_p6/conjunta
R=/home/mike/Proyectos/SSEE
BIT=$R/results/logs/vigilante_conjunta.log

echo "[$(date '+%F %T')] vigilante en marcha, PID $$" >> $BIT
while pgrep -f "cobaya_conjunta.py conjunta" > /dev/null; do
  n=$(cat $D/conjunta.[0-9]*.txt 2>/dev/null | grep -vc '^#')
  z=$(for f in $D/conjunta.[0-9]*.txt; do echo $(($(wc -l<$f)-1)); done | sort -n | head -1)
  echo "[$(date '+%F %T')] viva — $n filas, rezagada $z/1000" >> $BIT
  sleep 900
done

echo "[$(date '+%F %T')] la conjunta ya no corre. Leyendo..." >> $BIT
cd $R
OMP_NUM_THREADS=1 .venv/bin/python3 src/p06_growth/leer_conjunta.py >> $BIT 2>&1
echo "[$(date '+%F %T')] LEIDA. Resultado en results/logs/conjunta_vs_individual.json" >> $BIT
