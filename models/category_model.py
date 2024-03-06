from pymodm import MongoModel, fields

class Category(MongoModel):
    name = fields.CharField()