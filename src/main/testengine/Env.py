__author__ = "Mohit Gupta"
__credits__ = []
__version__ = "1.0.1"
__maintainer__ = "Mohit Gupta"
__status__ = "Prototype"

import utils
from pathlib import Path
import json
from os import path
from datetime import datetime
import logging

global test_engine_log_file
global report_directory_name
import sys, os


def getProjectRoot():
    """Returns project root folder."""
    return Path(__file__).parent.parent.parent.parent


default_config_file = 'test.json'
default_project_path = getProjectRoot()
default_oracle_client = path.join(default_project_path, 'dbclients', 'instantclient_19_6')
default_config_path = path.join(default_project_path, 'config')
default_oracle_config_path = path.join(default_config_path, 'oracle')
default_script_path = path.join(default_project_path, 'src', 'main', 'testscripts',
                                'oracle')
default_control_table = path.join(default_script_path, "control_table.csv")
default_config_file = path.join(default_oracle_config_path, default_config_file)
default_target_path = path.join(default_project_path, 'target')
default_log_path = path.join(default_target_path, 'log')

command_line_args = utils.getCommandLineArgs()
os.environ["PATH"] = default_oracle_client
os.environ["LD_LIBRARY_PATH"] = default_oracle_client


def getEngineLogFileName():
    global test_engine_log_file
    date_time = datetime.today()
    test_engine_log_file = 'test-engine-' + utils.createStringDate(date_time) + '.log'
    test_engine_log_file = path.join(default_log_path, test_engine_log_file)
    return test_engine_log_file


def getConfigFile():
    try:
        config_file = command_line_args.CONFIG_FILE_NAME

    except FileNotFoundError:
        logging.error(f'[-] config_file is not available at {config_file} ')
        raise
    except:
        print(f'[-] could not get config file {config_file}')
        logging.error(f'test failed because of following error \n {sys.exc_info()[1]}')
        raise
    else:
        logging.info(f'collected script path as {config_file}')
        return config_file


def getScriptPath():
    try:
        script_path = command_line_args.SCRIPT_PATH_STRING

    except FileNotFoundError:
        logging.error(f'[-] control is not available at {script_path} ')
        raise

    except:
        print(f'[-] could not get script path script file {script_path} ')
        logging.error(f'could not get script path script file because of following error  \n {sys.exc_info()[1]}')
        raise
    else:
        logging.info(f'collected script path as {script_path}')
        return script_path


def getControlFile():
    try:
        control_file = command_line_args.CONTROL_FILE_NAME
        return control_file
    except FileNotFoundError:
        logging.error(f'control is not available at {control_file} ')
        raise


def getConfig():
    try:
        config_file = getConfigFile()
        print(config_file)
        with open(config_file) as json_config_file:
            config = json.load(json_config_file)
        return config
    except FileNotFoundError:
        print(
            '[-] config file could not be found . please make sure that file %s exists in config folder ' % config_file)
        raise


class environment:
    def __init__(self, config):
        self.user = config['user']
        self.password = config['password']
        self.connect_string = config['connect_string']

    def GetMainConnectString(self):
        return "%s/%s@%s" % (self.user, self.password, self.connect_string)
