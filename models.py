""" ENCRYPTION IMPORTS """
import bcrypt


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
    collection = self._collection()
    entity = collection.find_one(query)
    if not entity: raise ValueError('Entity does not exist')
    self.is_saved = True
    self.data = entity
  
  def _collection(self):
    return db[self.__class__.__name__]
  
  def save(self):
    if self.is_saved: self._update()
    else: self._insert()
    return True
  
  def _update(self):
    collection = self._collection()
    entity = collection.update_one({
      '_id': self.data['_id']
    }, {
      '$set': self.data
    })
  
  def _insert(self):
    collection = self._collection()
    entity = collection.insert_one(self.data)
    self.is_saved = True
  
  def set(self, key, value):
    self.data[key] = value
  
  def get(self, key):
    return self.data[key]
  
  def identifier(self):
    return str(self.get('_id'))


class User(DBModel):
  
  BCRYPT_ROUNDS = 12
  
  def __init__(self, *args, username=None, **kwargs):
    super(User, self).__init__(*args, **kwargs)
    if username:
      self._load({'username': username})
  
  def set_password(self, password):
    encodedpassword = password.encode('utf-8')
    hashed = bcrypt.hashpw(encodedpassword, bcrypt.gensalt(self.BCRYPT_ROUNDS))
    self.set('password', hashed)
  
  def compare_password(self, password):
    encodedpassword = password.encode('utf-8')
    print(self.get('password'))
    return bcrypt.hashpw(encodedpassword, self.get('password')) == self.get('password')
  
  def save(self):
    if not self.is_saved:
      try:
        user = User(username = self.get('username'))
        return False
      except:
        pass
    return super(User, self).save()
  
  