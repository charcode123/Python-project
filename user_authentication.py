import pymongo
client=pymongo.MongoClient("mongodb://localhost:27017/")
db=client.Email_DB
collections=db.Users
def user_auth(username,password):
    user_data=collections.find_one({"username":username,"password":password})
    if user_data:
        return True
    else:
        return False