from quod_qa.fx.fx_taker_esp import QAP_110, QAP_1115, QAP_3364, QAP_382, QAP_2854, QAP_2947, QAP_231, QAP_3042, \
    QAP_492, QAP_2948, QAP_1591, QAP_2949, QAP_833, QAP_4156, QAP_404, QAP_2373, QAP_2416, QAP_4677, QAP_4673, QAP_4768, \
    QAP_2, QAP_19, QAP_105, QAP_228, QAP_458, QAP_530, QAP_851, QAP_3066, QAP_3068, QAP_3069, QAP_3157, QAP_3644, \
    QAP_3742
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
    report_id = bca.create_event('ESP Taker regression', parent_id)
    session_id = set_session_id()

    try:
        if not Stubs.frontend_is_open:
            prepare_fe_2(report_id, session_id)
        else:
            get_opened_fe(report_id, session_id)
        # QAP_2.execute(report_id, session_id) #pass
        QAP_19.execute(report_id, session_id)   # MyOrders
        QAP_105.execute(report_id, session_id)  # Date
        # QAP_110.execute(report_id, session_id)
        # QAP_228.execute(report_id, session_id) #pass
        # QAP_231.execute(report_id, session_id) #pass
        # QAP_382.execute(report_id, session_id)
        # QAP_404.execute(report_id, session_id) #pass
        # QAP_458.execute(report_id, session_id)
        # QAP_492.execute(report_id, session_id)
        # QAP_530.execute(report_id, session_id) #pass
        QAP_833.execute(report_id, session_id)  # Qty Precision
        # QAP_851.execute(report_id, session_id) #pass
        # QAP_1115.execute(report_id, session_id)
        QAP_1591.execute(report_id, session_id)     # Date
        # QAP_2373.execute(report_id, session_id)
        # QAP_2416.execute(report_id, session_id)
        QAP_2854.execute(report_id, session_id)
        QAP_2947.execute(report_id, session_id)
        QAP_2948.execute(report_id, session_id)
        QAP_2949.execute(report_id, session_id)
        QAP_3042.execute(report_id, session_id)
        QAP_3066.execute(report_id, session_id)
        QAP_3068.execute(report_id, session_id)     # StrategyName
        QAP_3069.execute(report_id, session_id)     # StrategyName
        QAP_3157.execute(report_id, session_id)
        QAP_3364.execute(report_id, session_id)
        QAP_3644.execute(report_id, session_id)
        QAP_3742.execute(report_id, session_id)
        QAP_4156.execute(report_id, session_id)     # Qty Precision
        QAP_4673.execute(report_id, session_id)
        QAP_4677.execute(report_id, session_id)
        QAP_4768.execute(report_id, session_id)     # Config for 314
    except Exception:
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
