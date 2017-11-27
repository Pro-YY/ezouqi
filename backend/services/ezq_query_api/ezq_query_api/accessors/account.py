from ezq_query_api.database import fetchrow, fetch

async def fetch_account_by_id(account_id, fields, *args, **kwargs):
    sc = '''SELECT "id","name","email","j","created_at" FROM "ezq_account" WHERE "id"=$1\
    '''
    sa = (account_id, )
    print(sc)
    print(sa)
    result = await fetchrow(sc, *sa)
    return result

async def query_account(fields, *args, **kwargs):
    sc = '''SELECT "id","name","email","j","updated_at" FROM "ezq_account"\
    '''
    sa = ()
    result = await fetch(sc, *sa)
    return result
