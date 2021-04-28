import logging
from datetime import datetime
from custom import basic_custom_actions as bca
from quod_qa.fx.fx_taker_rfq import QAP_636, QAP_612, QAP_847, QAP_848, QAP_849, QAP_850, QAP_982, QAP_3589, QAP_589, \
    QAP_683, QAP_643, QAP_578, QAP_587, QAP_594, QAP_687, QAP_702, QAP_842, QAP_714, QAP_741, QAP_609, QAP_1585
from rule_management import RuleManager
from schemas import rfq_tile_example
from stubs import Stubs
from quod_qa.fx import ui_tests
from test_cases import QAP_682, QAP_569

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False

channels = dict()


def test_run():
    # Generation id and time for test run
    report_id = bca.create_event('ostronov tests ' + datetime.now().strftime('%Y%m%d-%H:%M:%S'))
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
        start = datetime.now()
        print(f'start time = {start}')
        # QAP_585.execute(report_id)
        # QAP_568.execute(report_id)
        # QAP_569.execute(report_id)
        # QAP_570.execute(report_id)
        # testing.execute(report_id)
        # QAP_574.execute(report_id)
        # QAP_578.execute(report_id)
        # QAP_579.execute(report_id)
        # QAP_580.execute(report_id)
        # QAP_587.execute(report_id)
        # QAP_589.execute(report_id)
        # QAP_596.execute(report_id)
        # QAP_594.execute(report_id)
        # QAP_610.execute(report_id)
        # QAP_611.execute(report_id)
        # QAP_604.execute(report_id)
        # QAP_605.execute(report_id)
        # QAP_612.execute(report_id)
        # QAP_636.execute(report_id)
        # QAP_847.execute(report_id)
        # QAP_848.execute(report_id)
        # QAP_849.execute(report_id)
        # QAP_850.execute(report_id)
        # QAP_982.execute(report_id)
        # QAP_687.execute(report_id)
        # QAP_702.execute(report_id)
        # QAP_587.execute(report_id)
        QAP_842.execute(report_id)
        # QAP_1585.execute(report_id)
        # QAP_714.execute(report_id)
        # QAP_609.execute(report_id)
        # QAP_741.execute(report_id)
        # QAP_3589.execute(report_id)
        # QAP_683.execute(report_id)
        # QAP_643.execute(report_id)
        print('duration time = ' + str(datetime.now() - start))

        # ui_tests.execute(report_id)
        rm = RuleManager()
        # rm.remove_rules_by_id_range(4, 170)
        # rm.print_active_rules()



    except Exception:
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()

