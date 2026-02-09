# Portfolio Management Example

This example demonstrates how to use `etlite` to build a data pipeline that:
1. Extracts portfolio holdings from a local CSV file
2. Retrieves QQQ index composition data for benchmark comparison
3. Fetches real-time market prices from TradingView
4. Calculates portfolio weights and compares them against index allocations
5. Loads the processed results into Google Sheets for analysis



### Custom Transformations
```python
### pandas_trx.py
# Define specialized logic using standard Python libraries. 
# This transformation handles data cleaning and calculates the 
# current market value and relative weights for each holding.

import numpy as np
import pandas as pd



def calculate_portfolio_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """Cleans raw data and calculates portfolio valuation and weights."""

    # Handle missing values for new symbols or zero-share positions
    df.fillna({'benchmark_weight': '0,0', 'shares': 0}, inplace=True)
    
    # Calculate market value and internal weighting
    df['market_value'] = df['price'] * df['shares']
    df['portfolio_weight'] = df['market_value'] / df['market_value'].sum()
    
    return df
```

### Pipeline Configuration
```python
### pipeline_config.py
# The configuration layer decouples the pipeline logic from 
# the underlying data models.

import etlite.models as m
import pandas_trx as ptrx



# 1. Portfolio Data Models
portfolio_extractor = m.LocalExtractorModel(path='portfolio.csv')
portfolio_rename = m.RenameTransformerModel(columns_map={
    'Ticker': 'symbol', 
    'Number of shares': 'shares', 
    'Name': 'company'
})
portfolio_keep = m.KeepTransformerModel(columns_to_keep=['symbol', 'shares', 'company'])
portfolio_filter = m.StringFilterTransformerModel(column='symbol', operation='notin', args=['USD'])

# 2. Benchmark (QQQ) Data Models
benchmark_extractor = m.IndexWeightsYFExtractorModel(symbol='QQQ')
benchmark_rename = m.RenameTransformerModel(columns_map={
    'Symbol': 'symbol', 
    'Holding Percent': 'benchmark_weight'
})
benchmark_keep = m.KeepTransformerModel(columns_to_keep=['symbol', 'benchmark_weight'])

# 3. Data Integration (Blending)
initial_blend = m.MergeBlenderModel(blend_method='OuterJoin', on_column='symbol')

# 4. Real-time Market Pricing
def get_pricing_model(symbol_list):
    return m.LastPriceTradingviewExtractorModel(
        exchange='NASDAQ', 
        symbols=symbol_list, 
        interval='1D'
    )

pricing_rename = m.RenameTransformerModel(columns_map={'symbol': 'symbol', 'close': 'price'})

# 5. Final Processing and Export
final_blend = m.MergeBlenderModel(blend_method='LeftJoin', on_column='symbol')
metrics_transformer = m.PandasCustomTransformerModel(transformation_func=ptrx.calculate_portfolio_metrics)
final_keep = m.KeepTransformerModel(
    columns_to_keep=['symbol', 'price', 'shares', 'benchmark_weight', 'portfolio_weight'], 
    descending_by='benchmark_weight'
)

google_sheets_loader = m.GoogleSheetsLoaderModel(spreadsheet_name='Portfolio_Analysis', worksheet_name='Analysis_Export')
```


### Main Pipeline
```python
### pipeline.py
# Contains the main pipeline orchestration logic

import etlite as etl
import pipeline_config as cfg



# Step 1: Process Portfolio Holdings
portfolio_ds = etl.Extract(cfg.portfolio_extractor) \
    .transform(cfg.portfolio_rename) \
    .transform(cfg.portfolio_keep) \
    .transform(cfg.portfolio_filter) \
    .run()
    
# Step 2: Process Benchmark Data
benchmark_ds = etl.Extract(cfg.benchmark_extractor) \
    .transform(cfg.benchmark_rename) \
    .transform(cfg.benchmark_keep) \
    .run()

# Step 3: Merge Holdings with Benchmark
merged_ds = etl.Blend([portfolio_ds, benchmark_ds], cfg.initial_blend).run()

# Step 4: Enrich with Live Market Prices
active_symbols = merged_ds['symbol'].to_pylist()
market_prices_ds = etl.Extract(cfg.get_pricing_model(active_symbols)) \
    .transform(cfg.pricing_rename) \
    .run()

# Step 5: Final Analysis and Export
final_ds = etl.Blend([merged_ds, market_prices_ds], cfg.final_blend) \
    .transform(cfg.metrics_transformer) \
    .transform(cfg.final_keep) \
    .load(cfg.google_sheets_loader) \
    .run()

print(final_ds.to_pandas())
```

## Pipeline Overview

This example showcases the key features of `etlite`:

- **Extractors**: Retrieves data from multiple sources including local CSV files (`LocalExtractorModel`), Yahoo Finance API (`YFinanceAdapter`), and TradingView (`LastPriceTradingviewExtractorModel`)
- **Transformers**: Performs column renaming, filtering, selection, and custom Pandas transformations for portfolio analytics calculations
- **Blenders**: Combines datasets using SQL-style join operations (`OuterJoin` for comprehensive symbol lists, `LeftJoin` for price enrichment)
- **Loaders**: Exports the final processed dataset to Google Sheets for visualization and further analysis

The modular design allows each component to be configured independently and reused across different pipelines.