import os
import re
from .base import Document

END = '\n'
SPACE = '\x20'
TITLE_SIGN = '#'
REPLACE_FORMATTER = (
    (r'(\\)',  r'\\\1'),     # 转义\号
    (r'(\*)',  r'\\\1'),     # 转义*号
    (r'(\_)',  r'\\\1'),     # 转义_号
    (r'(\`)',  r'\\\1'),     # 转义`号
    (r'(\|)',  r'\\\1'),     # 转义|号
    (r'(!)',  r'\\\1'),      # 转义!号
    (r'(\[|\])',  r'\\\1'),  # 转义[]
    (r'(\(|\))',  r'\\\1'),  # 转义()
    (r'^(\x20*[0-9]+)(\.)(\x20)',  r'\1\\\2\3'),   # 有序列表
    (r'^(\x20*)(-|\*|\+)(\x20)',  r'\1\\\2\3'),    # 无序列表
    (r'^(\x20*)(#{1,6})(\x20)',  r'\1\\\2\3'),     # 标题
    (r'^(\x20*)(>)(.*)',  r'\1\\\2\3'),            # 引用
    (r'^(\x20*)(\*{3,}|-{3,}|_{3,})(\x20*)$',  r'\1\\\2\3'),  # 分隔线
    (r'^\s*$',  ''),
)

RECOGNIZE_FORMATTER = ()


class Markdown(Document):

    def __init__(self, data: str = "") -> None:
        message = self.normalize(data)
        super().__init__(message, data)

    @classmethod
    def escape(cls, text: str):
        """
        转义文本
        - text: str, 待转义文本
        """
        for pattern, repl in REPLACE_FORMATTER:
            text = re.sub(pattern, repl, text, flags=re.M)
        return text

    def last_line(self):
        "切换到上一行"
        self.data >> END

    def next_line(self):
        "切换到下一行"
        self.data << END

    def add_title(self, text: str, level: int):
        self.data << TITLE_SIGN * level << SPACE << text << END

    def add_text(self, text: str):
        text = self.escape(text)
        self.data << text

    def normalize(self):
        ...

    def export(self, name: str, directory: str = './'):
        directory = os.path.abspath(directory)
        with open(directory + '/' + name + '.md', 'w+', encoding='utf-8') as file:
            file.write(self.__str__())
            

    @staticmethod
    def load(path: str) -> 'Markdown':
        with open(path, 'r+', encoding='utf-8') as file:
            text = file.read()
        return Markdown(text)

            
    def __document__(self):
        ...