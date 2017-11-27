from datetime import datetime
from uuid import UUID
from functools import singledispatch

@singledispatch
def serialize(val):
    return str(val)

@serialize.register(UUID)
def _uuid_to_str(val):
    return str(val)

@serialize.register(datetime)
def _datetime_to_str(val):
    return val.isoformat() + 'Z' # val.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
