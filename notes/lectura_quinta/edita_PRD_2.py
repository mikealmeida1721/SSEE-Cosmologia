#!/usr/bin/env python3
"""PRD, quinta lectura, segunda pasada (2026-10-12): la escala absoluta es el H medido, también en el título de §VII.A y las conclusiones."""
import sys

P = "submission_PRD/SSEE_PRD.tex"
s = open(P).read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        sys.exit(f"conteo {c} != {n}: {old[:90]!r}")
    s = s.replace(old, new)


# ---- comunes con PRD (la escala absoluta es el H medido) ----
rep(r"""\subsection{What is measured, not derived: the vacuum scale}""",
    r"""\subsection{What is measured, not derived: the absolute scale}""")
rep(r"""We have been equally explicit about its limits: the vacuum scale is a
measured input""",
    r"""We have been equally explicit about its limits: the absolute scale is a
measured input (the local expansion rate)""")

open(P, "w").write(s)
print("PRD 2 editado")
