from typing import TypeAlias, NewType, TypeVar, List

def __import():
    global ndarray
    from numpy import ndarray

Embedding = NewType('Embedding', 'ndarray')
