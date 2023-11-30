import os
import re
import abc
import pickle
from typing import TypeAlias


def __import():
    global Node, Tree
    from nodoc import Node
    from nodoc import Tree

_Nodes: TypeAlias = list['Node']
_Forest: TypeAlias = list['Tree']

class dataBase(metaclass=abc.ABCMeta):

    def __init__(self) -> None:
        self._data: _Nodes = []
        self.__path: str = ""

    @abc.abstractmethod
    def export(self, name: str, directory: str = './'):
        export_pattern = re.compile(r'([0-9]|[a-z]|[A-Z]|_)+', re.UNICODE)
        if not export_pattern.match(name):
            raise ValueError('Database names: combination of "0~9", "a~z", "A~Z" and "_."')
        
        directory = os.path.abspath(directory) + '\\' # 预处理目录
        with open(directory + name + '.nodocdb', 'wb+') as file:
            pickle.dump(self, file)

    @abc.abstractstaticmethod
    def load(path: str):
        with open(path, 'rb+') as file:
            return pickle.load(file)

    @abc.abstractmethod
    def save(self):
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
    def data(self):
        return self._data