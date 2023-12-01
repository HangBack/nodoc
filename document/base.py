import abc


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
        self.__data: Data = Data(data)

    @property
    def data(self) -> Data:
        return self.__data

    def __lshift__(self, other):
        return self.__data << other

    def __str__(self) -> str:
        return self.__data.content