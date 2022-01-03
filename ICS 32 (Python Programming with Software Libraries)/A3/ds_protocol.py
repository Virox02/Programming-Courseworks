import json
from collections import namedtuple

DataTuple = namedtuple('DataTuple', ['foo','baz'])

ErrorTuple = namedtuple('ErrorTuple', ['typ','msg', 'token'])

def join(username, password):
    join_var = '{"join": {"username": "'+username+'","password": "'+password+'","token":""}}'
    return join_var

def post(tkn, message, timestamp): #fix param
    post_var = '{"token":"%s", "post": {"entry": "%s","timestamp": "%i"}}'%(tkn, message, timestamp)
    return post_var

def Bio(tkn, bio, timestamp): #fix param
    bio_var = '{"token":"%s", "bio": {"entry": "%s","timestamp": "%i"}}'%(tkn, bio, timestamp)
    return bio_var

def extract_json(json_msg:str) -> DataTuple:
  '''
  Call the json.loads function on a json string and convert it to a DataTuple object
  '''
  try:
    json_obj = json.loads(json_msg)
    foo = json_obj['foo']
    baz = json_obj['bar']['baz']
  except json.JSONDecodeError:
    print("Json cannot be decoded.")

  return DataTuple(foo, baz)


def extract_msg(json_msg:str) -> ErrorTuple:
  '''
  Call the json.loads function on a json string and convert it to a DataTuple object
  '''
  token = None
  try:
    json_obj = json.loads(json_msg)
    typ = json_obj['response']['type']
    msg = json_obj['response']['message']
    if typ == 'ok':
        token = json_obj['response']['token']    
    else:
        print("TOKEN ERROR, try again!")
  except json.JSONDecodeError:
    print("Json cannot be decoded.")

  return ErrorTuple(typ, msg, token)

