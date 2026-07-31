"""
generar_mapa_rsu.py
===================
Regenera la figura vectorial `resultados/figuras/fig_rsu_map.pdf` del artículo V4:
las RSU candidatas de la configuración de referencia (C: g_min=4, rho=20 m) sobre
las huellas de los edificios del Centro Histórico de Quito, en coordenadas
geográficas. Salida en PDF vectorial (calidad intacta al escalar).

Requiere matplotlib (ver requirements.txt).

Uso (desde la raíz del repo):
    python scripts/generar_mapa_rsu.py
"""
import json, os, sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)
OUT = os.path.join(RAIZ, "resultados", "output")
FIG = os.path.join(RAIZ, "resultados", "figuras", "fig_rsu_map.pdf")

import matplotlib
matplotlib.use("pdf")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MplPoly, Patch
from matplotlib.collections import PatchCollection
from backend.parsear_xml import filtrar_junctions_rsu, obtener_proyeccion, convertir_xy_a_lonlat

edificios = json.load(open(os.path.join(OUT, "edificios_limpios.json"), encoding="utf-8"))
junctions = json.load(open(os.path.join(OUT, "junctions_limpias.json"), encoding="utf-8"))
net = os.path.join(OUT, "mapa.net.xml")
proy = obtener_proyeccion(net)

# Config de referencia C
rsusC = filtrar_junctions_rsu(junctions, net, min_grado=4, radio_cluster=20.0)


def toll(x, y):
    lat, lon = convertir_xy_a_lonlat(x, y, proy)
    return lon, lat


fig, ax = plt.subplots(figsize=(7.4, 4.2))
patches = [MplPoly([toll(vx, vy) for vx, vy in verts], closed=True)
           for verts in edificios.values() if len(verts) >= 3]
ax.add_collection(PatchCollection(patches, facecolor="#f97316",
                  edgecolor="#c2600f", alpha=0.45, linewidths=0.15))
rx = [toll(d["x"], d["y"])[0] for d in rsusC.values()]
ry = [toll(d["x"], d["y"])[1] for d in rsusC.values()]
ax.scatter(rx, ry, s=11, c="#ef4444", edgecolors="#7f1d1d", linewidths=0.3, zorder=5)
ax.set_aspect("equal", adjustable="datalim")
ax.set_xlabel("Longitude (deg)", fontsize=9); ax.set_ylabel("Latitude (deg)", fontsize=9)
ax.tick_params(labelsize=7); ax.margins(0.02)
ax.legend(handles=[
    plt.Line2D([], [], marker='o', ls='', mfc="#ef4444", mec="#7f1d1d", ms=5,
               label="Candidate RSUs (n=%d)" % len(rx)),
    Patch(facecolor="#f97316", alpha=0.45, edgecolor="#c2600f", label="Buildings")],
    fontsize=7.5, loc="upper right", framealpha=0.9)
fig.savefig(FIG, bbox_inches="tight")
print(f"Figura regenerada: {FIG}  ({len(rx)} RSU candidatas)")
