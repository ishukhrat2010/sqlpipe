
# Standard delimiter codes 
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


class StandardDelimiters:
    def __init__(self):
        self._std_delims = {}
        self.init_collection()

    # Standard delimiters collection
    def init_collection(self):
        self._std_delims[DL_SPACE] = ' '
        self._std_delims[DL_NEWLINE] = '\n'
        self._std_delims[DL_TABULATOR] = '\t'
        self._std_delims[DL_COMMENT] = '--'
        self._std_delims[DL_MULTILINE_COMMENT_START] = '/*'
        self._std_delims[DL_MULTILINE_COMMENT_END] = '*/'
        self._std_delims[DL_SINGLE_QUOTE] = '\''
        self._std_delims[DL_DOUBLE_QUOTE] = '"'
        self._std_delims[DL_COMMA] = ','
        self._std_delims[DL_COLON] = ':'
        self._std_delims[DL_SEMICOLON] = ';'
        self._std_delims[DL_PARENTHESIS_OPEN] = '('
        self._std_delims[DL_PARENTHESIS_CLOSE] = ')'
        self._std_delims[DL_CURLY_BRACE_OPEN] = '{'
        self._std_delims[DL_CURLY_BRACE_CLOSE] = '}'
        self._std_delims[DL_SQUARE_BRACE_OPEN] = '['
        self._std_delims[DL_SQUARE_BRACE_CLOSE] = ']'


class SyntaxRules(StandardDelimiters):

    def __init__(self):
        BaseDelimiters.__init__(self)
        self._delimiter_metadata = {}
        self.init_delimiters()

    # Create dictionary for delimiter attributes, can be overriden in the successor class
    def _delim_attr( self, delim, exclude=False):
        if delim == None:
            return None
        else:
            delim_dict = {"length": len(str(delim)), # length of delimiter
                          "exclude": exclude}        # exclude delimiter value from parsing result
            return delim_dict

    # set delimiter's  metadata
    def _dlm(self, delim, exclude=False):

        md = self._delim_attr(delim, exclude)
        if md != None:
            self._delimiter_metadata[delim] = md

    def init_delimiters(self):
        dc = self._std_delims
        # print(dc)
        self._dlm(dc[DL_SPACE], True)
        self._dlm(dc[DL_COMMENT])
        self._dlm(dc[DL_TABULATOR], True)
        # if self.convert_tab_to_delimiter == False:
        #    self._dlm('\t', True)
        self._dlm(dc[DL_NEWLINE], True)

        self._dlm(dc[DL_COMMA])
        self._dlm(dc[DL_COLON])
        self._dlm(dc[DL_SEMICOLON])
        self._dlm(dc[DL_PARENTHESIS_OPEN])
        self._dlm(dc[DL_PARENTHESIS_CLOSE])
        self._dlm(dc[DL_CURLY_BRACE_OPEN])
        self._dlm(dc[DL_CURLY_BRACE_CLOSE])
        self._dlm(dc[DL_SQUARE_BRACE_OPEN])
        self._dlm(dc[DL_SQUARE_BRACE_CLOSE])
        self._dlm(dc[DL_SINGLE_QUOTE])
        self._dlm(dc[DL_DOUBLE_QUOTE])

    # return maximum length of delimiters in collection
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
