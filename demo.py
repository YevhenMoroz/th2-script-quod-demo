import logging
from datetime import datetime
from custom import basic_custom_actions as bca
from rule_management import RuleManager
from schemas import rfq_tile_example
from stubs import Stubs
from quod_qa.fx.fx_taker_rfq import QAP_574, QAP_585, QAP_569,  QAP_578, QAP_579, QAP_580
from quod_qa.fx.fx_taker_rfq import QAP_574, QAP_585, QAP_569, QAP_578, QAP_579, QAP_580
from quod_qa.fx import ui_tests
logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False

channels = dict()


def test_run():
    # Generation id and time for test run
    report_id = bca.create_event('kbrit tests ' + datetime.now().strftime('%Y%m%d-%H:%M:%S'))
    logger.info(f"Root event was created (id = {report_id.id})")

    test_cases = {
        'RFQ_example': {
            **channels,
            'case_id': bca.create_event_id(),
            'TraderConnectivity': 'gtwquod5-fx',
            'Account': 'MMCLIENT1',
            'SenderCompID': 'QUODFX_UAT',
            'TargetCompID': 'QUOD5',
            }
        }

    try:

        # QAP_1746.execute(report_id, test_cases['RFQ_example'])
        ui_tests.execute(report_id)
        rm = RuleManager()

    except Exception:
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()

