from .tables import tokens


async def insert(database, token, ip=''):
    # Acquiring new connection to database
    async with database.acquire() as conn:
        # Inserting values into database
        query = tokens.insert().values({'ip': ip, 'token': token})
        await conn.execute(query)


async def select(database, ip=None, token=None):
    # Acquiring new connection to database
    async with database.acquire() as conn:
        # Building select query to database
        if ip and token:
            query = tokens.select().where(tokens.c.ip == ip, tokens.c.token == token)
        elif token:
            query = tokens.select().where(tokens.c.token == token)
        elif ip:
            query = tokens.select().where(tokens.c.ip == ip)
        else:
            query = tokens.select()

        result = []
        # Selecting values from database
        async for row in conn.execute(query):
            # Converting RawProxy values to python dictionary and appending to result
            result.append(dict(row))

        return result


async def delete(database, ip=None, token=None):
    # Acquiring new connection to database
    async with database.acquire() as conn:
        # Building delete query to database
        if ip and token:
            query = tokens.delete().where(tokens.c.ip == ip, tokens.c.token == token)
        elif token:
            query = tokens.delete().where(tokens.c.token == token)
        elif ip:
            query = tokens.delete().where(tokens.c.ip == ip)
        else:
            query = tokens.delete()

        # Deleting values from database
        await conn.execute(query)