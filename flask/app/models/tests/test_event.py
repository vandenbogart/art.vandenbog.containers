import unittest
import json
from app.models.event import Event

class TestEventClass(unittest.TestCase):
    def test_init(self):
        props = {
            'attr1': 'value1',
            'attr2': 15
        }
        event = Event(props)
        self.assertEqual(event.attr1, 'value1')
        self.assertEqual(event.attr2, 15)

    def test_dumps(self):
        props = {
            "attr1": "value2",
            "attr2": 16
        }
        event = Event(props)
        json_str1 = event.dumps()
        self.assertEqual(json_str1, json.dumps(props))