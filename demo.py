import logging
from datetime import datetime
from custom import basic_custom_actions as bca
from quod_qa.fx import clone
from quod_qa.fx.fx_mm_esp import QAP_2990
from quod_qa.fx.fx_mm_positions import QAP_2500
from quod_qa.fx.fx_mm_rfq import QAP_1537, QAP_1539, QAP_2345, QAP_1746, QAP_1978, QAP_2089, QAP_2055, QAP_2090, \
    QAP_1755, QAP_2103
from quod_qa.fx.qs_fx_routine import rfq
from rule_management import RuleManager
from stubs import Stubs
from win_gui_modules.utils import set_session_id

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False

channels = dict()

def fx_mm_esp_fix(report_id):
    pass
    # QAP_1518.execute(report_id)
    # QAP_1558.execute(report_id)
    # QAP_1559.execute(report_id)
    # QAP_2797.execute(report_id)
    # QAP_2082.execute(report_id)
    # QAP_2084.execute(report_id)
    # QAP_2086.execute(report_id)
    # QAP_2085.execute(report_id)
    # QAP_2079.execute(report_id)
    # QAP_3841.execute(report_id)
    # QAP_1554.execute(report_id)
    # QAP_1597.execute(report_id)
    # QAP_3390.execute(report_id)
    # QAP_2750.execute(report_id)
    # QAP_2823.execute(report_id)
    # QAP_2874.execute(report_id)
    # QAP_2876.execute(report_id)
    # QAP_2880.execute(report_id)
    # QAP_2879.execute(report_id)
    # QAP_2873.execute(report_id)
    # QAP_2872.execute(report_id)
    # QAP_2966.execute(report_id)
    # QAP_3848.execute(report_id)
    # QAP_2012.execute(report_id)
    # QAP_2082.execute(report_id)

def fx_mm_rfq_fix(report_id):
    QAP_1746.execute(report_id)
    QAP_1978.execute(report_id)
    QAP_2089.execute(report_id)
    QAP_2090.execute(report_id)
    QAP_1755.execute(report_id)


def test_run():
    # Generation id and time for test run

    # report_id = bca.create_event(' tests ' + datetime.now().strftime('%Y%m%d-%H:%M:%S'))

    report_id = bca.create_event('KKL    ' + datetime.now().strftime('%Y%m%d-%H:%M:%S'))

    logger.info(f"Root event was created (id = {report_id.id})")


    test_cases = {
        'case_id': bca.create_event_id(),
        'TraderConnectivity': 'fix-ss-rfq-314-luna-standard',
        'Account': 'Iridium1',
        'SenderCompID': 'QUODFX_UAT',
        'TargetCompID': 'QUOD5',
    }
    session_id=set_session_id()
    try:
        # QAP_2089.execute(report_id)
        QAP_2500.execute(report_id,session_id)
        # QAP_2103.execute(report_id)





        # clone.execute(report_id)
        # test.execute(report_id)
        # SendMD.execute(report_id)
        # QAP_2750.execute(report_id)
        # QAP_1560.execute(report_id)
        # QAP_2825.execute(report_id)

        # QAP_1012.execute(report_id)
        # not_ready_QAP_1597.TestCase(report_id).execute()
        # frommeth.execute(report_id)
        # test.execute(report_id)
        # QAP_2082.TestCase(report_id).execute()
        # QAP_1520.TestCase(report_id).execute()




        # QAP_2797.TestCase(report_id).execute()

        # QAP_2956.execute('QAP-2956', report_id, test_cases['QAP-2956'])
        # QAP_1746.execute(report_id, test_cases['RFQ_example'])
        # TEST_QAP_2000.execute(report_id)
        # QAP_585.execute(report_id)
        # QAP_568.execute(report_id)
        # QAP_569.execute(report_id)
        # QAP_570.execute(report_id)
        # testing.execute(report_id)
        # QAP_574.execute(report_id)
        # QAP_578.execute(report_id)
        # QAP_579.execute(report_id)
        # QAP_580.execute(report_id)

        # rfq_tile_example.execute(report_id)
        #
        # rm = RuleManager()
        # rm.add_RFQ('fix-bs-rfq-314-luna-standard')
        # rm.print_active_rules()
        # rm.remove_rule_by_id()


    except Exception:
        logging.error("Error execution",exc_info=True)
   # try:
#

#
   #     rm.print_active_rules()
#
    #   ui_tests.execute(report_id)

    #except Exception:
        #logging.error("Error execution", exc_info=True)

if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()








