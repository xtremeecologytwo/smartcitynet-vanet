# Resultados verificados — SmartCityNet V4

Escenario real: **Centro Histórico de Quito, Ecuador**. Todos los valores se obtienen
ejecutando el programa sobre los datos en [`output/`](output/) y se reproducen con:

```bash
python scripts/analisis_sensibilidad.py     # Tablas 1 y 2
python scripts/generar_mapa_rsu.py          # figura del mapa (figuras/fig_rsu_map.pdf)
```

## Escenario / simulación

| Dato | Valor |
|---|---|
| Área (bbox) | lon −78.535°…−78.497°, lat −0.266°…−0.211° (UTM 17S, WGS84) |
| Mapa OSM descargado | 5 jun 2026 |
| Junctions elegibles (X) | 1211 |
| Duración simulación | 0–3660 s, muestreo cada 120 s → **31 snapshots** |
| Vehículos **distintos** | 132 |
| Activos por snapshot | min 1 · media 6.5 · max 9 |
| Instancias vehículo–snapshot (N) | 201 |
| Rango V2V/V2I (OBU) | 300 m · saltos máx **H = 3** |
| Entorno | SUMO 1.26.0 · Python 3.10 (NumPy 2.2, pandas 2.3) · AMD Ryzen 7 7735HS · 16 GB · Win 11 |

## Tabla 1 — Sensibilidad del conjunto candidato de RSU

Grado = **vecinos únicos** (grafo no dirigido). Desempate del *clustering* por id
ascendente (determinista).

| Config | g_min | ρ (m) | tras grado \|F\| | candidatas Y | reducción |
|---|---:|---:|---:|---:|---:|
| A | 3 | 15 | 1097 | 393 | 67.5 % |
| B | 3 | 20 | 1097 | 366 | 69.8 % |
| **C (referencia)** | **4** | **20** | **836** | **278** | **77.0 %** |
| D | 5 | 25 | 15 | 14 | 98.8 % |

A y B comparten |F|=1097 (mismo g_min=3). En este centro tipo malla pocas junctions
tienen ≥5 vecinos, por lo que g_min=5 (D) es muy selectivo.

## Tabla 2 — Conectividad y export (config C, 278 RSU, H=3)

| Métrica | Fórmula | Resultado |
|---|---|---:|
| Pares directos | M₁ = Σₛ nnz(S_{s,1}) | 1310 |
| Nuevos por salto | M₂ ; M₃ | 109 ; 8 |
| Todos los pares reales | K = Σ M_h = Σₛ nnz(R_{s,H}) | 1427 |
| Instancias vehículo–snapshot | N = Σₛ n_s | 201 |
| Tuplas exportadas | \|CVR\| = K + N | **1628** |
| Chequeo de integridad | \|CVR\| − K = N | ✓ (201) |
| Tiempos | visibilidad ≈ 3–4 s · multisalto < 0.1 s | — |
| Tamaño `.dat` | — | ≈ 63 KB |

El reenvío multisalto añade solo M₂+M₃ = 117 pares sobre los 1310 directos, porque
hay pocos vehículos activos por snapshot (media 6.5) que sirvan de repetidores.

## Extracto de export (trazabilidad)

| ⟨s,h,i,k⟩ | Significado | t (s) | vehículo SUMO | junction SUMO |
|---|---|---:|---|---|
| ⟨1,1,0,22⟩ | directa (1 salto) | 0 | V0 | 11135269234 |
| ⟨4,2,13,46⟩ | 2 saltos | 360 | V13 | 267037290 |
| ⟨26,3,116,50⟩ | 3 saltos | 3000 | V116 | 268253365 |
| ⟨1,4,0,0⟩ | artificial (r_∞) | 0 | V0 | — (sin servicio) |

## Archivos de la simulación ([`output/`](output/))

`map.osm`, `mapa.net.xml`, `mapa.poly.xml`, `mapa.rou.xml`, `mapa.sumocfg`, `fcd.xml`
(posiciones vehiculares), `junctions_limpias.json`, `edificios_limpios.json`,
`tuplas_visibilidad.json` (Matriz B / V2I), `tuplas_v2v.json` (Matriz A / V2V).
