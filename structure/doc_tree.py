import time
from typing import Any, Callable, Self, TypedDict, Unpack, Literal
# from typing import override
from .tree import Node, Tree
import sys


splitSign = Literal['\\']


def auto_update(func: Callable):
    def wrapper(cls: 'docTree', *args, **kwargs):
        result = func(cls, *args, **kwargs)
        cls.update()
        return result
    return wrapper


class metadata(TypedDict):
    create_time: str # 数据的创建时间
    modify_time: str # 数据的修改时间
    visit_time: str  # 数据的访问时间
    size: int # 数据大小

class dataArg(TypedDict):
    head: str | None # 数据的标头
    kind: Literal['title', 'table', 'image', 'text']
    content: str


class docArg(TypedDict):
    head: str # 文档的标头
    metadata: metadata # 元数据

class docNode(Node):
    
    def __init__(self, **data: Unpack[dataArg]) -> None:
        """
        文档节点
        - 构造
          - **data: dataArg, 文档节点具有的属性
            - kind: Literal['title', 'table', 'image', 'text'], 节点的种类，有三种字面量，默认值为'text'
            - content: str, 节点的文本内容
        - 属性\n
            继承自Node节点
        """
        # 默认值预处理
        data.setdefault('kind', 'text')

        super().__init__(**data)
        self.data: dataArg
        self._isTitle: bool = data['kind'] == 'title' # 是否是标题
        self._isTable: bool = data['kind'] == 'table' # 是否是表格
        self._isImage: bool = data['kind'] == 'image' # 是否是图像
        self._isText: bool = data['kind'] == 'text'   # 是否是图像
        self.__tree: 'docTree'

    def bind_tree(self, tree: 'docTree'):
        self.__tree = tree

    @property
    def tree(self) -> 'docTree':
        return self.__tree
    
    @property
    def children(self) -> list[Self]:
        return super().children

    @property
    def parent(self) -> Self:
        return super().parent

    @parent.setter
    def parent(self, node: 'docNode'):
        if not isinstance(node, type(self)):
            raise TypeError(f'期望：{type(self)}，实际：{type(node)}')
    
        if self._parent:
            self._parent.children.remove(self)

        self._parent = node
        self._parent.children.append(self)


    @property
    def isText(self) -> bool:
        "是否是正文节点"
        return self._isText
    
    @isText.setter
    def isText(self, value: bool):
        if not isinstance(value, bool):
            raise TypeError(f'期望：bool，实际：{type(value)}')
        
        self._isText = value


    @property
    def isTitle(self) -> bool:
        "是否是标题节点"
        return self._isTitle
    
    @isTitle.setter
    def isTitle(self, value: bool):
        if not isinstance(value, bool):
            raise TypeError(f'期望：bool，实际：{type(value)}')
        
        self._isTitle = value


    @property
    def isTable(self) -> bool:
        "是否是表格节点"
        return self._isTable
    
    @isTable.setter
    def isTable(self, value: bool):
        if not isinstance(value, bool):
            raise TypeError(f'期望：bool，实际：{type(value)}')
        
        self._isTable = value


    @property
    def isImage(self) -> bool:
        "是否是图像节点"
        return self._isImage
    
    @isImage.setter
    def isImage(self, value: bool):
        if not isinstance(value, bool):
            raise TypeError(f'期望：bool，实际：{type(value)}')
        
        self._isImage = value

    
    def __rshift__(self, other):
        if other is splitSign:
            return len(self.children) == 0

class docTree(Tree):

    def __init__(self, root: docNode, name: str = '文档树', **data: Unpack[docArg]) -> None:
        """
        文档树
        - 参数
         - 必选
          - root: docNode, 传入一个文档节点作为根节点。
         - 可选
          - name: str, 文档树的名称，用于查询。
        """
        data.setdefault('head', None)
        data.setdefault('metadata', {
            'create_time': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
            'modify_time': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
            'visit_time': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        })

        if not isinstance(root, docNode):
            raise TypeError(f'期望：docNode，实际：{type(root)}')
        
        super().__init__(root, name)
        self.data = data

    def update(self):
        self.data['metadata'].setdefault('size', sys.getsizeof(self.document))

    # @override
    def DFT(self, node=None, callback: Callable[[Node], bool] = lambda node: True) -> list[docNode] | None:
        return super().DFT(node, callback)
    
    # @override
    def BFT(self, callback: Callable[[Node], bool] = lambda node: True) -> list[docNode] | None:
        return super().BFT(callback)
    
    @auto_update
    def toMarkdown(self):
        from nodoc import Markdown
        document = Markdown()
        title_level = 1
        for node in self.DFT():
            content = node.data['content']
            if node.isTitle:
                document.add_title(content, title_level)

            if node.isImage:
                continue
                document.add_image(
                    url = content['url']
                )

            if node.isTable:
                continue
                document.add_table(
                    head = content['head'],
                    lines = content['lines']
                )

            if node.isText:
                document.add_text(content)

            title_level += 1
            if node >> splitSign:
                title_level = 1
                
        self.document = document
        return document
    
    @auto_update
    def toHtml(self):
        result = ''
        self.document = result

    def __str__(self):
        document = None
        if hasattr(self, 'document'):
            if len(self.document) <= 12:
                document = self.document.replace('\n', '')
            else:
                prefix = self.document[0:5].replace('\n', '')
                char_count = f'...({len(self.document) - 10}字)...'
                suffix = self.document[-6:-1].replace('\n', '')
                document = prefix + char_count + suffix
                
        size: list[int | list] = [self.data['metadata']['size'], ['B', 'KB', 'MB', 'GB', 'TB', 'PB']]
        while size[0] > 1024 and len(size[1]) > 1:
            size[0] /= 1024
            size[1].pop(0)
            
        result = f"""
{self.name}
- 创建时间：{self.data['metadata']['create_time']}
- 修改时间：{self.data['metadata']['modify_time']}
- 访问时间：{self.data['metadata']['visit_time']}
- 文档大小：{size[0]:.2f}{size[1][0]}
- 文档内容：{document}
"""
        return result