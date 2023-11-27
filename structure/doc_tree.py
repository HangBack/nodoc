from typing import Any, Callable, TypedDict, Unpack
from .tree import Node, Tree

class metadata(TypedDict):
    create_time: str # 数据的创建时间
    modify_time: str # 数据的修改时间
    visit_time: str  # 数据的访问时间

class dataArg(TypedDict):
    head: str # 数据的标头（标题等）
    metadata: metadata # 元数据
    content: Any # 数据的内容

class docNode(Node):
    
    def __init__(self, **data: Unpack[dataArg]) -> None:
        super().__init__(**data)
        self._isTitle: bool = False # 是否是标题
        self._isTable: bool = False # 是否是表格
        self._isImage: bool = False # 是否是图像


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

class docTree(Tree):

    def __init__(self, root: docNode, name: str = '文档树') -> None:
        """
        文档树
        - 参数
         - 必选
          - root: docNode, 传入一个文档节点作为根节点。
         - 可选
          - name: str, 文档树的名称，用于查询。
        """
        if not isinstance(root, docNode):
            raise TypeError(f'期望：docNode，实际：{type(root)}')
        
        super().__init__(root, name)