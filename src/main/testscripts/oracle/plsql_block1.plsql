-----------------------------------------Script Header-------------------------------------
--Script Name                : plsql_block1.plsql
--Description                : For testing Oracle Test runner for PLSQL with one bind variable
--Author                     : Mohit Gupta
--Bind Variables             :
--Passing Criteria SQL       : select c1 from  result_table1
--Passing Criteria value     : hello there

--<PLSQL>
DECLARE
    e_table_does_not_exist EXCEPTION;
    l_cnt PLS_INTEGER;
    sql_identifier VARCHAR2(100);
BEGIN
-- add your code here
--make sure ,errors are handled properly

    SELECT COUNT(*) INTO l_cnt  FROM
        user_tables
    WHERE
        upper(table_name) = upper('result_table1');

    IF ( l_cnt > 0 ) THEN
        sql_identifier := 'drop statement';
        EXECUTE IMMEDIATE ('drop table result_table1');
    END IF;

        sql_identifier := 'create statement';
        EXECUTE IMMEDIATE ( 'create table result_table1 as select ''hello there'' as c1 from dual' );
        DBMS_OUTPUT.PUT_LINE(sql_identifier||' completed '  );


EXCEPTION
   /* A named handler */
   WHEN e_table_does_not_exist
   THEN
      DBMS_OUTPUT.PUT_LINE(sql_identifier||' Table could not be create , Please check the script and rerun if necessary' );

     WHEN OTHERS
     THEN
        RAISE;
END;

--</PLSQL>