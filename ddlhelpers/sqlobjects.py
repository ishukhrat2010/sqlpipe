
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


class SQLSchema(SQLObject):
    pass


class SQLTable(SQLObject):

    @property
    def object_type(self):
        return 'table'

    @classmethod
    def init_from_tokens(cls, aTokens):
        return cls()

    def __repr__(self):
        return "SQL Table"


class SQLView(SQLObject):
    pass


class SQLMaterializedView(SQLObject):
    pass


class SQLFunction(SQLObject):
    pass


class SQLStoredProc(SQLObject):
    pass


class SQLObjectFabric():

    @staticmethod
    def create_sql_object(aTokens):

        def identify_class():
            result = None
            tokenList = aTokens[1:]
            for t in tokenList:
                idx = tokenList.index(t)
                curToken = str(t.value).upper()
                nextToken = str(tokenList[idx+1].value).upper()
                if curToken == 'SCHEMA':
                    result = SQLSchema

                elif curToken == 'TABLE':
                    result = SQLTable

                elif curToken == 'VIEW':
                    result = SQLView

                elif curToken == 'MATERIALIZED' and nextToken == 'VIEW':
                    result = SQLMaterializedView

                elif curToken == 'FUNCTION':
                    result = SQLFunction

                elif curToken == 'STORED' and nextToken == 'PROCEDURE':
                    result = SQLStoredProc

                if result != None:
                    break

            return result

        verb = str(aTokens[0].value).upper()
        objectClass = identify_class()
        if objectClass != None:
            objectClass.__verb__ = verb
            return objectClass
        return None
