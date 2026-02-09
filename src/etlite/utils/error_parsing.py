

def parse_pydantic_error(error):
    try:
        _type = error[0]['type'].capitalize()
        _loc = ", ".join(error[0]['loc'])
        _msg = error[0]['msg'].lower().split(' ')[::-1]
        rephrase = ' '.join(_msg)
        new_msg = f'{_type} {rephrase}: {_loc}'
        return new_msg
    except Exception:
        return error
    