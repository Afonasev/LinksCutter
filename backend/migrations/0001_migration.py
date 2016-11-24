"""
Migration '0001_migration.py'
Created at 2016-11-24T18:07:14.819054
"""

from linkscutter.application import connection_factory


def apply():
    with connection_factory() as connection:
        connection.executescript(
            '''
            CREATE TABLE links (
                pk INTEGER PRIMARY KEY,
                url TEXT,
                key TEXT UNIQUE,
                created_at TIMESTAMP
            );
            '''
        )


def rollback():
    with connection_factory() as connection:
        connection.executescript('DROP TABLE links')
