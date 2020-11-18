-----------------------------------------Script Header-------------------------------------
--Script Name                : sqlblock1.sql
--Description                : For testing Oracle Test runner with one bind Variable and single value passing criteria
--Author                     : Mohit Gupta
--Bind Variables             : var_subcasenumber (varchar)
--Passing Criteria SQL       : select count(*) from sql_block1
--Passing Criteria value     : (25 )

--<SQL>

DROP TABLE sql_block1;
CREATE TABLE sql_block1 AS SELECT 'case_0001' FROM dual WHERE 'case_0001' = var_subcasenumber;

--</SQL>