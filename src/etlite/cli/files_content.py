
from etlite.environ import EnvLoader



def gen_env() -> str:
    mandatory_vars = ['### Mandatory variables ###']
    optional_vars = ['### Optional variables ###']

    for name, md in EnvLoader._vars.items():
        ty, is_mandatory, default = md
        
        if ty == 'env':
            line = f'{name}={default}'
            
            if is_mandatory:
                mandatory_vars.append(line)
            else:
                optional_vars.append(line)

    content = [''] + mandatory_vars + ['', ''] + optional_vars
    return "\n".join(content)


def gen_pandas_trx(project):
    return f"""
import numpy as np



def dummy_pandas_trx(df):
    # define your pandas transformation
    return df
"""

def gen_pipeline_config(project):
    return f"""
import etlite.models as m
from pandas_trx import dummy_pandas_trx



input_extractor_model = m.LocalExtractorModel(path='/my/path')
dummy_trx_model = m.PandasCustomTransformerModel(transformation_func=dummy_pandas_trx)
"""

def gen_pipeline(project):
    return f"""
import etlite as etl
import pipeline_config as cfg 



dummy_data = etl.Extract(cfg.input_extractor_model).transform(cfg.dummy_trx_model).run() 
"""