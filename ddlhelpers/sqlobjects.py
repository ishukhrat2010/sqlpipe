from ddlhelpers.ddlsyntax import *

class SQLObject:
    __verb__ = ''

    def __init__(self):
        self.__objname__ = ''

    @staticmethod
    def ddl_reserved_words():
        return ['CREATE', 'DROP', 'ALTER']

    @staticmethod
    def from_tokens(aTokens):
        myClass = SQLObjectFabric.create_sql_object(aTokens)
        return myClass.init_from_tokens(aTokens)

    @classmethod
    def is_ddl_tokens(cls, aTokens):
        return(str(aTokens[0].value).upper() in cls.ddl_reserved_words())

    @classmethod
    def parse_tokens(cls, aTokens):
        pass

    @classmethod
    def init_from_tokens(cls, aTokens):
        pass

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


def supported_object_types():
    return ['DATABASE', 'TABLE', 'VIEW', 'FUNCTION', 'USER']

def getSQLObject(token_chain):
    obj=None
    plain_tokens = token_chain.copy([], [TT_COMMENT])
    if  str(plain_tokens.items[0].value).upper() == 'CREATE':
        objName = str(plain_tokens.items[1].value)
        if objName.upper() in supported_object_types():
            obj = type('SQLObject'+objName.capitalize(), (SQLObject,), {})
    return obj
