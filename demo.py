import logging
from datetime import datetime
from custom import basic_custom_actions as bca
from rule_management import RuleManager
from stubs import Stubs
from quod_qa.fx.fx_taker_rfq import QAP_574, QAP_585, QAP_569, testing, QAP_578, QAP_579, QAP_580, QAP_610, QAP_604, \
    QAP_605, QAP_611

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
        # QAP_585.execute(report_id)
        # QAP_568.execute(report_id)
        # QAP_569.execute(report_id)
        # QAP_570.execute(report_id)
        # testing.execute(report_id)
        # QAP_574.execute(report_id)
        # QAP_578.execute(report_id)
        # QAP_579.execute(report_id)
        # QAP_580.execute(report_id)
        # QAP_610.execute(report_id)
        # QAP_604.execute(report_id)
        # QAP_605.execute(report_id)
        QAP_611.execute(report_id)
        rm = RuleManager()

        rm.print_active_rules()

    except Exception:
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()
