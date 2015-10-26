""" PYMONGO IMPORTS """
from pymongo import MongoClient


""" PYMONGO SETUP """
mongo = MongoClient('localhost', 27017)
db = mongo.develop_database


""" BSON IMPORTS """
from bson.objectid import ObjectId


class User(object):
  
  def __init__(self, identifier=None, username=None):
    if identifier:
      self._load({'_id': ObjectId(identifier)})
      self.is_saved = True
    elif username:
      self._load({'username': username})
      self.is_saved = True
    else:
      self.data = {}
      self.is_saved = False
  
  def _load(self, query):
    user_collection = db.users
    user = user_collection.find_one(query)
    if not user: raise ValueError('User does not exist')
    self.data = user
  
  def save(self):
    if self.is_saved: self._update()
    else: self._insert()
  
  def _update(self):
    user_collection = db.users
    user = user_collection.update_one({
      '_id': self.data['_id']
    }, {
      '$set': self.data
    })
  
  def _insert(self):
    user_collection = db.users
    user = user_collection.insert_one(self.data)
    self.is_saved = True