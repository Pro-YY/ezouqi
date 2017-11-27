from uuid import uuid4
from datetime import datetime
from ezq_core.database import execute

async def store_event(event, params, *args, **kwargs):
    sc = '''INSERT INTO "ezq_event" VALUES ($1,$2,$3,$4,$5,$6);'''
    request_id = params['request_id'] if 'request_id' in params else None
    now = datetime.utcnow()
    sa = (
        str(uuid4()),           # id
        event,                  # name
        '{}',                   # j
        now,                    # created_at
        None,                   # updated_at
        request_id,             # request_id
    )
    return await execute(sc, *sa)

async def _set_columns_by_pkid(table, pkid, change,
        pkid_name='id', updated_at_name='updated_at'):
    change[updated_at_name] = datetime.utcnow()
    fields = sorted(change)
    update = [change[x] for x in fields]
    set_clause = ''
    for i in range(len(fields)):
        if i == 0:
            set_clause += '"{}"=${}'.format(fields[i], i+1)
        else:
            set_clause += ', "{}"=${}'.format(fields[i], i+1)
    sc = '''UPDATE "{0}" SET {1} WHERE {2}='{3}'\
    '''.format(table, set_clause, pkid_name, pkid)
    sa = update
    print('# sql c: ', sc)
    print('# sql a:', sa)
    return await execute(sc, *sa)

async def update_account(params, *args, **kwargs):
    account_id = params['account_id']
    d = params['request_json']['data']
    # the fields can be updated
    u = {}
    if 'name' in d:
        u['name'] = d['name']
    if 'email' in d:
        u['email'] = d['email']
    return await _set_columns_by_pkid('ezq_account', account_id, u)
