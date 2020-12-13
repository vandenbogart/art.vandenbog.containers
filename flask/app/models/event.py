import json
class Event:
    '''JSON serializable class to be extended by all models'''
    def __init__(self, dictionary):
        for k, v in dictionary.items():
            setattr(self, k, v)
    def dumps(self):
        return json.dumps(self.__dict__)
    