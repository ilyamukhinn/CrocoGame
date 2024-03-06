from dataclasses import dataclass
import os
from pymodm import MongoModel, fields

from definitions import ROOT_DIR

class Book(MongoModel):
    name = fields.CharField()
    
    @dataclass
    class AdditionalData():
        ICON: str = "📚"
        CATEGORY_NAME_RUS: str = "Книги"
        CATEGORY_NAME_ENG: str = "Books"
        FILENAME = os.path.join(ROOT_DIR, "data", "books")