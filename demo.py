import logging
from datetime import datetime
from custom import basic_custom_actions as bca
from quod_qa.fx import ui_tests
from rule_management import RuleManager
from schemas import rfq_tile_example
from stubs import Stubs
from quod_qa.fx.fx_taker_rfq import (QAP_574, QAP_585, QAP_569, QAP_578, QAP_579, QAP_580, QAP_611, QAP_596, QAP_589,
                                     QAP_590, QAP_591, QAP_593, QAP_597, QAP_599)
from quod_qa.fx.fx_taker_rfq import QAP_574, QAP_585, QAP_569, QAP_578, QAP_579, QAP_580
from test_cases import QAP_2129

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False

channels = dict()


def test_run():
    # Generation id and time for test run
    report_id = bca.create_event('kbrit tests ' + datetime.now().strftime('%Y%m%d-%H:%M:%S'))
    logger.info(f"Root event was created (id = {report_id.id})")

    try:

        rm = RuleManager()
        # rm.remove_rules_by_id_range(4,150)
        # rm.add_RFQ('fix-fh-fx-rfq')
        # rm.add_TRFQ('fix-fh-fx-rfq')
        rm.print_active_rules()
        start = datetime.now()
        print(f'start time = {start}')

        ui_tests.execute(report_id)
        print("1 - done")
        print('duration time = ' + str(datetime.now() - start))

        # QAP_2129.execute(report_id)


    except Exception:
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()

