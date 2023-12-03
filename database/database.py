import os
import re
import abc
import pickle
from typing import Any, Self, TypeAlias


def __import():
    global Node, Tree
    from nodoc import Node
    from nodoc import Tree

_Forest: TypeAlias = list['Tree']

class dataBase(metaclass=abc.ABCMeta):

    def __init__(self) -> None:
        self._data: Any
        self.__path: str = ""

    @abc.abstractmethod
    def export(self, name: str, directory: str = './'):
        """
        将数据库导出到对应的路径。
        - name: str, 数据库的导出名称（只能是数字、字母和下划线的组合）。
        - directory: str = './', 数据库的导出目录。
        """
        export_pattern = re.compile(r'([0-9]|[a-z]|[A-Z]|_)+', re.UNICODE)
        if not export_pattern.match(name):
            raise ValueError('Database names: combination of "0~9", "a~z", "A~Z" and "_."')
        
        directory = os.path.abspath(directory) + '\\' # 预处理目录
        with open(directory + name + '.nodocdb', 'wb+') as file:
            pickle.dump(self, file)

    @abc.abstractstaticmethod
    def load(path: str) -> Self:
        """
        将数据库从磁盘载入内存。
        - path: str, 数据库的导入路径。
        """
        with open(path, 'rb+') as file:
            return pickle.load(file)

    @abc.abstractmethod
    def save(self) -> None:
        """
        保存数据库（注：必须是由load方法载入的数据库才能使用save方法）
        """
        if self.__path == "":
            raise AttributeError("数据库从未存储至磁盘。")
        path = os.path.abspath(self.__path)
        path = os.path.splitdrive(path)
        directory = path[0]
        file = path[1]
        name = os.path.splitext(file)[0]
        self.export(name, directory)

    @abc.abstractproperty
    @property
    def data(self) -> Any:
        """数据库的信息"""
        return self._data