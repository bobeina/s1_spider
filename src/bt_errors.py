"""
自定义错误
2020/05/09 17:55
"""


class LoadUIFailError(Exception):
    def __init__(self, error_info):
        super().__init__(self) #初始化父类
        self.error_info = error_info

    def __str__(self):
        return self.error_info
