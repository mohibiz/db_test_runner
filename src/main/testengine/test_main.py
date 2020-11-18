__author__ = "Mohit Gupta"
__credits__ = []
__version__ = "1.0.1"
__maintainer__ = "Mohit Gupta"
__status__ = "Prototype"

import os, sys, ast, os.path, logging, unittest
import Executer
import Env
import utils
import Database

global oracle

config = Env.getConfig()
control_file = Env.getControlFile()
script_path = Env.getScriptPath()
control_data = utils.getCSVData(control_file)
connectionString = Env.environment(config["oracle"]).GetMainConnectString()
oracle = Database.Oracle(connectionString)
global test_engine_log_file


class oracleScriptTests(unittest.TestCase):
    def underTest(self, control_parameters):
        try:
            global oracle
            control_parameter_dict = processControlParameters(control_parameters)
            Executer.RunSqlScript(oracle, control_parameter_dict['script_file'],
                                  control_parameter_dict['input_variable'])
            Executer.validatePassingCriteria(oracle, control_parameter_dict['resultant_sql'],
                                             control_parameter_dict['passing_criteria'],
                                             control_parameter_dict['input_variable'])
        except AssertionError:
            logging.info(f'test failed because of following error \n {sys.exc_info()[1]}')
            raise
        else:
            logging.info(f'executed test for {test_name} and passed ')


class controlParameter:
    def __init__(self, csv_record):
        self.script_file = csv_record[1]['script_name']
        self.resultant_sql = csv_record[1]['resultant_sql']
        self.input_variable = csv_record[1]['input_variable']
        self.passing_criteria = csv_record[1]['passing_criteria']
        self.execution_flag = csv_record[1]['execution_flag']


def processControlParameters(control_parameters):
    try:
        script_file = os.path.join(script_path, control_parameters.script_file)
        input_variable = ast.literal_eval(control_parameters.input_variable)
        passing_criteria = control_parameters.passing_criteria
        if passing_criteria != 'NA':
            passing_criteria = ast.literal_eval(passing_criteria)
        resultant_sql = control_parameters.resultant_sql
        control_parameters_dict = {'script_file': script_file, 'input_variable': input_variable,
                                   'passing_criteria': passing_criteria, 'resultant_sql': resultant_sql}
    except:
        logging.error('could process control parameters because of following error %' % format(sys.exc_info()[1]))
    else:
        logging.info(f'processed control parameters for {test_name}')
    return control_parameters_dict


def getControlParameters(control_record):
    return controlParameter(control_record)


def createTest(control_record):
    def _createTest(self):
        try:
            self.underTest(control_record)
        except AssertionError:
            logging.info(f'executed test for {test_name} and failed with assertion error')
            raise
        except:
            logging.error(f'test failed with following error \n {sys.exc_info()[1]}')
            raise

    return _createTest


def getTestSuffix(csv_record):
    column_list = []
    column_index = 0
    try:
        for keys in (csv_record[1].keys()):

            column_list.append(csv_record[1][keys])
            column_index = column_index + 1
            if column_index == 4:
                break
        test_suffix = '_'.join(column_list)
    except:
        logging.error(
            f'Could not create test name based on csv record \n{test_name} \n because of following error \n {sys.exc_info()[1]}')
    else:
        logging.info(f'identified the test {test_suffix}  ')
    return test_suffix


for control_record in enumerate(control_data):
    control_parameters = getControlParameters(control_record)
    if control_parameters.execution_flag == 'Y':
        global test_name
        test_name = 'test_%s' % getTestSuffix(control_record)
        setattr(oracleScriptTests, test_name, createTest(control_parameters))
