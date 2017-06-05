class EncodeString(object):

    def __init__(self, **kwargs):
        return super().__init__(**kwargs)

    def getPropertiesString(self):
        listattrs = dir(self)
        result = ""
        for elem in listattrs:
            if(elem.startswith('_') or elem.endswith('_') or elem.startswith('get')):
                continue
            result += elem + '=' +getattr(self, elem) + ';'
        return result




