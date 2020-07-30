"""
raw2db.py
整理info_extractor获取到的数据并分别存放到各个草表中
2020/06/14 13:04
"""
import os
import time
import datetime
from info_extractor import S1PostsInfoExtractor
from db import PgDB


class RawToDB:
    def __init__(self):
        self.extractor = None
        self.pgdb = None

    def init_spider(self,
                    origin_url=None,
                    driver_path=None,
                    driver=None,
                    user_agent_str=None,
                    headless=True):
        """爬虫初始化"""
        print('RawToDB.init_spider() driver_path: ', driver_path)
        self.extractor = S1PostsInfoExtractor(
            origin_url=origin_url,
            driver_path=driver_path,
            driver=driver,
            user_agent_str=user_agent_str,
            headless=headless
        )
        self.init_website_with_cookie()

    def init_db(self,
                database="s1_raw_doc",
                user=None,
                password=None,
                host="localhost",
                port="5432"):
        """数据库初始化"""
        self.pgdb = PgDB(
            database=database,
            user=user,
            password=password,
            host=host,
            port=port
        )

    def init_website_with_cookie(self):
        self.parent_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        cookie_name = 'saraba1st.com.firefox.77.0.1.json'
        cookie_file = os.path.join(self.parent_dir, 'cookies', cookie_name)
        self.extractor.load_cookies_from_file(cookie_file)

    def format_data(self, raw_post):
        """解析帖子，拆分成三个数据包"""
        t = str(datetime.datetime.now())
        post = (int(raw_post["thread_id"]),
                raw_post["post_id"],
                raw_post["floor"],
                raw_post["post_title"],
                raw_post["raw_content"],
                raw_post["author_id"],
                raw_post["author"],
                raw_post["post_time"],
                raw_post["editor_nick"],
                raw_post["edited_time"],
                datetime.datetime.strptime(t, '%Y-%m-%d %H:%M:%S.%f'))
        scores = raw_post["scores"]
        author_info = (raw_post["author_id"], raw_post["author"])
        return post, scores, author_info

    # thread_id = '793032'  # 置顶帖
    def crawling(self, thread_id, usernm=None, pwd=None, continue_flag=False):
        print('RawToDB.crawling() start')
        if usernm is None or pwd is None:
            print('Please set an account with pwd for crawling.')
            return False
        if self.extractor is None:
            self.init_website_with_cookie()
        time.sleep(3)
        if not self.extractor.is_login():
            self.extractor.auto_login(usernm=usernm, pwd=pwd)
        time.sleep(1)
        counter = 0
        if continue_flag:
            post_num = self.pgdb.get_thread_posts_num(thread_id)
            little_tail = post_num % 30
            page = int(post_num / 30) +1
            if little_tail == 0:
                page += 1
            last_post_id = self.pgdb.get_last_post_id(thread_id) #, post_num, page)

            gen_func = self.extractor.continue_thread(thread_id, last_post_id, page)
            # 从数据库中获取该帖总数
        else:
            gen_func = self.extractor.parse_thread(thread_id)
        for page in gen_func:
            print('counter: ', counter)
            for raw_post in page:
                counter += 1
                post, scores, author_info = self.format_data(raw_post)
                self.pgdb.insert_raw_post(post)
                self.pgdb.insert_author(author_info)
                for score in scores:
                    score_data = tuple([(raw_post['post_id'])] + list(score))
                    self.pgdb.insert_score(score_data)
        self.pgdb.conn.commit()
        print('{n} post(s) total inserted.'.format(n=counter))
