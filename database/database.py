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
        self.__export_pattern = re.compile(r'([0-9]|[a-z]|[A-Z]|_)+', re.UNICODE)

    @abc.abstractmethod
    def export(self, name: str, directory: str = './'):
        if not self.__export_pattern.match(name):
            raise ValueError('Database names: combination of "0~9", "a~z", "A~Z" and "_."')
        
        directory = os.path.abspath(directory) + '\\' # 预处理目录
        with open(directory + name + '.nodocdb', 'wb+') as file:
            pickle.dump(self, file)

    @abc.abstractmethod
    def load(self, name: str, directory: str = './'):
        if not self.__export_pattern.match(name):
            raise ValueError('Database names: combination of "0~9", "a~z", "A~Z" and "_."')
        
        directory = os.path.abspath(directory) + '\\' # 预处理目录
        with open(directory + name + '.nodocdb', 'rb+') as file:
            self = pickle.load(self, file)

    @abc.abstractproperty
    @property
    def data(self):
        return self._data