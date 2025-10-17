# 🃏 Blackjack Counter Simulator — Hi-Lo System

## 📖 Overview
**Blackjack Counter Simulator** is a console-based application designed to simulate realistic blackjack games while implementing the **Hi-Lo card counting system**.  
Its main goal is to study the **statistical effectiveness** of the Hi-Lo method and **betting strategies** based on the *true count*, analyzing their impact on the player’s profitability against the house.

---

## 🎯 Project Goals
- Simulate realistic blackjack games using one or multiple decks.  
- Implement the **Hi-Lo** card counting system.  
- Dynamically adjust **bets** based on the true count.  
- Evaluate performance through **profit, ROI, and counting accuracy**.  
- Enable statistical studies of counting effectiveness.

---

## ⚙️ Core Features

### 🧩 Game Configuration
- Number of decks (1–8)  
- Player’s starting balance  
- Base bet  
- Betting multipliers based on true count  
- Optional: number of automatic simulations (e.g., 10,000 hands)

---

### 🃏 Game Simulation
- Deal cards (player and dealer)  
- Automated turns using a basic player strategy  
- Dealer follows official blackjack rules  
- Determine results (win, lose, push)  
- Update **Hi-Lo** and **true count** after each card  

#### Hi-Lo System
| Card | Count Value |
|------|--------------|
| 2–6  | +1           |
| 7–9  | 0            |
| 10–A | -1           |

**True Count** = `running_count / remaining_decks`

---

### 💰 Betting Strategy
The player adjusts their bet based on the true count:

| True Count | Bet Multiplier |
|-------------|----------------|
| ≤ 0         | 1x             |
| 1–2         | 2x             |
| 3–4         | 4x             |
| ≥ 5         | 8x             |

The final bet amount = `base_bet * multiplier`.

---

### 📊 Statistics & Analysis
After a simulation or session ends:

- Total hands played  
- Net profit or loss  
- ROI (%)  
- Average bet  
- Standard deviation of results  
- True count history  
- Number of counting errors or inconsistencies  

Results can be printed to the console or exported to `.csv`.

---

## 🧱 Project Structure

```
blackjack_sim/
│
├── main.py                # Main entry point
│
├── models/
│   ├── card.py            # Card class
│   ├── deck.py            # Deck/Shoe class (1–8 decks)
│   ├── hand.py            # Player/Dealer hand logic
│   ├── player.py          # Player with balance and strategy
│   └── dealer.py          # Dealer AI
│
├── logic/
│   ├── game.py            # Core game logic
│   ├── counting.py        # Hi-Lo counting logic
│   ├── strategy.py        # Betting strategy logic
│   └── stats.py           # Statistics and analysis
│
├── utils/
│   ├── display.py         # Console display functions
│   ├── config.py          # Game configuration parameters
│   └── logger.py          # Logging and debugging utilities
│
└── data/
    └── results.csv        # Stored simulation results
```

---

## 🗺️ Development Roadmap

### **Phase 1 — Base Game**
- [ ] Implement `Card`, `Deck`, and `Hand` classes  
- [ ] Add basic dealer and player logic  
- [ ] Simulate a single game (no counting or variable betting yet)  

✅ *Goal:* A functional blackjack game in the console.

---

### **Phase 2 — Hi-Lo Counting System**
- [ ] Implement `counting.py`  
- [ ] Update running count with each visible card  
- [ ] Display the true count during the game  

✅ *Goal:* Working Hi-Lo counting system in real-time.

---

### **Phase 3 — Betting Strategy**
- [ ] Implement `strategy.py`  
- [ ] Apply bet multipliers based on true count  
- [ ] Integrate betting with player balance  

✅ *Goal:* Simulate dynamic betting based on count.

---

### **Phase 4 — Statistics**
- [ ] Track each hand (count, bet, result, balance)  
- [ ] Compute performance metrics (profit, ROI, errors)  
- [ ] Export or display summary reports  

✅ *Goal:* Measure Hi-Lo system effectiveness.

---

### **Phase 5 — Automated Simulations**
- [ ] Allow running thousands of simulated hands  
- [ ] Generate statistical datasets  
- [ ] Analyze performance under various deck and rule setups  

✅ *Goal:* Quantitative evaluation of the Hi-Lo method.

---

### **Phase 6 — Web Interface (Future)**
- [ ] Build backend API with **FastAPI**  
- [ ] Create a frontend with **Next.js** or **Streamlit**  
- [ ] Add visual dashboards and charts (Plotly / Chart.js)  

✅ *Goal:* Interactive dashboard and visualization.

---

## 🧠 Suggested Tech Stack

**Console Phase:**
- Python 3.11+
- Built-in modules (`random`, `math`, `csv`, `statistics`, `argparse`)
- Optional: `pandas` for deeper data analysis

**Web Phase (future):**
- FastAPI  
- Next.js / React  
- Supabase (for storing results)  
- Plotly or Chart.js (for data visualization)

---

## 📁 Example Configuration (`utils/config.py`)

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

## 🧮 Example Simulation Output

```
[Game Start]
→ Shuffled 6 decks
→ Starting balance: $1000
→ Base bet: $10

[Hand 1]
→ Running count: +2
→ True count: +0.33
→ Bet: $20
→ Result: +$20
→ Balance: $1020

[Final Summary]
→ Hands played: 10000
→ Net profit: +$450
→ ROI: +4.5%
→ Average true count: +1.1
```

---

## 📈 Expected Outcomes
The simulator will allow you to:
- Evaluate the **statistical effectiveness** of the Hi-Lo system.  
- Determine the **expected edge** for the player.  
- Analyze how **deck count** and **bet strategy** influence performance.  

---

## 👨‍💻 Author
Developed by: *[Edwing Vera]*  
Initial version: 0.1.0  
License: MIT  
