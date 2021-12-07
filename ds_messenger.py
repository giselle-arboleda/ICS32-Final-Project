#ds_messenger.py
# Giselle Arboleda, Karissa Pratt, and Evan Fok

import socket
import json, time, os
from collections import namedtuple
from ds_protocol import extract_json, join, write_command, directmessage
from pathlib import Path


class Recipient(dict):
    """
    The Recipient class is responsible for working with the username and user's messages. It sets the username and messages as attributes of the class upon instantiation.
    """

    def __init__(self, username, messages=[]):
        self.set_username(username)
        self.set_messages(messages)
        dict.__init__(self, username=self.username, messages=self.messages)

    def set_username(self, u):
        #Sets the username
        self.username = u
        dict.__setitem__(self, 'username', u)

    def set_messages(self, m):
        #Sets the messages
        self.messages = m
        dict.__setitem__(self, 'messages', m)
        
    
class DirectMessage(dict):
    """ 
    The DirectMessege class works with the entry, recipient, sender, and timestamp. Upon instantiation
    it sets the given entry, timestamp, and recipient if given one.
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
        #sets the given entry into a class attribute
        self._entry = entry 
        dict.__setitem__(self, 'entry', entry)

        # If timestamp has not been set, generate a new from time module
        if self._timestamp == 0:
            self._timestamp = time.time()
            
    def set_recipient(self, r):
        #sets the recipient
        self._recipient = r 
        dict.__setitem__(self, 'recipient', r)

    def set_sender(self, send):
        #sets the sender
        self.sender = send
        dict.__setitem__(self, 'sender', send)
        
    def get_entry(self):
        #returns the entries
        return self._entry
    
    def set_time(self, time:float):
        #sets timestamp with the given time in the parameter
        self._timestamp = time
        dict.__setitem__(self, 'timestamp', time)
    
    def get_time(self):
        #returns the timestamp
        return self._timestamp

    """
    The property method is used to support get and set capability for entry and time values.
    When the value for entry is changed, or set, the timestamp field is updated to the
    current time.
    """ 
    entry = property(get_entry, set_entry)
    timestamp = property(get_time, set_time)



class DirectMessenger:
    """
    The DirectMesseger class works with the dsuserver, username, and password. If given a username and password,
    it sets the values into attributes of the class with the initializer. The attributes also include...
    self._msgs -> list of messages
    self._recipients -> a list of Recipient objects
    self._recipients_names -> a list of recipient names in string format
    """
    def __init__(self, dsuserver='168.235.86.101', username=None, password=None):
        self.token = None
        self.dsuserver = dsuserver
        self.username = username
        self.password = password
        self._msgs = []         # OPTIONAL   DEBUG
        self._recipients = []    # OPTIONAL   DEBUG
        self._recipients_names = []


    def send_function(self, server:str, port:int, username:str, password:str, message:str, recipient1=''):
        """
        The send_function connects to and joins a ds server while sending a message. If there is a recipient
        passed into the parameter, it sends a direct message to that recipient with the message given. 
        """
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
        """
        The send function adds a recipient to the recipient list if the recipient is new.
        Returns true if the message was successfully sent and false if the send failed. 
        """
        server = self.dsuserver
        port = 3021
        usr = self.username
        pwd = self.password
        if recipient not in self._recipients_names:
            self.add_recipient(recipient)
        for r in self._recipients:
            index = self._recipients.index(r)
            if recipient == r['username']:
                self._recipients[index]['messages'].append('You: '+message)
        if self.send_function(server, port, usr, pwd, message, recipient) == "Direct message sent":
            return True



    def retrieve_new(self) -> list:
        """
        The retrive_new method returns a list of DirectMessage objects that contain all new messages.
        Appends all new messages into a list and uses the "Incoming:" message to differentiate
        between the recipient and sender.
        """
        server = self.dsuserver
        port = 3021
        usr = self.username
        pwd = self.password
        dm_lst = []
        for msg in self.send_function(server, port, usr, pwd, "new"):
            dm_lst.append(msg)
            for r in self._recipients:
                index = self._recipients.index(r)
                if msg['from'] == r['username']:
                    self._recipients[index]['messages'].append('Incoming: '+msg['message'])
        return dm_lst

    def retrieve_all(self) -> list:
        """
        The retrive_all method returns a list of DirectMessage objects which contain all of the messages
        that have been sent. 
        """
        server = self.dsuserver
        port = 3021
        usr = self.username
        pwd = self.password
        dm_lst = []
        for msg in self.send_function(server, port, usr, pwd, "all"):
            dm_lst.append(msg)
        return dm_lst






    def add_recipient(self, recipient: str) -> None:
        """
        The add_recipient function appends a Recipient object to the private attribute "_recipients"
        while also appending the recipient names as a string to "_recipients_names" for later use.
        """
        self._recipients_names.append(recipient)
        self._recipients.append(Recipient(username=recipient, messages=[]))


    def get_recipients(self) -> list:
        """
        The get_recipients returns a list of recipients as a 'Recipient' that were stored in the classes attributes.
        """
        return self._recipients

    def add_msg(self, msg: DirectMessage) -> None:
        """
        add_msg accepts a DirectMessage object as parameter and appends it to the msg list. Msgs are stored in a 
        list object in the order they are added. 
        """
        self._msgs.append(msg)

    def del_msg(self, index: int) -> bool:
        """
        del_msg removes a msg at a given index and returns True if successful and False if an invalid 
        index was supplied. 
        """
        try:
            del self._msgs[index]
            return True
        except IndexError:
            return False
        

    def get_msgs(self) -> list:
        """
        get_msgs returns the list object containing all msgs that have been stored in the private attribute.
        """
        return self._msgs


    def save_profile(self, path: str) -> None:
        """
        save_profile accepts an existing dsu file to save the current instance of Profile to the file system.
        Example usage:
        _current_profile = DirectMessenger()
        _current_profile.save_profile('/path/to/file.dsu')
        Raises DsuFileError
        """
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


    def load_profile(self, path: str) -> None:
        """
        load_profile will populate the current instance of DirectMessager() with data stored in a DSU file.
        Example usage: 
        _current_profile = DirectMessenger()
        _current_profile.load_profile('/path/to/file.dsu')
        Raises DsuProfileError, DsuFileError
        """
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
                for name in obj['_recipients_names']:
                    self._recipients_names.append(name)
                f.close()
            except Exception as ex:
                raise DsuProfileError(ex)
        else:
            raise DsuFileError()
