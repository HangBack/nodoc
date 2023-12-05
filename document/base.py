import abc
from typing import Literal, Self, Sequence, TypedDict

import pandas as pd


class stylePadding(TypedDict):
    top: int | str
    bottom: int | str
    left: int | str
    right: int | str


class styleMargin(TypedDict):
    top: int | str
    bottom: int | str
    left: int | str
    right: int | str


class styleColor(TypedDict):
    "rgba"
    r: int | float
    red: int | float
    g: int | float
    green: int | float
    b: int | float
    blue: int | float
    a: int | float
    alpha: int | float

    "hsva"
    h: int | float
    hue: int | float
    s: int | float
    saturation: int | float
    v: int | float
    value: int | float
    a: int | float
    alpha: int | float

    "hsla"
    h: int | float
    hue: int | float
    s: int | float
    saturation: int | float
    l: int | float
    lightless: int | float
    a: int | float
    alpha: int | float


class Style(TypedDict):
    kind: Literal['title', 'table', 'image', 'text']

    "通用样式"
    box_width: int | float | str
    box_height: int | float | str

    "标题样式"
    title_level: int

    "字体通用样式"
    bold_level: int
    italic: bool
    underlined: bool
    color: styleColor
    align: Literal['left', 'right', 'center', 'justify',
                   'middle', 'vertical', 'horizontal', 'top', 'bottom', 'top-left', 'top-right', 'bottom-left', 'bottom-right']
    padding: stylePadding | Sequence[int, str] | int | str
    margin: styleMargin | Sequence[int, str] | int | str
    hyperlink: str

    "图像通用样式"
    width: int | float | str
    height: int | float | str


class Message(TypedDict):
    head: str
    kind: Literal['title', 'table', 'image', 'text', 'LaTeX']
    style: Style
    content: 'Message' | str | pd.DataFrame | list['Message']


class Data:

    def __init__(self, content: str = "") -> None:
        if not isinstance(content, str):
            raise ValueError(f"期望：str，实际：{type(content)}")
        self.__content: str = content

    @property
    def content(self) -> str:
        return self.__content

    def __lshift__(self, other):
        if isinstance(other, str):
            self.__content = self.__content + other

        return self

    def __str__(self) -> str:
        return self.__content


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
    def transform(source: 'Document', to: Literal[
        'markdown',
        'html',
        'pdf',
        'word',
        'ppt',
        'excel'
    ]) -> 'Document':

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
