import logging
from datetime import datetime
from custom import basic_custom_actions as bca
from examples.dealer_intervention import get_rfq_details
from quod_qa.eq.Algo_Multilisted import QAP_2982, QAP_1986, QAP_1988, QAP_1965, QAP_1985, QAP_1979, QAP_1977, QAP_1998, \
    QAP_1974, QAP_1968, QAP_1969, QAP_1976, QAP_1975, QAP_1961, QAP_1960, QAP_1980, QAP_1959, QAP_1810, QAP_1952, \
    QAP_1997, QAP_1996, QAP_1995, QAP_1992, QAP_2857, QAP_3019, QAP_3021, QAP_3022, QAP_3025, QAP_3027, QAP_1951, \
    QAP_1990, QAP_3028

from quod_qa.fx import ui_tests
from quod_qa.fx.fx_mm_rfq import (QAP_1970, QAP_1971, QAP_1972, QAP_2062, QAP_2121, QAP_1545, QAP_1537, QAP_1539WIP,
                                  QAP_1541CANCELLED, QAP_1542, QAP_1547, QAP_1548, QAP_1562, QAP_1563)
from rule_management import RuleManager
from stubs import Stubs
from test_cases import QAP_638, QAP_1552

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
            'case_id': bca.create_event_id(),
            'TraderConnectivity': 'gtwquod5-fx',
            'Account': 'MMCLIENT1',
            'SenderCompID': 'QUODFX_UAT',
            'TargetCompID': 'QUOD5',
        }
        # QAP_1970.execute(report_id, test_cases)
        # QAP_1971.execute(report_id, test_cases)
        # QAP_1972.execute(report_id, test_cases)
        # QAP_2062.execute(report_id, test_cases)
        # QAP_1545.execute(report_id, test_cases)
        # QAP_1537.execute(report_id, test_cases)
        # QAP_1539WIP.execute(report_id, test_cases)
        # QAP_1542.execute(report_id, test_cases)
        # QAP_1547.execute(report_id, test_cases)
        # QAP_1548.execute(report_id, test_cases)
        # QAP_1562.execute(report_id, test_cases)
        # QAP_1563.execute(report_id, test_cases)

        ui_tests.execute(report_id)
        # region Acceptance list RFQ Taker
        # QAP_568.execute(report_id)
        # QAP_569.execute(report_id)
        # QAP_574.execute(report_id)
        # QAP_2826.execute(report_id)
        # QAP_2835.execute(report_id)
        # QAP_2847.execute(report_id)
        # endregion
        # region Regression
        # QAP_6.execute(report_id)
        # QAP_564.execute(report_id)
        # QAP_565.execute(report_id)
        # QAP_566.execute(report_id)
        # QAP_567.execute(report_id)
        # QAP_568.execute(report_id)
        # QAP_569.execute(report_id)
        # QAP_570.execute(report_id)
        # QAP_571.execute(report_id)
        # QAP_573.execute(report_id)
        # QAP_574.execute(report_id)
        # # QAP_575.execute(report_id)
        # QAP_576.execute(report_id)
        # QAP_577.execute(report_id)
        # QAP_578.execute(report_id)
        # QAP_579.execute(report_id)
        # QAP_580.execute(report_id)
        # QAP_581.execute(report_id)
        # QAP_582.execute(report_id)
        # QAP_584.execute(report_id)
        # QAP_585.execute(report_id)
        # QAP_587.execute(report_id)
        # QAP_589.execute(report_id)
        # QAP_590.execute(report_id)
        # QAP_591.execute(report_id)
        # # QAP_592.execute(report_id)
        # QAP_593.execute(report_id)
        # QAP_594.execute(report_id)
        # QAP_595.execute(report_id)
        # QAP_597.execute(report_id)
        # QAP_598.execute(report_id)
        # QAP_599.execute(report_id)
        # QAP_600.execute(report_id)
        # QAP_601.execute(report_id)
        # QAP_602.execute(report_id)
        # QAP_604.execute(report_id)
        # QAP_605.execute(report_id)
        # QAP_606.execute(report_id)
        # QAP_609.execute(report_id)
        # QAP_610.execute(report_id)
        # QAP_611.execute(report_id)
        # QAP_612.execute(report_id)
        # QAP_636.execute(report_id)
        # QAP_643.execute(report_id)
        # QAP_645.execute(report_id)
        # QAP_646.execute(report_id)
        # QAP_648.execute(report_id)
        # QAP_683.execute(report_id)
        # QAP_687.execute(report_id)
        # QAP_702.execute(report_id)
        # QAP_708.execute(report_id)
        # QAP_709.execute(report_id)
        # QAP_710.execute(report_id)
        # QAP_714.execute(report_id)
        # QAP_718.execute(report_id)
        # QAP_741.execute(report_id)
        # QAP_751.execute(report_id)
        # QAP_842.execute(report_id)
        # QAP_847.execute(report_id)
        # QAP_848.execute(report_id)
        # QAP_849.execute(report_id)
        # QAP_850.execute(report_id)
        # QAP_982.execute(report_id)
        # QAP_992.execute(report_id)
        # QAP_1585.execute(report_id)
        # QAP_1713.execute(report_id)

        # QAP_2419.execute(report_id)
        # QAP_2514.execute(report_id)
        # QAP_2728.execute(report_id)
        # QAP_2729.execute(report_id)
        # QAP_2774.execute(report_id)
        # QAP_2826.execute(report_id)
        # QAP_2835.execute(report_id)
        # QAP_2847.execute(report_id)
        # QAP_3589.execute(report_id)
        # endregion




    except Exception:
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()
