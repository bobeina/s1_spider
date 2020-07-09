"""
init_db.py
2020/06/14 15:15
"""

from src.db import PgDB


def main():
    db = PgDB(user="s1recorder", password="RnaM379X62")
    db.create_tables()
    db.conn.close()


if __name__ == "__main__":
    main()
