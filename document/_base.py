from typing import Literal, NewType, Self, Sequence, TypeAlias, TypeVar, TypedDict

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
    align: Literal['left', 'right', 'center', 'justify',
                   'middle', 'vertical', 'horizontal', 'top', 'bottom', 'top-left', 'top-right', 'bottom-left', 'bottom-right']
    padding: stylePadding | Sequence[int | str] | int | str
    margin: styleMargin | Sequence[int | str] | int | str

    "标题样式"
    title_level: int

    "字体通用样式"
    bold_level: int
    italic: bool
    underlined: bool
    color: styleColor
    hyperlink: str

    "图像通用样式"
    width: int | float | str
    height: int | float | str


class Message(TypedDict):
    head: str
    kind: Literal['title', 'table', 'image', 'text', 'LaTeX']
    style: Style
    content: Self | str | pd.DataFrame | list[Self]


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
    
document_type: TypeAlias = Literal[
        'markdown',
        'html',
        'pdf',
        'word',
        'ppt',
        'excel'
    ]