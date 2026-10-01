# Corrida hi_class del sector campo

> **2026-09-30 — los números vigentes NO son los de este README.** La corrida se
> rehizo con log y acta: `src/p07_eft/hiclass_campo.py` →
> `results/logs/hiclass_campo.json` (etapa DVC `hiclass_campo`), y Paper 7 los
> imprime con `\val`. Este README queda como registro de la sesión del
> 2026-09-06; el juego «historico» del script reproduce sus σ₈ exactos.

`hi_class` v3.0 (CLASS v3.3.4), repo oficial
miguelzuma/hi_class_public, commit 0009f51
(2026-08-25), en `/mnt/datos/hi_class`.

## Qué se corre

El **campo solo**, no el modelo completo:

    K(X) = c1 X + c2 X^2,  c2 X/c1 = u
    u = (1-w0)/(3w0-1) = -0.52273538

que en lenguaje Bellini-Sawicki es
`propto_omega` con

    x_k = 3(5-3 w0) = 22.559548
    x_b = x_m = x_t = 0

y fondo con el w **del campo**, que es
constante:  w_phi = -0.839949771345.

## Resultado (2026-09-06)

    hi_class c_s^2  = +0.02128370
    algebra SSEE    = +0.02128370
    dif             = 0.000%

    c_s^2 = (M_v - T_r)/(5 M_v + 3 T_r)

constante de z=0 a z=1093. El codigo
ACEPTA el modelo (sin ghost ni
inestabilidad de gradiente).

    alpha_K(z=0) = 15.589549
    prediccion   = 15.591335  (0.011%)

La diferencia es que hi_class calcula
Omega_DE con los neutrinos dentro:
Omega_smg = 0.691040 vs 1-Om_m = 0.691119.

CORRECCION 2026-09-06: la primera version
de este README decia 0.0011%. Era un
factor 10 de menos. El valor correcto es
0.011%, y proviene de correr con omega_b
y omega_c a 6 decimales (0.022418 y
0.119514, antes 0.02242 y 0.11951).

CONTROL DE FONDO: el presupuesto de
hi_class devuelve Omega_m = 0.308882
habiendole dado solo omega_b, omega_c y h
-- nunca Omega_m. Reproduce el 0.308881
algebraico del Paper 1.

## Lo que esta corrida NO prueba

1. NO incluye la viscosidad, que es lo
   que produce w_a. Valida el SECTOR
   CAMPO, no el modelo completo.
2. Si se mete el w EFECTIVO (CPL, con
   w_a=-0.669975), hi_class RECHAZA:
   c_s^2 = -0.0678 en z~4e13. Correcto:
   c_s^2 = (1+w)/(5-3w) cambia de signo
   en el cruce fantasma (z=0.31), y ahi
   el campo ya no es quien lleva el w.
3. NO hay chi^2 de CMB. hi_class no
   admite un fondo viscoso.

## Controles corridos

    x_k=22.56  wa=-0.670  RECHAZA
    x_k=22.56  wa= 0      ACEPTA
    x_k=22.56  lcdm       ACEPTA
    x_k= 0     wa=-0.670  RECHAZA
    x_k= 1     wa=-0.670  RECHAZA (peor)

La inestabilidad la causa w_a, no
alpha_K: con alpha_K pequeno es PEOR.

## Falsabilidad de alpha_K (2026-09-06)

Control corrido con x_k = 1, 22.559548, 100
(fondo w = w_phi constante):

    sigma8   x_k=1     0.769916
             x_k=22.6  0.769929
             x_k=100   0.769973

x100 en alpha_K mueve sigma8 un 0.007%.
**alpha_K NO afecta S8, y S8 no restringe
alpha_K.** El S8=0.7555 canonico queda
intacto.

En TT el efecto existe pero solo en l<10:

    l=2   -9.14%   var.cosmica 63.2%
    l=5   -4.96%               42.6%
    l=10  -1.83%               30.9%
    l>=30 <0.1%

El ruido irreducible es ~7x el efecto.

**Conclusion honesta:** alpha_K = 15.591335
es una prediccion NO FALSABLE con datos
existentes. hi_class la valida solo como
CONSISTENCIA INTERNA (c_s^2, dif 0.000%),
no como contraste con dato.

## Viabilidad de c_s^2 = 0.021284 (2026-09-06)

CLASS, fluido CLP con el fondo SSEE,
aislando SOLO c_s^2:

    sigma8   c_s^2=1.0        0.828445
             c_s^2=0.021284   0.828453
             c_s^2=0.0        0.825006

TT, desviacion vs el caso liso:

    l=2    +3.10%   var.cosmica 63.2%
    l=5    +2.64%               42.6%
    l=10   +0.93%               30.9%
    l>=30  <0.03%

**c_s^2 = 0.021284 NO esta excluido.**
Es indistinguible de energia oscura lisa:
c_s = 0.146 => horizonte sonoro ~600 Mpc,
muy por encima de las escalas medidas.

Igual que alpha_K: consistente, no
excluido, y NO falsable con dato actual.
Lo que SI esta medido es w0 (0.24 sigma
vs DESI DR2), que es lo que el condensado
produce.
