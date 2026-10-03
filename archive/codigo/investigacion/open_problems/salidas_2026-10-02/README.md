# Salidas de scripts archivados (2026-10-02)

Los cajones (OPEN_PROBLEMS) citaban cifras de estos scripts sin que ninguna
corrida hubiera guardado su salida. Se corrieron tal cual, con el núcleo
vigente (`PYTHONPATH=src`), y cada log lleva en su primera línea el acta
(commit, sha del script y del núcleo). Las cifras citadas coinciden:

| script | cifra citada | OPEN_PROBLEMS |
|---|---|---|
| `ssee_op1_baryogenesis.py` | f_dil = 1.095e-18, T_rh,req = 1.031e-4 GeV | OP-1 |
| `op18_As_from_inflation.py` | V₀/M_Pl⁴ = 2.526e-10 | OP-18 |

`ssee_paperB_DW.py` NO se guardó: con el núcleo vigente da sin²(2θ) = 4.958e-5,
no el 4.7846e-5 citado, porque dependía de la m_φ retirada; en OPEN_PROBLEMS
la cifra quedó sin dígitos.
