import aiopg.sa as pg
from .tables import tokens


class Database:
    async def create_engine(self, config):
        self.db = await pg.create_engine(**config)

    async def close(self):
        self.db.close()
        await self.db.wait_closed()

    async def insert(self, token, ip=''):
        # Acquiring new connection to database
        async with self.db.acquire() as conn:
            # Inserting values into database
            query = tokens.insert().values({'ip': ip, 'token': token})
            await conn.execute(query)

    async def select(self, ip=None, token=None):
        # Acquiring new connection to database
        async with self.db.acquire() as conn:
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

    async def select_tokens(self):
        async with self.db.acquire() as conn:
            query = tokens.select()

            result = []
            async for token in conn.execute(query):
                result.append(token)

            return result

    async def delete(self, ip=None, token=None):
        # Acquiring new connection to database
        async with self.db.acquire() as conn:
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