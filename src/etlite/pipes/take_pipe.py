
import pyarrow as pa

from etlite.registry import Registry
from etlite.pipes.base_pipe import BasePipe



class Take(BasePipe):
    def __init__(self, table: pa.Table):
        super().__init__(
            table=table,
            registry=Registry()
        )
