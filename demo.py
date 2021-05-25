import logging
from datetime import datetime
from custom import basic_custom_actions as bca
from quod_qa.fx.fx_mm_esp.quickFix_tests import QAP_1597, QAP_4094, QAP_3555_bloked, SendMD, QAP_3390

from stubs import Stubs
from test_cases import QAP_638
from quod_qa.eq.Care import QAP_4015

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False

channels = dict()


def test_run():
    # Generation id and time for test run
    report_id = bca.create_event(' vskulinec  tests ' + datetime.now().strftime('%Y%m%d-%H:%M:%S'))
    logger.info(f"Root event was created (id = {report_id.id})")

    try:
        QAP_4015.execute(report_id)
        test_cases =  {
                'case_id': bca.create_event_id(),
                'TraderConnectivity': 'gtwquod5-fx',
                'Account': 'MMCLIENT1',
                'SenderCompID': 'QUODFX_UAT',
                'TargetCompID': 'QUOD5',
                }

        # rm = RuleManager()
        # # rm.remove_rules_by_id_range(5,150)
        # # rm.add_RFQ('fix-fh-fx-rfq')
        # # rm.add_TRFQ('fix-fh-fx-rfq')
        # # rm.print_active_rules()
        # # ui_tests.execute(report_i)
        # start = datetime.now()
        # print(f'start time = {start}')
        #
        # # fix_demo.execute(report_id,test_cases)
        # ui_tests.execute(report_id)
        # # QAP_1520.TestCase(report_id).execute()
        # # QAP_636.execute(report_id)
        # print("1 - done")
        # print('duration time = ' + str(datetime.now() - start), str(report_id))inec



    except Exception:
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()

