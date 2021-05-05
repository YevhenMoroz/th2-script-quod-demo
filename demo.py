import logging
from datetime import datetime
from custom import basic_custom_actions as bca
from quod_qa.eq.Sorping import QAP_2408
from rule_management import RuleManager
from schemas import rfq_tile_example
from stubs import Stubs
from quod_qa.fx import ui_tests
from quod_qa.eq.Care import QAP_1012
logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False

channels = dict()


def test_run():
    # Generation id and time for test run
    report_id = bca.create_event('Ziuban tests ' + datetime.now().strftime('%Y%m%d-%H:%M:%S'))
    logger.info(f"Root event was created (id = {report_id.id})")

    try:
        # QAP_1012.execute(report_id)
        QAP_2408.execute(report_id)
        # rm = RuleManager()
        # rm.add_NewOrdSingle_IOC("fix-bs-310-columbia","KEPLER","QDL1",False,2000,33)
    except Exception:
        logging.error("Error execution",exc_info=True)


if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()

