# R3 de KiDS-1000 con el burn-in sobre las cadenas PEGADAS — archivado 2026-10-03

**Motivo (a): corrida mala, reemplazada.** `R3_ssee_kids_S8.json` (2026-07) cortaba el 30 %
de burn-in sobre las cuatro cadenas concatenadas, no sobre cada una, como declaraba el
método. La reemplaza `results/logs/growth_2026-07/R3_ssee_kids_S8_rehecho.json` (etapa
`R3_rehecho` de `dvc.yaml`, script `src/p06_growth/analiza_ssee_R3.py`), con el burn-in por
cadena; es la que leen los papers por `\val`.

**Por qué sigue siendo entrada.** `analiza_ssee_R3.py` lo lee como control del otro lado
(R53): reproduce el método viejo («pegadas») y muestra cuánto movía el resultado. Por eso
es dependencia declarada de la etapa `R3_rehecho` desde esta carpeta.

**Archivos de esta carpeta** (lista exacta, la que comprueba R77):
- `R3_ssee_kids_S8.json`
