"""
mainwindow
2020/06/16 17:57
"""
import os
import pathlib

from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile, QIODevice, Slot
from PySide2.QtGui import QStandardItemModel, QStandardItem

from ABSBTWidget import ABSBTWidget
from bt_errors import LoadUIFailError

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
        try:
            raw_thread_id = self.handle.lineEdit.text()
            usernm = self.handle.lineEditUser.text()
            pwd = self.handle.lineEditPwd.text()

            if raw_thread_id is not None and usernm is not None and pwd is not None:
                # print('论坛 nick: ', usernm)
                # print('论坛 pwd: ', pwd)
                print('论坛 thread: ', raw_thread_id)
                self.spider.crawling(raw_thread_id, usernm=usernm, pwd=pwd)
        except Exception as e:
            # todo alert box
            # todo 待处理用户名密码不对的问题 print('请输入正确的话题id数字/登录论坛的用户名/密码')
            raise e
        self.handle.pushButton.setEnabled(True)
        self.handle.pushButton.clicked.connect(self.get_thread)

    @Slot()
    def renew_thread(self):
        self.handle.pushButton.setEnabled(False)
        try:
            self.handle.pushButton.clicked.disconnect()
        except Exception as e:
            pass
        try:
            raw_thread_id = self.handle.lineEdit_renew_id.text()
            usernm = self.handle.lineEditUser.text()
            pwd = self.handle.lineEditPwd.text()
            if raw_thread_id is not None and usernm is not None and pwd is not None:
                self.spider.crawling(raw_thread_id, usernm=usernm, pwd=pwd, continue_flag=True)
        except Exception as e:
            # todo alert box
            # todo 待处理用户名密码不对的问题 print('请输入正确的话题id数字/登录论坛的用户名/密码')
            raise e
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
        # 从帖子中间继续爬
        self.handle.pushButtonRenewByID.clicked.connect(self.renew_thread)

        # todo

    def auto_fill_user_info(self, user, pwd):
        self.handle.lineEditUser.setText(user)
        self.handle.lineEditPwd.setText(pwd)