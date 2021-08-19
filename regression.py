from regression_cycle import retail_regression, fx_regression, algo_regression, eq_regression
from stubs import Stubs
import logging
from custom import basic_custom_actions as bca
from datetime import datetime


logging.basicConfig(format='%(asctime)s - %(message)s')

def test_run(name ,algo = True, equity = True, forex = True, retail = True):
    report_id = bca.create_event(name + datetime.now().strftime('%Y%m%d-%H:%M:%S'))
    try:
        if algo:
            algo_regression.test_run(report_id)
        if equity:
            eq_regression.test_run(report_id)
        if forex:
            fx_regression.test_run(report_id)
        if retail:
            retail_regression.test_run(report_id)
    except Exception:
        logging.error("Error execution", exc_info=True)



if __name__ == '__main__':
    test_run('5.1.130.149|Regression|')
    #test_run('5.1.132.145|Redburn Tests|')  #RB
    Stubs.factory.close()