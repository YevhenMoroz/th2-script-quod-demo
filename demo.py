import logging
from datetime import datetime
from custom import basic_custom_actions as bca
from quod_qa.fx.fx_mm_esp import QAP_1560, QAP_2825, QAP_2555, QAP_2038, QAP_1599, QAP_1518, QAP_2034
from quod_qa.fx.fx_mm_rfq import QAP_1746
from quod_qa.fx.fx_taker_rfq import QAP_6, QAP_564, QAP_565, QAP_566, QAP_567, QAP_568, QAP_569, QAP_570, QAP_571, \
    QAP_573, QAP_574, QAP_576, QAP_577, QAP_578, QAP_579, QAP_580, QAP_581, QAP_582, QAP_584, QAP_585, QAP_587, QAP_589, \
    QAP_590, QAP_591, QAP_593, QAP_594, QAP_595, QAP_597, QAP_598, QAP_599, QAP_600, QAP_601, QAP_602, QAP_604, QAP_605, \
    QAP_606, QAP_609, QAP_610, QAP_611, QAP_612, QAP_636, QAP_643, QAP_645, QAP_646, QAP_648, QAP_683, QAP_687, QAP_702, \
    QAP_708, QAP_709, QAP_710, QAP_714, QAP_718, QAP_741, QAP_751, QAP_842, QAP_847, QAP_848, QAP_849, QAP_850, QAP_982, \
    QAP_992, QAP_1585, QAP_1713, QAP_2419, QAP_2514, QAP_2728, QAP_2729, QAP_2774, QAP_2826, QAP_2835, QAP_2847, \
    QAP_3589

from stubs import Stubs

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
        'case_id': bca.create_event_id(),
        'TraderConnectivity': 'gtwquod5-fx',
        'Account': 'MMCLIENT1',
        'SenderCompID': 'QUODFX_UAT',
        'TargetCompID': 'QUOD5',
    }
    try:



        start = datetime.now()
        print(f'start time = {start}')

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

        # QAP_595.execute(report_id)
        # QAP_751.execute(report_id)
        # QAP_2774.execute(report_id)
        # QAP_571.execute(report_id)
        # QAP_2729.execute(report_id)
        # my_test.execute(report_id)
        # QAP_718.execute(report_id)
        # QAP_2419.execute(report_id)
        # pricing_tile_test.execute(report_id)
        # QAP_1418.execute(report_id)
        # QAP_2556.execute(report_id)
        # QAP_569.execute(report_id)
        # QAP_2117.execute(report_id)

        # QAP_2855.execute(report_id)
        # QAP_3563.execute(report_id)
        # QAP_568.execute(report_id)
        # QAP_833.execute(report_id)
        # QAP_1115.execute(report_id)
        # QAP_110.execute(report_id)
        # QAP_2069.execute(report_id)
        # QAP_2646.execute(report_id)
        # QAP_2587.execute(report_id)
        # QAP_2796.execute(report_id)
        # QAP_992.execute(report_id)
        # QAP_1560.execute(report_id)
        # QAP_1536.execute(report_id)
        # QAP_2825.execute(report_id)
        # QAP_2555.execute(report_id)
        # QAP_2038.execute(report_id)
        # QAP_1599.execute(report_id)
        QAP_2034.execute(report_id)


        print('duration time = ' + str(datetime.now() - start))

    except Exception:
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()
