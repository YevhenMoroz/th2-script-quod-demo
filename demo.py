import logging
import os
import platform
import socket
from datetime import datetime
from custom import basic_custom_actions as bca
from quod_qa.fx import QAP_1537, QAP_1544, QAP_1538, QAP_1539, QAP_1540, QAP_1541, QAP_1746
from rule_management import RuleManager
from stubs import Stubs
from test_cases import QAP_1552, QAP_585, QAP_2143

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False

channels = dict()


def test_run():
    # Generation id and time for test run
    report_id = bca.create_event(os.environ["COMPUTERNAME"] + ' tests ' + datetime.now().strftime('%Y%m%d-%H:%M:%S'))
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
        # QAP_585.execute(report_id)
        QAP_2143.execute(report_id, test_cases['RFQ_example'])
        rm = RuleManager()
        # rm.add_RFQ('fix-fh-fx-rfq')
        # rm.add_TRFQ('fix-fh-fx-rfq')
        rm.print_active_rules()


    except Exception:
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()
