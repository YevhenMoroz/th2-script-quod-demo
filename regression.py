from regression_cycle import retail_regression
from stubs import Stubs
import logging
from custom import basic_custom_actions as bca
from datetime import datetime

from win_gui_modules.utils import set_session_id, prepare_fe, get_opened_fe
from win_gui_modules.wrappers import set_base

logging.basicConfig(format='%(asctime)s - %(message)s')


def test_run(name, retail=True):
    report_id = bca.create_event(name + datetime.now().strftime('%Y%m%d-%H:%M:%S'))
    try:
        start = datetime.now()
        print(f'start time = {start}')
        if retail:
            retail_regression.test_run(report_id)
        print('duration time = ' + str(datetime.now() - start))
    except Exception:
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    test_run('5.1.135.148 |Retail_Regression| i_rovchak', retail=True)
    Stubs.factory.close()

