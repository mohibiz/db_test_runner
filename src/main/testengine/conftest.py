#!/usr/bin/env python
__author__ = "Mohit Gupta"
__credits__ = []
__version__ = "1.0.1"
__maintainer__ = "Mohit Gupta"
__status__ = "Prototype"

import logging
import os
import os.path
import tempfile
from datetime import datetime
from pathlib import Path
from _pytest.nodes import Item
from _pytest.runner import CallInfo
import pytest
import utils
from _pytest.config import Config
from _pytest.main import Session
from _pytest.terminal import TerminalReporter

global report_directory_name
global FAILURES_FILE
global oracle
global test_engine_log_file
import Env


@pytest.hookimpl(tryfirst=True)
def pytest_sessionstart(session: Session):
    print("\n[*]starting test-engine session\n")


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item):
    global oracle
    print("[+]setting up testing env")


@pytest.hookimpl(trylast=True)
def pytest_sessionfinish(session, exitstatus):
    print("\n[*]  finished test-engine session")


def pytest_report_header(config):
    if config.getoption("verbose") > 0:
        return ["\n\n"
                "=======================================================================================================executing the tests====================================================  "]


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: Item, call: CallInfo):
    outcome = yield
    result = outcome.get_result()
    if result.when == "call" and result.failed:
        try:  # Just to not crash py.test reporting
            with open(str(FAILURES_FILE), "a") as f:
                f.write(result.nodeid + "\n")
        except Exception as e:
            print("ERROR", e)
            pass


@pytest.hookimpl(hookwrapper=True)
def pytest_terminal_summary(
        terminalreporter: TerminalReporter, exitstatus: int, config: Config
):
    # TerminalReporter.write(terminalreporter, content='testing termincal reporting')
    yield
    global FAILURES_FILE
    print(f"\n[+] Failures outputted to: {FAILURES_FILE}")
    print(f" to check failures..... run following command \nnotepad {FAILURES_FILE}")


@pytest.hookimpl(trylast=True)
def pytest_configure(config):
    print('[+] setting up pytest config')

    global FAILURES_FILE
    global report_directory_name
    report_directory_name = utils.createReportDirectoryStructure()
    FAILURES_FILE = Path(os.path.join(report_directory_name, 'failures.txt'))
    print(f'[+] creating directory for placing report artifacts {report_directory_name}')

    if FAILURES_FILE.exists():
        FAILURES_FILE.unlink()
    FAILURES_FILE.touch()
    tr = config.pluginmanager.getplugin('terminalreporter')
    if tr is not None:
        config._pytestsessionfile = tempfile.TemporaryFile('w+')
        oldwrite = tr._tw.write

        def tee_write(s, **kwargs):
            oldwrite(s, **kwargs)
            config._pytestsessionfile.write(str(s))

        tr._tw.write = tee_write


def pytest_unconfigure(config):
    if hasattr(config, '_pytestsessionfile'):
        config._pytestsessionfile.seek(0)
        sessionlog = config._pytestsessionfile.read()
        config._pytestsessionfile.close()
        del config._pytestsessionfile
        tr = config.pluginmanager.getplugin('terminalreporter')
        del tr._tw.__dict__['write']
        session_log_file = getLogFileName()
        print(f'\n[+] session log file is {session_log_file}')
        create_new_file(file=session_log_file, contents=sessionlog)


def getLogFileName():
    global report_directory_name

    date_time = utils.createStringDate(datetime.today())
    file_name = 'test_execution_' + str(date_time) + '.log'
    file_name = os.path.join(Env.getProjectRoot(), 'target', report_directory_name, file_name)
    logging.info(f'created session log of pyetest as {file_name}  ')
    return file_name


def create_new_file(file, contents):
    try:

        with open(file, 'w') as f:
            f.writelines(contents)
    except FileNotFoundError:
        print(f'[+] path to log directory could not be found {file}')
        raise
