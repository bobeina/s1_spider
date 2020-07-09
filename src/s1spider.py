"""
s1spider.py
2020 06/17 01:06
"""

import os
import argparse
from src.raw2db import RawToDB


def main(thread_id):
    spider = RawToDB()
    spider.init_db(user="s1recorder", password="RnaM379X62")

    parent_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    origin_url = "https://bbs.saraba1st.com/2b/forum-75-1.html"
    spider.init_spider(origin_url=origin_url, driver='geckodriver', headless=False)

    # thread_id = 1939205 # 疫情楼
    # thread_id = 1940086 # 风景区3
    # thread_id = 1941915  # 对喷屁股大战1

    # for thread_id in thread_id_list:
    # TODO 可能crawling模块需要重构为可以接受多个帖子id的模式
    spider.crawling(thread_id, usernm='暗金', pwd='6thparty')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--thread_id", help="The thread id that you want to crawl.")
    args = parser.parse_args()
    if args.thread_id:
        main(args.thread_id)
