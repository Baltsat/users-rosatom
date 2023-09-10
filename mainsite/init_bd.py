import psycopg2
import os
from dotenv import load_dotenv
load_dotenv()


def create_bd(DB_NAME=os.getenv("DB_NAME"), DB_ADMIN_PASSWORD=os.getenv("DB_ADMIN_PASSWORD")):

    conn = psycopg.connect(
        host="localhost",
        dbname="postgres",
        user="postgres",
        password=DB_ADMIN_PASSWORD
    )
    cursor = conn.cursor()

    # Обратите внимание, что для выражения "CREATE DATABASE" необходимо установить автокоммит
    # Благодаря этому команда SQL, во-первых, выполняется немедленно.
    # А во-вторых, выполняется вне транзакции
    # (выражение "CREATE DATABASE" должно выполняться именно вне транзакции)
    conn.autocommit = True

    # Запрос для создания новой базы данных "confDB"
    create_db_query = f'CREATE DATABASE "{DB_NAME}";'

    # выполняем код sql
    cursor.execute(create_db_query)

    cursor.close()
    conn.close()


if __name__ == '__main__':
    create_bd()

