#! usr/bin/local python
__author__ = "Mohit Gupta"
__credits__ = []
__version__ = "1.0.1"
__maintainer__ = "Mohit Gupta"
__status__ = "Prototype"

import sys
import argparse
import datetime
import os
import subprocess
import logging
import pandas
from datetime import datetime

import Env


def getCommandLineArgs():
    """
        get all the command line options into a single variable
    """
    parser = argparse.ArgumentParser(description="A Program to execute Oracle Scripts for Test")
    parser.add_argument('--config-file', dest='CONFIG_FILE_NAME',
                        type=str, default=Env.default_config_file, help="Name of the config file")

    parser.add_argument('--script-path', dest='SCRIPT_PATH_STRING',
                        type=str, default=Env.default_script_path,
                        help="Path for the folder or directory where sql /plsql scripts and control file are "
                             "located for execution")
    parser.add_argument('--control-file', dest='CONTROL_FILE_NAME', default=Env.default_control_table,
                        type=str, help="Name of the control file")
    args = parser.parse_args()
    return args


def getCSVData(file):
    try:
        # file = os.path.join(script_path, file)
        df = pandas.read_csv(file, sep='~').fillna('NA')
        print(df)
        dict_record = df.to_dict('index')
        input_list = []
        for dict in dict_record.values():
            input_list.append(dict)
    except ValueError as ve:
        err, = ve.args
        logging.error(f'something wrong with file setup.error occured {ve} ,recheck the file  {file} ')
        print(f'\n [-]recheck the file  {file} \n')
        raise
    except FileNotFoundError:
        logging.error(f'File not found  {file}')
        print(f'\n [-]File not found {file} \n')
        # raise
    else:
        logging.info(f'found control file : {file} \t processing it ')
        return input_list


def write_file(target_folder, file_name, file_text):
    try:
        if os.path.exists(target_folder):
            file = os.path.join(target_folder, file_name)
            with open(file, 'w') as fp:
                fp.write(file_text)
    except:
        logging.error(f'could not write to file  {file_name} because of the following error \n {sys.exc_info()[1]}')


def createDirectory(path):
    """TBD"""
    # if os.path.exists(path):
    try:
        os.mkdir(path)
    except OSError:
        print("Creation of the directory %s failed" % path)


def createStringDate(datetime):
    """TBD"""
    # str_date_time = str(datetime.today())
    str_date_time = str(datetime)
    str_date_time = str_date_time.replace(':', '-').replace(' ', '-')
    return str_date_time


def createReportDirectoryStructure():
    """TBD"""
    date_time = datetime.today()
    date_time = createStringDate(date_time)
    directory_name = 'report_' + str(date_time)
    directory_name = os.path.join(Env.default_target_path, directory_name)
    createDirectory(directory_name)
    return directory_name


def validate_file_option(self, args):
    """
        Validate the destination where files will be kept
    """
    try:
        self.output_path = args.output_path
        print("output destination set to %s" % self.output_path)
    except OSError:
        print("Creation of the directory %s failed" % self.output_path)
    else:
        pass


def ExecuteCmd(command):
    print("remote_cmd: " + command + "\n");
    output = subprocess.check_output(command, shell=True)
    print(output, "\n");
    return;


def StoreInDictionary(Dictionary, String, Delemeter='=', flag=0):
    mDictionary = Dictionary
    flag = String.count(Delemeter)
    if (String.find(Delemeter) != -1):
        if flag == 1:
            (mKey, mValue1) = String.split(Delemeter)
        else:
            (mKey, mValue1, mValue2) = String.split(Delemeter)
        if mValue1 not in mDictionary.values():
            mDictionary.setdefault(mKey, mValue1.rstrip())
    return;


def StoreInList(List, String, Delemeter):
    mList = List;
    if (String.find(Delemeter) != -1):
        (mKey, mValue) = String.split(Delemeter)
        mList.append(mKey);
    return;


def CfgFileReader(Dictionary, FileName, Delemeter='=', flag=0):
    mDictionary = Dictionary;
    mFileDescriptor = open(FileName, 'r')

    for Line in mFileDescriptor:
        StoreInDictionary(mDictionary, Line, Delemeter, flag);

    mFileDescriptor.close();
    return;
