from ddlhelpers.ddlsyntax import *

class SQLObject:

    def __init__(self, dialect:str=''):
        self._objname = '<undefined>'
        self._dialect = dialect
        self._tokenchain = None

    @property
    def name(self):
        return self._objname

    @name.setter
    def set_name(self, object_name):
        if len(object_name) > 0 and self.name_is_valid(object_name):
            self._objname = object_name
        else:
            msg = f'Invalid {self.object_type} name: <{object_name}>!'
            raise msg

    def name_is_valid(self, aName):
        return True

    def reconstruct(self):
        pass


class SQLObjectFabric():
    def __init__(self, dialect:str=''):
        self._dialect = dialect;
        self._gallery = [];
        self._init_metadata()

    def _obj_metadata(self, obj_type:str, descriptors:list):
        md = {"object_type": obj_type, "descriptor_count": len(descriptors), "descriptors": descriptors }
        return md

    def _init_metadata(self):
        self._gallery.clear()
        omd=self._obj_metadata

        self._gallery.append(omd('Database',   ['DATABASE']))

        self._gallery.append(omd('Schema',     ['SCHEMA']))
        self._gallery.append(omd('ExtSchema',  ['EXTERNAL', 'SCHEMA']))

        self._gallery.append(omd('Table',      ['TABLE']))
        self._gallery.append(omd('TempTable',  ['TEMP', 'TABLE']))
        self._gallery.append(omd('TempTable',  ['TEMPORARY', 'TABLE']))
        self._gallery.append(omd('ExtTable',   ['EXTERNAL', 'TABLE']))

        self._gallery.append(omd('View',       ['VIEW']))
        self._gallery.append(omd('Function',   ['FUNCTION']))
        self._gallery.append(omd('StoredProc', ['STORED', 'PROCEDURE']))

    def getSQLObject(self, token_chain):
        obj=None
        objName=''
        # let's get rid of comments
        plain_tokens = token_chain.copy([], [TT_COMMENT])

        # if first word in the statement is 'CREATE' - create sql object
        if  str(plain_tokens.items[0].value).upper() == 'CREATE':

            for x in self._gallery:
                descriptor_found = True
                # Check if token(s) match current object type descriptor(s)
                for i in range(0, x['descriptor_count']):
                    if str(plain_tokens.items[i+1].value).upper()!=str(x['descriptors'][i]).upper():
                        descriptor_found = False
                        break

                if descriptor_found:
                    objName = x['object_type']
                    obj = type('SQLObject'+objName, (SQLObject,), {})(self._dialect)
                    obj._tokenchain = token_chain # copy ?
                    break
            
        return obj
