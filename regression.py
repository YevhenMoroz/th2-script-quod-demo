from regression_cycle import algo_regression
from stubs import Stubs
import logging
from custom import basic_custom_actions as bca
from datetime import datetime

logging.basicConfig(format='%(asctime)s - %(message)s')


def test_run(name, algo=True, equity=False, forex=False, retail=False, web_admin=False):
    report_id = bca.create_event(name + datetime.now().strftime('%Y%m%d-%H:%M:%S'))
    try:
        start = datetime.now()
        print(f'start time = {start}')

        if algo:
            algo_regression.test_run(report_id)
        # if equity:
        #     eq_regression.test_run(report_id)
        # if forex:
        #     fx_regression.test_run(report_id)
        # if retail:
        #     retail_regression.test_run(report_id)
        # if web_admin:
        #     web_admin_regression.test_run(report_id)


        print('duration time = ' + str(datetime.now() - start))
    except Exception:
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    test_run('5.1.142.155|Regression|', algo=True, equity=False,forex=False, retail=False, web_admin=False)
    Stubs.factory.close()

