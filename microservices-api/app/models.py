from . import mongo

def add_user(user_data):
    return mongo.db.users.insert_one(user_data)

def get_users():
    return list(mongo.db.users.find({}, {"_id": 0}))
