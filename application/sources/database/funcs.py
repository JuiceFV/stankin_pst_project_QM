from .tables import tokens


async def insert(database, token, ip=''):
    # Acquiring new connection to database
    async with database.acquire() as conn:
        # Inserting values into database
        query = tokens.insert().values({'ip': ip, 'token': token})
        await conn.execute(query)


async def select(database, data=None):
    async with database.acquire() as conn:
        if data:
            query = tokens.select().where(**data)
        else:
            query = tokens.select()

        result = []
        async for row in conn.execute(query):
            result.append(row)

        return result