"""lcdm_planck.py — el LCDM del control (a), con SUS parametros, en un solo sitio.

El control (a) pregunta si una sonda distingue el fondo de SSEE del de LCDM.
Para que la comparacion sea justa, LCDM tiene que evaluarse en SU mejor punto
completo, no en una mezcla: hasta 2026-09-27 ACT, SPT, las supernovas y Union3
corrian LCDM con la masa de neutrinos de SSEE (0.06849 eV), y ACT y SPT ademas
con el A_s y el tau clavados de SSEE. Eso evaluaba a LCDM en un punto que no es
el suyo. (Lo cazo M. Almeida.)

Todos los valores: Planck 2018 VI (arXiv:1807.06209), Tabla 2, columna
TT,TE,EE+lowE+lensing. La masa de neutrinos es la del modelo base de Planck:
un solo autoestado masivo de 0.06 eV (Planck 2018 VI, sec. 2.1), que es lo que
CAMB pone con mnu=0.06 y su num_massive_neutrinos=1 por defecto.
"""
import math

LCDM_PLANCK = dict(
    ombh2=0.02237,   # Planck 2018 VI, Tabla 2
    omch2=0.1200,    # Planck 2018 VI, Tabla 2
    H0=67.36,        # Planck 2018 VI, Tabla 2
    ns=0.9649,       # Planck 2018 VI, Tabla 2
    mnu=0.06,        # Planck 2018 VI, sec. 2.1 (modelo base)
)
LOGA_PLANCK = 3.044  # Planck 2018 VI, Tabla 2, ln(10^10 A_s)
TAU_PLANCK = 0.0544  # Planck 2018 VI, Tabla 2
AS_PLANCK = math.exp(LOGA_PLANCK) * 1e-10
