# Winning Space Race with Data Science

Applied Data Science Capstone: predicting whether a **Falcon 9 first stage will land**, so a new launch provider (Space Y) can price bids against SpaceX ($62M with reuse vs $165M+ for competitors).

**Author:** Khyati Kendhe

## Key findings
- Landing success rose from 0% (2010-2014) to 88% (2020) as the booster matured.
- Modern boosters (FT, B4, B5) land 64% of the time vs 5% for v1.0/v1.1. CCAFS LC-40 looks weak (27%) mainly because it flew old boosters; with modern boosters only it reaches 75%, level with KSC LC-39A (77%).
- Among modern boosters, landing success is 83% up to 4,000 kg and 33% above 6,000 kg.
- Best model: tuned Decision Tree (10-fold CV 79%, test accuracy 71%). The test set is only 21 launches, so differences between models are within noise.

## Repository contents
| File | Purpose | Runs offline? |
|---|---|---|
| `jupyter-labs-spacex-data-collection-api.ipynb` | Data collection from the SpaceX REST API | needs internet |
| `jupyter-labs-webscraping.ipynb` | Web scraping of Wikipedia launch tables | needs internet |
| `labs-jupyter-spacex-Data wrangling.ipynb` | Missing values, counts, binary `Class` label | yes (outputs saved) |
| `jupyter-labs-eda-sql-coursera_sqllite.ipynb` | Ten SQL queries on SQLite | yes (outputs saved) |
| `edadataviz.ipynb` | EDA charts | yes (outputs saved) |
| `lab_jupyter_launch_site_location.ipynb` | Folium maps and distance lines | yes (outputs saved) |
| `spacex_dash_app.py` | Plotly Dash dashboard | yes |
| `SpaceX_Machine_Learning_Prediction_Part_5.ipynb` | LR, SVM, Decision Tree, KNN with GridSearchCV | yes (outputs saved) |
| `data/` | Launch table, dashboard data, wrangled data, model results | |
| `figures/` | Charts, schematic maps, generated Folium HTML maps | |
| `presentation/` | Final capstone slides (PDF and PPTX) | |
| `scripts/` | Scripts that regenerate the slide figures and model results | |

## Run it
```bash
pip install -r requirements.txt
jupyter lab                 # open the notebooks; run wrangling first
python spacex_dash_app.py   # dashboard at http://127.0.0.1:8050
```

## Notes on data and reproducibility
- Analysis notebooks use `data/spacex_launch_table.csv` (101 Falcon launches, 2010-2020) and `data/spacex_launch_dash.csv` (56 launches with a landing outcome).
- The two internet notebooks write their own CSVs (`dataset_part_1.csv`, `spacex_web_scraped.csv`) and were not executed when this repo was assembled; the Wikipedia page layout changes over time.
- Landing `Class` = 1 when `Landing_Outcome` starts with "Success"; failures, no-attempt and ocean tests are 0.
- Proximity coordinates in the Folium notebook are approximate points chosen by eye.
