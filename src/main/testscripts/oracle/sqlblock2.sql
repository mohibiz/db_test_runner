-----------------------------------------Script Header-------------------------------------
--Script Name                : sqlblock2.sql
--Description                : For testing Oracle Test runner with one bind Variable and single value passing criteria
--Author                     : Mohit Gupta
--Bind Variables             : var1 (number)
--Passing Criteria SQL       : select count(*) from sql_block2
--Passing Criteria value     : (1, )

--<SQL>

DROP TABLE sql_block2;
CREATE TABLE sql_block2 AS SELECT 0 AS c1 FROM dual WHERE 1 = var1 ;

--</SQL>