
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


def gen_custom_transformation(project):
    return f"""
from {project}.custom_transformers import 

"""