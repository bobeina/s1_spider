"""
一个控件基类，用于从 .ui 文件中读取各窗口控件信息
"""
import os
import abc
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile, QIODevice, Slot


class ABSBTWidget(object):
    """
    若初始化成功则 handle 不为 None
    """

    __metaclass__ = abc.ABCMeta

    def __init__(self, path, ui_name):
        self.handle = None
        self.data_mode = None
        # self.table_view = None

        ui_file_name = os.path.join(path, ui_name)
        ui_file = QFile(ui_file_name)
        if not ui_file.open(QIODevice.ReadOnly):
            print("Cannot open {}: {}".format(ui_file_name, ui_file.errorString()))
            return
        loader = QUiLoader()
        self.handle = loader.load(ui_file)
        ui_file.close()
        if not self.handle:
            print(loader.errorString())
            return
        self.create_sub_widgets()
        self.bind_events()
        self.other_init()

    @abc.abstractmethod
    def create_sub_widgets(self):
        """Create sub widgets"""
        pass

    @abc.abstractmethod
    def bind_events(self):
        """
        Bind events to widgets and sub-components
        注意：此处只绑定不涉及到上一级或其它对话框的控件事件；较复杂的事件应放到上一级或更高级的父窗口中处理
       :return:
        """
        pass

    @abc.abstractmethod
    # def other_init(self, *args, **kwargs):
    def other_init(self):
        """其它需要初始化的东西"""
        pass