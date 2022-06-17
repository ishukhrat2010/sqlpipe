# SQL-pipe project

## Purpose of the project

The purpose of the project is to create a CI tool for SQL database deployment. The main idea is to have a tool that generates script to transform database structure from *current DB state* to the state described by the particular git commit (usually the latest one).  The "current DB state" can be determined by either previous git commit or the actual state of the database at the deployment moment.

## Acceptance criteria
1. Multiple SQL dialects (or RDMBS types) are supported. E.g. MySQL, Postgress, Redshft, MS Transact-SQL, SQL ANSI-2000, etc.
2. git protocol support
3. Generated scripts are "data-loss safe"
4. Cloud-native
5. Best security practices
6.  - - - 

## High-level implementation logic
(placeholder)
