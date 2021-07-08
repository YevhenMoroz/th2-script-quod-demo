import logging
from datetime import datetime
from custom import basic_custom_actions as bca
from rule_management import RuleManager
from stubs import Stubs
from test_cases import QAP_1557, QAP_2715, QAP_5

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False

channels = dict()


def test_run():
    # Generation id and time for test run
    report_id = bca.create_event(' kbrit validate th2 ' + datetime.now().strftime('%Y%m%d-%H:%M:%S'))
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

        # QAP_1557.TestCase(report_id).execute()
        QAP_5.TestCase(report_id).execute()
        # QAP_2715.TestCase(report_id).execute()
        # rm = RuleManager()
        # rm.add_fx_md_to('fix-fh-fx-esp')
        # rm.print_active_rules()

    except Exception:
        logging.error("Error execution",exc_info=True)
   # try:
#

#
    #   ui_tests.execute(report_id)

    #except Exception:
        #logging.error("Error execution", exc_info=True)

if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()

