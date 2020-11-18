__author__ = "Mohit Gupta"
__credits__ = []
__version__ = "1.0.1"
__maintainer__ = "Mohit Gupta"
__status__ = "Prototype"

import cx_Oracle, logging


class Oracle(object):
    def __init__(self, conneciton_string):
        self.spoolFile = None
        try:
            self.con = cx_Oracle.connect(conneciton_string)
            print('Oracle connection successful')
        except cx_Oracle.DatabaseError as exc:
            err, = exc.args
            print("\t[-] Could not connect to Database using connection string : %s" % conneciton_string)
            print("\t[-]Oracle-Error-Code: %s and Oracle-Error-Message: %s " % (err.code, err.message))
            raise
        else:
            logging.info('connected to target oracle database')

    def spool(self, file_name):
        self.spoolFile = open(file_name, "w")
        return self.spoolFile

    def run_sql(self, sql_statement):
        cursor = cx_Oracle.Cursor(self.con)
        cursor.execute(sql_statement)
        return cursor

    def run_query(self, sql_statement):
        cursor = cx_Oracle.Cursor(self.con)
        cursor.prepare(sql_statement)
        rs = cursor.execute(None).fetchall()
        return rs

    def run_dml(self, dml_statement):
        cursor = cx_Oracle.Cursor(self.con)
        cursor.executemany(dml_statement)

    def run_ddl(self, ddl):
        cursor = cx_Oracle.Cursor(self.con)
        cursor.execute(ddl)
