#ds_messenger.py


import socket
import json, time, os
from collections import namedtuple
from ds_protocol import extract_json, join, bio_post, write_command, directmessage

class DirectMessage(dict):
    """ 
    DMs
    """
    def __init__(self, entry:str = None, recipient:str = None, timestamp:float = 0):
        self._timestamp = timestamp
        self.set_entry(entry)
        self.set_recipient(recipient)

        # Subclass dict to expose Post properties for serialization
        # Don't worry about this!
        dict.__init__(self, entry=self._entry, recipient=self._recipient, timestamp=self._timestamp)
    
    def set_entry(self, entry):
        self._entry = entry 
        dict.__setitem__(self, 'entry', entry)

        # If timestamp has not been set, generate a new from time module
        if self._timestamp == 0:
            self._timestamp = time.time()
            
    def set_recipient(self, r):
        self._recipient = r 
        dict.__setitem__(self, 'recipient', r)
        
    def get_entry(self):
        return self._entry
    
    def set_time(self, time:float):
        self._timestamp = time
        dict.__setitem__(self, 'timestamp', time)
    
    def get_time(self):
        return self._timestamp

    """

    The property method is used to support get and set capability for entry and time values.
    When the value for entry is changed, or set, the timestamp field is updated to the
    current time.

    """ 
    entry = property(get_entry, set_entry)
    timestamp = property(get_time, set_time)



class DirectMessenger:
  def __init__(self, dsuserver=None, username=None, password=None):
    self.token = None
    self.dsuserver = dsuserver
    self.username = username
    self.password = password
		
  def send(self, message:str, recipient:str) -> bool:
    '''
    The send function joins a ds server and sends a message, bio, or both

    :param server: The ip address for the ICS 32 DS server.
    :param port: The port where the ICS 32 DS server is accepting connections.
    :param username: The user name to be assigned to the message.
    :param password: The password associated with the username.
    :param message: The message to be sent to the server.
    :param bio: Optional, a bio for the user.
    '''


    PORT = 3021
    HOST = self.dsuserver

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
          client.connect((HOST, PORT))

          send = client.makefile('w')
          recv = client.makefile('r')

          print("client connected to", HOST, "on", PORT)

          join_msg = join(self.username, self.password)
          write_command(send, join_msg)

          srv_msg = recv.readline()
          print("Response", srv_msg)
          if extract_json(srv_msg).message_type == 'ok':
            user_token = extract_json(srv_msg)[1]
            
            dm = DirectMessage(message, recipient)
            print(dm)
            dm_msg = directmessage(user_token, dm)
            write_command(send, dm_msg)
            srv_msg = recv.readline()
            print("Response", srv_msg)
            if extract_json(srv_msg).message_type == 'ok':
                return True


		
  def retrieve_new(self) -> list:
    # returns a list of DirectMessage objects containing all new messages
    pass
 
  def retrieve_all(self) -> list:
    # returns a list of DirectMessage objects containing all messages
    pass
