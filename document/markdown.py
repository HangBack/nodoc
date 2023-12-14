import os
import re
from typing import Self
from .base import Data, Document, Message
# Use a pipeline as a high-level helper
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
        super().__init__(data)

    def escape(text: str):
        """
        转义文本
        - text: str, 待转义文本
        """
        if isinstance(text, Markdown):
            text = text.content
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

    def normalize(self) -> Message:
        ...

    def export(self, name: str, directory: str = './'):
        directory = os.path.abspath(directory)
        with open(directory + '/' + name + '.md', 'w+', encoding='utf-8') as file:
            file.write(self.__str__())

    @staticmethod
    def transform(source: Document) -> 'Markdown':
        document = Markdown.load_from_message(source.message)
        return document
    
    def load_from_message(message: Message | list[Message]) -> Self:
        """
        从消息中加载markdown。
        - message: Message, 传入的消息。
        """
        document = Markdown()
        def recur(message: Message | list[Message]):
            content = message['content']
            if isinstance(content, Message):
                text = recur(content)
            elif isinstance(content, list):
                text = []
                for span in content:
                    text.append(recur(span))
                text = "".join(text)
            match message['kind']:
                case 'title':
                    document.add_title(text)
                case 'image':
                    document.add_image(text)
                case 'LaTeX':
                    document.add_latex(text)
                case 'table':
                    document.add_table(text)
                case 'text':
                    document.add_text(text)
        recur(message)
        return document

    @staticmethod
    def load(path: str) -> 'Markdown':
        with open(path, 'r+', encoding='utf-8') as file:
            text = file.read()
        return Markdown(text)

            
    def __document__(self):
        ...