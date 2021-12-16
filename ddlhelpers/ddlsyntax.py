
DL_SPACE = 'SPC'
DL_NEWLINE = 'NL'
DL_TABULATOR = 'TAB'
DL_COMMENT = 'SLC'
DL_MULTILINE_COMMENT_START = 'MLCS'
DL_MULTILINE_COMMENT_END = 'MLCE'
DL_SINGLE_QUOTE = 'SQ'
DL_DOUBLE_QUOTE = 'DQ'
DL_COMMA = 'CM'
DL_COLON = 'CN'
DL_SEMICOLON = 'SCN'
DL_PARENTHESIS_OPEN = 'PTHO'
DL_PARENTHESIS_CLOSE = 'PTHC'
DL_CURLY_BRACE_OPEN = 'CBO'
DL_CURLY_BRACE_CLOSE = 'CBC'
DL_SQUARE_BRACE_OPEN = 'SQO'
DL_SQUARE_BRACE_CLOSE = 'SQC'


class BaseDelimiters:
    def __init__(self):
        self._delim_collection = {}
        self.init_collection()

    def init_collection(self):
        self._delim_collection[DL_SPACE] = ' '
        self._delim_collection[DL_NEWLINE] = '\n'
        self._delim_collection[DL_TABULATOR] = '\t'
        self._delim_collection[DL_COMMENT] = '--'
        self._delim_collection[DL_MULTILINE_COMMENT_START] = '/*'
        self._delim_collection[DL_MULTILINE_COMMENT_END] = '*/'
        self._delim_collection[DL_SINGLE_QUOTE] = '\''
        self._delim_collection[DL_DOUBLE_QUOTE] = '"'
        self._delim_collection[DL_COMMA] = ','
        self._delim_collection[DL_COLON] = ':'
        self._delim_collection[DL_SEMICOLON] = ':'
        self._delim_collection[DL_PARENTHESIS_OPEN] = '('
        self._delim_collection[DL_PARENTHESIS_CLOSE] = ')'
        self._delim_collection[DL_CURLY_BRACE_OPEN] = '{'
        self._delim_collection[DL_CURLY_BRACE_CLOSE] = '}'
        self._delim_collection[DL_SQUARE_BRACE_OPEN] = '['
        self._delim_collection[DL_SQUARE_BRACE_CLOSE] = ']'


class SyntaxRules(BaseDelimiters):

    def __init__(self):
        BaseDelimiters.__init__(self)
        self._delimiters = {}
        self.init_delimiters()

    def js(self, delim, exclude=False):
        if delim == None:
            return None
        else:
            return {"length": len(str(delim)), "exclude": exclude}

    def dla(self, delim, exclude=False):
        aValue = self.js(delim, exclude)
        if aValue != None:
            self._delimiters[delim] = aValue

    def init_delimiters(self):
        dc = self._delim_collection
        # print(dc)
        self.dla(dc[DL_SPACE], True)
        self.dla(dc[DL_COMMENT])
        self.dla(dc[DL_TABULATOR], True)
        # if self.convert_tab_to_delimiter == False:
        #    self.dla('\t', True)
        self.dla(dc[DL_NEWLINE], True)

        self.dla(dc[DL_COMMA])
        self.dla(dc[DL_COLON])
        self.dla(dc[DL_SEMICOLON])
        self.dla(dc[DL_PARENTHESIS_OPEN])
        self.dla(dc[DL_PARENTHESIS_CLOSE])
        self.dla(dc[DL_CURLY_BRACE_OPEN])
        self.dla(dc[DL_CURLY_BRACE_CLOSE])
        self.dla(dc[DL_SQUARE_BRACE_OPEN])
        self.dla(dc[DL_SQUARE_BRACE_CLOSE])
        self.dla(dc[DL_SINGLE_QUOTE])
        self.dla(dc[DL_DOUBLE_QUOTE])

    def _max_delim_size(self):
        mx = 0
        for v in self._delimiters.values():
            if v['length'] > mx:
                mx = v['length']
        return mx

    # def convert_tab_to_delimiter(self):
    #    return True

    # def ignore_comments(self):
    #    return True


if __name__ == "__main__":
    sr = SyntaxRules()
    print('\n')
    print('DEBUG DELIMITERS:')
    print('-----------------------------------------')
    print(sr._delimiters)
    print(f'max delim size = {sr._max_delim_size()}')
    print('-----------------------------------------')
