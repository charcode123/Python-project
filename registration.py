from matplotlib import collections
import pymongo
client=pymongo.MongoClient("mongodb://localhost:27017/")
db=client.Email_DB
collections=db.Users
def user_registration(username,password):
    user_data=collections.find_one({"username":username,"password":password})
    if user_data:
        return False
    else:
        collections.insert_one({"username":username,"password":password})
        return True