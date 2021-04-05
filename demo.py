import logging
from datetime import datetime
from custom import basic_custom_actions as bca
# from quod_qa.fx import  QAP_1746
# from quod_qa.fx import ui_tests, QAP_1746
from rule_management import RuleManager
from stubs import Stubs
from quod_qa.fx import ui_tests

# from test_cases import QAP_1552, QAP_585, QAP_2143, QAP_1560_class
# from test_cases import QAP_1552

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
        rm = RuleManager()
        # rm.add_RFQ('fix-fh-fx-rfq')
        # rm.add_RFQ('fix-fh-fx-rfq')
        # rm.remove_rules_by_id_range( 7,15)
        # rm.print_active_rules()


        ui_tests.execute(report_id)

        # QAP_568.execute(report_id)
        # QAP_1746.execute(report_id, test_cases['RFQ_example'])
        # QAP_1552.execute(report_id, test_cases['RFQ_example'])

    except Exception:
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()
