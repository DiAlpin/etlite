
import numpy as np
import pandas as pd
from pathlib import Path

import etlite.cli.files_content as content
from etlite.cli.parse_md import generate_filename_and_content



class Example:
    sections = [
        'Custom Transformations',
        'Pipeline Configuration',
        'Main Pipeline',
    ]
    def __init__(self, name, out_path):
        self._name = name
        self._out_root = Path(out_path) / self._name 
        self._source_md_path = self._get_source_md_path()
        
    def _get_source_md_path(self):
        root_path = Path(__file__).resolve().parents[3]
        return root_path / 'docs/examples/portfolio_management.md'
        
    def _create_dummy_portfolio(self):
        path = self._out_root / 'portfolio.csv'
        stocks = {
            'Ticker': [
                'AAPL', 'MSFT', 'GOOGL', 
                'AMZN', 'NVDA', 
                'USD'
                ],
            'Name': [
                'Apple Inc.', 'Microsoft', 'Alphabet', 
                'Amazon', 'NVIDIA', 
                'USD'
                ],
            'Number of shares': list(np.random.randint(10, 51, 5)) + [1500],
            'Sector': [
                'Technology', 'Technology', 'Technology', 
                'Consumer Cyclical', 'Technology',
                None
                ]
        }
        portfolio_df = pd.DataFrame(stocks)
        portfolio_df.to_csv(path, index=False)
    
    def init(self):
        self._create_dirs()
        self._create_files()
        self._create_dummy_portfolio()
        self._show_files_structure()

    def _create_dirs(self):
        self._out_root.mkdir(parents=True)
    
    def _create_files(self):
        for fn, ct in generate_filename_and_content(self._source_md_path, self.sections):
            (self._out_root / fn).write_text(ct)
        (self._out_root / ".env").write_text(content.gen_env())

    def _show_files_structure(self):
        print(f"\nSuccessfully created  example project '{self._name}' at {self._out_root.cwd()}")
        print(f"\nProject structure:")
        print(f"  {self._name}/")
        print(f"    ├── pandas_trx.py\t\t# Custom pandas transformations")
        print(f"    ├── pipeline_config.py\t# Pipeline configuration models")
        print(f"    ├── pipeline.py\t\t# Main pipeline script")
        print(f"    ├── portfolio.csv\t\t# Dummy portfolio")
        print(f"    └── .env\t\t\t# Environment variables")
        
        # Important reminder
        print("\n" + "="*80)
        print("IMPORTANT: Configure your environment variables!")
        print("="*80)
        print(f"\nNext steps:")
        print(f"   1. cd {self._name}")
        print(f"   2. Edit the .env file and add your credentials and required variables")
        print(f"   3. Run: python pipeline.py")
        print(f"\nRemember: Never commit your .env file to git repo!")
        print("="*80 + "\n")
