import os
import re
from .base import Document



class PDF(Document):

    def __init__(self, data: str = "") -> None:
        message = self.normalize(data)
        super().__init__(message, data)
        
    def normalize(self):
        ...

    def export(self, name: str, directory: str = './'):
        return super().export(name, directory)