import logging
from datetime import datetime
from custom import basic_custom_actions as bca
from quod_qa.eq.Algo_Iceberg import QAP_3055, QAP_3054
from quod_qa.eq.Algo_Multilisted import QAP_1979, QAP_1977, QAP_1998, QAP_1974, QAP_1968, QAP_1969, QAP_1976, QAP_1975, QAP_1961, QAP_1960, QAP_1980, QAP_1959, QAP_1810, QAP_1952, QAP_1997, QAP_1996, QAP_1995, QAP_1992, QAP_2857, QAP_3019, QAP_3021, QAP_3022, QAP_3025, QAP_3027,QAP_1951, QAP_1990, QAP_3028
from quod_qa.eq.Algo_TWAP import QAP_1318, QAP_3121, QAP_3120
from rule_management import RuleManager
from stubs import Stubs
from MD_SOR import md

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

timeouts = False

channels = dict()

def test_run():
    # Generation id and time for test run
    report_id = bca.create_event('FiLL tests ' + datetime.now().strftime('%Y%m%d-%H:%M:%S'))
    logger.info(f"Root event was created (id = {report_id.id})")
    try:
        #md(report_id)
        QAP_1968.execute(report_id)
    except Exception:
        logging.error("Error execution",exc_info=True)

if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()
