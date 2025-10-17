# 🃏 Blackjack Counter Simulator — Sistema Hi-Lo

## 📖 Descripción general
**Blackjack Counter Simulator** es una aplicación de consola diseñada para simular partidas reales de blackjack, implementando el sistema de conteo de cartas **Hi-Lo**.  
El objetivo es estudiar la **eficacia estadística** del conteo y las **estrategias de apuesta** basadas en el conteo real, analizando su impacto en la rentabilidad del jugador frente a la casa.

---

## 🎯 Objetivos del proyecto
- Simular partidas de blackjack realistas con barajas múltiples.  
- Implementar el **sistema Hi-Lo** de conteo de cartas.  
- Ajustar las **apuestas dinámicamente** en función del conteo real.  
- Evaluar resultados en base a **ganancia, rentabilidad y desempeño del conteo**.  
- Permitir estudios estadísticos sobre la eficacia del método.  

---

## ⚙️ Funcionalidades principales

### 🧩 Configuración del juego
- Número de mazos (1–8)  
- Balance inicial del jugador  
- Apuesta base  
- Factores de apuesta según el conteo real (multiplicadores)  
- Número de simulaciones (opcional, para modo automático)

---

### 🃏 Simulación de partida
- Reparto inicial de cartas (jugador y dealer).  
- Turnos automatizados con estrategia básica del jugador.  
- Turno del dealer según reglas oficiales.  
- Resolución de resultados (ganar, perder, empatar).  
- Actualización del conteo **Hi-Lo** y **conteo real**.  

#### Sistema Hi-Lo
| Carta | Valor de conteo |
|--------|-----------------|
| 2–6    | +1              |
| 7–9    | 0               |
| 10–A   | -1              |

**Conteo real** = `conteo_corriente / mazos_restantes`

---

### 💰 Estrategia de apuestas
El jugador ajusta su apuesta en función del conteo real:

| Conteo Real | Multiplicador de apuesta |
|--------------|--------------------------|
| ≤ 0          | 1x                       |
| 1–2          | 2x                       |
| 3–4          | 4x                       |
| ≥ 5          | 8x                       |

El valor de la apuesta resultante se aplica sobre la apuesta base definida en la configuración.

---

### 📊 Estadísticas y análisis
Al finalizar la sesión o simulación:

- Total de manos jugadas  
- Ganancia o pérdida neta  
- Rentabilidad (%)  
- Promedio de apuesta  
- Desviación estándar de ganancias  
- Evolución del conteo real  
- Número de errores o conteos inconsistentes  

Los resultados pueden mostrarse en consola o exportarse en formato `.csv`.

---

## 🧱 Estructura del proyecto

```
blackjack_sim/
│
├── main.py                # Punto de entrada principal
│
├── models/
│   ├── card.py            # Clase Carta
│   ├── deck.py            # Clase Mazo (1 o varios mazos)
│   ├── hand.py            # Clase Mano del jugador/dealer
│   ├── player.py          # Clase Jugador con balance y estrategia
│   └── dealer.py          # Clase Dealer (IA básica)
│
├── logic/
│   ├── game.py            # Lógica central de la partida
│   ├── counting.py        # Sistema Hi-Lo y conteo real
│   ├── strategy.py        # Estrategia de apuesta dinámica
│   └── stats.py           # Registro y análisis estadístico
│
├── utils/
│   ├── display.py         # Visualización en consola
│   ├── config.py          # Parámetros globales de configuración
│   └── logger.py          # Registro de jugadas o errores
│
└── data/
    └── results.csv        # Almacenamiento de resultados de simulaciones
```

---

## 🗺️ Roadmap de desarrollo

### **Fase 1 — Base del juego**
- [ ] Implementar clases `Card`, `Deck` y `Hand`  
- [ ] Crear lógica básica del dealer y del jugador  
- [ ] Ejecutar una partida simple (sin conteo ni estrategia avanzada)  

✅ *Objetivo:* obtener un juego funcional de blackjack en consola.

---

### **Fase 2 — Sistema de conteo Hi-Lo**
- [ ] Implementar módulo `counting.py`  
- [ ] Actualizar conteo con cada carta visible  
- [ ] Calcular y mostrar conteo real en consola  

✅ *Objetivo:* tener un conteo funcional en tiempo real.

---

### **Fase 3 — Estrategia de apuestas**
- [ ] Crear módulo `strategy.py`  
- [ ] Aplicar multiplicadores de apuesta según el conteo real  
- [ ] Integrar con balance del jugador  

✅ *Objetivo:* simular variaciones de apuesta basadas en conteo.

---

### **Fase 4 — Estadísticas**
- [ ] Registrar cada mano con resultado, apuesta y conteo  
- [ ] Calcular métricas de rendimiento (ganancia, ROI, etc.)  
- [ ] Exportar resultados a `.csv` o mostrar resumen en consola  

✅ *Objetivo:* medir la eficacia del conteo.

---

### **Fase 5 — Simulaciones automáticas**
- [ ] Añadir opción de correr miles de partidas automáticamente  
- [ ] Analizar resultados globales y patrones estadísticos  

✅ *Objetivo:* obtener evidencia cuantitativa del rendimiento del sistema Hi-Lo.

---

### **Fase 6 — Interfaz Web (futuro)**
- [ ] Backend con **FastAPI** para simulaciones  
- [ ] Frontend interactivo con **Next.js** o **Streamlit**  
- [ ] Visualización de gráficos y estadísticas (Plotly / Chart.js)  

✅ *Objetivo:* interfaz visual y dashboard de análisis.

---

## 🧠 Tecnologías sugeridas

**Etapa consola:**
- Python 3.11+
- Módulos estándar (`random`, `math`, `csv`, `statistics`, `argparse`)
- `pandas` (para análisis opcional)

**Etapa web (futuro):**
- FastAPI  
- Next.js / React  
- Supabase (para almacenar estadísticas)  
- Plotly o Chart.js (para visualización)

---

## 📁 Ejemplo de configuración (`utils/config.py`)

```python
CONFIG = {
    "decks": 6,
    "starting_balance": 1000,
    "base_bet": 10,
    "bet_factors": {
        0: 1,
        1: 2,
        3: 4,
        5: 8
    },
    "auto_simulations": 10000
}
```

---

## 🧮 Ejemplo de flujo de simulación

```
[Inicio del juego]
→ Barajar 6 mazos
→ Balance inicial: $1000
→ Apuesta base: $10

[Partida 1]
→ Conteo corriente: +2
→ Conteo real: +0.33
→ Apuesta: $20
→ Resultado: +$20
→ Balance: $1020

[Resumen final]
→ Manos jugadas: 10000
→ Ganancia neta: +$450
→ ROI: +4.5%
→ Conteo promedio: +1.1
```

---

## 📈 Resultados esperados
El simulador permitirá:
- Evaluar la **eficacia estadística** del conteo Hi-Lo.  
- Determinar la **ventaja esperada** del jugador frente a la casa.  
- Analizar el **impacto del número de mazos** y la **estrategia de apuestas**.  

---

## 👨‍💻 Autor  
Desarrollado por: *[Edwing Vera]*  
Versión inicial: 0.1.0  
Licencia: MIT  
