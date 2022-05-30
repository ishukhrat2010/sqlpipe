from ddlhelpers.parser import *
from ddlhelpers.sqlobjects import SQLObjectFabric


fName = '/Users/shawn.ismailov/Documents/projects/dbl-bigdata/BigData/SQL_Redshift/deepThought/DDL/table/gold/dim_district_dates.sql'


def do_test():
    #fName = '/Users/shawn.ismailov/Documents/projects/dbl-bigdata/BigData/SQL_Redshift/deepThought/DDL/table/gold/dim_district_dates.sql'
    #testing commit
    fName = '/Users/shawn.ismailov/Documents/projects/python-courses/sqlpipe/ddlhelpers/test_fp.txt'
    fp = FileProcessor(fName, ';')

    #fp._tokenizer._tokenchain.load( clear_tokens)

    for x in fp._tokenizer.token_chain.items:
        print(x)

    myblocks = fp._tokenizer.split_tokens(
        'type', TT_END_OF_STATEMENT, True)

    myFabric = SQLObjectFabric('ANSI-92')

    for xx in myblocks:
        print('----------------------------------')

        myObj = myFabric.getSQLObject(xx)
        print(myObj)


if __name__ == "__main__":
    do_test()
