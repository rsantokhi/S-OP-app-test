# PlanFlow — S&OP Planning Application

A comprehensive web-based Sales & Operations Planning (S&OP) application for Lucas Bols, built with Streamlit.

## Features

- **Demand Planning** — Forecast management with multiple statistical models (ETS, SARIMA, Prophet, Ensemble)
- **Inventory Planning** — Stock management, safety stock calculation, automated reorder proposals
- **Capacity Planning** — Manufacturing capacity monitoring and bottleneck detection
- **Production Scheduling** — Gantt charts and order management
- **S&OP Review** — Planning cycle management with exception tracking
- **Workflow & Approvals** — Multi-step approval workflow for forecasts and plans
- **Promotional Planning** — Campaign tracking and demand uplift modeling
- **New Product Introduction** — NPI pipeline and launch planning
- **Full Audit Trail** — Changes log and user activity tracking
- **Executive Dashboard** — KPI summary and key metrics

## Installation

### 1. Install Python & Dependencies

```bash
# Install dependencies from requirements.txt
pip install -r requirements.txt
```

### 2. Prepare Your Environment

Ensure you have:
- Python 3.9+
- The data file `LB_Transactional_Data.xlsx` in this directory (already included)

### 3. Run the Application

```bash
streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`

## Architecture

```
S&OP Lucas Bols/
├── app.py                    # Main app entry + sidebar
├── requirements.txt          # Python dependencies
├── LB_Transactional_Data.xlsx  # Source data file
├── utils/
│   ├── data_loader.py        # Excel data ingestion
│   ├── forecast_engine.py    # ETS, SARIMA, Prophet, Ensemble models
│   ├── styling.py            # PlanFlow CSS theme and components
│   ├── exceptions_engine.py  # Exception detection rules
│   └── __init__.py
└── pages/
    ├── 1_Dashboard.py        # Executive dashboard
    ├── 2_Demand.py           # Demand planning
    ├── 3_Inventory.py        # Inventory management
    ├── 4_Capacity.py         # Capacity planning
    ├── 5_Schedule.py         # Production scheduling
    ├── 6_SOP_Review.py       # S&OP review cycle
    ├── 7_Approvals.py        # Workflow approvals
    ├── 8_Promo_Planning.py   # Promotional planning
    ├── 9_New_Products.py     # New product tracking
    ├── 10_Changes_Log.py     # Audit trail
    └── 11_Settings.py        # Configuration
```

## Data Structure

### Excel Input (LB_Transactional_Data.xlsx)

- **Transactions** — 17,403 sales records by date, item, location, market
- **Item Info** — 626 SKUs with lead times, suppliers, inventory levels
- **Orders to Receive** — Open inbound purchase orders
- **Orders to Ship** — Open outbound shipments
- **Bill of Materials** — Component requirements for finished goods

## Forecasting Models

The app includes multiple statistical forecasting models:

| Model | Algorithm | Use Case |
|-------|-----------|----------|
| **ETS** | Exponential Smoothing with trend & seasonality | Seasonal product demand |
| **SARIMA** | Auto-regressive integrated moving average | Complex temporal patterns |
| **Prophet** | Facebook's time series library | Holidays & structural breaks |
| **Naive Seasonal** | Same month last year | Baseline/fallback |
| **Ensemble** | Weighted average (inverse MAPE) | Best overall accuracy |

All models automatically select based on lowest mean absolute percentage error (MAPE) on validation set.

### Safety Stock Calculation

```
SS = Z(service_level) × σ(demand) × √(lead_time_months)
```

- Service level: 98% (configurable)
- Z-score: 2.054 for 98% service level
- Lead time: From item master or defaults

## Key Features

### 1. Demand Forecasting
- Upload historical demand from Excel
- Run forecasts with configurable models
- Manual overrides for promotional periods
- Track forecast accuracy (MAPE, RMSE)

### 2. Inventory Management
- Real-time stock level monitoring
- Automatic safety stock calculations
- "Generate Order Proposals" to create POs
- Items below safety stock highlighted for attention

### 3. Capacity Planning
- Monitor manufacturing utilization by workstation
- Identify overloaded periods
- Bottleneck analysis and mitigation recommendations

### 4. S&OP Review
- Cycle status tracking (Submitted, In Progress, Approved)
- Exception management (shortage, overstock, capacity)
- Financial impact estimation
- Export meeting pack for executive review

### 5. Workflow & Approvals
- Multi-role approvals (Planner, Approver, Admin)
- Full audit trail of all changes
- Change log with before/after values
- User & timestamp tracking

## Configuration

### Settings Page (pages/11_Settings.py)

Configure:
- Forecast horizon (1-36 months)
- Seasonal threshold for pattern detection
- Service level for safety stock (80-99%)
- Default lead times and order cycles
- Sync frequencies with ERP systems
- Email alert thresholds

## Performance

- **Data Loading**: Cached with `@st.cache_data` — Excel loaded once per session
- **Forecasting**: ETS/SARIMA grid search completes in <10 seconds per SKU
- **Rendering**: All Plotly charts render interactively in <2 seconds

## Production Deployment

PlanFlow is designed for AWS deployment:

- **Compute**: ECS Fargate (containerized Node.js + Streamlit)
- **Database**: PostgreSQL RDS Multi-AZ (€185/month)
- **Load Balancer**: AWS ALB with blue-green deployment
- **Monitoring**: CloudWatch logs and metrics
- **Cost**: €452/month for production configuration (15-50 users)

See `planflow_kosten.html` for detailed cost analysis.

## Troubleshooting

### "ModuleNotFoundError: prophet"
Prophet is an optional dependency. If not installed, the app falls back to ETS/SARIMA.

```bash
pip install prophet
```

### Excel file not loading
Ensure `LB_Transactional_Data.xlsx` is in the same directory as `app.py`.

### Charts not rendering
Update Plotly:

```bash
pip install --upgrade plotly
```

## Usage Example

1. **Open Dashboard** — View KPI summary and sync status
2. **Go to Demand Planning** — Select forecasting model and run forecast
3. **Check Inventory** — Review items below safety stock, generate PO proposals
4. **Monitor Capacity** — Identify bottlenecks in manufacturing
5. **S&OP Review** — Track exceptions and cycle status
6. **Approvals** — Approve or reject pending items
7. **Settings** — Customize forecasting and inventory parameters

## API Integration (Future)

Currently uses static data from Excel. Future versions will integrate:
- Oracle Fusion Cloud REST API (items, inventory, purchase orders)
- Azure Active Directory for authentication
- AWS EventBridge for scheduled forecast runs

## Support

For questions or issues:
- Check `planflow_architecture.html` for technical details
- Review `requirements.txt` for dependency versions
- Refer to individual page files (pages/*.py) for feature documentation

## License

Internal use only — Lucas Bols & Finext Digital Finance

---

**Version:** 1.0  
**Last Updated:** April 2026  
**Built with:** Streamlit, Pandas, Plotly, StatsModels, Prophet
