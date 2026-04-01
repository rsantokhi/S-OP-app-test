# PlanFlow S&OP App — Setup Guide for Team

## Quick Start (5 minutes)

### 1. Clone the Repository
```bash
git clone https://github.com/rsantokhi/S-OP-app-test.git
cd "S&OP Lucas Bols"
```

### 2. Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the App
```bash
streamlit run app.py
```

The app will open at **http://localhost:8501**

---

## Project Structure

```
S&OP Lucas Bols/
├── app.py                          # Main entry point
├── requirements.txt                # Python dependencies
├── LB_Transactional_Data.xlsx      # Data file (must stay in root)
├── QUICKSTART.md                   # User guide
├── SETUP.md                        # This file
├── .gitignore                      # Git ignore rules
├── .streamlit/
│   └── config.toml                 # Streamlit configuration
├── utils/
│   ├── data_loader.py              # Excel data ingestion & caching
│   ├── forecast_engine.py          # ETS, SARIMA, Prophet, Ensemble models
│   └── styling.py                  # PlanFlow CSS theme & components
└── pages/
    ├── 1_Dashboard.py              # KPI overview
    ├── 2_Demand.py                 # Demand forecasting
    ├── 3_Inventory.py              # Inventory management
    ├── 4_Capacity.py               # Capacity planning
    ├── 5_Schedule.py               # Production scheduling
    ├── 6_SOP_Review.py             # S&OP cycle management
    ├── 7_Approvals.py              # Approval workflows
    ├── 8_Promo_Planning.py         # Promotion calendar
    ├── 9_New_Products.py           # NPI tracking
    ├── 10_Changes_Log.py           # Audit trail
    └── 11_Settings.py              # Configuration
```

---

## Requirements

- **Python 3.8+** (tested with 3.11)
- **Streamlit 1.35+** (for multi-page support)
- **Pandas 2.0+** (data manipulation)
- **Plotly 5.17+** (interactive charts)
- **statsmodels 0.14+** (ETS, SARIMA forecasting)
- **Prophet 1.1+** (optional, for Facebook's Prophet model)

See `requirements.txt` for complete list.

---

## Data File

**Important:** The file `LB_Transactional_Data.xlsx` must be in the project root directory.

It contains:
- **Transactions** (17,403 rows) — Historical sales data
- **Item info** (626 rows) — SKU master data with lead times, suppliers, inventory
- **Orders to receive** (5 rows) — Incoming purchase orders
- **Orders to ship** (6 rows) — Outgoing shipments
- **Bill of materials** (6 rows) — Component requirements

All data is cached in Streamlit session — refresh browser to reload Excel file.

---

## Development Workflow

### Making Changes

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** to pages, utils, or config

3. **Test locally**
   ```bash
   streamlit run app.py
   ```

4. **Commit with clear messages**
   ```bash
   git add .
   git commit -m "Add: your feature description"
   ```

5. **Push to GitHub**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create Pull Request** on GitHub for review

### Branch Naming Conventions

- `feature/` — New features
- `fix/` — Bug fixes
- `docs/` — Documentation updates
- `refactor/` — Code cleanup (no functional changes)
- `test/` — Test additions

---

## Common Issues

### "Port 8501 is already in use"
```bash
streamlit run app.py --server.port 8502
```

### "Prophet not installed"
Prophet is optional. If you don't need it:
- Remove from requirements.txt
- App will fall back to ETS/SARIMA models automatically

### "Excel file not found"
Ensure `LB_Transactional_Data.xlsx` is in the same directory as `app.py`

### Cache issues
Streamlit caches data aggressively. To clear cache:
```bash
rm -rf .streamlit/cache
# Then refresh the browser
```

---

## Features Overview

### Demand Planning
- Load historical demand from Excel
- Run forecasts with multiple models (ETS, SARIMA, Prophet, Ensemble)
- Manual forecast overrides with audit trail
- Demand trend visualization

### Inventory Management
- View all 626 items with lead times and suppliers
- Identify items below safety stock (Attention tab)
- Automated purchase order proposal generation
- Safety stock calculated at 98% service level

### Capacity Planning
- Monitor 2 manufacturing groups
- Detect capacity overloads (utilization > 100%)
- Bottleneck analysis with recommendations

### Forecasting Models

| Model | Best For | Speed | Requirements |
|-------|----------|-------|--------------|
| **ETS** | Seasonal demand | Fast (<1s) | 13+ months |
| **SARIMA** | Complex patterns | Medium (2-5s) | 24+ months |
| **Prophet** | Holidays/breaks | Slow (5-10s) | 1+ year |
| **Ensemble** | General purpose | ~10s | All models |
| **Naive** | Baseline | Instant | 12+ months |

---

## Team Collaboration Tips

1. **Always pull before starting work**
   ```bash
   git pull origin main
   ```

2. **Keep commits small and focused** — easier to review and revert if needed

3. **Write descriptive commit messages** — include what, why, and impact

4. **Test changes locally before pushing**

5. **Document any new parameters or configurations** in this file

---

## Support

For questions about:
- **Data sources:** Check QUICKSTART.md
- **API:** Review docstrings in utils/*.py
- **Streamlit:** See https://docs.streamlit.io
- **Forecasting models:** See docstrings in utils/forecast_engine.py

---

## Status

✓ All 11 pages verified and working
✓ Data loads successfully (626 items, 17,403 transactions)
✓ Forecasting engine functional
✓ Ready for team collaboration

---

**Last updated:** April 1, 2026
