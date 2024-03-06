from dataclasses import dataclass
import os
from pymodm import MongoModel, fields

from definitions import ROOT_DIR

class Film(MongoModel):
    name = fields.CharField()

    @dataclass
    class AdditionalData():
        ICON: str = "🎬"
        CATEGORY_NAME_RUS: str = "Фильмы"
        CATEGORY_NAME_ENG: str = "Films"
        FILENAME = os.path.join(ROOT_DIR, "data", "films")