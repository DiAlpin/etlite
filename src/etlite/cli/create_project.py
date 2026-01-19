
from pathlib import Path

import etlite.cli.files_content as content



class Project:
    def __init__(self, name, path):
        self._name = name
        self._path = Path(path) / self._name 
        
    def init(self):
        self._check_if_project_exist()
        self._create_dirs()
        self._create_files()
        self._show_files_structure()
        
    def _check_if_project_exist(self):
        if self._path.exists():
            raise ValueError(f"Directory '{self._name}' already exists")

    def _create_dirs(self):
        self._path.mkdir(parents=True)
        # (self._path / "sql_queries").mkdir()
    
    def _create_files(self):
        (self._path / "pandas_trx.py").write_text(content.gen_pandas_trx(self._name))
        (self._path / "pipeline_config.py").write_text(content.gen_pipeline_config(self._name))
        (self._path / "pipeline.py").write_text(content.gen_pipeline(self._name))
        (self._path / ".env").write_text(content.gen_env())

    def _show_files_structure(self):
        print(f"Successfully created project '{self._name}' at {self._path.cwd()}")
        print(f"\nProject structure:")
        print(f"  {self._name}/")
        # print(f"    ├── sql_queries/")
        print(f"    ├── pandas_trx.py")
        print(f"    ├── pipeline_config.py")
        print(f"    ├── pipeline.py")
        print(f"    └── .env")
        
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



    

