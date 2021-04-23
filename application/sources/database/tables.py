from sqlalchemy import (
    Table, Integer, VARCHAR, MetaData, Column
)


__all__ = 'tokens'

meta = MetaData()

tokens = Table(
    'tokens', meta,
    Column('id', Integer, primary_key=True),
    Column('ip', VARCHAR(255), nullable=True),
    Column('token', VARCHAR(3))
)
