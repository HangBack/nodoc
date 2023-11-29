from collections import deque
from typing import Any, Callable, TypeAlias
import abc


__Nodes: TypeAlias = list['Node']

class Node(metaclass=abc.ABCMeta):


    def __init__(self, **data) -> None:
        """
        节点
        - 关键字参数:
          - **data: Any, 节点保存的数据
        - 属性:
          - parent: Node, 该节点的父节点
          - left: Node, 该节点的左节点
          - right: Node, 该节点的左节点
          - children: list[Node], 该节点的所有子节点
          - visited: bool, 该节点是否被访问
        """
        self._parent: Node = None          # 父节点
        self._left: Node = None            # 左节点
        self._right: Node = None           # 右节点
        self._children: __Nodes = []       # 子节点列表
        self._data = data                  # 节点数据
        self._visited: bool = False        # 是否被访问
        self._count: int = 1               # 包括自己在内的节点数量（包含深度）

    @property
    def visited(self) -> bool:
        "是否被访问"
        return self._visited

    @visited.setter
    def visited(self, value: bool) -> bool:
        self._visited = value

    @property
    def parent(self):
        """
        父节点
        - setter:
          - node: `Node`，设置该节点的父亲节点
        """
        return self._parent

    @parent.setter
    def parent(self, node: 'Node'):
        if not isinstance(node, type(self)):
            raise TypeError(f'期望：{type(self)}，实际：{type(node)}')

        if self._parent:
            self._parent.children.remove(self)

        self._parent = node
        self._parent.children.append(self)

    @property
    def left(self) -> 'Node':
        """
        兄弟节点-左
        - node: `Node`，设置该节点的左节点
        """
        return self._left

    @left.setter
    def left(self, node: 'Node'):
        if not isinstance(node, type(self)):
            raise TypeError(f'期望：{type(self)}，实际：{type(node)}')

        self._left = node
        if self._left.right is not self:  # 同时防止递归过深
            self._left.right = self

    @property
    def right(self) -> 'Node':
        """
        兄弟节点-右
        - node: `Node`，设置该节点的右节点
        """
        return self._right

    @right.setter
    def right(self, node: 'Node'):
        if not isinstance(node, type(self)):
            raise TypeError(f'期望：{type(self)}，实际：{type(node)}')

        self._right = node
        if self._right.left is not self:  # 同时防止递归过深
            self._right.left = self

    @property
    def children(self) -> list['Node']:
        "子节点"
        return self._children

    @children.setter
    def children(self, value):
        self._children = value

    @property
    def data(self):
        "节点数据"
        return self._data

    @data.setter
    def data(self, value: Any):
        self._data = value

    @property
    def count(self) -> int:
        "节点数量"
        return self._count

    @count.setter
    def count(self, value: int):
        self._count = value

    @property
    def type(self):
        "节点类型"
        return type(self._data)


class Tree(metaclass=abc.ABCMeta):

    def __init__(self, root: Node, name: str = '无名树') -> None:
        """
        - root: `Node`, 传入任意一个节点作为该树的根节点。
        - name: `str`, 树的名字，用于查询。
        """
        self.name: str = name
        self.root: Node = root
        self.current_node: Node = root
        self.__nodecount: int = 1

    @property
    def nodecount(self) -> int:
        return self.__nodecount

    """
    
    栈
    queue = [time1 -> a, time2 -> b...]
    以下循环：直到栈空
    栈出
    queue.popleft() 现在 queue 相当于 [time2 -> b, time3 -> c...]
    栈入
    queue.extend(nodeList) 现在 queue 相当于 [time2 -> b, time3 -> c...timeN1 -> Na, timeN2 -> Nb...]

    """

    def BFS(self, callback: Callable[[Node], bool] = lambda node: True) -> Node | None:
        """
        广度优先搜索（层次搜索）
        - callback: `Callable`, 用于判断node是否符合指定条件
        """
        visited = set()
        queue = deque([self.root])
        while queue:
            current_node = queue.popleft()

            if callback(current_node):
                return current_node  # 第一个符合条件的节点

            visited.add(current_node)

            queue.extend(child
                         for child in current_node.children
                         if child not in visited
                         and
                         child not in queue)
        return None  # 没有任何满足条件的节点

    @abc.abstractmethod
    def BFT(self, callback: Callable[[Node], bool] = lambda node: True) -> list[Node] | None:
        """
        广度优先遍历（层次遍历）
        - callback: `Callable`, 用于判断node是否符合指定条件
        """
        visited = set()
        queue = deque([self.root])
        result = []
        while queue:
            current_node = queue.popleft()

            if callback(current_node):
                result.append(current_node)  # 追加一个符合条件的节点

            visited.add(current_node)

            queue.extend(child
                         for child in current_node.children
                         if child not in visited
                         and
                         child not in queue)

        return result

    """
    
    递归
    从当前节点开始优先找子节点，子节点也优先找子节点，直到到底了都还没找到则返回父节点并找该节点的另一个子节点，以此类推

    """

    def DFS(self, node=None, callback: Callable[[Node], bool] = lambda node: True) -> Node | None:
        """
        深度优先搜索
        - node: `Node`, 传入的节点，默认为根节点
        - callback: `Callable`, 用于判断node是否符合指定条件
        """
        result = None
        if node is None:
            node = self.root

        if callback(node):
            return node  # 找到符合条件的节点

        node.visited = True
        for child in node.children:
            if not child.visited:
                result = self.DFS(child, callback)
            if result is not None:
                return result  # 在子树中找到符合条件的节点
        node.visited = False

        return None  # 在当前子树未找到符合条件的节点

    @abc.abstractmethod
    def DFT(self, node=None, callback: Callable[[Node], bool] = lambda node: True) -> list[Node]:
        """
        深度优先遍历
        - node: `Node`, 传入的节点，默认为根节点
        - callback: `Callable`, 用于判断node是否符合指定条件
        """
        result = None
        if node is None:
            node = self.root

        result = []

        if callback(node):
            result.append(node)  # 找到符合条件的节点

        node.visited = True
        for child in node.children:
            if not child.visited:
                current_node = self.DFT(child, callback)
                result.extend(current_node)
        node.visited = False

        return result
