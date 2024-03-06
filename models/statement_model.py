from dataclasses import dataclass
import os
from pymodm import MongoModel, fields

from definitions import ROOT_DIR

class Statement(MongoModel):
    name = fields.CharField()

    @dataclass
    class AdditionalData():
        ICON: str = "💭"
        CATEGORY_NAME_RUS: str = "Высказывания"
        CATEGORY_NAME_ENG: str = "Statements"
        FILENAME = os.path.join(ROOT_DIR, "data", "statements")