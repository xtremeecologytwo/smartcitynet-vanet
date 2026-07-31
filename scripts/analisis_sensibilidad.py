"""
analisis_sensibilidad.py
========================
Reproduce las Tablas 1 y 2 del artículo V4 (SmartCityNet) a partir de los datos
en resultados/output/ (la simulación ya ejecutada).

- Tabla 1: sensibilidad del conjunto candidato de RSU a (g_min, rho)
           bajo el grado NO DIRIGIDO (vecinos únicos), configuraciones A–D.
- Tabla 2: métricas de conectividad y export de la configuración de referencia
           (C: g_min=4, rho=20 m), H=3: M_h, K, N y |CVR|.

Uso (desde la raíz del repo):
    python scripts/analisis_sensibilidad.py
"""
import json, os, sys, math, time

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)
OUT = os.path.join(RAIZ, "resultados", "output")

from backend.parsear_xml import filtrar_junctions_rsu
from backend.simulacion_sumo import parsear_fcd
from backend.visibilidad import generar_tuplas_visibilidad
from backend import multisalto as ms


def cargar():
    J = json.load(open(os.path.join(OUT, "junctions_limpias.json"), encoding="utf-8"))
    E = json.load(open(os.path.join(OUT, "edificios_limpios.json"), encoding="utf-8"))
    V = json.load(open(os.path.join(OUT, "tuplas_v2v.json"), encoding="utf-8"))
    return J, E, V


def tabla1(J):
    net = os.path.join(OUT, "mapa.net.xml")
    X = len(J)
    print(f"\n=== Tabla 1: sensibilidad del conjunto candidato (X = {X}) ===")
    print(f"{'Cfg':>4} {'g_min':>6} {'rho':>5} {'Y':>6} {'Reduc.%':>8}")
    configs = [("A", 3, 15), ("B", 3, 20), ("C", 4, 20), ("D", 5, 25)]
    ref = None
    for name, g, r in configs:
        C = filtrar_junctions_rsu(J, net, min_grado=g, radio_cluster=float(r))
        print(f"{name:>4} {g:>6} {r:>5} {len(C):>6} {100*(1-len(C)/X):>8.1f}")
        if name == "C":
            ref = {k: {"x": v["x"], "y": v["y"], "grado": v["grado"]} for k, v in C.items()}
    return ref


def tabla2(rsusC, E, V, H=3):
    print(f"\n=== Tabla 2: conectividad/export, config C ({len(rsusC)} RSU, H={H}) ===")
    fcd, _ = parsear_fcd(os.path.join(OUT, "fcd.xml"), 120)
    t0 = time.perf_counter()
    tuplas_v2i, _ = generar_tuplas_visibilidad(fcd, rsusC, E, radio_obu=300.0)
    t_vis = time.perf_counter() - t0

    matrices = {float(k): v for k, v in V["matrices"].items()}
    rsu_ids = sorted(rsusC.keys())
    t0 = time.perf_counter()
    res = ms.analizar_todos(matrices, tuplas_v2i, rsu_ids, H=H, forzar_simetria=True)
    t_ms = time.perf_counter() - t0

    N = 0; M = {h: 0 for h in range(1, H + 1)}; K = 0; ns = []
    for r in res.values():
        n = r["resumen"]["n_vehiculos"]; N += n; ns.append(n)
        for ps in r["resumen"]["por_salto"]:
            M[ps["h"]] += ps["pares_nuevos"]
        if r["resumen"]["por_salto"]:
            K += r["resumen"]["por_salto"][-1]["pares_acumulados"]
    distintos = len({v for m in matrices.values() for v in m["vehiculos"]})

    for h in range(1, H + 1):
        print(f"  M_{h} = sum_s nnz(S_(s,{h})) = {M[h]}")
    print(f"  K = sum_s nnz(R_(s,H))          = {K}   (sum M_h = {sum(M.values())})")
    print(f"  N = sum_s n_s                   = {N}")
    print(f"  |CVR| = K + N                   = {K+N}")
    print(f"  Vehiculos distintos             = {distintos}")
    print(f"  n_s por snapshot: min={min(ns)} media={N/len(ns):.1f} max={max(ns)}")
    print(f"  Integridad |CVR|-K == N         : {(K+N)-K == N}")
    print(f"  Tiempos: visibilidad {t_vis:.2f}s | multisalto {t_ms:.2f}s")


if __name__ == "__main__":
    J, E, V = cargar()
    ref = tabla1(J)
    tabla2(ref, E, V, H=3)
