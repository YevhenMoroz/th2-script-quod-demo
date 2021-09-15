from quod_qa.fx.fx_mm_esp import QAP_1418, QAP_1536, QAP_1560, QAP_1599, QAP_1601, QAP_2034, QAP_2035, QAP_2037, \
    QAP_2038, QAP_2039, QAP_2069, QAP_2072, QAP_2075, QAP_2117, QAP_2523, QAP_2555, QAP_2556, QAP_2587, QAP_2796, \
    QAP_2825, QAP_2855, QAP_3045, QAP_3563, QAP_1518, QAP_1558, QAP_1559, QAP_2797, QAP_2082, QAP_2084, \
    QAP_2086, QAP_2085, QAP_2079, QAP_3841, QAP_1554, QAP_1597, QAP_3390, QAP_2750, QAP_2823, QAP_2874, QAP_2876, \
    QAP_2880, QAP_2879, QAP_2873, QAP_2872, QAP_2966, QAP_3848, QAP_2012, QAP_4094, QAP_2078, QAP_1511, QAP_1589, \
    QAP_4061, QAP_3661
from quod_qa.fx.fx_mm_synthetic import QAP_2646
from stubs import Stubs
import logging
from custom import basic_custom_actions as bca

from win_gui_modules.utils import set_session_id, prepare_fe_2, get_opened_fe

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False
channels = dict()


def test_run(parent_id=None):
    report_id = bca.create_event('ESP MM regression', parent_id)
    session_id = set_session_id()
    Stubs.custom_config['qf_trading_fe_main_win_name'] = "Quod Financial - Quod site 314"

    try:
        if not Stubs.frontend_is_open:
            prepare_fe_2(report_id, session_id)
        else:
            get_opened_fe(report_id, session_id)
        # QAP_1418.execute(report_id, session_id)
        # QAP_1536.execute(report_id, session_id)
        # # QAP_1560.execute(report_id, session_id)
        # QAP_1599.execute(report_id, session_id)
        # QAP_1601.execute(report_id, session_id)
        # QAP_2034.execute(report_id, session_id)
        # QAP_2035.execute(report_id, session_id)
        # QAP_2037.execute(report_id, session_id)
        QAP_2038.execute(report_id, session_id)
        QAP_2039.execute(report_id, session_id)
        # QAP_2069.execute(report_id, session_id)
        # QAP_2072.execute(report_id, session_id)
        # QAP_2075.execute(report_id, session_id)
        # QAP_2117.execute(report_id, session_id)
        # QAP_2523.execute(report_id, session_id)
        # QAP_2555.execute(report_id, session_id)
        # QAP_2556.execute(report_id, session_id)
        # QAP_2587.execute(report_id, session_id)
        # QAP_2646.execute(report_id, session_id)
        # QAP_2796.execute(report_id, session_id)
        # QAP_2825.execute(report_id, session_id)
        # QAP_2855.execute(report_id, session_id)
        # QAP_3045.execute(report_id, session_id)
        # QAP_3563.execute(report_id, session_id)
        # QAP_1511.execute(report_id, session_id)
        # QAP_1589.execute(report_id, session_id)
        # QAP_4061.execute(report_id, session_id)
        # QAP_3661.execute(report_id, session_id)
        # # QAP_1518.execute(report_id)
        # # QAP_1554.execute(report_id)
        # # QAP_1558.execute(report_id)
        # QAP_1559.execute(report_id)
        # # QAP_1597.execute(report_id)
        # QAP_2012.execute(report_id)
        # # QAP_2078.execute(report_id)
        # # QAP_2079.execute(report_id)
        # # QAP_2082.execute(report_id)
        # # QAP_2084.execute(report_id)
        # # QAP_2085.execute(report_id)
        # # QAP_2086.execute(report_id)
        # QAP_2750.execute(report_id)
        # # QAP_2797.execute(report_id)
        # # QAP_2823.execute(report_id)
        # QAP_2872.execute(report_id)
        # QAP_2873.execute(report_id)
        # # QAP_2874.execute(report_id)
        # # QAP_2876.execute(report_id)
        # # QAP_2879.execute(report_id)
        # # QAP_2880.execute(report_id)
        # QAP_2966.execute(report_id)
        # QAP_3390.execute(report_id)
        # # QAP_3841.execute(report_id)
        # # QAP_3848.execute(report_id)
        # QAP_4094.execute(report_id)

    except Exception:
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
