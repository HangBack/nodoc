import time
from typing import Any, Callable, Self, TypedDict, Unpack, Literal
from nodoc import const

from nodoc.document.base import Document
from .tree import Node, Nodes, Tree
import sys


splitSign = Literal['\\']


def auto_update(func: Callable):
    def wrapper(cls: 'docTree', *args, **kwargs):
        result = func(cls, *args, **kwargs)
        cls.update()
        return result
    return wrapper


class metadata(TypedDict):
    create_time: str  # 数据的创建时间
    modify_time: str  # 数据的修改时间
    visit_time: str   # 数据的访问时间
    size: int         # 数据大小


class dataArg(TypedDict):
    head: str | None  # 数据的标头
    kind: Literal['title', 'table', 'image', 'text']
    content: str


class docArg(TypedDict):
    head: str           # 文档的标头
    metadata: metadata  # 元数据


class docNode(Node):

    def __init__(self, **data: Unpack[dataArg]) -> None:
        """
        文档节点
          - **data: dataArg, 文档节点具有的属性
            - kind: Literal['title', 'table', 'image', 'text'], 节点的种类，有三种字面量，默认值为'text'
            - content: str, 节点的文本内容
        - 属性\n
            继承自Node节点
        """
        # 默认值预处理
        data.setdefault('head', None)
        data.setdefault('kind', 'text')

        super().__init__(**data)
        self.data: dataArg
        self._isTitle: bool = data['kind'] == 'title'  # 是否是标题
        self._isTable: bool = data['kind'] == 'table'  # 是否是表格
        self._isImage: bool = data['kind'] == 'image'  # 是否是图像
        self._isText: bool = data['kind'] == 'text'   # 是否是正文
        self._tree: docTree
        self._parent: docNode
        self._children: docNodes
        self._right: docNode
        self._left: docNode

    @property
    def tree(self) -> 'docTree':
        return super().tree

    @tree.setter
    def tree(self, value: 'docTree'):
        super(docNode, docNode).tree.__set__(self, value)

    @property
    def children(self) -> 'docNodes':
        return super().children

    @children.setter
    def children(self, value):
        super(docNode, docNode).children.__set__(self, value)

    @property
    def parent(self) -> 'docNode':
        return super().parent

    @parent.setter
    def parent(self, value: 'docNode'):
        super(docNode, docNode).parent.__set__(self, value)

    @property
    def left(self) -> 'docNode':
        return super().left

    @left.setter
    def left(self, value: 'docNode'):
        super(docNode, docNode).left.__set__(self, value)

    @property
    def right(self) -> 'docNode':
        return super().right

    @right.setter
    def right(self, value: 'docNode'):
        super(docNode, docNode).right.__set__(self, value)

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

    def __eq__(self, __value: object) -> bool:
        if __value is splitSign:
            return len(self.children) == 0
        return super().__eq__(__value)

    def __rshift__(self, other):
        result = super().__rshift__(other)
        if result is None:
            return None
        return docNodes(result)

    def __lshift__(self, other):
        result = super().__lshift__(other)
        if result is None:
            return None
        return docNodes(result)

    def get_route(self, endpoint: 'docNode', condition: Callable[['docNode'], bool] = lambda node: True) -> 'docNodes':
        """
        获取子父节点的路由 -> 默认是从该节点到目标节点之间的所有标题节点（不包括该节点）。
        - endpoint: Node，该节点的目标节点。
        """
        if condition is None:
            def condition(node: docNode):
                return node.isTitle
        result = super().get_route(endpoint, condition)
        if result is None:
            return None
        return docNodes(list(result))

    def __matmul__(self, other):
        result = super().__matmul__(other)
        return result

    def __str__(self):
        return f"""
标头：{self.data['head']}
内容：{self.data['content']}
类型：{self.data['kind']}
路由：{self >> self.tree.root}
"""


class docNodes(Nodes):

    def __init__(self, nodes: list[docNode]) -> None:
        super().__init__(nodes)

    def prepend(self, node: docNode):
        return super().prepend(node)

    def append(self, node: docNode):
        return super().append(node)
    
    def remove(self, node: docNode):
        return super().remove(node)

    def __str__(self) -> str:
        return "/".join([node.data['content'] for node in self.data])


class docTree(Tree):

    def __init__(self, root: docNode, name: str = '文档树', **data: Unpack[docArg]) -> None:
        """
        实例化一个文档树对象。
        - root: docNode, 文档树的根节点。
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
        self.root: docNode

    def update(self):
        self.data['metadata'].setdefault('size', sys.getsizeof(self.document))

    def from_document(self, document: Document):
        ...

    # @override
    def DFT(self, node=None, callback: Callable[[Node], bool] = lambda node: True) -> list[docNode] | None:
        result = super().DFT(node, callback)
        return docNodes(result)

    # @override
    def BFT(self, callback: Callable[[Node], bool] = lambda node: True) -> list[docNode] | None:
        result = super().BFT(callback)
        return docNodes(result)

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

        result = f"""
{self.name}
- 创建时间：{self.data['metadata']['create_time']}
- 修改时间：{self.data['metadata']['modify_time']}
- 访问时间：{self.data['metadata']['visit_time']}
- 文档大小：{const.get_size(self.data['metadata']['size'])}
- 文档内容：{document}
"""
        return result
