import os, psutil
from typing import Literal, TypeAlias, NewType, TypeVar, List

def __import():
    global ndarray
    from numpy import ndarray

Embedding = NewType('Embedding', 'ndarray')

def get_size(size: int, mode: Literal['str', 'tuple'] = 'str'):
    unit: list[str] = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    while size > 1024 and len(unit) > 1:
        size /= 1024
        unit.pop(0)
    match mode:
        case 'str':
            return f"{size}{unit[0]}"
        case 'tuple':
            return (size, unit[0])

def show_memory_info():
    pid = os.getpid()
    process = psutil.Process(pid)
    info = process.memory_full_info()
    memory = info.vms
    return memory

class c_source:
    directory = os.path.join(os.path.dirname(__file__), 'c_source')
    vectordb = os.path.join(directory, 'vectordb.dll')