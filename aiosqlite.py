import sqlite3

class Cursor:
    def __init__(self, cursor):
        self._cursor = cursor

    async def fetchone(self):
        return self._cursor.fetchone()

    async def fetchall(self):
        return self._cursor.fetchall()

    @property
    def description(self):
        return self._cursor.description

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        pass

class Connection:
    def __init__(self, conn):
        self._conn = conn

    @property
    def total_changes(self):
        return self._conn.total_changes

    async def execute(self, sql, params=()):
        cursor = self._conn.execute(sql, params)
        return Cursor(cursor)

    async def commit(self):
        self._conn.commit()

    async def close(self):
        self._conn.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.close()

async def connect(path):
    conn = sqlite3.connect(path)
    return Connection(conn)
