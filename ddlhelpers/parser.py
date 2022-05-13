from ddlhelpers.ddlsyntax import *
from ddlhelpers.sqlobjects import *


# Token types
TT_PLAIN = 'TT_PLAIN'             # any word, either reserved or not
TT_SINGLE_QUOTED = 'TT_S_QUOTED'  # a token between single quotes
TT_DOUBLE_QUOTED = 'TT_D_QUOTED'  # a token between double quotes
TT_COMMENT = 'TT_COMMENT'         # a token between comment sign and end of line
TT_END_OF_STATEMENT = 'TT_EOS'    # token is the standard sql stament terminator

# this function replaces \t \r with space in the string
def clean_spaces(strValue):
    aValue = str(strValue).replace('\t', ' ')
    aValue = str(aValue).replace('\r', ' ')
    return aValue

# This class converts a text to a list of basic tokens
class BaseTokenizer(SyntaxRules):

    def __init__(self, content=''):
        SyntaxRules.__init__(self)
        self._tokens = None
        self._content = content

    # Searches for delimiters and returns the index of the leftmost delimiter
    def _contains_delimiter(self, aLine, expectedDelims=None):
        idx = -1
        delim = None
        delim_data = None
        min_idx = -1
        if expectedDelims != None:
            searchDelims = expectedDelims
        else:
            searchDelims = self._delimiters
        for dl in searchDelims:
            idx = str(aLine).find(dl)
            if idx == 0:  # delimiter is at the very beginning of the string
                delim = dl
                delim_data = searchDelims[dl]
                break
            elif idx > 0:
                # search for the leftmost delimiter
                if min_idx == -1 or idx < min_idx:
                    min_idx = idx
                    delim = dl
                    delim_data = searchDelims[dl]

        return (idx, delim, delim_data)

    # iterator function, produces next token from the content
    def gen_token(self, strValue):
        max_buf = self._max_delim_size()

        # returns token definition
        def _token(tValue, tLine, tPos, tokenType=TT_PLAIN):
            return {"Value": tValue,  "Line": tLine, "Pos": tPos, "TokenType": tokenType}

        # returns delimiter definition
        def single_delim_definition(aDelim, aExclude=False):
            result = {}
            sd = self._delim_collection[aDelim]
            result[sd] = {'length': len(sd), 'exclude': aExclude}
            return result

        # core of the tokenizer
        line_ofs = 0  # current line's offset in the input. E.g. line 1 has offset 0, line 3 offset 87
        chr_ofs = 0  # character's offset in the current line
        abs_ofs = 0  # abs_ofs = line_ofs + chr_ofs ; absolute offset in input
        str_accumulator = ''
        curTokenType = TT_PLAIN
        oldPos = 1
        line_no = 1
        expectedDelims = None

        while True:
            mychar = strValue[abs_ofs:abs_ofs+max_buf]
            (pos, dl, dl_data) = self._contains_delimiter(mychar, expectedDelims)

            if pos < 0:  # no delimiters were found
                str_accumulator = str_accumulator + mychar[:1]
                chr_ofs += 1
            else:  # Delimiter found
                str_accumulator = str_accumulator + mychar[:pos]
                if len(str_accumulator) > 0:
                    yield(_token(str_accumulator, line_no, oldPos, curTokenType))
                    str_accumulator = ''
                chr_ofs += pos
                oldPos = chr_ofs+1

                if dl == self._delim_collection[DL_COMMENT]:
                    # switch to 'comment' mode;
                    # from now scan for newline delimiter in order to switch back to 'plain' mode
                    expectedDelims = single_delim_definition(DL_NEWLINE, True)
                    curTokenType = TT_COMMENT

                elif dl == self._delim_collection[DL_SINGLE_QUOTE]:
                    if curTokenType == TT_PLAIN:
                        # switch to block 'string literal' mode (single quoted);
                        # from now scan for another single quote to switch back to 'plain' mode
                        expectedDelims = single_delim_definition(
                            DL_SINGLE_QUOTE)
                        curTokenType = TT_SINGLE_QUOTED
                    elif curTokenType == TT_SINGLE_QUOTED:
                        # switch back to 'plain' mode
                        expectedDelims = None

                elif dl == self._delim_collection[DL_DOUBLE_QUOTE]:
                    if curTokenType == TT_PLAIN:
                        # switch to block 'string literal' mode (double quoted);
                        # from now scan for another double quote to switch back to 'plain' mode
                        expectedDelims = single_delim_definition(
                            DL_DOUBLE_QUOTE)
                        curTokenType = TT_DOUBLE_QUOTED
                    elif curTokenType == TT_DOUBLE_QUOTED:
                        # switch back to 'plain' mode
                        expectedDelims = None

                if dl_data['exclude'] == False:
                    if (dl == self._delim_collection[DL_SEMICOLON]) and (curTokenType == TT_PLAIN):
                        ctt = TT_END_OF_STATEMENT
                    else:
                        ctt = curTokenType
                    yield(_token(dl, line_no, oldPos, ctt))
                chr_ofs += dl_data['length']

                if (dl == self._delim_collection[DL_NEWLINE]) and (curTokenType in [TT_PLAIN, TT_COMMENT]):
                    line_no += 1
                    line_ofs += chr_ofs
                    chr_ofs = 0
                    curTokenType = TT_PLAIN
                    expectedDelims = None

                elif dl == self._delim_collection[DL_SINGLE_QUOTE] and expectedDelims == None:
                    # switch back to 'plain' mode from single quoted
                    curTokenType = TT_PLAIN

                elif dl == self._delim_collection[DL_DOUBLE_QUOTE] and expectedDelims == None:
                    # switch back to 'plain' mode from double quoted
                    curTokenType = TT_PLAIN

                oldPos = chr_ofs+1

            # ----------------------------
            abs_ofs = line_ofs + chr_ofs

            if mychar == '':
                break

        if str_accumulator != '':
            yield _token(str_accumulator, line_no, oldPos, curTokenType)

    def copy_tokens(self, includeTokenType: list = [], excludeTokenType: list = []):

        def isListed(aToken, TokenList) -> bool:
            result = aToken['TokenType'] in TokenList
            return result
        if len(excludeTokenType) == 0:
            new_list = [token.copy() for token in self._tokens]
        else:
            new_list = [token.copy() for token in self._tokens if not isListed(
                token, excludeTokenType)]

        if len(includeTokenType) != 0:
            new_list = [token.copy() for token in self._tokens if isListed(
                token, includeTokenType)]
        return new_list

    def split_tokens(self, tkey, tvalue, includeSplitter=False):
        result = []
        indexList = [self._tokens.index(x)
                     for x in self._tokens if x[tkey] == tvalue]

        # print(indexList)
        i2 = 0
        startIdx = 0
        endIdx = 0
        tCount = len(self._tokens)

        #print(f'Total tokens: {tCount}')
        while startIdx+1 <= tCount:

            if i2+1 <= len(indexList):
                endIdx = indexList[i2]
            else:
                endIdx = tCount+1

            if startIdx >= endIdx:
                #print(startIdx, endIdx, 'break condition triggered')
                break

            if includeSplitter == True:
                endIdx += 1
            #print(startIdx, endIdx)
            temp_list = self._tokens[startIdx:endIdx]
            if len(temp_list) > 0:
                result.append([x.copy() for x in temp_list])

            # -----
            startIdx = endIdx
            if includeSplitter == False:
                startIdx += 1
            i2 += 1

        # ----------
        return result

class TokenChain:

    def __init__(self, tokens: list):
        self._tokens=[]


class Tokenizer(BaseTokenizer):

    def __init__(self, content=''):
        BaseTokenizer.__init__(self, content)

    # returns list of tokens, calls iterator function
    def tokenize(self, _debug=False):
        self._tokens = list(self.gen_token(str(self._content)))

# This class reads the file and tokenizes it
class FileProcessor:
    def __init__(self, filename, object_delimiter):
        self.filename = filename
        self.object_delimiter = object_delimiter
        self._tokenizer = Tokenizer()
        self.tokenize()

    def tokenize(self):
        with open(self.filename) as f:
            try:
                self._tokenizer._content = f.read()

                self._tokenizer.tokenize()
            finally:
                f.close()


# class ddlObject:
#     def __init__(self, sqlText=''):
#         self._sqlText = sqlText


# -------------------------------------------
if __name__ == "__main__":
    # myTokenizer = Tokenizer(
    #    'create table customers(\n_id int,\n fullname varchar(100),\n primary key(_id))')
    # print(myTokenizer._tokens)

    #fName = '/Users/shawn.ismailov/Documents/projects/dbl-bigdata/BigData/SQL_Redshift/deepThought/DDL/table/gold/dim_district_dates.sql'
    fName = '/Users/shawn.ismailov/Documents/projects/python-courses/sqlpipe/ddlhelpers/test_fp.txt'
    fp = FileProcessor(fName, ';')
    if fp._tokenizer._tokens != None:
        clear_tokens = fp._tokenizer.copy_tokens([], [TT_COMMENT])
        fp._tokenizer._tokens = clear_tokens

        for x in fp._tokenizer._tokens:
            print(x)

        myblocks = fp._tokenizer.split_tokens(
            'TokenType', TT_END_OF_STATEMENT)
        for xx in myblocks:
            print('----------------------------------')
            if str(xx[0]['Value']).upper() == 'CREATE' and str(xx[1]['Value']).upper() == 'TABLE':
                myObj = SQLObject.from_tokens(xx)
            else:
                for y in xx:
                    print(y['Value'])
