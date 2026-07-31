# SmartCityNet — Plataforma Web de Generación de Matrices de Conectividad V2V/V2I (VANET)

**Trabajo de Integración Curricular — Redes Vehiculares Ad-hoc (VANETs) · Escuela Politécnica Nacional**

Plataforma web que automatiza la obtención de los **datos de entrada** para modelos de
optimización de despliegue de RSU (*Road Side Units*). Sigue el flujo:

```
área geográfica → escenario SUMO → snapshots de movilidad → RSU candidatas
              → matrices V2V/V2I → conectividad multisalto → dataset para optimización
```

Selecciona un área real en un mapa, descarga la topología de OpenStreetMap, la procesa
con SUMO, simula el tráfico, y calcula la conectividad **V2I** (vehículo–RSU) y **V2V**
(vehículo–vehículo) con **línea de vista (LoS)** considerando los edificios como
obstáculos. Luego extiende la conectividad a **varios saltos** y exporta el conjunto de
datos listo para un *solver*.

> Este repositorio es la versión **curada** que acompaña al artículo de las Jornadas
> **SmartCityNet (V4)**: contiene la plataforma, los scripts para reproducir los
> resultados, la simulación/resultados obtenidos, y el artículo final.

---

## 📂 Estructura

```
smartcitynet-vanet/
├── app.py                     # 🎯 Programa: orquestador (Streamlit)
├── frontend/                  # 🖥️ mapa interactivo + visualización (Folium)
├── backend/                   # ⚙️ descarga OSM, SUMO, LoS, V2V/V2I, multisalto, export
├── optimizacion/              # 🧮 export .dat + solver de RSU (docplex/CPLEX)
├── scripts/                   # 🔁 reproducir los resultados del artículo
│   ├── analisis_sensibilidad.py   # Tablas 1 y 2 (A–D, M_h, K, |CVR|)
│   └── generar_mapa_rsu.py        # figura vectorial del mapa de RSU
├── resultados/                # 📊 lo que sale de EJECUTAR el programa
│   ├── output/                #    simulación: red SUMO, FCD, tuplas V2V/V2I …
│   ├── figuras/fig_rsu_map.pdf
│   └── RESULTADOS.md          #    números verificados de la V4
├── paper/                     # 📄 artículo final V4 (.tex + .pdf + Definitions/)
├── requirements.txt
└── DOCUMENTACION_COMPLETA.md  # 📖 documentación técnica extensa del proyecto
```

---

## 🚀 Instalación y ejecución

**Requisitos:** Python **3.10** (recomendado: es la única versión que corre también el
motor completo de CPLEX), **SUMO** (con `netconvert`/`polyconvert` en el PATH y
`SUMO_HOME` configurado).

```bash
python -m venv .venv
.venv\Scripts\activate            # Windows  (Linux/Mac: source .venv/bin/activate)
pip install -r requirements.txt

# 1) Ejecutar la plataforma web
streamlit run app.py              # abre http://localhost:8501

# 2) Reproducir los resultados del artículo (usa resultados/output/)
python scripts/analisis_sensibilidad.py
python scripts/generar_mapa_rsu.py
```

> **Sin correr la simulación:** los datos de `resultados/output/` ya están incluidos,
> así que los scripts reproducen los números y la figura del artículo directamente.
> Para generar un escenario nuevo, usa la interfaz (`streamlit run app.py`).

---

## 📊 Resultados (V4)

Escenario: **Centro Histórico de Quito**. Resumen (detalle y reproducción en
[`resultados/RESULTADOS.md`](resultados/RESULTADOS.md)):

- 1211 junctions elegibles → configuración de referencia **C** (g_min=4, ρ=20 m):
  **278 RSU candidatas** (77 % de reducción).
- 31 snapshots, 132 vehículos distintos (media 6.5 activos/snapshot), N = 201.
- Conectividad: M₁=1310 pares directos, K=1427 pares alcanzables, **|CVR|=1628** tuplas
  exportadas (chequeo |CVR|−K=N ✓).

El artículo completo está en [`paper/articulo_smartcitynetV4.pdf`](paper/articulo_smartcitynetV4.pdf).

---

## 🧩 Módulos principales (backend)

| Módulo | Función |
|---|---|
| `descargar_osm.py` | Descarga el área desde la API de OpenStreetMap |
| `sumo_pipeline.py` | `netconvert` → red vial, `polyconvert` → edificios, `randomTrips` → rutas |
| `simulacion_sumo.py` | Corre SUMO y parsea el FCD (posiciones por instante) |
| `parsear_xml.py` | Junctions/edificios + **filtrado de RSU** (grado no dirigido + clustering) |
| `visibilidad.py` | Línea de vista (LoS) + tuplas V2I y V2V |
| `multisalto.py` | Matrices R_h, S_h, D_H (conectividad multisalto) |
| `exportar_dat.py` | Exporta el dataset `<s,h,v,r>` (CVR) para optimización |

Para el detalle matemático y de implementación, ver
[`DOCUMENTACION_COMPLETA.md`](DOCUMENTACION_COMPLETA.md).

---

## 📝 Licencia

Trabajo de Integración Curricular — Escuela Politécnica Nacional.
