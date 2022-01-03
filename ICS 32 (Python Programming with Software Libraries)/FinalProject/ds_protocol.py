import json
from collections import namedtuple


#join function, called in client
def join (username, password, token):
    setup = {"join": {"username": username,"password": password,"token": token}}
    setup = str(setup)
    setup = setup.replace("'", "\"")
    return setup

#post function called in client
def post(token, timestamp, usr_post):
    setup = {"token": token, "post": {"entry": usr_post,"timestamp": timestamp}}
    setup = str(setup)
    setup = setup.replace("'", "\"")
    return setup

# Send a directmessage to anoXther DS user
def send_dm(user_token, entry, recipient, timestamp):
    setup = {"token": user_token, "directmessage": {"entry": entry,"recipient": recipient, "timestamp": timestamp}}
    setup = str(setup)
    setup = setup.replace("'", "\"")
    return setup
def unread_mes(user_token, keyword):
    setup = {"token": user_token, "directmessage": keyword}
    setup = str(setup)
    setup = setup.replace("'", "\"")
    return setup

def all_mes(user_token, keyword):
    setup = {"token": user_token, "directmessage": keyword}
    setup = str(setup)
    setup = setup.replace("'", "\"")
    return setup


  
# Create a namedtuple to hold the values we expect to retrieve from json messages.
DataTuple = namedtuple('DataTuple', ['foo'])

#extracts the token from the message received from server, called in client
def extract_json(json_msg:str) -> DataTuple:
  '''
  Call the json.loads function on a json string and convert it to a DataTuple object
  '''
  foo = None
  try:
    json_obj = json.loads(json_msg)
    foo = json_obj['response']['token']
  except json.JSONDecodeError:
    print("Json cannot be decoded.")

  return DataTuple(foo)
