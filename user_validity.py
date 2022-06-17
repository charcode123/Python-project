import pymongo
client=pymongo.MongoClient("mongodb://localhost:27017/")
db=client.Email_DB
collections=db.Users
def user_validity(username):
    user_data=collections.find_one({"username":username})
    if user_data:
        return True
    else:
        return False