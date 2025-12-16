

import abc

import pandas as pd
import pyarrow as pa



class PandasBaseTransformer(abc.ABC):
        
    @abc.abstractmethod
    def main_transformation(self, df: pd.DataFrame) -> pd.DataFrame:
        """Here should define all the logic of the transformer"""
        pass
    
    def __call__(self, table: pa.Table) -> pa.Table:
        df = table.to_pandas()
        df = self.main_transformation(df)
        return pa.Table.from_pandas(df)
