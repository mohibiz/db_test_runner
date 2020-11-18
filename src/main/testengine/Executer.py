__author__ = "Mohit Gupta"
__credits__ = []
__version__ = "1.0.1"
__maintainer__ = "Mohit Gupta"
__status__ = "Prototype"

import logging
import os, sys, cx_Oracle, pytest
import Env
import conftest

global spoolFile
global report_directory_name

report_directory_name = conftest.report_directory_name


def parameterSubstitution(sqlStatement, parameterDict):
    try:
        for key in parameterDict:
            """ write input validation here
            TypeError: replace() argument 2 must be str, not int"""
            sqlStatement = sqlStatement.replace(key, str(parameterDict[key]))

    except:
        logging.error(f'test failed because of following error \n {sys.exc_info()[1]}')

    else:
        logging.info(f'parameter substitution was successful script')
        return sqlStatement


def RunSqlScript(connection, file_name, parameterDict):
    try:
        file = open(file_name, 'r')
        script = s = " ".join(file.readlines())
        global spoolFile
        spoolFile = initiateSpool(connection, file_name)

        if file_name.endswith('.sql'):
            processSqlScripts(file_name, connection, script, parameterDict)
        elif file_name.endswith('.plsql'):
            processPLSqlScripts(file_name, connection, script, parameterDict)
        else:
            message = f'No Script file not found for execution with name : {file_name}'
            logging.info(message)
            print(message)

    except FileNotFoundError as fnf:
        err, message = fnf.args
        print("[-] Error-Code:", fnf.errno)
        print("[-] Error-Message:", fnf.strerror)
        logging.error(f'File not found at {file_name}')
        raise
    except:
        sys.stderr.write("[-] Something bad happened: {0}\n"
                         .format(sys.exc_info()[1]))
        raise

    else:
        logging.info(f'script execution was successful : {file_name}  ')
        finaliseSpool(spoolFile)


def getSpoolFileName(script_file_name):
    spool_file_name = script_file_name.split('\\')[-1].split('.')[0]
    spool_file_name = spool_file_name + '.out'
    return spool_file_name


def processSqlScripts(file_name, connection, sql, parameterDict):
    sql = sql[sql.find("--<SQL>") + len("--<SQL>"):sql.find("--</SQL>")]
    sql = sql.split(';')

    for sql_statement in sql:
        sql_statement = sql_statement.strip()

        try:
            if not sql_statement.__len__() == 0 and not sql_statement.startswith('--'):
                cursor = connection.con.cursor()
                sqlStatement = parameterSubstitution(sql_statement, parameterDict)
                spoolFile.write(sqlStatement + '\n')
                cursor.execute(sqlStatement)

        except cx_Oracle.DatabaseError as exc:
            err, = exc.args
            print("\t[-] Script did not Execute: %s" % sqlStatement)
            print("\t[-]Oracle-Error-Code: %s and Oracle-Error-Message: %s " % (err.code, err.message))
            writeSpoolError(err, sqlStatement, spoolFile)
            raise
        except:
            sys.stderr.write("[-] Something bad happened: {0}\n"
                             .format(sys.exc_info()[1]))
            raise


def initiateSpool(connection, file_name):
    spool_file_name = getSpoolFileName(file_name)
    spool_file_name = os.path.join(Env.default_target_path, report_directory_name, spool_file_name)
    spool_file = connection.spool(str(spool_file_name))
    spool_file.write(f'\n [+]execution started for the test script {file_name} \n \n')
    return spool_file


def finaliseSpool(spool_file):
    spool_file.write(f'\n [+]execution completed for the test script  \n')


def writeSpoolError(err, script, spool_file):
    spool_to_write = "\n[-]Script did not Execute correctly : \n \t" + "\n[-]Oracle-Error-Code:" + str(
        err.code) + "\t Oracle-Error-Message:" + str(err.message) + '\n'
    spool_file.write(spool_to_write)


def processPLSqlScripts(file_name, connection, plsql, parameterDict):
    if plsql.__len__() != 0:

        try:
            cursor = connection.con.cursor()
            plsql_block = parameterSubstitution(plsql, parameterDict)
            spoolFile.write(plsql_block + '\n')
            cursor.execute(plsql_block)

        except cx_Oracle.DatabaseError as exc:
            err, = exc.args
            print("\t[-] Script did not Execute: %s" % plsql_block)
            print("\t[-]Oracle-Error-Code: %s and Oracle-Error-Message: %s " % (err.code, err.message))
            writeSpoolError(err, plsql_block, spoolFile)
            pytest.fail('script failed to execute correctly ')


def validatePassingCriteria(connection, resultant_sql, passing_criteria, input_dict):
    try:
        rs = connection.run_query(resultant_sql)
        if len(rs) == 0 and passing_criteria != 'NA':
            pytest.fail('no rows returned in resultant sql :' + str(resultant_sql) + ' but passing criteria is' + str(
                passing_criteria))

        elif len(rs) != 0 and passing_criteria == 'NA':
            pytest.fail('rows returned in resultant sql :' + str(resultant_sql) + ' but passing criteria is empty')
        else:
            for row in rs:
                assert row == passing_criteria, 'rows returned in resultant sql :' + str(resultant_sql) + ' as :' + str(
                    row) + ' which did not match ' + str(passing_criteria)
                break
    except cx_Oracle.DatabaseError as exc:
        err, = exc.args
        print("\t[-] Script did not Execute: %s" % resultant_sql)
        print("\t[-]Oracle-Error-Code: %s and Oracle-Error-Message: %s " % (err.code, err.message))
        writeSpoolError(err, resultant_sql, spoolFile)
        pytest.fail('script failed to execute correctly ')


def printDBMSOutput(cursor):
    chunk_size = 100
    lines_var = cursor.arrayvar(str, chunk_size)
    num_lines_var = cursor.var(int)
    num_lines_var.setvalue(0, chunk_size)
    while True:
        cursor.callproc("dbms_output.get_lines", (lines_var, num_lines_var))
        num_lines = num_lines_var.getvalue()
        lines = lines_var.getvalue()[:num_lines]
        for line in lines:
            print(line or "")
        if num_lines < chunk_size:
            break
