#test_ds_message_protocol.py

from ds_protocol import directmessage
import unittest
import json



class DSMessageTest(unittest.TestCase):
    dm_msg = {"entry": "Hello World!","recipient":"ohhimark", "timestamp": "1603167689.3928561"}
    dm_new = "new"
    dm_all = "all"
    user_token = "user_token"
    
    def test_directmessage(self):
        self.assertEqual(directmessage(self.user_token, self.dm_msg), json.dumps({"token":"user_token", "directmessage": {"entry": "Hello World!","recipient":"ohhimark", "timestamp": "1603167689.3928561"}}))
        self.assertEqual(directmessage(self.user_token, self.dm_new), json.dumps({"token":"user_token", "directmessage": "new"}))
        self.assertEqual(directmessage(self.user_token, self.dm_all), json.dumps({"token":"user_token", "directmessage": "all"}))

        


if __name__ == '__main__':
    unittest.main()
