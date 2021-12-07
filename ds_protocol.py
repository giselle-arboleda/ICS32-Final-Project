# ds_protocol.py
# Giselle Arboleda, Karissa Pratt, Evan Fok


import json
from collections import namedtuple


DataTuple = namedtuple('DataTuple', ['message','token', 'message_type'])

class DSPProtocolError(Exception):
  pass

def extract_json(json_msg:str) -> DataTuple:
  '''
  Call the json.loads function on a json string and convert it to a DataTuple object
  
  Returns the message and token from the DSP Server as a namedtuple
  if there is no error in the message.
  '''
  try:
    json_obj = json.loads(json_msg)
    msg = 'message'
    if msg in json_obj['response']:
      message = json_obj['response']['message']
    message_type = json_obj['response']['type']
    token = None
    tkn = 'token'
    if message_type == 'ok' and 'token' in json_obj['response']:
      token = json_obj['response']['token']
    msgs = 'messages'
    if msgs in json_obj['response']:
      message = json_obj['response']['messages']
  except json.JSONDecodeError:
    print("Json cannot be decoded.")

  return DataTuple(message, token, message_type)


def join(username, password, user_token=''):
  '''
  Accept username, password, and token and creates a formatted join message
  for the DSP server. Call the json.dumps function on a python message and convert
  it to a json object. Returns the object.
  '''
  python_msg = {"join": {"username": username,"password": password,"token":user_token}}
  json_obj = json.dumps(python_msg)
  
  return json_obj


def bio_post(user_token, bio_or_post, entry):
  '''
  Accept token, the word "bio" or "post", and an entry and creates a formatted bio or post message
  for the DSP server. Call the json.dumps function on a python message and convert
  it to a json object. Returns the object.
  '''
  python_msg = {"token": user_token, bio_or_post: {"entry": entry,"timestamp": "1603167689.3928561"}}
  json_obj = json.dumps(python_msg)
  
  return json_obj

def write_command(connection, msg: str):
  '''
  Accepts a connection and a message as parameters. Performs the required commands
  and steps to send a message. Appends a newline, writes the message, and flushes the
  buffer.
  '''
  try:
    connection.write(msg + '\r\n')
    connection.flush()
  except:
    raise DSPProtocolError


def directmessage(user_token, message):
  '''
  Accept username, password, message, and token and creates a formatted join message
  for the DSP server. Call the json.dumps function on a python message and convert
  it to a json object. Returns the object.
  '''
  python_msg = {"token":user_token, "directmessage": message}
  json_obj = json.dumps(python_msg)
  
  return json_obj
