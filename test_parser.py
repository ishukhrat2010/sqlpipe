from ddlhelpers.parser import Tokenizer
from ddlhelpers.fileprocessor import FileReader


fName = '/Users/shawn.ismailov/Documents/projects/dbl-bigdata/BigData/SQL_Redshift/deepThought/DDL/table/gold/dim_district_dates.sql'


def do_test():
    global fName
    with open(fName) as f:
        fContent = f.read()
    myTok = Tokenizer(fContent)
    # 'create table customers(\n_id int,\n fullname varchar(100),\n primarykey(_id))')
    for x in myTok._tokens:
        print(x)


# do_test()

#fr = FileReader(fName)
# fr.readfile()

print(len('\t'))
