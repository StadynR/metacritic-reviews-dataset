<div align="center">

# Metacritic Video Game Reviews Dataset & Scraper

Asynchronous Python scraper (Jupyter notebook) to build a structured dataset of video game metadata (title, platform, release date, critic metascore, user score, developer, publishers, genres) from Metacritic's public game listing/search pages.

</div>

> Data collection performed on: **October 7, 2025**  

This repository is based on the idea (and a bit of code) from [projectGames](https://github.com/BrunoBVR/projectGames) (2020), but it has been rewritten to account for the current structure of the Metacritic website and to extract the specific data I wanted.

## Features

- **🚀 Production-Ready Web App**: Modern Streamlit application with professional UI/UX design
- **🔄 Fully Asynchronous Scraping**: Built with `httpx` + `asyncio` + bounded concurrency for optimal performance
- **🛡️ Resilient Data Collection**: Retries with exponential backoff on transient errors (403/429/network issues)
- **📊 Advanced Machine Learning**: Random Forest model with feature engineering for accurate user score predictions
- **🎨 Interactive Visualizations**: Comprehensive charts using Plotly with elegant gauge displays and metrics
- **📈 Temporal & Trend Analysis**: Multi-dimensional data exploration across genres, platforms, and time periods
- **🔧 Robust Error Handling**: Graceful degradation and fallback mechanisms throughout the application
- **💾 Incremental Processing**: Per-page CSV snapshots for resilience and resumability during scraping
- **🎯 Smart Predictions**: Context-aware predictions with developer reputation, seasonal effects, and platform interactions
- **📱 Responsive Design**: Mobile-friendly interface with modern CSS styling and animations

## Repository Structure

```
pages/                          # Incremental per-page CSV outputs (games_data-page<N>.csv)
app/                           # Streamlit web application
├── app.py                     # Main application file
├── styles.py                  # Custom CSS styles and components
└── metacritic_dataset_features_enhanced.csv  # Enhanced dataset with engineered features
metacritic_scraper.ipynb        # Main scraping + cleaning notebook (end‑to‑end workflow)
metacritic_visualizations.ipynb # Data visualization and exploratory analysis
metacritic_model.ipynb          # Machine learning model for score prediction
metacritic_dataset_raw.csv      # Full raw concatenated dataset (may contain null / 'tbd')
metacritic_dataset_clean.csv    # Cleaned dataset (no nulls, scores numeric, 'tbd' removed)
requirements.txt                # Core Python dependencies (updated with Streamlit and Plotly)
README.md                      # This document
```

## Structure of the Datasets (Columns)

| Column | Type (raw) | Type (clean) | Description |
|--------|------------|--------------|-------------|
| `name` | string | string | Game title |
| `platform` | string / null | string | Platform identifier as listed by Metacritic |
| `release_date` | string | datetime64 | Initial release date (any platform) |
| `metascore` | string / int / 'tbd' | float | Critic metascore (0–100); 'tbd' removed in clean set |
| `user_score` | string / float / 'tbd' | float | Average user score (0–10); 'tbd' removed in clean set |
| `developer` | string / null | string | Primary developer |
| `publisher` | list / string | list | Publisher(s) |
| `genre` | list / string | list | Genre (may reflect composite genres) |

## Installation & Environment

Tested with **Python 3.10** (3.10+ should work) in a virtual environment.

### Windows (PowerShell)
```powershell
# Clone the repository
git clone https://github.com/StadynR/metacritic-reviews-dataset.git
cd metacritic-reviews-dataset

# Create and activate virtual environment
python -m venv env
./env/Scripts/Activate.ps1

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### Linux/macOS
```bash
# Clone the repository
git clone https://github.com/StadynR/metacritic-reviews-dataset.git
cd metacritic-reviews-dataset

# Create and activate virtual environment
python -m venv env
source env/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### (Optional) Jupyter Environment Setup
For data analysis and model development:
```bash
pip install ipykernel
python -m ipykernel install --user --name metacritic-env --display-name "Metacritic Analysis"
```

### Troubleshooting
If you encounter event loop issues in Jupyter:
```bash
pip install nest_asyncio
```

For Windows users experiencing execution policy issues:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## Usage

### Data Collection (Scraping Workflow)

1. Open `metacritic_scraper.ipynb` in Jupyter / VS Code.  
2. (Optional) Adjust parameters near the top:  
   - `PAGES` (total listing pages to process)  
   - `MAX_CONCURRENCY` (active HTTP tasks limit)  
   - `BATCH_SIZE` (pages processed per orchestrated chunk)  
3. Run cells sequentially until the async runner executes. This will:  
   - Fetch each listing page.  
   - Extract all game links.  
   - Fetch & parse each game detail (platforms, scores, JSON-LD metadata, publishers, genres, developer).  
   - Write per-page CSVs to `pages/`.  
4. After completion, run the concatenation cell to build the unified DataFrame and save `metacritic_dataset_raw.csv`.  
5. Run the cleaning section to output `metacritic_dataset_clean.csv`.  

#### Resuming / Partial Runs
Currently the notebook does not skip already-downloaded page CSVs automatically—re-running will overwrite existing per-page files. To resume, manually adjust the page range to start after the last completed page.

### Data Visualization

Open `metacritic_visualizations.ipynb` to explore the dataset through various visualizations:
- **Temporal Analysis**: Metascore vs User Score evolution over years
- **Genre Distribution**: Pie charts and frequency analysis of game genres
- **Metagenre Classification**: Grouped genre analysis for broader categorization
- **Platform/Manufacturer Analysis**: Score trends across different gaming platforms and manufacturers

### Machine Learning Model

Open `metacritic_model.ipynb` to:
- Train a Random Forest model to predict user scores
- Explore feature engineering including developer reputation, seasonal effects, platform-genre interactions
- Evaluate model performance with cross-validation
- Make predictions for new games based on their characteristics

The model uses features such as:
- Metascore (scaled to 0-10)
- Developer reputation (historical average scores)
- Release timing (month, holiday releases)
- Platform characteristics (age, manufacturer)
- Genre popularity and platform-genre interactions

### Web Application

Launch the interactive Streamlit web application:

```bash
cd app
streamlit run app.py
```

The application features a modern interface with:

#### Professional UI/UX Design
- **Elegant Color Scheme**: Professional grey gradient backgrounds for optimal readability
- **Custom CSS Styling**: Modern cards, shadows, and animations throughout the interface
- **Mobile-Responsive**: Adapts seamlessly to different screen sizes and devices

#### Advanced Prediction Interface
- **Interactive Score Gauge**: Large, color-coded circular gauge with smooth animations
- **Smart Input Forms**: Dropdowns populated with popular options from the actual dataset
- **Example Game Buttons**: Quick-start presets for Nintendo, PlayStation, and PC games
- **Real-time Validation**: Comprehensive input validation with helpful error messages

#### Advanced Visualizations
- **Score Gauge Chart**: Beautiful circular gauge showing prediction with color-coded ranges
- **Animated Metrics**: Eye-catching metric cards with performance indicators
- **Dataset Insights**: Live statistics from the current dataset

#### Error Handling & Robustness
- **Graceful Degradation**: App works even if optional libraries (like Plotly) aren't installed
- **Input Validation**: Comprehensive validation for all user inputs
- **Fallback Values**: Smart defaults when data is missing from the dataset
- **Error Recovery**: Detailed error messages and recovery suggestions

#### User Experience
- **Contextual Help**: Tooltips and explanations for each input field
- **Example Games**: Quick-start buttons with popular game configurations
- **Score Interpretation**: Clear categorization of prediction results (Exceptional, Good, Mixed, Poor)
- **Feature Explanations**: Detailed sidebar explaining how each factor affects predictions

If you want to check the app in action, go to https://metacritic-user-review-prediction.streamlit.app

## Contributing
I created this repository for a class project in my master's program, but after much consideration I decided to make it public because most video game databases stop at 2020 and the scrapers used to obtain that information are outdated. I probably will not maintain or update this repository for long after the project ends, so if you want to help keep it updated, please do.

## License
Released under the **MIT License** (see `LICENSE`).

Note: While the code is MIT-licensed, the underlying game metadata (scores, release info, etc.) originates from Metacritic. If you redistribute derivative datasets, attribute Metacritic as the original source and ensure your usage complies with their terms of service.

## FAQ

**Q: Can I scrape all 580 pages safely?**  
A: Technically yes, but be mindful of server load. Consider lowering concurrency or splitting over time.

**Q: Some rows have missing or unexpected publisher / genre data.**  
A: Site markup or JSON-LD may be incomplete for certain legacy titles; heuristic extraction can be improved.

**Q: Why are some platforms duplicated with different scores?**  
A: Different platform releases (and sometimes re-releases) have independent critic/user scores on Metacritic.

**Q: How do I add new fields (e.g., ESRB rating)?**  
A: Extend `get_game_details` with new selectors and update the DataFrame assembly accordingly.

**Q: What's the accuracy of the machine learning model?**  
A: The enhanced Random Forest model achieves an R² score of ~0.3-0.4, indicating moderate predictive power. The model works best for games with established developer histories and common genre-platform combinations.

**Q: Can I use the model to predict scores for unreleased games?**  
A: Yes, but ensure the game's developer, platform, and genre exist in the training data. The model may have reduced accuracy for completely new developers or unusual genre-platform combinations.

**Q: How do I update the app with new data?**  
A: Replace the CSV files in the `app/` directory with updated datasets, then restart the Streamlit application. The caching system will automatically load the new data.

**Q: Can I customize the app's appearance?**  
A: Yes! Edit the `app/styles.py` file to modify colors, layouts, and styling. The CSS is modular and well-documented for easy customization.

