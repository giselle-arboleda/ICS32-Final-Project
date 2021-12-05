#ds_messenger.py


import socket
import json, time, os
from collections import namedtuple
from ds_protocol import extract_json, join, write_command, directmessage
from pathlib import Path


class DirectMessage(dict):
    """ 
    DMs
    """
    def __init__(self, entry:str = None, recipient:str = None, sender = None, timestamp:float = 0):
        self._timestamp = timestamp
        self.set_entry(entry)

        # Subclass dict to expose Post properties for serialization
        # Don't worry about this!
        if sender is not None:
            self.set_sender(sender)
            dict.__init__(self, entry=self._entry, sender=self.sender, timestamp=self._timestamp)
        elif recipient is not None:
            self.set_recipient(recipient)
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

    def set_sender(self, send):
        self.sender = send
        dict.__setitem__(self, 'sender', send)
        
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
        self._msgs = []         # OPTIONAL   DEBUG
        self._recipients = []    # OPTIONAL   DEBUG

    def send_function(self, server:str, port:int, username:str, password:str, message:str, recipient1=''):


        PORT = port
        HOST = server

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

                if recipient1 != '':
                    dm = DirectMessage(message, recipient=recipient1)
                    print(dm)
                else:
                    dm = message
                dm_msg = directmessage(user_token, dm)
                write_command(send, dm_msg)
                srv_msg = recv.readline()
                print("Response", srv_msg)
                return extract_json(srv_msg).message
                    


		
    def send(self, message:str, recipient:str) -> bool:
        server = self.dsuserver
        port = 3021
        usr = self.username
        pwd = self.password
        if recipient not in self._recipients:
            self._recipients.append(recipient)
        if self.send_function(server, port, usr, pwd, message, recipient) == "Direct message sent":
            return True

                
    def retrieve_new(self) -> list:
        server = self.dsuserver
        port = 3021
        usr = self.username
        pwd = self.password
        dm_lst = []
        for msg in self.send_function(server, port, usr, pwd, "new"):
            dm_lst.append(msg)
        return dm_lst

    def retrieve_all(self) -> list:
        server = self.dsuserver
        port = 3021
        usr = self.username
        pwd = self.password
        dm_lst = []
        for msg in self.send_function(server, port, usr, pwd, "all"):
            dm_lst.append(msg)
            if msg not in self._msgs:
                self.add_msg(msg)
        return dm_lst






    def add_recipient(self, recipient: str) -> None:
        self._recipients.append(recipient)


    def get_recipients(self) -> list:
        return self._recipients
    """

    add_post accepts a Post object as parameter and appends it to the posts list. Posts are stored in a 
    list object in the order they are added. So if multiple Posts objects are created, but added to the 
    Profile in a different order, it is possible for the list to not be sorted by the Post.timestamp property. 
    So take caution as to how you implement your add_post code.

    """

    def add_msg(self, msg: DirectMessage) -> None:
        self._msgs.append(msg)

    """

    del_post removes a Post at a given index and returns True if successful and False if an invalid 
    index was supplied. 

    To determine which post to delete you must implement your own search operation on the posts 
    returned from the get_posts function to find the correct index.

    """

    def del_msg(self, index: int) -> bool:
        try:
            del self._msgs[index]
            return True
        except IndexError:
            return False
        
    """
    
    get_posts returns the list object containing all posts that have been added to the Profile object

    """
    def get_msgs(self) -> list:
        return self._msgs

    """

    save_profile accepts an existing dsu file to save the current instance of Profile to the file system.

    Example usage:

    profile = Profile()
    profile.save_profile('/path/to/file.dsu')

    Raises DsuFileError

    """
    def save_profile(self, path: str) -> None:
        p = path.replace(os.sep, '\\')
        p = Path(p)

        if os.path.exists(p):
            try:
                f = open(p, 'w')
                json.dump(self.__dict__, f)
                f.close()
            except Exception as ex:
                raise DsuFileError("An error occurred while attempting to process the DSU file.", ex)
        else:
            raise DsuFileError("Invalid DSU file path or type")

    """

    load_profile will populate the current instance of Profile with data stored in a DSU file.

    Example usage: 

    profile = Profile()
    profile.load_profile('/path/to/file.dsu')

    Raises DsuProfileError, DsuFileError

    """
    def load_profile(self, path: str) -> None:
        p = Path(path)

        if os.path.exists(p):
            try:
                f = open(p, 'r')
                obj = json.load(f)
                print(obj)
                self.username = obj['username']
                self.password = obj['password']
                self.dsuserver = obj['dsuserver']
                
                for dm_obj in obj['_msgs']:
                    post = DirectMessage(dm_obj['message'],sender=dm_obj['sender'],timestamp=dm_obj['timestamp'])
                    self._msgs.append(msg)
                for rec in obj['_recipients']:
                    self._recipients.append(rec)
                f.close()
            except Exception as ex:
                raise DsuProfileError(ex)
        else:
            raise DsuFileError()
