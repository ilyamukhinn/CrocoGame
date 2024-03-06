from dataclasses import dataclass
import os
from pymodm import MongoModel, fields

from definitions import ROOT_DIR

class Character(MongoModel):
    name = fields.CharField()
    
    @dataclass
    class AdditionalData():
        ICON: str = "⭐️"
        CATEGORY_NAME_RUS: str = "Персонажи"
        CATEGORY_NAME_ENG: str = "Characters"
        FILENAME = os.path.join(ROOT_DIR, "data", "characters")