import asyncpg
from typing import Union
from asyncpg import Connection
from asyncpg.pool import Pool
from data import config
class Database:
    def __init__(self):
        self.pool: Union[Pool, None] = None
    async def create(self):
        self.pool = await asyncpg.create_pool(
            host=config.DB_HOST,
            user=config.DB_USER,
            password=config.DB_PASS,
            database=config.DB_NAME
        )
    async def execute(self, sql_command, *args,
                      fatch: bool=False,
                      fetchrows: bool=False,
                      execute: bool=False,
                      fetchvall: bool=False
                      ):
        async with self.pool.acquire() as connection:
            connection: Connection
            if fatch:
                result = await connection.fetch(sql_command, *args)
            elif fetchrows:
                result = await connection.fetchrow(sql_command, *args)
            elif fetchvall:
                result = await connection.fetchval(sql_command, *args)
            elif execute:
                result = await connection.execute(sql_command, *args)
            return result

    @staticmethod
    def format_kwargs(sql_command, parameters: dict):
        sql_command += " AND ".join([f"{key}='{value}'" for key, value in parameters.items()])
        return sql_command

    async def create_table_users(self):
        sql = """
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                fullname VARCHAR(255) NOT NULL,
                telegram_id BIGINT NOT NULL UNIQUE
                )
        """
        return await self.execute(sql, execute=True)

    async def create_table_taxsis(self):
        sql = """
            CREATE TABLE IF NOT EXISTS taxsis (
                viloyatdan VARCHAR(255) NOT NULL,
                tumandan VARCHAR(255) NOT NULL,
                viloyatga VARCHAR(255) NOT NULL,
                tumanga VARCHAR(255) NOT NULL,
                mashina VARCHAR(255) NOT NULL,
                tel_nomer VARCHAR(255) NOT NULL,
                yurish_vaqti TIME NOT NULL,
                telegram_id BIGINT NOT NULL UNIQUE
                )
        """
        return await self.execute(sql, execute=True)
    async def create_table_yolovchi(self):
        sql = """
            CREATE TABLE IF NOT EXISTS yolovchi (
                viloyatdan VARCHAR(255) NOT NULL,
                tumandan VARCHAR(255) NOT NULL,
                viloyatga VARCHAR(255) NOT NULL,
                tumanga VARCHAR(255) NOT NULL,
                tel_nomer VARCHAR(255) NOT NULL,
                yurish_vaqti TIME NOT NULL,
                telegram_id BIGINT NOT NULL UNIQUE
                )
        """
        return await self.execute(sql, execute=True)

    async def add_user(self, fullname: str, telegram_id: int):
        sql = "INSERT INTO users (fullname, telegram_id) VALUES ($1, $2)"
        return await self.execute(sql, fullname, telegram_id, execute=True)

    async def add_taxi(self, viloyatdan: str, tumandan: str, viloyatga: str,
                       tumanga: str, mashina: str, tel_nomer: str,
                       yurish_vaqti: str, telegram_id: int):
        sql = ("INSERT INTO taxsis (viloyatdan, tumandan, viloyatga, tumanga, mashina,"
               " tel_nomer, yurish_vaqti, telegram_id) VALUES ($1, $2, $3, $4, $5, $6, $7, $8)")
        return await self.execute(sql, viloyatdan, tumandan, viloyatga, tumanga,
                                  mashina, tel_nomer, yurish_vaqti, telegram_id, execute=True)
    async def add_yolovchi(self, viloyatdan: str, tumandan: str, viloyatga: str,
                       tumanga: str, tel_nomer: str,
                       yurish_vaqti: str, telegram_id: int):
        sql = ("INSERT INTO yolovchi (viloyatdan, tumandan, viloyatga, tumanga, tel_nomer,"
               " yurish_vaqti, telegram_id) VALUES ($1, $2, $3, $4, $5, $6, $7)")
        return await self.execute(sql, viloyatdan, tumandan, viloyatga, tumanga,
                                  tel_nomer, yurish_vaqti, telegram_id, execute=True)
    async def select_all_table(self, table):
        sql = f"""SELECT * FROM {table}"""
        return await self.execute(sql, fatch=True)

    async def search_column(self, table, **kwargs):
        sql = f"""SELECT * FROM {table} WHERE """
        sql = self.format_kwargs(sql, kwargs)
        return await self.execute(sql, fatch=True)

    async def search_taxsis(self,**kwargs):
        sql = f"""SELECT * FROM taxsis WHERE viloyatdan=$1 AND tumandan=$2 """


    async def get_count(self, table):
        sql = f"""SELECT COUNT(*) FROM $1"""
        return await self.execute(sql,table, fetchvall=True)

    async def delete_user(self, table, telegram_id):
        sql = f"""DELETE FROM {table} WHERE telegram_id = $1"""
        return await self.execute(sql, telegram_id, execute=True)

    async def delete_all_users(self, table):
        sql = f"""
        DELETE FROM {table}
        """
        return await self.execute(sql, execute=True)
    async def drop_table(self, teble):
        sql = f"""
        DROP TABLE IF EXISTS {teble}
        """
        return await self.execute(sql, execute=True)