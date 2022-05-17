from ddlhelpers.parser import *
from ddlhelpers.sqlobjects import SQLObject


fName = '/Users/shawn.ismailov/Documents/projects/dbl-bigdata/BigData/SQL_Redshift/deepThought/DDL/table/gold/dim_district_dates.sql'


def do_test():
    #fName = '/Users/shawn.ismailov/Documents/projects/dbl-bigdata/BigData/SQL_Redshift/deepThought/DDL/table/gold/dim_district_dates.sql'
    #testing commit
    fName = '/Users/shawn.ismailov/Documents/projects/python-courses/sqlpipe/ddlhelpers/test_fp.txt'
    fp = FileProcessor(fName, ';')
    if fp._tokenizer._tokens != None:
        clear_tokens = fp._tokenizer.copy([], [TT_COMMENT])
        fp._tokenizer._tokenchain.load( clear_tokens)

        for x in fp._tokenizer.copy():
            print(x)

        myblocks = fp._tokenizer.split_tokens(
            'type', TT_END_OF_STATEMENT)
        for xx in myblocks:
            print('----------------------------------')
            if str(xx[0].value).upper() == 'CREATE' and str(xx[1].value).upper() == 'TABLE':
                myObj = SQLObject.from_tokens(xx)
                print(type(myObj))
                for y in xx:
                    print(y.value)
            else:
                for y in xx:
                    print(y.value)


if __name__ == "__main__":
    do_test()
