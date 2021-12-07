#test_ds_messenger.py

from ds_messenger import DirectMessage, DirectMessenger
import unittest

class DSMessengerTest(unittest.TestCase):

    def test_dmsend(self):
        dm = DirectMessenger("168.235.86.101", "EvanKarGiselle", "pwd123")
        self.assertTrue(dm.send('testing message entry 1', 'ohhimark'))
        self.assertTrue(dm.send('testing message entry 2', 'EvanKarGiselle'))

    def test_retrieve_new(self):
        dm = DirectMessenger("168.235.86.101", "EvanKarGiselle", "pwd123")
        self.assertIsNotNone(dm.retrieve_new())

    def test_retrieve_all(self):
        dm = DirectMessenger("168.235.86.101", "EvanKarGiselle", "pwd123")
        self.assertIn({'message': 'testing message entry 2', 'from': 'EvanKarGiselle', 'timestamp': '1638652218.10286'}, dm.retrieve_all())


if __name__ == '__main__':
    unittest.main()
