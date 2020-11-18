-----------------------------------------Script Header-------------------------------------
--Script Name                : sqlblock3.sql
--Description                : For testing Oracle Test runner with multiple bind Variable and single value passing criteria
--Author                     : Mohit Gupta
--Bind Variables             : var1 (number) , var2 (varchar)
--Passing Criteria SQL       : select count(*) from sql_block3
--Passing Criteria value     : (1, )

--<SQL>

DROP TABLE sql_block3;
CREATE TABLE sql_block3 AS SELECT 'test' AS c1 FROM dual WHERE 1 = var1 and 'pass' = var2 ;

--</SQL>