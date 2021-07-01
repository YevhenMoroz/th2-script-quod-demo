from quod_qa.fx.fx_taker_rfq import QAP_6, QAP_564, QAP_565, QAP_566, QAP_567, QAP_568, QAP_569, QAP_570, QAP_571, \
    QAP_573, QAP_574, QAP_575, QAP_576, QAP_577, QAP_578, QAP_579, QAP_580, QAP_581, QAP_582, QAP_584, QAP_585, QAP_587, \
    QAP_589, QAP_590, QAP_591, QAP_593, QAP_594, QAP_595, QAP_597, QAP_598, QAP_592, QAP_599, QAP_600, QAP_601, QAP_602, \
    QAP_604, QAP_605, QAP_606, QAP_609, QAP_610, QAP_611, QAP_612, QAP_636, QAP_643, QAP_645, QAP_646, QAP_648, QAP_683, \
    QAP_687, QAP_702, QAP_708, QAP_709, QAP_710, QAP_714, QAP_718, QAP_741, QAP_751, QAP_842, QAP_847, QAP_848, QAP_849, \
    QAP_850, QAP_982, QAP_992, QAP_1585, QAP_1713, QAP_2419, QAP_2514, QAP_2728, QAP_2729, QAP_2774, QAP_2826, QAP_2835, \
    QAP_2847, QAP_3589
from stubs import Stubs
import logging
from custom import basic_custom_actions as bca

from win_gui_modules.utils import set_session_id

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False
channels = dict()


def test_run(parent_id=None):
    report_id = bca.create_event('RFQ Taker regression', parent_id)
    session_id = set_session_id()
    try:
        QAP_6.execute(report_id, session_id)
        QAP_564.execute(report_id, session_id)
        QAP_565.execute(report_id, session_id)
        QAP_566.execute(report_id, session_id)
        QAP_567.execute(report_id, session_id)
        QAP_568.execute(report_id, session_id)
        QAP_569.execute(report_id, session_id)
        QAP_570.execute(report_id, session_id)
        QAP_571.execute(report_id, session_id)
        QAP_573.execute(report_id, session_id)
        QAP_574.execute(report_id, session_id)
        QAP_575.execute(report_id, session_id)
        QAP_576.execute(report_id, session_id)
        QAP_577.execute(report_id, session_id)
        QAP_578.execute(report_id, session_id)
        QAP_579.execute(report_id, session_id)
        QAP_580.execute(report_id, session_id)
        QAP_581.execute(report_id, session_id)
        QAP_582.execute(report_id, session_id)
        QAP_584.execute(report_id, session_id)
        QAP_585.execute(report_id, session_id)
        QAP_587.execute(report_id, session_id)
        QAP_589.execute(report_id, session_id)
        QAP_590.execute(report_id, session_id)
        QAP_591.execute(report_id, session_id)
        QAP_592.execute(report_id, session_id)
        QAP_593.execute(report_id, session_id)
        QAP_594.execute(report_id, session_id)
        QAP_595.execute(report_id, session_id)
        QAP_597.execute(report_id, session_id)
        QAP_598.execute(report_id, session_id)
        QAP_599.execute(report_id, session_id)
        QAP_600.execute(report_id, session_id)
        QAP_601.execute(report_id, session_id)
        QAP_602.execute(report_id, session_id)
        QAP_604.execute(report_id, session_id)
        QAP_605.execute(report_id, session_id)
        QAP_606.execute(report_id, session_id)
        QAP_609.execute(report_id, session_id)
        QAP_610.execute(report_id, session_id)
        QAP_611.execute(report_id, session_id)
        QAP_612.execute(report_id, session_id)
        QAP_636.execute(report_id, session_id)
        QAP_643.execute(report_id, session_id)
        QAP_645.execute(report_id, session_id)
        QAP_646.execute(report_id, session_id)
        QAP_648.execute(report_id, session_id)
        QAP_683.execute(report_id, session_id)
        QAP_687.execute(report_id, session_id)
        QAP_702.execute(report_id, session_id)
        QAP_708.execute(report_id, session_id)
        QAP_709.execute(report_id, session_id)
        QAP_710.execute(report_id, session_id)
        QAP_714.execute(report_id, session_id)
        QAP_718.execute(report_id, session_id)
        QAP_741.execute(report_id, session_id)
        QAP_751.execute(report_id, session_id)
        QAP_842.execute(report_id, session_id)
        QAP_847.execute(report_id, session_id)
        QAP_848.execute(report_id, session_id)
        QAP_849.execute(report_id, session_id)
        QAP_850.execute(report_id, session_id)
        QAP_982.execute(report_id, session_id)
        QAP_992.execute(report_id, session_id)
        QAP_1585.execute(report_id, session_id)
        QAP_1713.execute(report_id, session_id)
        QAP_2419.execute(report_id, session_id)
        QAP_2514.execute(report_id, session_id)
        QAP_2728.execute(report_id, session_id)
        QAP_2729.execute(report_id, session_id)
        QAP_2774.execute(report_id, session_id)
        QAP_2826.execute(report_id, session_id)
        QAP_2835.execute(report_id, session_id)
        QAP_2847.execute(report_id, session_id)
        QAP_3589.execute(report_id, session_id)
    except Exception:
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
