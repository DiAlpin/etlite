# ETLite

A lightweight Python library for creating local ETL (Extract, Transform, Load) pipelines. ETLite provides a simple, declarative API for building data pipelines with support for multiple data sources, transformations, and destinations. Built on PyArrow for efficient data processing, it enables you to extract data from various sources (S3, local files, HTML, TradingView), apply transformations using pandas, PyArrow or SQL through DuckDB, blend multiple datasets, and load results to destinations like Google Sheets, AWS S3, SQL DB or local.

## Features

- **Multiple Extractors**: S3, local files, HTML scraping, TradingView data
- **Flexible Transformations**: Built-in transformers (rename, filter, fillna, keep columns) and custom pandas transformations
- **Data Blending**: Merge and join multiple datasets
- **Loaders**: Export data to Google Sheets and more
- **Type-Safe Configuration**: Pydantic models for pipeline configuration
- **CLI Tool**: Quick project setup with `etl init`

## Installation

ETLite requires Python 3.12 or higher.


### Install from Source

```bash
git clone https://github.com/DiAlpin/etlite.git
cd etlite
pip install .
```

## Quick Start

### 1. Activate Your Python Environment

First, activate the Python environment where ETLite is installed:

```bash
# For virtualenv/venv
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate  # On Windows

# For conda
conda activate your_env_name
```

### 2. Create a New Project

Once your environment is activated, navigate to any location where you want to create your pipeline project and use the CLI to scaffold a new ETL project:

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

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Author

Daniel Broboana (daniel.broboana@gmail.com)
