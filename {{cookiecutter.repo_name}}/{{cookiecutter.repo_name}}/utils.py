from dateutil.parser import parse


def cast_to_datetime(datetime_str):
    if datetime_str is None:
        return None
    return parse(datetime_str)
