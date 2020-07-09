"""
mainwindow
2020/06/16 17:57
"""
import os
import pathlib

from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile, QIODevice, Slot
from PySide2.QtGui import QStandardItemModel, QStandardItem

from src.ABSBTWidget import ABSBTWidget
from src.bt_errors import LoadUIFailError

# windows
# from source_path_window import SourcePathWindow
# from dir_fail import DirFailWindow


@Slot()
def debug_info():
    info = 'EVERYTHING IS OK'
    print(info)


class MainWindow(ABSBTWidget):
    """
    主窗口类
    """

    def other_init(self):
        pass

    def get_db_and_spider_handles(self, spider):
        self.spider = spider

    @Slot()
    def get_thread(self):
        self.handle.pushButton.setEnabled(False)
        try:
            self.handle.pushButton.clicked.disconnect()
        except:
            pass
        # print('get_thread() started')
        raw_thread_id = None
        try:
            # raw_thread_id = int(self.handle.lineEdit.text().encode('utf-8'))
            raw_thread_id = self.handle.lineEdit.text()#.encode('utf-8')
            usernm = self.handle.lineEditUser.text()#.encode('utf-8').strip()
            pwd = self.handle.lineEditPwd.text()#.encode('utf-8').strip()

            if raw_thread_id is not None and usernm is not None and pwd is not None:
                print('论坛 nick: ', usernm)
                print('论坛 pwd: ', pwd)
                print('论坛 thread: ', raw_thread_id)
                self.spider.crawling(raw_thread_id, usernm=usernm, pwd=pwd)
        except Exception as e:
            # todo alert box
            print(e)
            print('请输入正确的话题id数字/登录论坛的用户名/密码')
        self.handle.pushButton.setEnabled(True)
        self.handle.pushButton.clicked.connect(self.get_thread)

    def create_sub_widgets(self):
        pass

    def bind_events(self):
        if self.handle is None:
            raise LoadUIFailError("主窗口初始化失败！")
        # 从头爬
        self.get_thread_btn = self.handle.pushButton
        self.handle.pushButton.clicked.connect(self.get_thread)

        # todo