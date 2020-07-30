"""
main.py
启动图形界面
2020 06/16 17:53
"""
from multiprocessing import Process, Queue
import json

import os
import sys
# from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication
from PySide2.QtCore import QFile, QIODevice, Slot

from raw2db import RawToDB
from mainwindow import *
from load_cfg import load_cfg


class MyInterFace:
    def __init__(self):
        self.root_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        UI_path = os.path.join(self.root_dir, 'UI')
        self.main_window = MainWindow(UI_path, 'mainwindow.ui')
        # self.main_window.create_sub_widgets()
        self.main_window.bind_events()
        # 爬虫初始化
        #读取测试用的s1用户名
        # s1_account_cfg = load_cfg('s1_account.ini')
        # if len(s1_account_cfg) == 0 or 'user' not in s1_account_cfg or 'pwd' not in s1_account_cfg:
        #     username = input("Please input your username for s1: ")
        #     pwd = input("Please input your pwd for s1: ")
        #     if len(username) == 0 or len(pwd) == 0:
        #         return
        # else:
        #     username = s1_account_cfg['user']
        #     pwd = s1_account_cfg['pwd']

        # 读取爬引擎及数据库相关信息
        config_file = 'config.ini'
        cfg = load_cfg(config_file)
        if len(cfg) == 0:
            print("唉你说的这个文件 {file} 有点问题啊……".format(file=config_file))
            return
        spider = RawToDB()
        spider.init_db(user=cfg['pgdb_user'], password=cfg['pgdb_pwd'])
        # 数据库初始化
        spider.init_spider(origin_url=cfg['start_page'],
                           driver_path=cfg['driver_path'],
                           driver=cfg['driver'],
                           user_agent_str=cfg['user_agent_str'],
                           headless=False)
        self.main_window.get_db_and_spider_handles(spider)
        account = load_cfg('s1_account.ini')
        if len(account) > 0:
            self.main_window.auto_fill_user_info(account['user'], account['pwd'])

    def init_threads(self):
        # todo 施工中，待修改为多进程版本——界面不单开进程会卡住，目前先凑合 2020/07/10
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