# Kuros Biosciences – OPEX Planningsmodel 2026

A web-based planning application for managing OPEX budgets across multiple cost centers at Kuros Biosciences.

## 🎯 Features

- **Multi-Cost Center Planning**: Manage OPEX for 3 cost centers (CH01 IT, NL01 R&D, NL01 Manufacturing)
- **Dynamic Budget Grid**: Edit monthly values (Jan–Dec) with real-time totals
- **Categories & Line Items**: Organize expenses by category with customizable GL accounts
- **Visualizations**: Monthly trends, category distribution, cumulative forecasts
- **Summary Dashboard**: Compare all cost centers side-by-side
- **Export**: Download planning as CSV for further analysis
- **Responsive Design**: Works on desktop and tablet

## 📁 Project Structure

```
AIApps/
├── opex_planning.html          # Main planning app (all-in-one)
├── parse_excel.ps1             # PowerShell script to extract Excel data
├── parse_pptx.ps1              # PowerShell script to extract PowerPoint data
├── README.md                    # This file
└── Budget Files/                # Source budget Excel files (not in repo)
    ├── Budget 2026 Kuros - Master - 20251121.xlsx
    ├── CH01_Budget2026_4710_RHU_v2.xlsx
    ├── NL01_Budget2026_1100_FDG_v2.xlsx
    ├── NL01_Budget2026_3100_SMU_v2.xlsx
    └── Budget Days Round 2 20251104.pptx
```

## 🚀 Getting Started

### Option 1: Open Directly in Browser
```bash
# Simply open the HTML file
open opex_planning.html
# or from PowerShell:
Start-Process 'opex_planning.html'
```

### Option 2: Run on a Local Web Server (recommended)
```bash
# Using Python 3
python -m http.server 8000

# Using Node.js http-server
npx http-server
```
Then navigate to `http://localhost:8000/opex_planning.html`

## 📊 Budget Workflow (2026)

| Date | Milestone | Owner |
|------|-----------|-------|
| Oct 6 | Budget owners submit detailed budgets | Finance |
| Oct 16-17 | **Budget Days** (presentations) | ELT |
| Nov 4-5 | **Budget Days 2** (final review) | ELT |
| Nov 25 | **BoD approval** – Final budget & MTP | BoD |

## 💾 Data Structure

Each cost center contains:
- **Categories**: Personnel, Travel, Training, Production, etc.
- **Line Items**: GL Account, Description, Monthly Values (1–12), Comments
- **Calculations**: Automatic monthly and annual totals

### Built-in Cost Centers

| Code | Name | Company | Leader | Currency |
|------|------|---------|--------|----------|
| 4710 | IT | CH01 | Rafael Hutter | CHF |
| 1100 | R&D General | NL01 | Florence de Groot | EUR |
| 3100 | Manufacturing | NL01 | Sjoerd Musters | EUR |

## 🔧 Customization

### Add a New Cost Center
Edit the `STATE.costCenters` array in the HTML (around line 150):
```javascript
{
  id: 'CODE-XXXX',
  code: 'XXXX',
  name: 'Your Cost Center',
  company: 'COMPANY',
  leader: 'Leader Name',
  currency: 'USD',
  categories: [...]
}
```

### Import Data from Excel
Use the provided PowerShell scripts:
```powershell
# Extract sheet data
.\parse_excel.ps1 "path\to\file.xlsx" "xl/worksheets/sheet8.xml"

# Extract presentation content
.\parse_pptx.ps1 "path\to\presentation.pptx"
```

## 🎨 UI Notes

- **Sidebar**: Switch between cost centers
- **Info Bar**: Quick view of CC metadata and FY total
- **Tabs**: OPEX Planning → Charts → Summary
- **Table**: Editable grid with real-time recalculation
- **Charts**: Interactive visualizations (Chart.js)
- **Print**: Hide sidebar and controls for clean printing

## 📄 Export & Reporting

Click **"Export CSV"** to download budget as CSV:
- Includes all categories and line items
- Maintains monthly breakdown + FY totals
- Compatible with Excel/Sheets for further analysis

## 🛠 Technologies

- **Frontend**: HTML5 + Tailwind CSS
- **Charts**: Chart.js 3.x
- **State**: Vanilla JavaScript (no framework)
- **Styling**: Responsive, print-friendly

## 📝 License

Internal Kuros Biosciences use only.

## 👤 Support

For issues or feature requests, contact the finance planning team.

---

**Version**: 1.0  
**Last Updated**: March 2026  
**Status**: Active
