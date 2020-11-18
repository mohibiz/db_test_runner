-----------------------------------------Script Header-------------------------------------
--Script Name                : sqlblock4.sql
--Description                : For testing Oracle Test runner with one bind Variable and single value passing criteria
--Author                     : Mohit Gupta
--Bind Variables             : var1 (date)
--Passing Criteria SQL       : select * from sql_block4
--Passing Criteria value     : (test, )

--<SQL>

DROP TABLE sql_block4;
CREATE TABLE sql_block4 AS SELECT 'test' AS c1 FROM dual WHERE trunc(sysdate) = var1 ;

--</SQL>