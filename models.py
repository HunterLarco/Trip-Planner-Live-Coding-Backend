""" PYMONGO IMPORTS """
from pymongo import MongoClient


""" PYMONGO SETUP """
mongo = MongoClient('localhost', 27017)
db = mongo.develop_database


""" BSON IMPORTS """
from bson.objectid import ObjectId


class DBModel(object):
  
  def __init__(self, identifier=None):
    self.is_saved = False
    if identifier:
      self._load({'_id': ObjectId(identifier)})
    else:
      self.data = {}
  
  def _load(self, query):
    user_collection = db.users
    user = user_collection.find_one(query)
    if not user: raise ValueError('User does not exist')
    self.is_saved = True
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
  
  def set(self, key, value):
    self.data[key] = value
  
  def get(self, key):
    return self.data[key]
  
  def identifier(self):
    return str(self.get('_id'))



class User(DBModel):
  
  def __init__(self, *args, username=None, **kwargs):
    super(User, self).__init__(*args, **kwargs)
    if username:
      self._load({'username': username})
  
  