__author__ = "Mohit Gupta"
__credits__ = []
__version__ = "1.0.1"
__maintainer__ = "Mohit Gupta"
__status__ = "Prototype"

import sys
import logging
import pytest
import Env


def main():
    try:
        global test_engine_log_file
        test_engine_log_file = Env.getEngineLogFileName()
        logging.basicConfig(filename=test_engine_log_file, level=logging.INFO, format='%(asctime)s %(message)s')
        logging.info('Started test engine')
        pytest.main(["-v", "--tb=native"])
    except:
        logging.error(f'test run failed with following error \n {sys.exc_info()[1]}')
    finally:
        logging.info('Finished test engine')


if __name__ == '__main__':
    main()
