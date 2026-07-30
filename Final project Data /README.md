# Tech Employment Trends (2001–2025)
**Data Visualization — Final Individual Project, Summer 2026**

An analysis of hiring, layoffs, and revenue efficiency across 25 major tech
companies (2001–2025), connected to US macroeconomic conditions
(GDP growth, unemployment).

## 🔗 Live Dashboard
https://tech-employment-viz-93r5rgmd5siqepylaaynzq.streamlit.app/

## 📁 Repo Contents
- `app.py` — Streamlit dashboard (interactive, curated subset of the analysis)
- `requirements.txt` — dependencies for Streamlit Cloud
- `tech_employment_2000_2025.csv` — dataset
- `tech_employment_analysis.ipynb` — full analysis notebook (10 analytical
  questions, each with a Plotly visualization)

## 📊 Key Questions Explored
1. How do layoffs relate to US GDP growth and unemployment?
2. How have hiring and attrition rates diverged over time?
3. Are companies growing revenue faster than headcount ("efficiency era")?
4. Does the stock market react to layoff announcements?
5. Which companies cut deepest in 2008, 2020, and 2022–23?
6. Which companies show the most volatile hiring patterns?
7. How has revenue-per-employee evolved?
8. Does US unemployment predict tech layoffs, and with what lag?
9. Do estimated/lower-confidence data points cluster around crisis years?
10. How do mature companies compare to recently-IPO'd companies?

## 🛠️ Run Locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

