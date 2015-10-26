""" FLASK IMPORTS """
from flask import Flask, request, make_response, jsonify
from flask_restful import Resource, Api


""" FLASK BOILERPLATE """
app = Flask(__name__)
api = Api(app)


""" IMPLEMENT REST Resource """
class MyObject(Resource):
  def get(self):
    return {
      'test': 7*6
    }


""" ADD REST RESOURCE TO API """
api.add_resource(MyObject, '/myobject/')


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
