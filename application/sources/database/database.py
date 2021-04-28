import aiopg.sa as pg
from .tables import tokens
from sqlalchemy import select, insert, delete, asc


class Database:
    async def create_engine(self, config):
        self.db = await pg.create_engine(**config)

    async def close(self):
        self.db.close()
        await self.db.wait_closed()

    async def insert(self, data):
        # Acquiring new connection to database
        async with self.db.acquire() as conn:
            # Inserting values into database
            query = insert(tokens).values(**data)
            await conn.execute(query)

    async def select(self, where):
        # Acquiring new connection to database
        async with self.db.acquire() as conn:
            # Building select query to database
            query = select(tokens).filter_by(**where).order_by(asc(tokens.c.id))

            result = []
            # Selecting values from database
            async for row in conn.execute(query):
                # Converting RawProxy values to python dictionary and appending to result
                result.append(dict(row))

            return result

    async def get_tokens(self):
        async with self.db.acquire() as conn:
            query = select([tokens.c.token]).order_by(asc(tokens.c.id))

            result = []
            async for token in conn.execute(query):
                result.append(token['token'])

            return result

    async def pop(self):
        async with self.db.acquire() as conn:
            query = select(tokens).order_by(asc(tokens.c.id))
            result = await conn.execute(query)
            row = await result.first()

            if row:
                print('Popped up token:', row['token'])

                query = delete(tokens).filter_by(id=row['id'])
                await conn.execute(query)

                return row

            return None

    async def delete(self, where):
        # Acquiring new connection to database
        async with self.db.acquire() as conn:
            # Building delete query to database
            query = delete(tokens).filter_by(**where)
            # Deleting values from database
            await conn.execute(query)