-----------------------------------------Script Header-------------------------------------
--Script Name                : plsql_block2.plsql
--Description                : For testing Oracle Test runner for PLSQL with bind variable
--Author                     : Mohit Gupta
--Bind Variables             : var_plsql_1(number)
--Passing Criteria SQL       : select c1 from  result_table2
--Passing Criteria value     : i am the check for number bind variable

--<PLSQL>
DECLARE
    test_var1 NUMBER;
    e_table_does_not_exist EXCEPTION;
    l_cnt PLS_INTEGER;
    sql_identifier VARCHAR2(100);
BEGIN
-- add your code here
--make sure ,errors are handled properly


    SELECT COUNT(*) INTO l_cnt  FROM
        user_tables
    WHERE
        upper(table_name) = upper('result_table2');

    IF ( l_cnt > 0 ) THEN -- check if table exists before attempt to delete
        sql_identifier := 'drop statement';
        EXECUTE IMMEDIATE ('drop table result_table2');
    END IF;
        test_var1 := var_plsql_1;
        sql_identifier := 'create statement';
        EXECUTE IMMEDIATE ( 'create table result_table2 as select ''i am the check for number bind variable'' as c1 from dual where 1 ='||test_var1 );


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