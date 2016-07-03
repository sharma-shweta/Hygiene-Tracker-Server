from sqlalchemy.inspection import inspect

class Serializer(object):

    def serialize(self):
        serDict = {c: getattr(self, c) for c in inspect(self).attrs.keys()}
        serDict.pop('question')
        return serDict

    @staticmethod
    def serialize_list(l):
        s = [m.serialize() for m in l]
        return s