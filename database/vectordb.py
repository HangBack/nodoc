from typing import Any, Literal, TypeAlias, Self
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

    def insert(self, index: int, node: 'docNode'):
        self.ebmapping.insert(index, node)
        self.embeddings = np.insert(
            self.embeddings, index,
            self.model.encode(node.data['content']),
            axis=0
        )

    def query(self, text: str):
        text = self.model.encode(text, normalize_embeddings=True)
        text_vector = np.array([text])
        index = (self.embeddings @ text_vector.T).argmax()
        return self.ebmapping[index]

    def export(self, name: str, directory: str = './'):
        return super().export(name, directory)
    

    def load(path: str) -> Self:
        return dataBase.load(path)

    @property
    def data(self):
        return super().data
