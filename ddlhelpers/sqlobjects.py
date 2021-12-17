
class SQLObject:

    def __init__(self):
        self.__objname__ = ''

    @property
    def object_type(self):
        return 'unknown'

    @property
    def name(self):
        return self.__objname__

    @name.setter
    def name(self, object_name):
        if len(object_name) > 0 and self.name_is_valid(object_name):
            self.__objname__ = object_name
        else:
            msg = f'Invalid {self.object_type} name: <{object_name}>!'
            raise msg

    def name_is_valid(self, aName):
        return True


class SQLTable(SQLObject):

    def __init__(self):
        SQLObject(self).__init__()

    @property
    def object_type(self):
        return 'table'
