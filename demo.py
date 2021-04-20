import logging
from datetime import datetime
from custom import basic_custom_actions as bca
from quod_qa.fx import ui_tests, fix_demo
from rule_management import RuleManager
from schemas import rfq_tile_example
from stubs import Stubs
from quod_qa.fx.fx_taker_rfq import (QAP_574, QAP_585, QAP_569, QAP_578, QAP_579, QAP_580, QAP_611, QAP_596, QAP_589,
                                     QAP_590, QAP_591, QAP_593, QAP_597, QAP_599)
from quod_qa.fx.fx_taker_rfq import QAP_574, QAP_585, QAP_569, QAP_578, QAP_579, QAP_580
from test_cases import QAP_638, QAP_1520

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

        rm = RuleManager()
        # rm.remove_rules_by_id_range(5,150)
        # rm.add_RFQ('fix-fh-fx-rfq')
        # rm.add_TRFQ('fix-fh-fx-rfq')
        # rm.print_active_rules()
        # ui_tests.execute(report_i)
        start = datetime.now()
        print(f'start time = {start}')

        fix_demo.execute(report_id,test_cases['RFQ_example'])
        # ui_tests.execute(report_id)
        # QAP_1520.TestCase(report_id).execute()
        print("1 - done")
        print('duration time = ' + str(datetime.now() - start), str(report_id))
        # bca.create_event('duration time = ' + str(datetime.now() - start))
        # QAP_638.execute(report_id)
        # QAP_638.execute(report_id)
        # QAP_590.execute(report_id)
        # print("2 - done")
        # QAP_591.execute(report_id)
        # print("3 - done")
        # QAP_593.execute(report_id)
        # QAP_596.execute(report_id)
        # QAP_597.execute(report_id)
        # QAP_599.execute(report_id)
        # QAP_600.execute(report_id)
        # QAP_601.execute(report_id)
        # QAP_602.execute(report_id)
        # QAP_604.execute(report_id)
        # QAP_605.execute(report_id)
        # QAP_606.execute(report_id)
        # QAP_610.execute(report_id)
        # QAP_611.execute(report_id)
        # QAP_612.execute(report_id)
        # QAP_636.execute(report_id)
        # QAP_646.execute(report_id)
        # QAP_847.execute(report_id)
        # QAP_848.execute(report_id)
        # QAP_849.execute(report_id)
        # QAP_850.execute(report_id)
        # QAP_982.execute(report_id)
        # QAP_1713.execute(report_id)
        # QAP_2514.execute(report_id)
        # QAP_2728.execute(report_id)
        # QAP_2826.execute(report_id)
        # QAP_2847.execute(report_id)


    except Exception:
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()
