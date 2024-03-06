from pymodm import MongoModel, fields

class User(MongoModel):
    user_id = fields.IntegerField(primary_key=True)
    roll_dice = fields.BooleanField(default=True)