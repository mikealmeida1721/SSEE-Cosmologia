# Plan de orden — quemar la deuda declarada

> **Por qué existe este documento (2026-09-07).** El guardián estaba en
> VERDE con 18 problemas abiertos y 188 sitios de deuda. Verde por
> construcción: cada defecto encontrado se *declaraba* (un `track_open`,
> un tope de deuda) y el titular seguía en verde. Se podía forzar.
>
> Y el patrón de trabajo lo alimentaba: se corregía **el número**, se
> reportaba el resultado, y la propagación al resto de la documentación
> quedaba a medias. De ahí salen los síntomas: cosas retiradas que siguen
> vigentes en otro documento, rutas que apuntan al vacío, el mismo símbolo
> con dos valores.
>
> Desde hoy el veredicto separa **REGRESIÓN** (¿empeoró algo?) de
> **MODELO** (¿está en orden?). El titular lo manda el segundo.

## Regla de trabajo

Un arreglo no está hecho hasta que:

1. el número está corregido **en su fuente**;
2. **todos** los documentos que lo citan dicen lo mismo;
3. lo retirado está **en `archive/`** con un README que explica por qué;
4. quien lo citaba **apunta a su sitio nuevo**;
5. hay una **regla del guardián con su control**, probada contra el
   commit anterior;
6. y el contador de deuda **baja**, no sube.

Si falta cualquiera de las seis, el trabajo está a medias — que es de
donde vienen los errores que luego encontramos a mano.

## Deuda actual

| # | Frente | Sitios | Qué es |
|---|---|---|---|
| 1 | `particula_md` | 57 | la partícula retirada, presentada como vigente en los `.md` |
| 2 | `R44` | 76 | constantes de la lectura sin 6 decimales |
| 3 | `R42` | 26 | deuda de lectura página-por-página |
| 4 | `R43` | 22 | ídem |
| 5 | `R45` | 7 | OP resuelto citado como abierto |
| — | abiertos | 18 | problemas rastreados (7 derivaciones · 5 tensiones · 2 corridas · 4 higiene) |

## Orden acordado con Mike

```
1º limpieza      <- aqui estamos
2º corridas      (2)
3º tensiones     (5)
4º derivaciones  (7)
```

### 1º Limpieza — en curso

- [x] 5 apuntes que no eran problemas → comprobaciones (`bde6172`)
- [x] figuras: causa raíz de la ranciedad, `R57` (`85caadf`)
- [x] `β_c` al cajón + 20 rutas muertas, `R59` (`85caadf`)
- [x] `β_c = −AURA` retirado de OP-7, `R58` (`dc3eeff`)
- [x] la guarda de la partícula sólo miraba `.tex` (`4548ed7`)
- [ ] **bajar `particula_md` de 57 a 0** ← siguiente
- [ ] 3 valores de pipeline sin log committeado
- [ ] 5 logs con constante retirada
- [ ] 12 logs sin fuente en `PROPAGACION.yaml`

### 2º Corridas

- [x] `fσ₈` contra BOSS crudo — hecho 2026-10-20 con el montaje de Chen+22 y su control (`boss_chen21.json`); el R1/R2 de 2017 quedó retirado
- [ ] control metodológico ΛCDM (R4)
- [ ] regenera `fig_b1_*` (4 figuras, salen del MCMC de Paper 3)

### 3º Tensiones

- [ ] `M⁴` distinto en P7 y P10
- [ ] `M⁴` calibrado a SH0ES, no derivado
- [ ] `c²_s` no se agrupa **[CENTRAL]** — su enunciado está rancio,
      hay que reescribirlo antes de auditarlo
- [ ] MIRA sin mecanismo (4 descartados)
- [ ] el disformal de P8 presupone materia oscura, y P1 la prohíbe
      — **contradicción frontal, la más grave de las cinco**

### 4º Derivaciones

`H₀` dimensional · exponente 7 de `n_s` · k-mouflage de P8 ·
`ω_b` sin BBN · separabilidad UV-IR · `S₈` no lineal · `δ_local = 2`
