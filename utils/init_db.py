"""
init_db.py
2020/06/14 15:15
"""

from src.db import PgDB


def main():
    db = PgDB(user="s1recorder", password="This_is_your_pwd_understand?")
    db.create_tables()
    db.conn.close()


if __name__ == "__main__":
    main()
