"""
init_db.py
2020/06/14 15:15
"""
from src.db import PgDB
from src.load_cfg import load_cfg


def main():
    config_file = 'config.ini'
    cfg = load_cfg(config_file)
    if len(cfg) == 0:
        print("唉你说的这个文件 {file} 有点问题啊……".format(file=config_file))
        return
    db = PgDB(user=cfg['pgdb_user'], password=cfg['pgdb_pwd'])
    db.create_tables()
    db.conn.close()


if __name__ == "__main__":
    main()
