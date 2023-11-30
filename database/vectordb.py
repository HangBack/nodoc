from typing import Any, Literal, TypeAlias, Self, Callable
from .database import dataBase
from nodoc.const import Embedding
from sentence_transformers import SentenceTransformer
import numpy as np
import os


def __import():
    global docNode, docTree
    from nodoc import docNode
    from nodoc import docTree


_docNodes: TypeAlias = list['docNode']
_Embeddings: TypeAlias = np.ndarray[Embedding]
_Forest: TypeAlias = list['docTree']


class vectorDB(dataBase):

    def __init__(self, forest: _Forest = None, mode: Literal['exact', 'low'] = 'exact', cache_folder='./') -> None:
        super().__init__()
        match mode:
            case 'low':
                model = 'BAAI/bge-small-zh'
            case _:
                model = 'BAAI/bge-large-zh-v1.5'
        self.model = SentenceTransformer(model, cache_folder=cache_folder)
        self.ebmapping: _docNodes = [
            node for tree in forest for node in tree.DFT()]
        
        self.embeddings: _Embeddings = self.model.encode([
            node.data['content']
            for node in self.ebmapping
        ], normalize_embeddings=True)
        self.__path: str = ""

    def insert(self, index: int, node: 'docNode'):
        self.ebmapping.insert(index, node)
        self.embeddings = np.insert(
            self.embeddings, index,
            self.model.encode(node.data['content']),
            axis=0
        )

    def query(self, text: str, threshold: float = 0.5) -> 'docNode':
        """
        查询节点
        - text: str, 输入查询文本，将根据该文本返回最相似内容的节点。
        - 可选
          - threshold: float, 相似阈值，小于该值结果将被抛弃，默认为0.5。
        """
        text = self.model.encode(text, normalize_embeddings=True)
        text_vector = np.array([text])
        similarity = self.embeddings @ text_vector.T
        index = similarity.argmax()
        _max = similarity.max()
        if _max < threshold:
            None
        return self.ebmapping[index]
    
    def __query(self, text: str) -> int:
        text = self.model.encode(text, normalize_embeddings=True)
        text_vector = np.array([text])
        index = (self.embeddings @ text_vector.T).argmax()
        return index

    
    def delete(self, text_or_index: str | int, mode: Literal['force', 'default'] = 'default') -> Self:
        """
        *警告：不推荐使用该方法删除节点，其具有不可预见性。
        返回一个即将被删除的节点
        - text_or_index: str | int, 传入一个文本或索引，传入文本时将找到最匹配的节点。
        - mode: Literal['force', 'default'], force字面量将强制删除而无需验证，default即默认模式是需要验证的。
        """
        
        if isinstance(text_or_index, int):
            index = text_or_index
        elif isinstance(text_or_index, str):
            index = self.__query(text_or_index)
        else:
            raise ValueError('只能接收索引或字符串。')
        
        self.embeddings = np.delete(self.embeddings, index, axis=0)
        del self.ebmapping[index]
    
        return self.ebmapping[index]

    def export(self, name: str, directory: str = './'):
        return super().export(name, directory)
    
    def save(self):
        return super().save()

    def load(path: str) -> Self:
        database: Self = dataBase.load(path)
        database.__path = path
        return database

    @property
    def data(self):
        return super().data
