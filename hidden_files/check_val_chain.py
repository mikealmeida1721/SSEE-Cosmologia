#!/usr/bin/env python3
"""Verifica la cadena completa: valores.yaml -> log#clave -> valores_generados.tex
y la completitud de _procedencia de cada log citado.
Salida: JSON con hallazgos por nombre."""
import json, re, sys, os, hashlib

BASE = os.path.expanduser("~/workspace/SSEE")
os.chdir(BASE)

def get_key(d, path):
    cur = d
    for p in path.split("."):
        if isinstance(cur, dict) and p in cur:
            cur = cur[p]
        elif isinstance(cur, list) and p.lstrip("-").isdigit() and -len(cur) <= int(p) < len(cur):
            cur = cur[int(p)]
        else:
            return None, f"clave '{path}' no existe (falla en '{p}')"
    return cur, None

def parse_yaml_fuentes(path):
    """Lee valores.yaml con PyYAML real. Devuelve nombre -> {fuente, formato}."""
    import yaml
    raw = yaml.safe_load(open(path, encoding="utf-8"))
    out = {}
    for name, info in raw.items():
        if isinstance(info, dict):
            out[name] = {"fuente": info.get("fuente", ""), "formato": info.get("formato", "")}
        else:
            out[name] = {"fuente": "", "formato": ""}
    return out

def parse_tex_vals(path):
    out = {}
    for line in open(path, encoding="utf-8"):
        m = re.match(r'\\expandafter\\def\\csname ssee@val@([A-Za-z0-9_]+)\\endcsname\{([^}]*)\}\s*%\s*(.*)$', line)
        if m:
            out[m.group(1)] = (m.group(2), m.group(3).strip())
    return out

def fmt_check(value, formato, tex_val):
    # replica exacta de src/valores_tex.py: format(v, formato) si no es str
    try:
        esperado = value if isinstance(value, str) else format(value, formato)
    except Exception:
        try:
            esperado = format(float(value), formato)
        except Exception as e:
            return False, f"no formateable: {e}"
    if esperado == tex_val:
        return True, ""
    return False, f"tex='{tex_val}' vs log formateado='{esperado}' (crudo={value!r})"

def main():
    yaml = parse_yaml_fuentes("manuscript/valores.yaml")
    tex = parse_tex_vals("manuscript/valores_generados.tex")
    log_cache = {}
    hallazgos = []
    ok_count = 0
    proced_log_ok = {}
    for name, info in yaml.items():
        fuente = info.get("fuente", "")
        formato = info.get("formato", "")
        if "#" not in fuente:
            hallazgos.append({"nombre": name, "severidad": "ADVERTENCIA",
                              "causa": "fuente sin separador #log#clave", "evidencia": fuente})
            continue
        logpath, key = fuente.split("#", 1)
        # 1. existe en tex
        if name not in tex:
            hallazgos.append({"nombre": name, "severidad": "CRITICO",
                              "causa": "definido en valores.yaml pero AUSENTE en valores_generados.tex",
                              "evidencia": fuente})
            continue
        tex_val, tex_src = tex[name]
        if tex_src != fuente:
            hallazgos.append({"nombre": name, "severidad": "ADVERTENCIA",
                              "causa": "comentario de procedencia en .tex difiere del yaml",
                              "evidencia": f"tex: {tex_src} | yaml: {fuente}"})
        # 2. log existe y clave existe
        if logpath not in log_cache:
            try:
                log_cache[logpath] = json.load(open(logpath, encoding="utf-8"))
            except FileNotFoundError:
                log_cache[logpath] = None
            except Exception as e:
                log_cache[logpath] = ("ERROR", str(e))
        logd = log_cache[logpath]
        if logd is None:
            hallazgos.append({"nombre": name, "severidad": "CRITICO",
                              "causa": "log citado NO EXISTE", "evidencia": logpath})
            continue
        if isinstance(logd, tuple):
            hallazgos.append({"nombre": name, "severidad": "CRITICO",
                              "causa": "log ilegible", "evidencia": f"{logpath}: {logd[1]}"})
            continue
        v, err = get_key(logd, key)
        if err:
            hallazgos.append({"nombre": name, "severidad": "CRITICO",
                              "causa": "clave no existe en el log", "evidencia": f"{logpath}#{key}"})
            continue
        # 3. valor coincide
        okf, msg = fmt_check(v, formato, tex_val)
        if not okf:
            hallazgos.append({"nombre": name, "severidad": "CRITICO",
                              "causa": "valor del log NO coincide con el .tex", 
                              "evidencia": f"{logpath}#{key}: {msg}"})
            continue
        # 4. procedencia del log (solo una vez por log)
        if logpath not in proced_log_ok:
            p = logd.get("_procedencia")
            if not p:
                proced_log_ok[logpath] = f"log {logpath}: SIN bloque _procedencia"
            else:
                faltan = [k for k in ("commit", "script", "script_sha256" if "script_sha256" in p or "sha256" in str(p) else "script") if k not in p]
                # chequeo flexible: requiere commit + script + algún checksum
                req = ["commit", "script"]
                faltan = [k for k in req if k not in p]
                haschk = any(k in p for k in ("script_sha256", "sha256", "checksum"))
                det = []
                if faltan:
                    det.append(f"faltan campos: {faltan}")
                if not haschk:
                    det.append("sin checksum del script")
                commit = p.get("commit", "")
                # ¿existe el commit?
                import subprocess
                try:
                    r = subprocess.run(["git", "cat-file", "-t", commit], capture_output=True, text=True, cwd=BASE)
                    if r.returncode != 0 or r.stdout.strip() != "commit":
                        det.append(f"commit {commit[:12]} no existe en el repo")
                except Exception:
                    det.append("no se pudo verificar el commit")
                sp = p.get("script", "")
                if sp and not os.path.exists(os.path.join(BASE, sp)):
                    det.append(f"script {sp} no existe en el repo")
                proced_log_ok[logpath] = ("; ".join(det) if det else None)
        pd = proced_log_ok[logpath]
        if pd:
            hallazgos.append({"nombre": name, "severidad": "ADVERTENCIA",
                              "causa": "procedencia del log incompleta/dudosa",
                              "evidencia": pd})
            continue
        ok_count += 1
    # nombres en tex pero no en yaml
    for name in tex:
        if name not in yaml:
            hallazgos.append({"nombre": name, "severidad": "ADVERTENCIA",
                              "causa": "\\val definido en .tex pero sin entrada en valores.yaml",
                              "evidencia": tex[name][1]})
    out = {"ok": ok_count, "total_yaml": len(yaml), "hallazgos": hallazgos}
    json.dump(out, open("/tmp/audit_val_chain.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    crit = sum(1 for h in hallazgos if h["severidad"] == "CRITICO")
    adv = sum(1 for h in hallazgos if h["severidad"] == "ADVERTENCIA")
    print(f"OK={ok_count}/{len(yaml)}  CRITICO={crit}  ADVERTENCIA={adv}")

main()
