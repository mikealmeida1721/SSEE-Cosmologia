# Referencias históricas — mediciones viejas que una etapa vigente usa como CONTROL

No son resultados del modelo: son el número contra el que una corrida nueva comprueba
que reproduce lo de antes. Se guardan aquí, y no en `results/logs/`, porque ningún script
vigente las produce; cada una dice de dónde salió y quién la lee.

| archivo | de dónde salió | quién la lee y para qué |
|---|---|---|
| `cmb_ajuste_conjunto_wc_ns_01d4369.json` | Ajuste conjunto (w_c, n_s libres) contra Planck crudo, commit 01d4369, entró SIN su script. Su fila ΛCDM corrió con la ecuación de estado de SSEE (bug R64) y no vale. | `src/p03_cmb/ajuste_conjunto_wc_ns.py` (etapas `ajuste_conjunto_SSEE/LCDM`), control (b): la medida rehecha con script debe caer a <0.2σ del perfil de la vieja, sólo en la fila SSEE. |
