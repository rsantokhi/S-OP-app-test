# PlanFlow — Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Install Dependencies

```bash
cd "c:\Users\Ravi\Documents\AIApps\S&OP Lucas Bols"
pip install -r requirements.txt
```

### Step 2: Run the App

```bash
streamlit run app.py
```

The app opens at `http://localhost:8501`

### Step 3: Explore Modules

**Dashboard** — Executive summary of KPIs
- Total inventory value, forecast accuracy, revenue at risk
- ERP sync status

**Demand Planning** — Forecast management
- Load historical demand from Excel (17k transactions)
- Run forecasts with ETS, SARIMA, Prophet, or Ensemble models
- 406 SKUs across Lucas Bols portfolio
- 12-month forecast horizon

**Inventory Planning** — Stock management
- View all 626 items with lead times, suppliers, on-hand quantities
- Highlight items below safety stock (Attention tab)
- Generate automated purchase order proposals
- Safety stock calculated at 98% service level

**Capacity Planning** — Manufacturing resource planning
- Monitor 2 manufacturing groups (Finished Products, Intermediate)
- Detect capacity overloads (utilization > 100%)
- Bottleneck analysis with mitigation recommendations

**Production Scheduling** — Gantt charts & order management
- Visualize production workload by workstation
- View all incoming and outgoing orders
- Track lead times and delivery dates

**S&OP Review** — Planning cycle management
- Monitor cycle status (Submitted, In Progress, Approved)
- Track 7 open exceptions with financial impact
- Export meeting pack for executive review

**Approvals** — Workflow management
- 4 pending items for approval
- Full approval history
- Change audit trail

**Promo Planning** — Promotion calendar
- 4 active/planned promotional campaigns
- Track uplift % and impact on demand
- Status: Approved, Pending, Draft

**New Products** — NPI pipeline
- 3 products in launch pipeline
- Track launch dates and comparable SKUs
- Initial forecast generation

**Changes Log** — Full audit trail
- All user actions timestamped
- Before/after values tracked
- Filter by user, module, date range

**Settings** — Configuration
- Forecast model parameters (horizon, seasonality, outliers)
- Inventory parameters (lead times, safety stock service level)
- System settings (sync frequency, alerts, retention)

---

## 📊 Using Demand Forecasting

1. Go to **Demand Planning** page
2. Select forecasting model: **Ensemble** (recommended)
3. Set forecast horizon: **12 months**
4. Click **Run Forecast** button
5. Models trained automatically on historical data
6. View forecast chart and statistics

**Models Used:**
- **ETS** — Exponential smoothing (seasonality detection)
- **SARIMA** — Auto-ARIMA with seasonal parameters
- **Prophet** — Facebook time series (holidays, structural breaks)
- **Ensemble** — Weighted by inverse MAPE for best accuracy

---

## 📦 Inventory Reorder Workflow

1. Go to **Inventory Planning** page
2. Click **Attention** tab → Items below safety stock
3. Scroll to **Order Proposals** tab
4. Click **Generate Proposals**
5. Review recommended quantities and lead times
6. **Approve All** to create purchase orders
7. POs ready to push to Oracle Fusion

**Safety Stock Formula:**
```
SS = 2.054 (98% service level) × σ(demand) × √(lead_time_months)
```

---

## 🎯 Exception Management

PlanFlow automatically detects:

1. **Shortages** — On-hand + incoming < (lead_time_months × avg_demand)
2. **Overstock** — Days on hand > 190 days
3. **Capacity Breaches** — Utilization > 100% for manufacturing group/month
4. **Supplier Delays** — Delivery dates past due
5. **Forecast Issues** — Accuracy below threshold

View all exceptions in **S&OP Review** page.

---

## 📈 Dashboard KPIs

| Metric | Formula | Target |
|--------|---------|--------|
| **Total Inventory Value** | Σ(on_hand × unit_value) | Monitor for optimization |
| **Forecast Accuracy (MAPE)** | Mean Absolute % Error | >85% |
| **Revenue at Risk** | Value of items below safety stock | <€5M |
| **Overstock Exposure** | Value of high-inventory items | <€100M |
| **OTIF Rate** | On-Time-In-Full delivery % | >95% |
| **Open POs** | Count of pending purchase orders | Monitor |

---

## 🔧 Configuration Tips

### For High Seasonality Products
- Increase **Seasonal Threshold** in Settings (0-10)
- Use **ETS** or **Prophet** model
- Extend forecast **Horizon** to 24 months to capture annual cycle

### For New Products
- Use **Comparable SKU** from Settings
- Manually override forecast in Demand Planning
- Adjust **Top-Down Forecast** to Brand or Category level

### For Demand Sensing (fast-moving items)
- Enable **Demand Sensing** in Settings
- Opens last 2 weeks for real-time adjustment
- Requires point-of-sale or web traffic data

### For Safety Stock Optimization
- Increase **Service Level** (80-99%) for critical items
- Decrease for slow-moving items to reduce carrying costs
- Target: Balance between stockout risk and inventory cost

---

## 💾 Data Files

**LB_Transactional_Data.xlsx** contains:
- **Transactions** (17,403 rows) — Historical daily sales
- **Item Info** (626 rows) — SKU master data
- **Orders to Receive** (5 rows) — Open inbound POs
- **Orders to Ship** (6 rows) — Open outbound shipments
- **Bill of Materials** (6 rows) — Component requirements

All data is cached in Streamlit session — refresh to reload Excel file.

---

## 🚨 Common Tasks

### "I need to change a forecast"
1. Go to **Demand Planning**
2. Select item from chart
3. Enter manual override value
4. Change appears in **Changes Log** with timestamp

### "Show me items about to stockout"
1. Go to **Inventory Planning**
2. Click **Attention** tab
3. All items with on_hand < safety_stock highlighted in yellow

### "Which suppliers are delayed?"
1. Go to **Inventory Planning**
2. Click **Open Orders In** tab
3. Sort by Delivery Date
4. Red highlighting shows past-due orders

### "Is our capacity sufficient?"
1. Go to **Capacity Planning**
2. View "Capacity vs Load Trend" chart
3. Red bars indicate overload
4. Check "Bottleneck Analysis" for mitigation options

### "Export the S&OP meeting pack"
1. Go to **S&OP Review**
2. Click **Export Meeting Pack** button
3. CSV file downloads with exception details

---

## 🎓 Understanding the Models

### ETS (Exponential Smoothing)
- **Best for:** Seasonal demand with clear trends
- **Speed:** Fast (< 1 second)
- **Requirements:** 13+ historical months

### SARIMA (Seasonal ARIMA)
- **Best for:** Complex autocorrelation patterns
- **Speed:** Medium (2-5 seconds, grid search)
- **Requirements:** 24+ historical months

### Prophet (Facebook)
- **Best for:** Holidays, structural breaks, trend changes
- **Speed:** Slow (5-10 seconds)
- **Requirements:** 1+ year of history

### Ensemble (Best-Pick)
- **Runs all models** and weights by accuracy (inverse MAPE)
- **Best for:** General-purpose forecasting
- **Speed:** ~10 seconds (all models combined)

---

## 📱 Mobile Access

PlanFlow is responsive — works on tablets and phones. However:
- **Data editor** in Demand Planning optimized for desktop
- **Gantt charts** better viewed on wide screens
- **CSV exports** recommended for mobile-only access

---

## 🔒 User Roles (Simulated)

Current user: **Jan Koops** (S&OP Planner)
- Can: View all modules, run forecasts, create POs, submit for approval
- Future: Will integrate with Azure AD for role-based access

Supported roles (future):
- **Planner** — View, create, edit forecasts
- **Approver** — Approve/reject, push to ERP
- **Finance** — View-only dashboard & reports
- **Admin** — Configure settings, manage users

---

## 🆘 Troubleshooting

**"Excel file not found"**
```
→ Ensure LB_Transactional_Data.xlsx is in same directory as app.py
```

**"Prophet not installed"**
```
→ Run: pip install prophet
   (Optional dependency — app works without it)
```

**"Charts not loading"**
```
→ Update Plotly: pip install --upgrade plotly
```

**"Slow performance on large datasets"**
```
→ Data is cached — refresh to reload
→ Forecast grid search can take 5-10 seconds
→ Approve/reject buttons disabled while processing
```

**"Settings not saving"**
```
→ Ensure you click "Save Settings" button
→ Settings stored in st.session_state (cleared on refresh)
```

---

## 📞 Next Steps

1. ✅ Start the app: `streamlit run app.py`
2. 📊 Explore Dashboard — view KPIs and ERP sync status
3. 📈 Run a demand forecast in Demand Planning module
4. 📦 Check Inventory for items needing attention
5. ✔️ Generate and approve purchase order proposals
6. 🎯 Monitor S&OP cycle status and exceptions

---

**Questions?** Refer to `README.md` for detailed documentation or check individual page files in `/pages/` directory.

**Ready for production?** See `planflow_kosten.html` for AWS deployment architecture and cost analysis.
