"""
db.py
2020 06/06 22:11

数据草稿：
rvalue = {
    # 'thread_id': thread_id,
    'post_id': post_id,
    'floor': floor,
    'post_title': post_title,
    'raw_content': raw_content,
    'author_id': author_id,
    'author': author_nick,
    'post_time': post_time,
    'editor_nick': editor_nick,
    'edited_time': edited_time,
    'scores': scores
}
"""

import psycopg2
import datetime


# def check_param(func):
#     def wrapper(*args, **kw):
#     # params, param_format_list
#         if len(params) != len(param_format_list):
#             return False
#         for i, param in enumarate(params):
#             if type(param) != param_format_list[i]:
#                 return False
#         return True
#     return decorator


class PgDB:
    def __init__(self,
                 database="s1_raw_doc",
                 user=None,
                 password=None,
                 host="localhost",
                 port="5432"):
        if user is None or password is None:
            raise RuntimeError("出错：未提供数据库用户名/密码。")
        self.conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
        self.cursor = self.conn.cursor()

    def create_tables(self):
        """
        建表：post/score/author -> 主帖、分数、发帖人
        TODO 加try...except
        """
        self.cursor.execute("CREATE TABLE raw_post(" +
                            "id serial primary key, " +
                            "thread_id int, " +
                            "post_id int, " +
                            "floor int, " +
                            "post_title varchar(80), " +
                            "raw_content text, " +
                            "author_id int, " +
                            "author varchar(16),"
                            "post_time varchar(20), " +
                            "editor_nick varchar(16), " +
                            "edited_time varchar(20)," +
                            "date timestamp" +
                            ");")
        # ['战斗力 -1 鹅', '活久见', '2019-9-30 11:47', '', uid]
        self.cursor.execute("CREATE TABLE raw_score(" +
                            "id serial primary key, " +
                            "post_id int, " +
                            "score varchar(48), " +
                            "author varchar(18), " +
                            "score_time varchar(20), " +
                            "note varchar(48), " +
                            "author_id varchar(12)" +
                            ");")
        # 精华 战斗力 帖子 积分 权限 注册时间
        self.cursor.execute("CREATE TABLE raw_author_info(" +
                            "id serial primary key, " +
                            "author_id int UNIQUE, " +
                            "author varchar(16), " +
                            "excellent_articles int, " +
                            "power int, " +
                            "post_num int, " +
                            "exp int, " +
                            "reg_time  varchar(20), " +
                            "date timestamp" +
                            ");")
        # 待考虑添加话题信息：tag等
        # self.cursor.execute("CREATE TABLE thread_info(" +
        #                     "id bigint, " +
        #                     "thread_id varchar(12), " +
        #                     "thread_title varchar(80), " +
        #                     ");")
        self.conn.commit()

    def drop_tables(self):
        self.cursor.execute("DROP TABLE raw_post;")
        self.cursor.execute("DROP TABLE score;")
        self.cursor.execute("DROP TABLE user_info;")
        # self.cursor.execute("DROP TABLE thread_info;")

    # @check_param
    def insert_raw_post(self, data):
        """注意：请自己调用 self.conn.commit()"""
        sql_str = "INSERT INTO raw_post(" + \
                  "thread_id, " + \
                  "post_id, " + \
                  "floor, " + \
                  "post_title, " + \
                  "raw_content, " + \
                  "author_id, " + \
                  "author, " + \
                  "post_time, " + \
                  "editor_nick, " + \
                  "edited_time, " + \
                  "date" + \
                  ") VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
        self.cursor.execute(sql_str, data)

    def insert_score(self, data):
        sql_str = "INSERT INTO raw_score(" + \
                  "post_id, " + \
                  "score, " + \
                  "author, " + \
                  "score_time, " + \
                  "note, " + \
                  "author_id " + \
                  ") VALUES (%s,%s,%s,%s,%s,%s);"

        # print('insert_score() sql_str = ', sql_str, end='')
        # print(' data:', data)
        
        self.cursor.execute(sql_str, data)

    def insert_author(self, data):
        # sql_str = "INSERT INTO raw_author_info(" + \
        #           "author_id, " + \
        #           "author, " + \
        #           "excellent_articles, " + \
        #           "power, " + \
        #           "author_id, " + \
        #           "post_num, " + \
        #           "exp, " + \
        #           "reg_time, " + \
        #           ")VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"

        # sql_str = "INSERT INTO raw_author_info(" + \
        #           "author_id, " + \
        #           "author" + \
        #           ") VALUES (%s,%s);"
        sql_str = "INSERT INTO raw_author_info (author_id, author) VALUES (%s,%s) ON CONFLICT (author_id) DO NOTHING"
        self.cursor.execute(sql_str, data)

    def get_thread_posts_num(self, thread_id):
        sql_str = "SELECT COUNT(*) FROM (SELECT DISTINCT post_id FROM raw_post WHERE thread_id=%s) AS temp;"
        self.cursor.execute(sql_str, (thread_id,))
        result = self.cursor.fetchone()
        print('get_thread_posts_num() result: ', result)
        return result[0]

    def get_last_post_id(self, thread_id):
        sql_str = "SELECT MAX(post_id) FROM raw_post WHERE thread_id=%s" # AS temp;"
        self.cursor.execute(sql_str, (thread_id,))
        result = self.cursor.fetchone()
        print('get_last_post_id() result: ', result)
        return result[0]

    def del_raw_post(self):
        pass

    def del_score(self):
        pass

    def del_author(self):
        pass

    # select
    def find_raw_post(self):
        pass

    def find_score(self):
        pass

    def find_author(self):
        pass

    # update
    def update_raw_post(self):
        pass

    def update_score(self):
        pass

    def update_author(self):
        pass

    def load_thread_list(self, offset=0, num=20):
        # sql_str = "SELECT DISTINCT id,thread_id,post_title,author " +\
        #           "FROM raw_post " + \
        #           "LIMIT %s OFFSET %s"

        # sql_str = "SELECT min(id),thread_id,post_title,author " +\
        #           "FROM raw_post " + \
        #           "GROUP BY thread_id, post_title, author " + \
        #           "LIMIT %s OFFSET %s;"

        # sql_str = "SELECT id, thread_id,post_title,author FROM raw_post " + \
        #           "WHERE id=(SELECT min(id) FROM raw_post GROUP BY thread_id) " + \
        #           "LIMIT %s OFFSET %s;"
        # self.cursor.execute(sql_str, (num, offset,))

        # SELECT brand, size, sum(sales) FROM items_sold GROUP BY GROUPING SETS ((brand), (size), ());

        sql_str = "SELECT id, thread_id, post_title, author " + \
                  "FROM raw_post " + \
                  "WHERE id IN " + \
                  "(SELECT min(id) FROM raw_post GROUP BY thread_id) " + \
                  "LIMIT %s OFFSET %s;"
        self.cursor.execute(sql_str, (num, offset,))
        # result = self.cursor.fetchone()
        result = self.cursor.fetchall()
        print('load_contents() result: ', result)
        return result

