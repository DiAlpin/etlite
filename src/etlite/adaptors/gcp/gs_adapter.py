
import gspread
import pandas as pd 
from gspread_dataframe import set_with_dataframe

from etlite.environ import EnvLoader as env



class GoogleSheetAdapter:
    env_requirements = ['GCP_TOKEN_PATH']
    
    def __init__(self, spreadsheet_name, worksheet_name):
        self._spreadsheet_name = spreadsheet_name
        self._worksheet_name = worksheet_name
        self._credentials_path = env.GCP_TOKEN_PATH
        self._worksheet = None
    
    def insert_df(self, df: pd.DataFrame):
        if self._worksheet is None:
             raise RuntimeError("Worksheet connection not established.")
             
        set_with_dataframe(
            worksheet=self._worksheet,
            dataframe=df, 
            include_index=False, 
            include_column_header=True,
            resize=False
        )
     
    def __enter__(self):
        try:
            gc = gspread.service_account(filename=self._credentials_path)
            spreadsheet = gc.open(self._spreadsheet_name)
            self._worksheet = spreadsheet.worksheet(self._worksheet_name)
            return self 
            
        except FileNotFoundError:
            raise RuntimeError(f"Error: Credentials file not found at {self._credentials_path}")
        except gspread.exceptions.SpreadsheetNotFound:
            raise RuntimeError(f"Error: Spreadsheet '{self._spreadsheet_name}' not found.")  
        except gspread.exceptions.WorksheetNotFound:
            raise RuntimeError(f"Error: Worksheet '{self._worksheet_name}' not found.")
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        return False
        