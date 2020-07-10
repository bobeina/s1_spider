"""
main_cmd.py
2020 06/17 01:06
"""

import os
import argparse
from src.raw2db import RawToDB
from src.load_cfg import load_cfg


def main(thread_id):
    s1_account_cfg = load_cfg('s1_account.ini')
    if len(s1_account_cfg) == 0 or 'user' not in s1_account_cfg or 'pwd' not in s1_account_cfg:
        username = input("Please input your username for s1: ")
        pwd = input("Please input your pwd for s1: ")
        if len(username) == 0 or len(pwd) == 0:
            return
    else:
        username = s1_account_cfg['user']
        pwd = s1_account_cfg['pwd']

    config_file = 'config.ini'
    cfg = load_cfg(config_file)
    if len(cfg) == 0:
        print("唉你说的这个文件 {file} 有点问题啊……".format(file=config_file))
        return
    spider = RawToDB()
    spider.init_db(user=cfg['pgdb_user'], password=cfg['pgdb_pwd'])

    parent_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    spider.init_spider(origin_url=cfg['start_page'],
                       driver_path=cfg['driver_path'],
                       driver=cfg['driver'],
                       user_agent_str=cfg['user_agent_str'],
                       headless=False)

    # thread_id = 1939205 # 疫情楼
    # thread_id = 1940086 # 风景区3
    # thread_id = 1941915  # 对喷屁股大战1

    # for thread_id in thread_id_list:
    # TODO 可能crawling模块需要重构为可以接受多个帖子id的模式
    spider.crawling(thread_id, usernm=username, pwd=pwd)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--thread_id",
                        help="-t --thread_id: The thread id that you want to crawl.\n -s --start: The page you want to start.")
    args = parser.parse_args()
    if args.thread_id:
        main(args.thread_id)
