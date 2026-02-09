# ETLite

![Python 3.12](https://img.shields.io/badge/python-3.12%2B-blue)

A lightweight Python library for building local ETL (Extract, Transform, Load) pipelines with a simple, declarative API. Extract data from multiple sources (S3, local files, HTML, TradingView), transform using pandas, PyArrow, or SQL (DuckDB), and load to destinations like Google Sheets, S3, or databases. Built on PyArrow for efficient processing.

## Features

- **Extractors**: S3, local files, HTML scraping, TradingView and more
- **Transformations**: Built-in transformers and custom pandas/SQL transformations
- **Data Blending**: Merge and join multiple datasets
- **Loaders**: Export data to Google Sheets and more
- **Type-Safe Configuration**: Pydantic models for pipeline configuration
- **CLI Tool**: Quick project setup with `etl init`

## Installation

```bash
git clone https://github.com/DiAlpin/etlite.git
cd etlite
pip install -e .
```
**Note**: The `-e` flag (or `--editable`) installs the package in editable mode allowing you to make changes to the source code and have them immediately reflected without needing to reinstall the package.

## Quick Start

### 1. Activate Your Python Environment

First, activate the Python environment where ETLite is installed:

```bash
# For virtualenv/venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate     # On Windows

# For conda environment
conda activate your_env_name
```

### 2. Create a New Project

Once your environment is activated, navigate to any location where you want to create your pipeline project and use the CLI to create a new ETL project:

```bash
cd /path/to/your/pipelines
etl init -n my_etl_pipeline
```

This creates a new project directory with the following structure:

```
my_etl_project/
├── pandas_trx.py           # Custom pandas transformations
├── pipeline_config.py      # Pipeline configuration models
├── pipeline.py             # Main pipeline script
└── .env                    # Environment variables (configure this!)
```

### 3. Execute pipeline

To ensure that environment variables are correctly loaded from the 
`.env` file, execute the pipeline from the project's root directory:

```bash
cd my_etl_pipeline
python pipeline.py
```

## Examples

For a detailed walkthrough of building a real-world pipeline, see the [Portfolio Management Example](docs/examples/portfolio_management.md).

You can also initialize a pre-configured example project to explore the features by running:

```bash
etl init-example
```

## Available Components

### Extractors
- `LocalExtractorModel` - Extract from local CSV/TSV files
- `S3ExtractorModel` - Extract from AWS S3
- `HtmlExtractorModel` - Extract data from HTML pages
- `OhlcTradingviewExtractorModel` - Extract OHLC data from TradingView
- `LastPriceTradingviewExtractorModel` - Extract last price data from TradingView
- `PickDayPriceTradingviewExtractorModel` - Extract price data for a specific day

### Transformers
- `RenameTransformerModel` - Rename columns
- `KeepTransformerModel` - Keep specific columns
- `FillnaTransformerModel` - Fill missing values
- `StringFilterTransformerModel` - Filter rows based on string conditions
- `PandasCustomTransformerModel` - Apply custom pandas transformations

### Blenders
- `MergeBlenderModel` - Merge/join multiple datasets

### Loaders
- `GoogleSheetsLoaderModel` - Load data to Google Sheets

**Note on Roadmap:** New components, including additional extractors, transformation modules and additional loaders, are currently under development to further improve pipeline flexibility.

## Background

ETLite started as a fun project for the rapid prototyping of data pipelines used in quantitative analysis.
