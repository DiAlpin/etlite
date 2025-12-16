

import abc

import pyarrow as pa



class PyarrowBaseTransformer(abc.ABC):
        
    @abc.abstractmethod
    def main_transformation(self, table: pa.Table) -> pa.Table:
        """Here should define all the logic of the transformer"""
        pass
    
    def __call__(self, table: pa.Table) -> pa.Table:
        return self.main_transformation(table)
