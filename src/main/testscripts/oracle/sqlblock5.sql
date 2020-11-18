-----------------------------------------Script Header-------------------------------------
--Script Name                : sqlblock5.sql
--Description                : For testing Oracle SQL in Test runner with one bind Variable and Multiple value in passing criteria
--Author                     : Mohit Gupta
--Bind Variables             : var1 (date)
--Passing Criteria SQL       : select count(*) from sql_block5
--Passing Criteria value     : (1,'i am correct')

--<SQL>

DROP TABLE sql_block5;
CREATE TABLE sql_block5 AS SELECT 1 AS c1 , 'i am correct' AS c2 FROM dual WHERE 1 = var1;

--</SQL>