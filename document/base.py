import abc
from typing import Literal, Self
from ._base import document_type
from ._base import Message
from ._base import Data

import pandas as pd



class Document(metaclass=abc.ABCMeta):

    def __init__(self, data: str = "") -> None:
        self.__message: Message = self.normalize()
        self.__data: Data = Data(data)

    @property
    def data(self) -> Data:
        return self.__data

    @property
    def content(self) -> str:
        return self.__data.content

    @property
    def message(self) -> Data:
        return self.__message

    @abc.abstractmethod
    def __document__(self):
        ...

    @abc.abstractmethod
    def normalize(self) -> Message:
        "文档标准化为消息。"

    @abc.abstractmethod
    def export(self, name: str, directory: str = './'):
        "文档的导出方法。"

    @abc.abstractstaticmethod
    def load(path: str) -> 'Document':
        "文档的导入方法。"

    @abc.abstractstaticmethod
    def load_from_message(message: Message) -> Self:
        """
        从消息中加载markdown。
        - message: Message, 传入的消息。
        """

    @staticmethod
    def transform(source: 'Document', to: document_type) -> 'Document':

        match to:
            case 'markdown':
                from . import Markdown
                return Markdown.transform(source)
            case 'html':
                from . import Html
                return Html.transform(source)
            case 'pdf':
                from . import PDF
                return PDF.transform(source)
            case 'word':
                from . import Word
                return Word.transform(source)
            case 'ppt':
                from . import PPT
                return PPT.transform(source)
            case 'excel':
                from . import Excel
                return Excel.transform(source)

    def __lshift__(self, other):
        return self.__data << other

    def __str__(self) -> str:
        return self.__data.content
