# SQL-pipe project

## Purpose of the project

The purpose of the project is to create a CI tool for SQL database deployment. The main idea is to have a tool that generates script to transform database structure from *current DB state* to the state described by the particular git commit (usually the latest one).  The "current DB state" can be determined by either previous git commit or the actual state of the database at the deployment moment.

## Acceptance criteria
1. Multiple SQL dialects (or RDMBS types) are supported. E.g. MySQL, Postgress, Redshft, MS Transact-SQL, SQL ANSI-2000, etc.
2. git protocol support
3. Generated scripts are "data-loss safe"
4. Cloud-aware
5. Best security practices


## High-level implementation logic

### Scenario A (pessimistic approach)
The application considers current state of database as unknown and scans database structure every time.   
The application receives git commit reference to the repo with sql-scripts, connects to RDBMS and analyses differences between DDLs in the repo and what is found in database. As a result of the analysis, a sql-script is generated to create, alter or drop objects in database so that it mirrors the repository.  
Pro: 
 - always brings DB to the repo state
 - idempotent 
 - don't need to store DB meta-data
Con:
 - scans DB everytime (time consuming)
 - 'parallel' deployment on the same DB is impossible (TBD)


### Scenario B (ultra-optimistic approach)
The application receives git commit reference and generates migration scripts only for those sql-objects that were changed by commit. 
Pro:
 - parallel deployment of non-overlapping pieces
 - faster, doesn't spend time on untouched objects
Con:
 - Complex diff-algorythm

### Scenario C ()
