"""
main.py
启动图形界面
2020 06/16 17:53
"""
from multiprocessing import Process, Queue
import os, time, random
import json

import sys
# from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication
from PySide2.QtCore import QFile, QIODevice, Slot

from src.raw2db import RawToDB
from src.mainwindow import *


class MyInterFace:
    def __init__(self):
        self.root_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        UI_path = os.path.join(self.root_dir, 'UI')
        self.main_window = MainWindow(UI_path, 'mainwindow.ui')
        # self.main_window.create_sub_widgets()
        self.main_window.bind_events()
        # 爬虫初始化
        spider = RawToDB()
        spider.init_db(user="s1recorder", password="RnaM379X62")
        # 数据库初始化
        parent_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        origin_url = "https://bbs.saraba1st.com/2b/forum-75-1.html"
        spider.init_spider(origin_url=origin_url, driver='geckodriver', headless=False)
        self.main_window.get_db_and_spider_handles(spider)

    def init_threads(self):
        self.que = Queue()
        # p_msg_main = Process(target=self.main, args=(q,))
        self.p_msg_reciever = Process(target=self.message_reciver, args=(self.que,))
        # 启动子进程pw，写入:
        # p_msg_main.start()
        # 启动读取子进程:
        self.p_msg_reciever.start()
        # 等待pw结束:
        # p_msg_main.join()

    # def main(self):
    #     pass

    def message_send(self, msg):
        self.que.put(msg)

    def message_reciver(self, que):
        flag = True
        while flag:
            msg = que.get(True)
            # todo self.parse_msg(msg)
            cmd, params = self.parse_msg(msg)
            if cmd == 'STOP':
                flag = False

    def parse_msg(self, msg):
        data = json.loads(msg)
        return data['cmd'], data['params']

    def show_interface(self):
        self.main_window.handle.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    interface = MyInterFace()

    # print('window.children(): ', window.pushButton)
    # button = window.pushButton
    # button.clicked.connect(say_hello)

    # menus
    # menu1 = main_window.statusbar
    # menu1.addAction(say_hello)

    interface.show_interface()

    sys.exit(app.exec_())