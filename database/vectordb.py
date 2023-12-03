import re
from typing import Literal, TypeAlias, Self, Union

import torch
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
        """
        实例化一个向量数据库对象。
        - forest: _Forest, 树列表，作为数据库的查询树。
        - mode: Literal['exact', 'low'], `exact`为准确模式，`low`为低耗模式，决定数据库使用的Embedding模型。
        - cache_folder: str = './', 数据库模型的缓存路径。
        """
        super().__init__()
        match mode:
            case 'low':
                model = 'BAAI/bge-small-zh'
            case _:
                model = 'BAAI/bge-large-zh-v1.5'
        device = 'cuda' if torch.cuda.is_available() else None
        self.model = SentenceTransformer(
            model, cache_folder=cache_folder, device=device)
        "该数据库使用的模型（该模型必须是或继承自SentenceTransformer）。"

        self.ebmapping: _docNodes = [
            node for tree in forest for node in tree.DFT()]
        "Eb节点映射，包含了数据库中所有的节点，可通过索引的方式直接顺序访问这些节点（不推荐）。"

        self.embeddings: _Embeddings = self.model.encode([
            node.data['content']
            for node in self.ebmapping
        ], normalize_embeddings=True)
        "文本嵌入查询矩阵，用于计算查询相似度，不推荐读取。"

    def insert(self, index: int, node: 'docNode'):
        self.ebmapping.insert(index, node)
        self.embeddings = np.insert(
            self.embeddings, index,
            self.model.encode(node.data['content']),
            axis=0
        )

    def query(self, text: str, count: int = 1, threshold: float = 0.5) -> Union['docNode', list['docNode']]:
        """
        从数据库中查询节点。
        - text: str, 查询的文本，作为相似性判断的根据。
        - count: int, 查询节点的数量。
        - threshold: float = 0.5, 查询阈值，低于阈值将被抛弃。
"""
        maintain_text = self.__find_chinese(text)
        if maintain_text == '':
            return None
        final_text = self.model.encode(
            maintain_text, normalize_embeddings=True)
        text_vector = np.array([final_text])
        similarity = (self.embeddings @ text_vector.T).flatten()
        indexs = torch.from_numpy(similarity).topk(count).indices
        indexs = list(indexs)
        _max = similarity.max()
        if _max < threshold:
            return None
        for position, index in enumerate(indexs):
            if similarity[index] < threshold:
                del indexs[position]

        nodes = []
        for index in indexs:
            nodes.append(self.ebmapping[index])
        if len(nodes) == 1:
            return nodes[0]
        return nodes

    def __query(self, text: str) -> int:
        text = self.model.encode(text, normalize_embeddings=True)
        text_vector = np.array([text])
        index = (self.embeddings @ text_vector.T).argmax()
        return index

    def __find_chinese(self, text: str):
        pattern = re.compile(r'[^\u4e00-\u9fa50-9]+')
        chinese = re.sub(pattern, '', text)
        return chinese

    def delete(self, text_or_index: str | int) -> Self:
        """
        **警告**：不推荐使用该方法删除节点，其具有不可预见性。
        删除节点，并返回被删除的节点。
        - text_or_index: str | int, 为文本时，根据相似度删除节点，为索引时删除对应索引位置的节点。
        """

        if isinstance(text_or_index, int):
            index = text_or_index
        elif isinstance(text_or_index, str):
            index = self.__query(text_or_index)
        else:
            raise ValueError('只能接收索引或字符串。')

        self.embeddings = np.delete(self.embeddings, index, axis=0)
        result = self.ebmapping[index]
        del self.ebmapping[index]

        return result

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
