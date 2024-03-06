from pymodm import MongoModel, fields
from models import category_model, user_model

class UserCategory(MongoModel):
    user = fields.ReferenceField(user_model.User)
    category = fields.ReferenceField(category_model.Category)
    amount = fields.IntegerField()
