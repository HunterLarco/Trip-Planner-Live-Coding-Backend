""" FLASK IMPORTS """
from flask import Flask, request, make_response, jsonify
from flask_restful import Resource, Api


""" FLASK BOILERPLATE """
app = Flask(__name__)
api = Api(app)


""" LOCAL IMPORTS """
from models import *


""" IMPLEMENT REST Resource """
class Users(Resource):
  def post(self):
    json = request.json
    if not 'username' in json or not 'password' in json or not json['username'] or not json['password']:
      return ({'error': 'Request requires username and password'}, 400, None)
    
    user = User()
    user.set('username', json['username'])
    user.set_password(json['password'])
    user.save()
    
    return {
      'identifier': user.identifier()
    }
  
  def get(self):
    auth = request.authorization
    if not auth:
      return ({'error': 'Basic Auth Required.'}, 401, None)
    
    try:
      user = User(username=auth.username)
    except:
      return ({'error': 'Invalid Auth.'}, 401, None)
    
    if not user.compare_password(auth.password):
      return ({'error': 'Invalid Auth.'}, 401, None)
    
    return {}


""" ADD REST RESOURCE TO API """
api.add_resource(Users, '/users/')


""" API RESPONSE ENCODING """
@api.representation('application/json')
def output_json(data, code, headers=None):
  from json import dumps as stringify
  resp = make_response(stringify(data), code)
  resp.headers.extend(headers or {})
  return resp


""" START SERVER COMMANDS """
if __name__ == '__main__':
  app.config['TRAP_BAD_REQUEST_ERRORS'] = True
  app.run(debug=True)
