<div align="center">

# Metacritic Video Game Reviews Dataset & Scraper

Asynchronous Python scraper (Jupyter notebook) to build a structured dataset of video game metadata (title, platform, release date, critic metascore, user score, developer, publishers, genres) from Metacritic's public game listing/search pages.

</div>

> Data collection performed on: **October 7, 2025**  
> The visualization notebook is currently a **work in progress** (WIP) and will likely not run as-is.

This repository is based on the idea (and a bit of code) from [projectGames](https://github.com/BrunoBVR/projectGames) (2020), but it has been rewritten to account for the current structure of the Metacritic website and to extract the specific data I wanted.

## Features

- Fully asynchronous scraping with `httpx` + `asyncio` + bounded concurrency.
- Resilient request helper: retries with backoff on transient errors (403 / 429 / network).
- Two-stage extraction: list pages → detail pages (HTML + JSON-LD parsing).
- Per-page incremental CSV snapshots saved under `pages/` for resilience & resumability.
- Final raw & cleaned consolidated datasets: [metacritic_dataset_raw.csv](https://github.com/StadynR/metacritic-reviews-dataset/blob/main/metacritic_dataset_raw.csv), [metacritic_dataset_clean.csv](https://github.com/StadynR/metacritic-reviews-dataset/blob/main/metacritic_dataset_clean.csv).
- Data cleaning pipeline embedded in the scraper notebook.

## Repository Structure

```
pages/                          # Incremental per-page CSV outputs (games_data-page<N>.csv)
metacritic_scraper.ipynb        # Main scraping + cleaning notebook (end‑to‑end workflow)
metacritic_visualizations.ipynb # (WIP) early exploratory plots
metacritic_dataset_raw.csv      # Full raw concatenated dataset (may contain null / 'tbd')
metacritic_dataset_clean.csv    # Cleaned dataset (no nulls, scores numeric, 'tbd' removed)
requirements.txt                # Core Python dependencies
README.md                       # This document
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

Tested with **Python 3.11** (3.10+ should work) in a virtual environment.

### Windows (PowerShell)
```powershell
python -m venv env
./env/Scripts/Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
```

### (Optional) Jupyter Kernel Registration
If you want the virtual environment to appear as a Jupyter kernel:
```powershell
pip install ipykernel
python -m ipykernel install --user --name metacritic-env --display-name "Metacritic Env"
```

Implicit / standard library: `asyncio`, `json`, `re`, `ast`, `pathlib`, `time`, `random`.

If you encounter nested event loop issues inside Jupyter, install:
```
pip install nest_asyncio
```

## Usage (Scraping Workflow)

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

### Resuming / Partial Runs
Currently the notebook does not skip already-downloaded page CSVs automatically—re-running will overwrite existing per-page files. To resume, manually adjust the page range to start after the last completed page.

## Visualizations (WIP)
`metacritic_visualizations.ipynb` currently contains early exploratory line plots (yearly average metascore / user score). It will evolve.

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

