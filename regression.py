from regression_cycle import algo_regression
from stubs import Stubs
import logging
from custom import basic_custom_actions as bca
from datetime import datetime
import os

logging.basicConfig(format='%(asctime)s - %(message)s')


def regression_run(name, algo=True, equity=True, forex=True, retail=True, web_admin=True):
    logging.getLogger().setLevel(logging.WARN)
    report_id = bca.create_event(name + datetime.now().strftime('%Y%m%d-%H:%M:%S'))
    try:
        start = datetime.now()
        print(f'start time = {start}')

        if algo:
            algo_regression.test_run(report_id)
        #if equity:
            #eq_regression.test_run(report_id)
        #if forex:
            #fx_regression.test_run(report_id)
        #if retail:
            #retail_regression.test_run(report_id)
        #if web_admin:
            #web_admin_regression.test_run(report_id)

        print('duration time = ' + str(datetime.now() - start))
    except Exception:
        logging.error("Error execution", exc_info=True)


print(os.enviroment['NAME'])

if __name__ == '__main__':
    regression_run(name=os.enviroment['NAME'], algo=os.enviroment['ALGO'], equity=os.enviroment['OMS'], forex=os.enviroment['FOREX'], retail=os.enviroment['RETAIL'], web_admin=os.enviroment['WEB_ADMIN'])
    Stubs.factory.close()
